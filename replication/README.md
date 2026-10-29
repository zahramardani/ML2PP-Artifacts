# ML2++ Replication Guide

[Research README](../README.md) · [Artifact inventory](ARTIFACT_INVENTORY.csv) · [Package status](PACKAGE_STATUS.json)

## What is deposited

This directory contains six thesis-transcribed forecasting specifications, per-run status notes, reported metric tables, instruments and manifest utilities. It is one part of the public artifact collection.

The newer [Chapter 5 evidence collection](../generated-artifacts/chapter5-technical-validation/README.md) separately contains retained model instances, text run records and full-run checksum lists. Both collections should be consulted; they have different provenance.

## Find a configuration

| Run | Transcribed specification and status | Retained execution records |
|---|---|---|
| River LSTM | [river-flow-lstm](runs/river-flow-lstm/) | [RiverForecastLSTM_Chapter5](../generated-artifacts/chapter5-technical-validation/run-records/RiverForecastLSTM_Chapter5/) |
| River GRU | [river-flow-gru](runs/river-flow-gru/) | [RiverForecastGRU_Chapter5](../generated-artifacts/chapter5-technical-validation/run-records/RiverForecastGRU_Chapter5/) |
| Smart Energy ARIMA | [smart-home-arima](runs/smart-home-arima/) | [SmartHomeARIMA_Chapter5](../generated-artifacts/chapter5-technical-validation/run-records/SmartHomeARIMA_Chapter5/) |
| Smart Energy Holt–Winters | [smart-home-holt-winters](runs/smart-home-holt-winters/) | [SmartHomeHoltWinters_Chapter5](../generated-artifacts/chapter5-technical-validation/run-records/SmartHomeHoltWinters_Chapter5/) |
| Solar XGBoost | [solar-power-xgboost](runs/solar-power-xgboost/) | [SolarXGBoost_Chapter5](../generated-artifacts/chapter5-technical-validation/run-records/SolarXGBoost_Chapter5/) |
| Solar Prophet | [solar-power-prophet](runs/solar-power-prophet/) | [SolarProphet_Chapter5](../generated-artifacts/chapter5-technical-validation/run-records/SolarProphet_Chapter5/) |

## Current limits

Specification coverage is **6/6**. Original generated sources, point-level predictions, complete logs and original run directories are not all deposited. The per-run status notes describe these gaps. The checksum lists in the retained-evidence collection identify local run files; the files themselves must be available before those hashes can be checked independently.

The [reported metrics CSV](results/reported_metrics.csv) is a transcription with its own [provenance note](results/RESULTS_PROVENANCE.md). Running a synthetic companion does not regenerate those scientific values.

## Verify an original run when its files are available

From the repository root, after obtaining the actual run artifacts:

```bash
python replication/scripts/create_run_manifest.py \
  --run-dir replication/runs/river-flow-lstm \
  --run-id river-flow-lstm \
  --generator-commit 4253f75e7f3b3f94620d79e672e4db52b477d32c \
  --command "<exact execution command>"

python replication/scripts/verify_run_manifest.py \
  replication/runs/river-flow-lstm/run-manifest.json
```

The manifest tool creates a new record for the files supplied. It does not recover absent historical files or establish that manually written code was generated.

## Data and study material

- [Datasets](../datasets/README.md): deposited inputs, reconstruction scripts and source terms.
- [Questionnaires](questionnaires/README.md): instruments, tutorial and deposited Stage 4 tables.
- [Staged study](studies/study1_eight_participants/README.md): existing study archives and model material.
- [Data-protection guidance](docs/DATA_PROTECTION.md): access and release boundaries.

For a runnable demonstration, start with the [Python reference examples](../examples/python/README.md).
