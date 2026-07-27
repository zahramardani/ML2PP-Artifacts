# ML2++ PhD reproducibility package

This directory is the evidence boundary for the forecasting configurations
reported in the ML2++ dissertation. It is intentionally explicit about what
is present, what is only a reference example, and what is still required.

## Current status

**Incomplete but uploadable.** This package now contains thesis-transcribed
DSL specifications for the six reported technical-validation runs, a
machine-readable transcription of the aggregate metric tables, the complete
questionnaire-instrument appendix, provenance documentation, and manifest
creation/verification tools. It does not contain the byte-exact executed
models, exact generated sources, dataset split files, dependency locks,
point-level prediction files, execution logs, or run manifests.

The existing files `LSTM.thingml`, `GRU.thingml`, `ARIMA.thingml`, and
`xgboost.thingml` under the textual-editor samples are useful reference
models. They must not be presented as the exact dissertation configurations
without checking them against the original executed files. Known differences
include feature names, algorithm/seasonal settings, and forecast horizons.
See [ARTIFACT_INVENTORY.csv](ARTIFACT_INVENTORY.csv).

The model files under `runs/*/model/` reproduce the revised thesis listings
and are marked accordingly in their headers. They resolve the absence of
public model documentation but do not, without the original files and logs,
establish L2 generation or L3 execution provenance.

## Runs that require complete archival

1. `river-flow-lstm`
2. `river-flow-gru`
3. `smart-home-arima`
4. `smart-home-holt-winters`
5. `solar-power-xgboost`
6. `solar-power-prophet`

All six configurations were executed end to end in the dissertation work.
For Prophet, as for the other configurations, this repository currently
preserves a thesis-transcribed specification rather than the byte-exact
executed model, generated sources, logs, data snapshot, and point-level
predictions. The absence of those archived files is a reproducibility
limitation; it is not evidence that the backend execution was incomplete.

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

For datasets that cannot legally be redistributed, include a stable source
URL, acquisition date, query/export parameters, licence, preprocessing steps,
and a SHA-256 checksum of the exact local input. Do not upload restricted data.

## Creating and verifying a manifest

After copying the original artefacts into a run directory, create its
manifest:

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

The manifest proves file identity; it does not by itself prove that a file
was generated. Preserve the generator log and command, and label manually
written compatible scripts as `reference` rather than `generated`.

## Evaluation instruments and participant data

Standalone questionnaire instruments may be placed in `questionnaires/`.
Participant-level responses, identities, session recordings, and raw logs
must not be committed unless the consent form and data-protection assessment
explicitly permit public release. Prefer anonymised aggregate tables and a
clear description of filtering and scale direction.

## Completion criterion

This directory may be called a complete numerical replication package only
after all six runs contain their exact model, generated artefacts, data
provenance, environment lock, metrics, prediction files, logs, and a manifest
whose hashes verify successfully.
