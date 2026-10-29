# Repository guide

[Research README](../README.md) · [All projects](../PROJECTS.md)

## Directory responsibilities

| Directory | Purpose |
|---|---|
| [datasets/](../datasets/) | Deposited research subsets, data cards and acquisition/preprocessing documentation |
| [generated-artifacts/chapter5-technical-validation/](../generated-artifacts/chapter5-technical-validation/) | Retained Chapter 5 model instances, text evidence and checksum lists |
| [replication/runs/](../replication/runs/) | Six thesis-transcribed specifications and per-run status |
| [replication/results/](../replication/results/) | Reported metric transcription and provenance notes |
| [replication/scripts/](../replication/scripts/) | Manifest creation, verification and package utilities |
| [replication/questionnaires/](../replication/questionnaires/) | Instruments, tutorial and deposited Stage 4 tables |
| [replication/studies/](../replication/studies/) | Existing staged-study material |
| [examples/python/](../examples/python/) | Runnable forecasting companions; synthetic data by default |
| [portfolio/](../portfolio/) | Independent API, microservice and RAG demonstrations |
| [publications/](../publications/) | Publication documentation and bibliography |
| [thesis/source/](../thesis/source/) | Deposited dissertation bibliography |
| [docs/](../docs/) | Navigation and reading guides |

The `language/`, `generators/`, `experiments/`, `evaluation/`, `use-cases/` and `generated-artifacts/` directories also contain historical overview or placeholder documentation. Use this guide and the linked artifact paths to identify actual deposited files.

## Reading order

1. Read [USE_CASES.md](../USE_CASES.md) for the research scope.
2. Inspect the [retained evidence](../generated-artifacts/chapter5-technical-validation/README.md).
3. Read the relevant [dataset documentation](../datasets/README.md).
4. Check [replication status](../replication/PACKAGE_STATUS.json) before attempting numerical reconstruction.
5. Use [Python companions](../examples/python/README.md) for a self-contained workflow demonstration.

## Evidence types

| Material | What it establishes |
|---|---|
| Retained model instance | The deposited model text |
| Text run record | The recorded metadata, audits and quantitative summaries |
| Full-run checksum list | The recorded identities of files in the retained local run |
| Thesis-transcribed specification | A specification aligned with the documented thesis listing |
| Python companion or portfolio app | An inspectable implementation with its own stated scope |

A checksum for an absent file does not provide that file. A runnable synthetic demonstration does not reproduce the dissertation's numerical results.

## Path stability

Legacy run IDs and paths such as `smart-home-energy` remain stable. Human-readable documentation may use **Smart Energy**. Reference paths should be checked against the deposited files before being cited.
