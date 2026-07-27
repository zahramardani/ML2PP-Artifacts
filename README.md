# ML2++ Research Artifacts

Research artifacts for **ML2++: Model-Driven Engineering for Time-Series
Forecasting in IoT and Cyber-Physical Systems**.

ML2++ is a model-driven framework and domain-specific modelling language for
specifying time-series forecasting workflows and connecting forecast horizons
to IoT/CPS behaviour. The main implementation is maintained separately in
[`micss-lab/ML-QuadratPP`](https://github.com/micss-lab/ML-QuadratPP).

## Repository status

This repository is an **incomplete but auditable artifact package**. It
documents six configurations reported as executed end to end:

| Use case | Configurations |
|---|---|
| River-flow forecasting | LSTM, GRU |
| Smart-home energy forecasting | ARIMA, Holt–Winters |
| Solar-power forecasting | XGBoost, Prophet |

The repository includes thesis-transcribed model specifications, aggregate
reported metrics, questionnaire instruments, provenance notes,
manifest/checksum tools, and runnable Python reference workflows for the
three thesis use cases. It does **not yet** include all byte-exact executed
models, generated sources, exact dataset snapshots or acquisition records,
dependency locks, point-level predictions, execution logs, and verified run
manifests. Therefore it must not yet be described as a complete numerical
replication package.

## Start here

- [`replication/README.md`](replication/README.md): evidence boundary,
  completion criteria, and verification instructions
- [`replication/ARTIFACT_INVENTORY.csv`](replication/ARTIFACT_INVENTORY.csv):
  machine-readable inventory of all six configurations
- [`replication/PACKAGE_STATUS.json`](replication/PACKAGE_STATUS.json):
  current package status and missing evidence
- [`replication/results/reported_metrics.csv`](replication/results/reported_metrics.csv):
  aggregate metrics transcribed from the dissertation
- [`replication/questionnaires/`](replication/questionnaires/):
  evaluation instruments; no participant identities or raw personal data
- [`replication/scripts/`](replication/scripts/): run-manifest creation and
  hash-verification utilities
- [`datasets/`](datasets/): dataset specifications and legal/provenance
  requirements
- [`USE_CASES.md`](USE_CASES.md): thesis-to-artifact map for all three domains
- [`examples/python/`](examples/python/): runnable Python reference workflows,
  synthetic-data fallbacks, configurations, metrics, plots, and tests

## Pinned implementation revision

The dissertation results reference ML-QuadratPP revision:

`4253f75e7f3b3f94620d79e672e4db52b477d32c`

Use that revision when reconstructing the evaluated generator and runtime.

## Data protection

Do not commit participant identities, raw participant responses, credentials,
restricted datasets, or third-party data without redistribution permission.
See [`replication/docs/DATA_PROTECTION.md`](replication/docs/DATA_PROTECTION.md).

## Citation and licensing

Citation metadata is provided in [`CITATION.cff`](CITATION.cff). A
repository-wide licence has not yet been selected; see
[`LICENSE_STATUS.md`](LICENSE_STATUS.md). Third-party material retains its
original terms.

## Author

**Zahra Mardani Korani**  
LNEC/CICTI and Iscte-IUL/ISTA/ISTAR

Supervisors: João Carlos Ferreira, Armin Moin, and Alberto Rodrigues da Silva.
