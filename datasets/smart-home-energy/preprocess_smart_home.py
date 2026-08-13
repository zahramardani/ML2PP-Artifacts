#!/usr/bin/env python3
"""Rebuild the Smart Home use-case dataset from the real source variable `use [kW]`.

The original Smart Home dataset records one row per second.  This script uses the
first 252,000 raw observations (4,200 minutes), averages each consecutive block
of 60 `use [kW]` observations, and writes the one-minute ML2++ artifact.

The Kaggle data card is the authoritative original source.  A commit-pinned
public GitHub mirror of Home.csv is used here only to make the transformation
re-runnable without Kaggle credentials.
"""

from __future__ import annotations

import csv
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
RAW_MIRROR_URL = (
    "https://raw.githubusercontent.com/MihaiNastase/MongoDB-IoT-Application/"
    "0afc3e385a09e23f910444a333c6556d8fad6e33/DataSetup/Data/Home.csv"
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


def fetch_and_aggregate() -> list[tuple[str, float]]:
    request = urllib.request.Request(
        RAW_MIRROR_URL,
        headers={"User-Agent": "ML2PP-Artifacts/1.0"},
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        text_stream = io.TextIOWrapper(response, encoding="utf-8-sig", newline="")
        reader = csv.DictReader(text_stream)
        if not reader.fieldnames or "time" not in reader.fieldnames or RAW_TARGET not in reader.fieldnames:
            raise RuntimeError(
                f"Unexpected source schema. Required columns: 'time' and {RAW_TARGET!r}; "
                f"found: {reader.fieldnames}"
            )

        output: list[tuple[str, float]] = []
        block_sum = 0.0
        block_count = 0
        block_start_time: int | None = None
        previous_time: int | None = None

        for index, row in enumerate(reader):
            if index >= RAW_ROWS_NEEDED:
                break

            raw_time = int(float(row["time"]))
            raw_value = float(row[RAW_TARGET])

            if index == 0:
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
                    f"Non-consecutive raw timestamp at row {index}: "
                    f"{previous_time} -> {raw_time}."
                )
            previous_time = raw_time

            if block_count == 0:
                block_start_time = raw_time
            block_sum += raw_value
            block_count += 1

            if block_count == ROWS_PER_MINUTE:
                assert block_start_time is not None
                timestamp = datetime.fromtimestamp(
                    block_start_time, tz=timezone.utc
                ).strftime("%Y-%m-%d %H:%M:%S")
                output.append((timestamp, block_sum / ROWS_PER_MINUTE))
                block_sum = 0.0
                block_count = 0
                block_start_time = None

    if len(output) != OUTPUT_ROWS:
        raise RuntimeError(
            f"Expected {OUTPUT_ROWS} complete one-minute aggregates; got {len(output)}."
        )
    if output[0][0] != "2016-01-01 05:00:00":
        raise RuntimeError(f"Unexpected first output timestamp: {output[0][0]}")
    if output[-1][0] != "2016-01-04 02:59:00":
        raise RuntimeError(f"Unexpected last output timestamp: {output[-1][0]}")

    return output


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


def write_readme(rows: list[tuple[str, float]], stats: dict[str, float]) -> None:
    readme = f"""# Use Case 2 - smart-home energy dataset

## Checked processed file

`use_case_2_smart_home_energy.csv`

- 4,200 one-minute observations
- period: {rows[0][0]} through {rows[-1][0]}
- target: `use_kW`, derived from the source variable `use [kW]`
- raw source cadence used for this artifact: one second
- aggregation: arithmetic mean of each consecutive 60 raw `use [kW]` observations
- raw observations used: first {RAW_ROWS_NEEDED:,} rows (4,200 complete one-minute blocks)
- target range: {stats['min']:.6f} to {stats['max']:.6f} kW
- target mean: {stats['mean']:.6f} kW
- no missing timestamps, missing target values, or duplicate output timestamps
- forecast horizon used by the documented use case: three minutes
- model families documented for this use case: ARIMA(1,1,1) and additive Holt-Winters
- original source: {ORIGINAL_SOURCE}
- commit-pinned reconstruction mirror: {RAW_MIRROR_URL}

## Reproducible preprocessing

Run:

```bash
python datasets/smart-home-energy/preprocess_smart_home.py
```

The script validates the source schema and the first raw record, verifies one-second timestamp continuity across the selected raw interval, groups consecutive observations into non-overlapping 60-second blocks, averages only `use [kW]`, and writes the 4,200-row one-minute dataset. The timestamp assigned to each output row is the UTC timestamp of the first raw observation in that 60-second block.

The processed target is household power use in kW. It is not humidity and is not a weather variable.

## Correction note

On 13 August 2026, the previously deposited CSV was found to have been derived from the source `humidity` column while being labelled `use_kW`. That file has been superseded by the reconstruction from the actual `use [kW]` source variable described above. Numerical model results produced from the superseded CSV must not be interpreted as household-energy forecasting results unless they are rerun on this corrected dataset.
"""
    README_PATH.write_text(readme, encoding="utf-8")


def write_pdf(rows: list[tuple[str, float]], stats: dict[str, float]) -> None:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except ImportError as exc:
        raise RuntimeError(
            "PDF generation requires reportlab. Install it with: pip install reportlab"
        ) from exc

    width, height = A4
    c = canvas.Canvas(str(PDF_PATH), pagesize=A4)
    left = 48
    y = height - 52

    c.setFont("Helvetica-Bold", 16)
    c.drawString(left, y, "ML2++ Use Case 2 - Smart Home Energy Dataset")
    y -= 28

    c.setFont("Helvetica", 10)
    lines = [
        "Processed file: use_case_2_smart_home_energy.csv",
        f"Observations: 4,200 one-minute values",
        f"Period: {rows[0][0]} through {rows[-1][0]} UTC",
        "Target: use_kW (household power use, kW)",
        "Source variable: use [kW]",
        "Transformation: arithmetic mean of each consecutive 60 one-second source observations",
        f"Raw observations used: first {RAW_ROWS_NEEDED:,}",
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
        "The repository preprocessing script uses a commit-pinned public GitHub mirror only "
        "to make the transformation reproducible without Kaggle credentials."
    )
    for part in wrap(provenance, width=105):
        c.drawString(left, y, part)
        y -= 13

    y -= 8
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
    rows = fetch_and_aggregate()
    stats = dataset_stats(rows)
    write_csv(rows)
    write_readme(rows, stats)
    write_pdf(rows, stats)
    print(f"Wrote {CSV_PATH}")
    print(f"Wrote {README_PATH}")
    print(f"Wrote {PDF_PATH}")
    print(
        "Stats: "
        f"min={stats['min']:.9f}, max={stats['max']:.9f}, mean={stats['mean']:.9f}"
    )


if __name__ == "__main__":
    main()
