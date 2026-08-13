#!/usr/bin/env python3
"""Rebuild the Smart Home use-case dataset from the real source variable `use [kW]`.

The source dataset contains second-level measurements. This script selects the
actual `use [kW]` series, takes the first 252,000 consecutive one-second values
(4,200 minutes), averages each non-overlapping block of 60 observations, and
writes the one-minute ML2++ artifact.

The Kaggle data card is the authoritative original source. For reproducibility
without Kaggle credentials, the script reads the complete public converted CSV
stream published by Yotahub/Machbase from that Kaggle dataset. The conversion
script used by that mirror is linked below and preserved at a commit-pinned URL.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import io
import statistics
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from textwrap import wrap

ORIGINAL_SOURCE = (
    "https://www.kaggle.com/datasets/taranvee/"
    "smart-home-dataset-with-weather-information"
)
PUBLIC_RECONSTRUCTION_STREAM = (
    "https://data.yotahub.com/2024-1/datahub-2024-1-home.csv.gz"
)
PUBLIC_RECONSTRUCTION_STREAM_HTTP = (
    "http://data.yotahub.com/2024-1/datahub-2024-1-home.csv.gz"
)
MIRROR_CONVERSION_SCRIPT = (
    "https://github.com/machbase/datahub/blob/"
    "bbfb34f51c905743099dde49a684138cac964284/"
    "dataset/2024/01.Smart%20Home%20Dataset/conv/convert.py"
)
RAW_TARGET = "use [kW]"
ROWS_PER_MINUTE = 60
OUTPUT_ROWS = 4200
RAW_ROWS_NEEDED = ROWS_PER_MINUTE * OUTPUT_ROWS
EXPECTED_FIRST_RAW_TIME = 1451624400
EXPECTED_FIRST_RAW_VALUE = 0.932833333

HERE = Path(__file__).resolve().parent
CSV_PATH = HERE / "use_case_2_smart_home_energy.csv"
README_PATH = HERE / "README.md"
PDF_PATH = HERE / "use_case_2_smart_home_energy.pdf"


def _open_public_stream():
    """Open the public gzip stream, preferring HTTPS and falling back to HTTP."""
    errors: list[str] = []
    for url in (PUBLIC_RECONSTRUCTION_STREAM, PUBLIC_RECONSTRUCTION_STREAM_HTTP):
        try:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "ML2PP-Artifacts/1.0"},
            )
            return urllib.request.urlopen(request, timeout=180), url
        except Exception as exc:  # pragma: no cover - only used for network fallback
            errors.append(f"{url}: {exc}")
    raise RuntimeError("Could not open public reconstruction stream: " + " | ".join(errors))


def _epoch_seconds(value: str) -> int:
    """Normalize common Unix second/ms/us/ns integer encodings to seconds."""
    raw = int(float(value))
    magnitude = abs(raw)
    if magnitude >= 10**17:  # nanoseconds
        return raw // 1_000_000_000
    if magnitude >= 10**14:  # microseconds
        return raw // 1_000_000
    if magnitude >= 10**11:  # milliseconds
        return raw // 1_000
    return raw


def _normalized_name(value: str) -> str:
    value = value.strip()
    if value.startswith("TAG-"):
        value = value[4:]
    return value


def fetch_and_aggregate() -> tuple[list[tuple[str, float]], str, str]:
    response, used_url = _open_public_stream()
    with response:
        with gzip.GzipFile(fileobj=response) as gz:
            text_stream = io.TextIOWrapper(gz, encoding="utf-8-sig", newline="")
            reader = csv.DictReader(text_stream)
            if not reader.fieldnames:
                raise RuntimeError("Public reconstruction stream has no CSV header.")

            fields = {name.strip().lower(): name for name in reader.fieldnames}
            time_field = fields.get("time")
            name_field = fields.get("name")
            value_field = fields.get("value")
            if not time_field or not name_field or not value_field:
                raise RuntimeError(
                    "Unexpected public-stream schema. Required columns are time, name, value; "
                    f"found: {reader.fieldnames}"
                )

            output: list[tuple[str, float]] = []
            block_sum = 0.0
            block_count = 0
            block_start_time: int | None = None
            previous_time: int | None = None
            selected_count = 0
            digest = hashlib.sha256()

            for row in reader:
                if _normalized_name(row[name_field]) != RAW_TARGET:
                    continue
                if selected_count >= RAW_ROWS_NEEDED:
                    break

                raw_time = _epoch_seconds(row[time_field])
                raw_value = float(row[value_field])

                if selected_count == 0:
                    if raw_time != EXPECTED_FIRST_RAW_TIME:
                        raise RuntimeError(
                            f"Unexpected first raw timestamp: {raw_time}; "
                            f"expected {EXPECTED_FIRST_RAW_TIME}."
                        )
                    if abs(raw_value - EXPECTED_FIRST_RAW_VALUE) > 1e-9:
                        raise RuntimeError(
                            f"Unexpected first {RAW_TARGET} value: {raw_value}; "
                            f"expected approximately {EXPECTED_FIRST_RAW_VALUE}."
                        )

                if previous_time is not None and raw_time != previous_time + 1:
                    raise RuntimeError(
                        f"Non-consecutive target timestamp at selected row {selected_count}: "
                        f"{previous_time} -> {raw_time}."
                    )
                previous_time = raw_time

                digest.update(f"{raw_time},{raw_value!r}\n".encode("utf-8"))

                if block_count == 0:
                    block_start_time = raw_time
                block_sum += raw_value
                block_count += 1
                selected_count += 1

                if block_count == ROWS_PER_MINUTE:
                    assert block_start_time is not None
                    timestamp = datetime.fromtimestamp(
                        block_start_time, tz=timezone.utc
                    ).strftime("%Y-%m-%d %H:%M:%S")
                    output.append((timestamp, block_sum / ROWS_PER_MINUTE))
                    block_sum = 0.0
                    block_count = 0
                    block_start_time = None

    if selected_count != RAW_ROWS_NEEDED:
        raise RuntimeError(
            f"Expected {RAW_ROWS_NEEDED} {RAW_TARGET!r} observations; got {selected_count}."
        )
    if len(output) != OUTPUT_ROWS:
        raise RuntimeError(
            f"Expected {OUTPUT_ROWS} complete one-minute aggregates; got {len(output)}."
        )
    if output[0][0] != "2016-01-01 05:00:00":
        raise RuntimeError(f"Unexpected first output timestamp: {output[0][0]}")
    if output[-1][0] != "2016-01-04 02:59:00":
        raise RuntimeError(f"Unexpected last output timestamp: {output[-1][0]}")

    return output, digest.hexdigest(), used_url


def write_csv(rows: list[tuple[str, float]]) -> None:
    with CSV_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["timestamp", "use_kW"])
        for timestamp, value in rows:
            writer.writerow([timestamp, repr(value)])


def dataset_stats(rows: list[tuple[str, float]]) -> dict[str, float]:
    values = [value for _, value in rows]
    return {
        "min": min(values),
        "max": max(values),
        "mean": statistics.fmean(values),
    }


def write_readme(
    rows: list[tuple[str, float]],
    stats: dict[str, float],
    raw_digest: str,
    used_url: str,
) -> None:
    readme = f"""# Use Case 2 - smart-home energy dataset

