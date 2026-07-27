#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ml2pp_reference.core import USE_CASES, load_frame, metrics, persist_config, supervised
from ml2pp_reference.models import (
    fit_arima, fit_holt_winters, fit_linear_sequence, fit_prophet, fit_xgboost,
)


def parse_args():
    parser = argparse.ArgumentParser(description="Run an ML2++ thesis use case.")
    parser.add_argument("usecase", choices=USE_CASES)
    parser.add_argument("--csv", help="Optional user-owned CSV; synthetic data is default.")
    parser.add_argument("--model", help="Model name; defaults to the first model for the use case.")
    parser.add_argument("--output", default="artifacts")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main():
    args = parse_args()
    cfg = USE_CASES[args.usecase]
    model_name = args.model or cfg.models[0]
    if model_name not in cfg.models:
        raise SystemExit(f"Choose one of: {', '.join(cfg.models)}")
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    frame = load_frame(args.usecase, args.csv)
    x, y = supervised(frame, cfg)
    split = int(len(x) * 0.8)
    x_train, x_test, y_train, y_test = x[:split], x[split:], y[:split], y[split:]

    if model_name == "linear-sequence":
        predicted = fit_linear_sequence(x_train, y_train, x_test)
    elif model_name == "xgboost":
        predicted = fit_xgboost(x_train, y_train, x_test)
    elif model_name in {"arima", "holt-winters"}:
        raw_split = cfg.n_in + split
        train = frame[cfg.target].to_numpy()[:raw_split]
        history = frame[cfg.target].to_numpy()[raw_split : raw_split + len(y_test)]
        runner = fit_arima if model_name == "arima" else fit_holt_winters
        predicted = runner(train, history, cfg.n_out)
    elif model_name == "prophet":
        raw_split = cfg.n_in + split
        predicted = fit_prophet(
            frame["timestamp"], frame[cfg.target].to_numpy(), raw_split, cfg.n_out
        )
        y_test = y_test[: len(predicted)]
    else:
        raise AssertionError(model_name)

    prediction_rows = []
    for horizon in range(cfg.n_out):
        prediction_rows.append(
            pd.DataFrame(
                {
                    "sample": np.arange(len(y_test)),
                    "horizon": horizon + 1,
                    "observed": y_test[:, horizon],
                    "predicted": predicted[:, horizon],
                    "model": model_name,
                }
            )
        )
    pd.concat(prediction_rows).to_csv(output / "predictions.csv", index=False)
    scores = metrics(y_test, predicted)
    scores.insert(0, "model", model_name)
    scores.to_csv(output / "metrics.csv", index=False)
    persist_config(output, cfg, args.csv, args.seed)

    plt.figure(figsize=(10, 4))
    plt.plot(y_test[:200, 0], label="observed", linewidth=1.5)
    plt.plot(predicted[:200, 0], label="predicted t+1", linewidth=1.2)
    plt.xlabel("Test sample")
    plt.ylabel(cfg.target)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output / "forecast.png", dpi=180)
    print(scores.to_string(index=False))


if __name__ == "__main__":
    main()

