from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class UseCase:
    name: str
    cadence: str
    inputs: tuple[str, ...]
    target: str
    n_in: int
    n_out: int
    models: tuple[str, ...]


USE_CASES = {
    "river": UseCase(
        "river-flow", "D", ("disch1", "disch2", "disch3"), "disch3",
        20, 3, ("linear-sequence",),
    ),
    "energy": UseCase(
        "smart-home-energy", "min", ("energy",), "energy",
        60, 3, ("arima", "holt-winters"),
    ),
    "solar": UseCase(
        "solar-power", "h", ("ac_power",), "ac_power",
        24, 2, ("xgboost", "prophet"),
    ),
}


def synthetic_frame(key: str, rows: int = 1200, seed: int = 42) -> pd.DataFrame:
    cfg = USE_CASES[key]
    rng = np.random.default_rng(seed)
    t = np.arange(rows, dtype=float)
    index = pd.date_range("2022-01-01", periods=rows, freq=cfg.cadence)
    if key == "river":
        seasonal = 60 + 25 * np.sin(2 * np.pi * t / 90)
        d1 = seasonal + rng.normal(0, 5, rows)
        d2 = 0.75 * np.roll(d1, 1) + 15 + rng.normal(0, 4, rows)
        d3 = 0.55 * np.roll(d2, 1) + 0.25 * d1 + rng.normal(0, 3, rows)
        return pd.DataFrame(
            {"timestamp": index, "disch1": d1, "disch2": d2, "disch3": d3}
        )
    if key == "energy":
        signal = 1.4 + 0.35 * np.sin(2 * np.pi * t / 60)
        return pd.DataFrame(
            {"timestamp": index, "energy": signal + rng.normal(0, 0.05, rows)}
        )
    daylight = np.maximum(0, np.sin(2 * np.pi * (t % 24 - 6) / 24))
    power = np.maximum(0, 4500 * daylight + rng.normal(0, 180, rows))
    return pd.DataFrame({"timestamp": index, "ac_power": power})


def load_frame(key: str, csv: str | None) -> pd.DataFrame:
    cfg = USE_CASES[key]
    frame = synthetic_frame(key) if csv is None else pd.read_csv(csv)
    required = {"timestamp", *cfg.inputs}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing CSV columns: {sorted(missing)}")
    frame = frame.loc[:, ["timestamp", *cfg.inputs]].copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], errors="raise")
    frame = frame.sort_values("timestamp").drop_duplicates("timestamp")
    numeric = list(cfg.inputs)
    frame[numeric] = frame[numeric].apply(pd.to_numeric, errors="coerce")
    frame[numeric] = frame[numeric].interpolate(limit=10).ffill().bfill()
    return frame.dropna().reset_index(drop=True)


def supervised(frame: pd.DataFrame, cfg: UseCase) -> tuple[np.ndarray, np.ndarray]:
    values = frame.loc[:, cfg.inputs].to_numpy(float)
    target_index = cfg.inputs.index(cfg.target)
    xs, ys = [], []
    for end in range(cfg.n_in, len(values) - cfg.n_out + 1):
        xs.append(values[end - cfg.n_in : end])
        ys.append(values[end : end + cfg.n_out, target_index])
    return np.asarray(xs), np.asarray(ys)


def metrics(y_true: np.ndarray, y_pred: np.ndarray) -> pd.DataFrame:
    rows = []
    for horizon in range(y_true.shape[1]):
        actual, predicted = y_true[:, horizon], y_pred[:, horizon]
        error = actual - predicted
        mse = float(np.mean(error**2))
        denominator = float(np.sum((actual - actual.mean()) ** 2))
        rows.append(
            {
                "horizon": horizon + 1,
                "mae": float(np.mean(np.abs(error))),
                "mse": mse,
                "rmse": float(np.sqrt(mse)),
                "r2": 1 - float(np.sum(error**2)) / denominator
                if denominator else float("nan"),
            }
        )
    return pd.DataFrame(rows)


def persist_config(output: Path, cfg: UseCase, csv: str | None, seed: int) -> None:
    payload = {**asdict(cfg), "data_source": csv or "synthetic", "seed": seed}
    output.joinpath("run_config.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )

