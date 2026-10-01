# ML2++ PhD reproducibility package

This directory is the evidence boundary for the forecasting configurations reported in the ML2++ dissertation. It documents the complete public reproducibility package accompanying the thesis and keeps model, data, execution, environment, result, and provenance evidence clearly separated.

## Current status

**Complete public thesis reproducibility package.** The package provides complete thesis-listing specification coverage for the three final Chapter 5 technical-validation use cases: six run-specific DSL specifications aligned on 2026-08-14, together with the corresponding retained execution records, aggregate and horizon-wise quantitative evidence, provenance metadata, and checksum manifests. The six configurations are LSTM and GRU for River flow, ARIMA(1,1,1) and Holt–Winters for Smart Energy, and XGBoost and Prophet for Solar power.

The existing files `LSTM.thingml`, `GRU.thingml`, `ARIMA.thingml`, and `xgboost.thingml` under textual-editor samples are useful reference models. They must not be presented as the exact dissertation configurations without checking them against the final technical-validation specifications. Known differences can include feature names, algorithm/seasonal settings, preprocessing, and forecast horizons. See [ARTIFACT_INVENTORY.csv](ARTIFACT_INVENTORY.csv).

The model files under `runs/*/model/` reproduce the final Chapter 5 thesis listings and are marked accordingly in their headers. Retained run evidence, generated-artifact hashes, dataset hashes, and execution metadata provide the public provenance boundary for the thesis results.

## Archived runs

1. `river-flow-lstm`
2. `river-flow-gru`
3. `smart-home-arima`
4. `smart-home-holt-winters`
5. `solar-power-xgboost`
6. `solar-power-prophet`

All six configurations are reported as executed end to end in the dissertation's final technical-validation chapter. The repository preserves the public evidence associated with those executions through thesis-aligned model specifications, retained run records, quantitative summaries, provenance metadata, and SHA-256 manifests.

## Required layout for each run

Place each run under `replication/runs/<run-id>/` using this layout:

```text
<run-id>/
├── model/          exact ML2++ model instance submitted to the generator
├── generated/      unmodified files emitted by the pinned generator
├── data/           acquisition instructions, checksums and split indices
├── environment/    dependency lock, software and hardware information
├── results/        metrics, horizon-wise predictions and figures
├── logs/           generation and execution logs
└── run-manifest.json
```

For datasets that cannot legally be redistributed, include a stable source URL, acquisition date, query/export parameters, licence, preprocessing steps, and a SHA-256 checksum of the exact local input. Do not upload restricted data.

## Creating and verifying a manifest

After copying the original artefacts into a run directory, create its manifest:

```bash
python replication/scripts/create_run_manifest.py \
  --run-dir replication/runs/river-flow-lstm \
  --run-id river-flow-lstm \
  --generator-commit 4253f75e7f3b3f94620d79e672e4db52b477d32c \
  --command "<exact execution command>"
```

Then verify all archived hashes:

```bash
python replication/scripts/verify_run_manifest.py \
  replication/runs/river-flow-lstm/run-manifest.json
```

The manifest proves file identity; it does not by itself prove that a file was generated. Preserve the generator log and command, and label manually written compatible scripts as `reference` rather than `generated`.

## Evaluation instruments and participant data

Standalone questionnaire instruments may be placed in `questionnaires/`. Participant-level responses, identities, session recordings, and raw logs must not be committed unless the consent form and data-protection assessment explicitly permit public release. Prefer anonymised aggregate tables and a clear description of filtering and scale direction.

## Package scope

The public package is organised around the six Chapter 5 configurations and their dissertation evidence. Run-level identity and provenance are recorded through model specifications, run identifiers, generated-script and dataset hashes, retained quantitative evidence, and verification manifests.
