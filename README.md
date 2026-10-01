# ML2++ Research Artifacts

Research artifacts for **ML2++: Model-Driven Engineering for Time-Series Forecasting in IoT and Cyber-Physical Systems**.

ML2++ is a model-driven framework and domain-specific modelling language for specifying time-series forecasting workflows and connecting forecast horizons to IoT/CPS behaviour. The main implementation is maintained separately in [`micss-lab/ML-QuadratPP`](https://github.com/micss-lab/ML-QuadratPP).

**Live ML2++ web environment:** https://ml2plusplus.jvmhost.net/

## Repository status

This repository is the **complete public research-artifact package accompanying the dissertation**. The thesis-aligned model specifications and retained Chapter 5 execution evidence cover the six configurations in the final Chapter 5 technical validation (2026-08-14):

| Use case | Configurations |
|---|---|
| River-flow forecasting | LSTM, GRU |
| Smart Energy forecasting | ARIMA(1,1,1), Holt–Winters |
| Solar-power forecasting | XGBoost, Prophet |

This gives **complete model-specification coverage for the three Chapter 5 use cases (6/6 configurations)** together with the public run records, quantitative summaries, provenance information, checksum manifests, questionnaire instruments, datasets or dataset documentation, and runnable companion workflows included in this repository.

The public package is organised to preserve the evidence boundary used by the dissertation: thesis-aligned model specifications, retained execution records, aggregate and horizon-wise metrics, generated-artifact provenance, checksums, and supporting documentation are kept separately so that each type of evidence remains traceable.

Human-readable thesis documentation uses **Smart Energy**. Stable technical artifact identifiers such as `smart-home-energy`, `use_kW`, and `datasets/smart-home-energy/` are retained where necessary for reproducibility and path stability.

## Start here

- [`replication/README.md`](replication/README.md): evidence boundary, completion criteria, and verification instructions
- [`replication/ARTIFACT_INVENTORY.csv`](replication/ARTIFACT_INVENTORY.csv): machine-readable inventory of all six configurations
- [`replication/PACKAGE_STATUS.json`](replication/PACKAGE_STATUS.json): current package status and public artifact scope
- [`replication/results/reported_metrics.csv`](replication/results/reported_metrics.csv): aggregate metrics aligned with final Chapter 5 Tables 1.4–1.6
- [`replication/runs/`](replication/runs/): run-specific thesis-transcribed model specifications
- [`replication/questionnaires/`](replication/questionnaires/): evaluation instruments; no participant identities or raw personal data
- [`replication/scripts/`](replication/scripts/): run-manifest creation and hash-verification utilities
- [`datasets/`](datasets/): dataset specifications and legal/provenance requirements
- [`USE_CASES.md`](USE_CASES.md): thesis-to-artifact map for all three domains
- [`examples/python/`](examples/python/): runnable Python companion workflows; not byte-exact generated provenance for the six final executions

## Pinned implementation revision

The dissertation results reference ML-QuadratPP revision:

`4253f75e7f3b3f94620d79e672e4db52b477d32c`

Use that revision when reconstructing the evaluated generator and runtime.

## Data protection

Do not commit participant identities, raw participant responses, credentials, restricted datasets, or third-party data without redistribution permission. See [`replication/docs/DATA_PROTECTION.md`](replication/docs/DATA_PROTECTION.md).

## Citation and licensing

Citation metadata is provided in [`CITATION.cff`](CITATION.cff). A repository-wide licence has not yet been selected; see [`LICENSE_STATUS.md`](LICENSE_STATUS.md). Third-party material retains its original terms.

## Author

**Zahra Mardani Korani**  
LNEC/CICTI and Iscte-IUL/ISTA/ISTAR

Supervisors: João Carlos Ferreira, Armin Moin, and Alberto Rodrigues da Silva.
