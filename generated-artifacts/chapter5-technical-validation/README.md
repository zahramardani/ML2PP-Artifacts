# Chapter 5 Technical-Validation Evidence

This directory contains the retained execution evidence used in Chapter 5 of the dissertation.

## Evaluated configurations

- River flow: LSTM and GRU
- Smart-home energy: ARIMA and Holt-Winters
- Solar power: XGBoost and Prophet

The river-flow forecasting target is `almourol_discharge`.

SARIMA is intentionally not part of the Chapter 5 technical-validation set. It belongs to the separate Stage 1--3 empirical workflow discussed in Chapter 6.

## Repository structure

### `model-instances/`
Six standalone `.thingml` model instances copied from the corresponding retained executed runs.

### `full-run-archives/`
One complete ZIP archive for each of the six retained Chapter 5 run directories. These archives preserve the run directory as supplied, including the merged ThingML model, generated Java/Python source, Maven output, model/checkpoint/pickle files, generated PNG plots, horizon-wise point predictions and metrics, preflight and leakage-audit reports, evaluation metadata, plot manifests, and run metadata.

### `Chapter5_Run_Records_Text_6_Models_2026-08-15.zip`
A smaller text-oriented bundle for direct inspection of the six model instances and text-based generated evidence without the larger binary model/plot files.

### `SHA256SUMS.txt`
SHA-256 checksums and byte sizes for the six full-run archives and the text-oriented bundle.

## Retained run identifiers

| Configuration | Run ID |
|---|---|
| River LSTM | `ML2RUN_dd3ced1e34f8c5bd` |
| River GRU | `ML2RUN_08456d77a0581444` |
| Smart-home ARIMA | `ML2RUN_0bff91e91c1d2114` |
| Smart-home Holt-Winters | `ML2RUN_3b520673ebbef3f6` |
| Solar XGBoost | `ML2RUN_c172ec1499ab509c` |
| Solar Prophet | `ML2RUN_672b6608ffe4419b` |

## Scope

These retained artifacts support the scoped technical-validation claims in Chapter 5. They do not establish exhaustive coverage of the ML2++ grammar, every supported or anticipated algorithm, every hyperparameter combination, or production deployment readiness.
