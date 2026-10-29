# ML2++ Research Artifacts

Research artifacts for **Model-Driven Engineering for Time-Series Forecasting in IoT and Cyber-Physical Systems**.

**Zahra Mardani Korani** · LNEC/CICTI and Iscte-IUL/ISTA/ISTAR  
[All projects](PROJECTS.md) · [Repository guide](docs/REPOSITORY_GUIDE.md) · [Portfolio demonstrations](portfolio/README.md)

ML2++ provides a domain-specific modelling language and model-driven workflows for forecasting and its integration with IoT/CPS behaviour. The main implementation is maintained in [micss-lab/ML-QuadratPP](https://github.com/micss-lab/ML-QuadratPP). The documented web environment is [ML2++](https://ml2plusplus.jvmhost.net/); availability is independent of this repository.

## Start here

| Goal | Entry point |
|---|---|
| Understand the three research use cases | [Use cases](USE_CASES.md) |
| Inspect retained Chapter 5 model instances and run records | [Technical-validation evidence](generated-artifacts/chapter5-technical-validation/README.md) |
| Find datasets and their provenance | [Dataset catalog](datasets/README.md) |
| Inspect thesis-transcribed configurations and replication status | [Replication guide](replication/README.md) |
| Run companion forecasting workflows | [Python reference examples](examples/python/README.md) |
| Find evaluation instruments and study material | [Questionnaires](replication/questionnaires/README.md) · [Study directory](replication/studies/study1_eight_participants/README.md) |
| Explore independent API and RAG projects | [Portfolio index](portfolio/README.md) |
| Map dissertation material to available files | [Artifact map](ARTIFACT_MAP.md) |

## Research configurations

| Use case | Documented configurations |
|---|---|
| River flow | LSTM, GRU |
| Smart Energy | ARIMA(1,1,1), Holt–Winters |
| Solar power | XGBoost, Prophet |

Two collections serve different purposes:

- [Chapter 5 evidence](generated-artifacts/chapter5-technical-validation/) contains retained model instances, text run records and full-run checksum lists.
- [Replication runs](replication/runs/) contains thesis-transcribed specifications and per-run status documentation.

Six specifications are present. Original generated sources, point-level predictions, full logs and complete local run directories are not all deposited here. A checksum list identifies retained local files; it does not make absent files available for independent verification. See the [package status](replication/PACKAGE_STATUS.json) and [artifact inventory](replication/ARTIFACT_INVENTORY.csv).

## Run a companion workflow

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r examples/python/requirements.txt
python examples/python/run_usecase.py river --output artifacts/river
```

The examples use synthetic data by default. Their outputs are separate from the dissertation's reported results. The [example guide](examples/python/README.md) documents all three workflows and CSV schemas.

## Implementation revision

The documented generator revision is [4253f75e7f3b3f94620d79e672e4db52b477d32c](https://github.com/micss-lab/ML-QuadratPP/tree/4253f75e7f3b3f94620d79e672e4db52b477d32c). Use the revision appropriate to the retained run being reconstructed; consult that run's metadata.

## Data, citation and licensing

Study material and dataset documentation have separate provenance and access boundaries. Follow the [data-protection guidance](replication/docs/DATA_PROTECTION.md) and each dataset's source terms. Participant-related files already present are not an authorization to redistribute additional study records.

[CITATION.cff](CITATION.cff) supplies citation metadata. A repository-wide licence has not been selected; see [LICENSE_STATUS.md](LICENSE_STATUS.md).

Supervisors: João Carlos Ferreira, Armin Moin and Alberto Rodrigues da Silva.