## Checked processed file

`use_case_2_smart_home_energy.csv`

- 4,200 one-minute observations
- period: {rows[0][0]} through {rows[-1][0]} UTC
- target: `use_kW`, derived from the source variable `use [kW]`
- raw cadence used for this artifact: one second
- aggregation: arithmetic mean of each consecutive 60 raw `use [kW]` observations
- raw observations used: first {RAW_ROWS_NEEDED:,} target observations (4,200 complete one-minute blocks)
- target range: {stats['min']:.6f} to {stats['max']:.6f} kW
- target mean: {stats['mean']:.6f} kW
- no missing timestamps, missing target values, or duplicate output timestamps
- forecast horizon used by the documented use case: three minutes
- model families documented for this use case: ARIMA(1,1,1) and additive Holt-Winters
- original source: {ORIGINAL_SOURCE}
- public reconstruction stream used: {used_url}
- public mirror conversion script: {MIRROR_CONVERSION_SCRIPT}
- SHA-256 of the selected 252,000 `(epoch_second,use [kW])` pairs: `{raw_digest}`

## Reproducible preprocessing

Run:

```bash
python -m pip install reportlab
python datasets/smart-home-energy/preprocess_smart_home.py
```

The script validates the public-stream schema and the first target observation, verifies one-second timestamp continuity across the selected `use [kW]` interval, groups target observations into non-overlapping 60-second blocks, averages only `use [kW]`, and writes the 4,200-row one-minute dataset. Each output timestamp is the UTC timestamp of the first raw observation in its 60-second block.

