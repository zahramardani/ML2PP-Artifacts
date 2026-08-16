#!/usr/bin/env python3
"""Re-run the Chapter 5 smart-home ARIMA and Holt-Winters configurations.

The script mirrors the ML2++ V13.1 Chapter-validation protocol used by the
Python/Java generator:
- chronological 80/20 split;
- three-step rolling-origin evaluation;
- ARIMA(1,1,1), trend='n', fixed fitted parameters with observed-state append;
- additive damped Holt-Winters with period 60, with smoothing coefficients
  learned on the training partition and held fixed during rolling-origin
  refiltering.

It intentionally runs the two models separately and writes independent result
folders so that neither model shares fitted state with the other.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import sklearn
import statsmodels
from sklearn.metrics import mean_squared_error
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing

EXPECTED_DATASET_SHA256 = "8211344ec98cff4287496c3daeadd7217c586d18d6b2ca68fe5bb856efd7e7dc"
TARGET = "use_kW"
STEPS = 3
SEASONAL_PERIOD = 60


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_data(path: Path) -> pd.DataFrame:
    digest = sha256_file(path)
    if digest != EXPECTED_DATASET_SHA256:
        raise RuntimeError(
            f"Dataset SHA-256 mismatch: {digest}; expected {EXPECTED_DATASET_SHA256}"
        )
    df = pd.read_csv(path)
    if "timestamp" not in df.columns or TARGET not in df.columns:
        raise ValueError(f"Expected columns timestamp and {TARGET}; found {list(df.columns)}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="raise", utc=True)
    df[TARGET] = pd.to_numeric(df[TARGET], errors="raise")
    df = df.sort_values("timestamp").reset_index(drop=True)
    if len(df) != 4200:
        raise ValueError(f"Expected 4200 rows; found {len(df)}")
    if df["timestamp"].duplicated().any():
        raise ValueError("Duplicate timestamps found")
    if df[TARGET].isna().any():
        raise ValueError("Missing target values found")
    delta = df["timestamp"].diff().dropna()
    if not (delta == pd.Timedelta(minutes=1)).all():
        raise ValueError("Timestamp cadence is not a complete one-minute sequence")
    return df


def split_series(df: pd.DataFrame) -> tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    split_idx = int(len(df) * 0.8)
    if split_idx != 3360:
        raise AssertionError(f"Unexpected split index {split_idx}")
    train = pd.Series(df[TARGET].iloc[:split_idx].to_numpy(dtype=float), index=df["timestamp"].iloc[:split_idx])
    test = pd.Series(df[TARGET].iloc[split_idx:].to_numpy(dtype=float), index=df["timestamp"].iloc[split_idx:])
    if len(train) != 3360 or len(test) != 840:
        raise AssertionError("Expected 3360 training and 840 held-out observations")
    return train, test, df["timestamp"].iloc[:split_idx], df["timestamp"].iloc[split_idx:]


def horizon_metrics(actual: np.ndarray, forecast: np.ndarray) -> dict[str, float]:
    actual = np.asarray(actual, dtype=float)
    forecast = np.asarray(forecast, dtype=float)
    valid = np.isfinite(actual) & np.isfinite(forecast)
    actual = actual[valid]
    forecast = forecast[valid]
    error = actual - forecast
    mae = float(np.mean(np.abs(error)))
    mse = float(np.mean(error ** 2))
    rmse = float(np.sqrt(mse))
    nonzero = np.abs(actual) > np.finfo(float).eps
    mape = float(np.mean(np.abs(error[nonzero] / actual[nonzero])) * 100.0) if np.any(nonzero) else float("nan")
    smape = float(np.mean(200.0 * np.abs(error) / (np.abs(actual) + np.abs(forecast) + np.finfo(float).eps)))
    denom = np.sum((actual - np.mean(actual)) ** 2)
    r2 = float(1.0 - np.sum(error ** 2) / denom) if denom > 0 else float("nan")
    return {"MAE": mae, "MSE": mse, "RMSE": rmse, "MAPE_percent": mape, "sMAPE_percent": smape, "R2": r2}


def save_common_outputs(
    outdir: Path,
    model_name: str,
    df: pd.DataFrame,
    train: pd.Series,
    test: pd.Series,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    dataset_path: Path,
    model_parameters: dict,
) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    diagnostics = outdir / "diagnostics"
    plots = outdir / "plots"
    diagnostics.mkdir(exist_ok=True)
    plots.mkdir(exist_ok=True)

    records = []
    for h in range(STEPS):
        m = horizon_metrics(y_true[:, h], y_pred[:, h])
        records.append({"Horizon": f"t+{h+1}", "Samples": int(len(y_true)), **m})
        pd.DataFrame({
            "Actual": y_true[:, h],
            "Forecast": y_pred[:, h],
            "Error": y_true[:, h] - y_pred[:, h],
        }).to_csv(diagnostics / f"forecast_values_horizon_t_plus_{h+1:02d}.csv", index_label="Sample")

        fig, ax = plt.subplots(figsize=(12.8, 6.4))
        ax.plot(np.arange(len(y_true)), y_true[:, h], label="Actual", linewidth=1.5)
        ax.plot(np.arange(len(y_pred)), y_pred[:, h], label="Forecast", linewidth=1.3, linestyle="--")
        ax.set_title(f"{model_name}: Forecast vs Actual — Horizon t+{h+1}")
        ax.set_xlabel("Held-out rolling origin")
        ax.set_ylabel("use_kW")
        ax.legend(loc="best")
        fig.tight_layout()
        fig.savefig(plots / f"forecast_vs_actual_horizon_t_plus_{h+1:02d}.png", dpi=180, bbox_inches="tight")
        plt.close(fig)

    metrics_df = pd.DataFrame(records)
    metrics_df.to_csv(diagnostics / "forecast_metrics_by_horizon.csv", index=False)

    flat_true = y_true.reshape(-1)
    flat_pred = y_pred.reshape(-1)
    overall = horizon_metrics(flat_true, flat_pred)
    model_eval = {"metric": "RMSE", "value": overall["RMSE"], "n_test": int(flat_true.size)}
    (outdir / "model_evaluation.json").write_text(json.dumps(model_eval, indent=2), encoding="utf-8")
    (outdir / "overall_metrics.json").write_text(json.dumps({**overall, "n_test": int(flat_true.size)}, indent=2), encoding="utf-8")

    metadata = {
        "execution_kind": "independent corrected-use_kW rerun",
        "compiler_protocol_reference": "ML2++ PythonJava V13.1 Chapter-validation rolling-origin semantics",
        "model": model_name,
        "target": TARGET,
        "forecast_steps": STEPS,
        "split_policy": "first_80_percent_train_last_20_percent_test",
        "training_rows": int(len(train)),
        "held_out_rows": int(len(test)),
        "complete_rolling_origins": int(len(y_true)),
        "dataset_sha256": sha256_file(dataset_path),
        "dataset_rows": int(len(df)),
        "dataset_start_utc": str(df["timestamp"].iloc[0]),
        "dataset_end_utc": str(df["timestamp"].iloc[-1]),
        "target_min": float(df[TARGET].min()),
        "target_max": float(df[TARGET].max()),
        "target_mean": float(df[TARGET].mean()),
        "model_parameters": model_parameters,
        "python": sys.version,
        "platform": platform.platform(),
        "packages": {
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scipy": scipy.__version__,
            "scikit-learn": sklearn.__version__,
            "statsmodels": statsmodels.__version__,
            "matplotlib": matplotlib.__version__,
        },
    }
    (outdir / "run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    preflight = {
        "status": "PASS",
        "checks": {
            "dataset_sha256_matches_corrected_artifact": True,
            "rows": len(df) == 4200,
            "one_minute_cadence": True,
            "no_missing_target": True,
            "no_duplicate_timestamps": True,
            "training_rows": len(train) == 3360,
            "held_out_rows": len(test) == 840,
            "complete_three_step_origins": len(y_true) == 838,
        },
    }
    (outdir / "rerun_preflight_report.json").write_text(json.dumps(preflight, indent=2), encoding="utf-8")

    manifest = []
    for p in sorted(outdir.rglob("*")):
        if p.is_file():
            manifest.append({"file": str(p.relative_to(outdir)), "sha256": sha256_file(p), "bytes": p.stat().st_size})
    (outdir / "SHA256_MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def run_arima(df: pd.DataFrame, train: pd.Series, test: pd.Series, outdir: Path, dataset_path: Path) -> None:
    # Exact Chapter-5 DSL configuration: ARIMA(1,1,1), trend='n'.
    model = ARIMA(train, order=(1, 1, 1), seasonal_order=(0, 0, 0, 0), trend="n")
    model_fit = model.fit()

    state = model_fit
    pred_rows: list[np.ndarray] = []
    true_rows: list[np.ndarray] = []
    for origin in range(len(test) - STEPS + 1):
        fc = np.asarray(state.forecast(steps=STEPS), dtype=float).reshape(-1)
        truth = np.asarray(test.iloc[origin:origin + STEPS], dtype=float).reshape(-1)
        if len(fc) != STEPS or len(truth) != STEPS:
            continue
        pred_rows.append(fc)
        true_rows.append(truth)
        if origin < len(test) - 1:
            state = state.append(test.iloc[origin:origin + 1], refit=False)

    y_pred = np.vstack(pred_rows)
    y_true = np.vstack(true_rows)
    if y_true.shape != (838, 3):
        raise AssertionError(f"Unexpected ARIMA evaluation shape {y_true.shape}")
    save_common_outputs(
        outdir, "ARIMA(1,1,1)", df, train, test, y_true, y_pred, dataset_path,
        {"order": [1, 1, 1], "seasonal_order": [0, 0, 0, 0], "trend": "n", "refit_on_held_out": False},
    )


def run_holt_winters(df: pd.DataFrame, train: pd.Series, test: pd.Series, outdir: Path, dataset_path: Path) -> None:
    # Exact Chapter-5 DSL configuration.
    model = ExponentialSmoothing(
        train,
        trend="add",
        damped_trend=True,
        seasonal="add",
        seasonal_periods=SEASONAL_PERIOD,
        initialization_method="heuristic",
        use_boxcox=False,
    )
    model_fit = model.fit(optimized=True, remove_bias=False)
    params = dict(model_fit.params)
    history = pd.Series(train).copy()
    pred_rows: list[np.ndarray] = []
    true_rows: list[np.ndarray] = []

    for origin in range(len(test) - STEPS + 1):
        if origin == 0:
            state = model_fit
        else:
            base = model_fit.model
            hw_model = ExponentialSmoothing(
                history,
                trend=getattr(base, "trend", None),
                damped_trend=getattr(base, "damped_trend", False),
                seasonal=getattr(base, "seasonal", None),
                seasonal_periods=getattr(base, "seasonal_periods", None),
                initialization_method="estimated",
            )
            state = hw_model.fit(
                smoothing_level=params.get("smoothing_level"),
                smoothing_trend=params.get("smoothing_trend"),
                smoothing_seasonal=params.get("smoothing_seasonal"),
                damping_trend=params.get("damping_trend"),
                optimized=False,
            )
        fc = np.asarray(state.forecast(STEPS), dtype=float).reshape(-1)
        truth = np.asarray(test.iloc[origin:origin + STEPS], dtype=float).reshape(-1)
        if len(fc) != STEPS or len(truth) != STEPS:
            continue
        pred_rows.append(fc)
        true_rows.append(truth)
        history = pd.concat([history, test.iloc[origin:origin + 1]])

    y_pred = np.vstack(pred_rows)
    y_true = np.vstack(true_rows)
    if y_true.shape != (838, 3):
        raise AssertionError(f"Unexpected Holt-Winters evaluation shape {y_true.shape}")

    save_common_outputs(
        outdir, "Holt-Winters", df, train, test, y_true, y_pred, dataset_path,
        {
            "trend": "add", "damped_trend": True, "seasonal": "add",
            "seasonal_periods": 60, "initialization_method_initial_fit": "heuristic",
            "initialization_method_rolling_refilter": "estimated", "use_boxcox": False,
            "remove_bias": False, "optimized_initial_fit": True,
            "optimized_held_out_refilter": False,
            "fixed_smoothing_parameters": {
                k: (float(v) if isinstance(v, (int, float, np.floating)) else v)
                for k, v in params.items() if k in {"smoothing_level", "smoothing_trend", "smoothing_seasonal", "damping_trend"}
            },
        },
    )

    plots = outdir / "plots"
    fig, ax = plt.subplots(figsize=(12.8, 6.4))
    ax.plot(df["timestamp"], df[TARGET], linewidth=1.0)
    ax.set_title("Smart-home household power use")
    ax.set_xlabel("Time (UTC)")
    ax.set_ylabel("use_kW")
    fig.tight_layout()
    fig.savefig(plots / "line_use_kW.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(12.8, 6.4))
    plot_acf(df[TARGET].to_numpy(dtype=float), lags=120, ax=ax)
    ax.set_title("Autocorrelation of use_kW")
    fig.tight_layout()
    fig.savefig(plots / "acf_use_kW.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    # Refresh manifest to include line/ACF plots.
    manifest = []
    for p in sorted(outdir.rglob("*")):
        if p.is_file() and p.name != "SHA256_MANIFEST.json":
            manifest.append({"file": str(p.relative_to(outdir)), "sha256": sha256_file(p), "bytes": p.stat().st_size})
    (outdir / "SHA256_MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    df = load_data(args.data)
    train, test, _, _ = split_series(df)
    args.output.mkdir(parents=True, exist_ok=True)

    # Separate executions: fit and evaluate each model independently.
    run_arima(df, train, test, args.output / "SmartHomeARIMA_corrected_useKW", args.data)
    run_holt_winters(df, train, test, args.output / "SmartHomeHoltWinters_corrected_useKW", args.data)

    summary = {}
    for name in ["SmartHomeARIMA_corrected_useKW", "SmartHomeHoltWinters_corrected_useKW"]:
        p = args.output / name
        summary[name] = {
            "model_evaluation": json.loads((p / "model_evaluation.json").read_text()),
            "horizon_metrics": pd.read_csv(p / "diagnostics/forecast_metrics_by_horizon.csv").to_dict(orient="records"),
            "metadata": json.loads((p / "run_metadata.json").read_text()),
        }
    (args.output / "SMART_HOME_CORRECTED_RERUN_SUMMARY.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
