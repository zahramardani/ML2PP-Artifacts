# Chapter 5 Technical-Validation Evidence

This directory contains the six executed ML2++ model instances and the retained browsable run evidence used for Chapter 5 of the dissertation.

## Evaluated configurations

- River flow: LSTM and GRU
- Smart-home energy: ARIMA and Holt-Winters
- Solar power: XGBoost and Prophet

The river-flow forecasting target is `almourol_discharge`.

SARIMA is intentionally not part of the Chapter 5 technical-validation set. It belongs to the separate Stage 1--3 empirical workflow discussed in Chapter 6.

## Repository structure

- `model-instances/` — six standalone `.thingml` instances copied from the retained executed runs.
- `run-records/` — per-model generated run evidence: run metadata, preflight reports, leakage-audit reports, evaluation metadata, plot manifests, horizon-wise metric summaries, and XGBoost tuning-selection records where applicable.
- Each run-record folder also contains a SHA-256 file manifest for the complete retained local run directory. The manifest covers generated source, point-level prediction CSVs, PNG plots, model/checkpoint/pickle files, Maven outputs, and the other retained files even when a large binary file is not directly browsable in this repository copy.

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

These artifacts support the scoped technical-validation claims in Chapter 5. They do not establish exhaustive coverage of the ML2++ grammar, every supported or anticipated algorithm, every hyperparameter combination, or production deployment readiness.