The Kaggle data card is the authoritative original source. The Yotahub/Machbase stream is a public converted copy used only to make the transformation reproducible without Kaggle credentials; its conversion script is linked above.

The processed target is household power use in kW. It is not humidity and is not a weather variable.

## Correction note

On 13 August 2026, the previously deposited CSV was found to have been derived from the source `humidity` column while being labelled `use_kW`. That file has been superseded by the reconstruction from the actual `use [kW]` source variable described above. Numerical model results produced from the superseded CSV must not be interpreted as household-energy forecasting results unless they are rerun on this corrected dataset.
"""
    README_PATH.write_text(readme, encoding="utf-8")


def write_pdf(
    rows: list[tuple[str, float]],
    stats: dict[str, float],
    raw_digest: str,
) -> None:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except ImportError as exc:
        raise RuntimeError(
            "PDF generation requires reportlab. Install it with: pip install reportlab"
        ) from exc

    _, height = A4
    c = canvas.Canvas(str(PDF_PATH), pagesize=A4)
    left = 48
    y = height - 52

    c.setFont("Helvetica-Bold", 16)
    c.drawString(left, y, "ML2++ Use Case 2 - Smart Home Energy Dataset")
    y -= 28

    c.setFont("Helvetica", 10)
    lines = [
        "Processed file: use_case_2_smart_home_energy.csv",
        "Observations: 4,200 one-minute values",
        f"Period: {rows[0][0]} through {rows[-1][0]} UTC",
        "Target: use_kW (household power use, kW)",
        "Source variable: use [kW]",
        "Transformation: arithmetic mean of each consecutive 60 one-second target observations",
        f"Raw target observations used: first {RAW_ROWS_NEEDED:,}",
        f"Range: {stats['min']:.6f} to {stats['max']:.6f} kW",
        f"Mean: {stats['mean']:.6f} kW",
        "Missing output timestamps: 0",
        "Missing target values: 0",
        "Duplicate output timestamps: 0",
        "Documented forecast horizon: 3 minutes",
        "Documented models: ARIMA(1,1,1) and additive Holt-Winters",
    ]
    for line in lines:
        for part in wrap(line, width=92):
            c.drawString(left, y, part)
            y -= 14
        y -= 2

    y -= 8
    c.setFont("Helvetica-Bold", 11)
    c.drawString(left, y, "Provenance")
    y -= 17
    c.setFont("Helvetica", 9)
    provenance = (
        "Original source: Kaggle Smart Home Dataset with weather Information by Taranvee. "
        "Reconstruction uses the public Yotahub/Machbase converted stream; the repository "
        "README links the conversion script and records a SHA-256 digest of the selected "
        "252,000 target pairs."
    )
    for part in wrap(provenance, width=105):
        c.drawString(left, y, part)
        y -= 13

    y -= 5
    c.setFont("Helvetica", 7.5)
    c.drawString(left, y, f"Selected-pair SHA-256: {raw_digest}")
    y -= 18

    c.setFont("Helvetica-Bold", 11)
    c.drawString(left, y, "Correction note")
    y -= 17
    c.setFont("Helvetica", 9)
    correction = (
        "Corrected on 13 August 2026. The previously deposited CSV had been derived from "
        "humidity while labelled use_kW. It is superseded by the dataset rebuilt from the "
        "actual use [kW] column. Results from the superseded CSV require rerunning before "
        "being described as household-energy forecasting results."
    )
    for part in wrap(correction, width=105):
        c.drawString(left, y, part)
        y -= 13

    c.save()


def main() -> None:
    rows, raw_digest, used_url = fetch_and_aggregate()
    stats = dataset_stats(rows)
    write_csv(rows)
    write_readme(rows, stats, raw_digest, used_url)
    write_pdf(rows, stats, raw_digest)
    print(f"Wrote {CSV_PATH}")
    print(f"Wrote {README_PATH}")
    print(f"Wrote {PDF_PATH}")
    print(f"Source stream: {used_url}")
    print(f"Selected-pair SHA-256: {raw_digest}")
    print(
        "Stats: "
        f"min={stats['min']:.9f}, max={stats['max']:.9f}, mean={stats['mean']:.9f}"
    )


if __name__ == "__main__":
    main()
