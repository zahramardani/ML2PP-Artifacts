# Chapter 5 Technical-Validation Evidence

This directory contains the six ML2++ model instances and the retained text-based execution evidence used in Chapter 5 of the dissertation. SARIMA is intentionally excluded from Chapter 5; it belongs to the separate Stage 1--3 empirical workflow discussed in Chapter 6.

## Configurations

- River flow: LSTM and GRU
- Smart-home energy: ARIMA and Holt-Winters
- Solar power: XGBoost and Prophet

River-flow forecasting target: `almourol_discharge`.

## Structure

- `model-instances/` — six standalone `.thingml` model instances copied from the corresponding retained executed runs.
- `runs/` — corresponding retained generated run records. Each run contains the merged ThingML model, generated `preprocess.py` and `train.py`, preflight and leakage-audit reports, model-evaluation metadata, run metadata, plot manifests, horizon-wise metrics, and point-level forecast CSV files. XGBoost additionally includes the retained tuning-selection records.
- `SHA256SUMS.txt` — hashes for the complete local evidence package, including binary model/checkpoint and PNG files.

## Binary run artifacts

The GitHub browser copy focuses on model instances, generated source, metadata, metrics, and point-level prediction records. Large binary cache/checkpoint files and PNG plot files are not committed here; their SHA-256 hashes are retained in `SHA256SUMS.txt`. The numerical plot inputs and horizon-wise point predictions required to regenerate the reported forecast plots are committed under each run's `plots/diagnostics/` directory.

## Scope

These artifacts support the scoped technical-validation claims in Chapter 5. They do not establish exhaustive coverage of the ML2++ grammar, every supported or anticipated algorithm, all hyperparameter combinations, or production deployment readiness.
