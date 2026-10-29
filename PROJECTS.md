# Zahra Mardani Korani — Project Catalog

Applied machine learning, time-series forecasting, model-driven engineering and software prototypes.

[GitHub profile](https://github.com/zahramardani) · [ML2++ research entry point](README.md)

## Research and engineering demonstrations

| Project | What to inspect | Start here |
|---|---|---|
| ML2++ research artifacts | Forecasting DSL models, retained run records, datasets and reference workflows | [Research README](README.md) |
| Forecasting API | Synthetic time series, XGBoost versus persistence, FastAPI, Docker and tests | [river_prediction](https://github.com/zahramardani/river_prediction) |
| SQL station analytics | SQLite schema, joins, CTEs, windows and gap-aware historical features | [SQL walkthrough](https://github.com/zahramardani/river_prediction/tree/main/sql/station_analytics) |
| ML2++ RAG Copilot | Document retrieval, optional semantic retrieval, optional LLM answers and evaluation scripts | [RAG Copilot](portfolio/ml2pp-rag-copilot/README.md) |
| AI microservice | FastAPI inference, SQL persistence, a Go gateway and deployment packaging | [Microservice demo](portfolio/ai-microservice-demo/README.md) |

The API, SQL and RAG examples are portfolio prototypes. Their synthetic data, demonstration metrics and deployment templates are separate from validated research outcomes.

## Historical applications and design archives

| Repository | Contents | Status |
|---|---|---|
| [river_prediction1](https://github.com/zahramardani/river_prediction1) | Django station-data and preprocessing interface | Earlier prototype; incomplete training integration |
| [Temperature-Monitoring-System](https://github.com/zahramardani/Temperature-Monitoring-System) | Eclipse/Xtext metadata and original project archive | Historical project export |
| [Smart-Home-Heterogeneous-hardware-](https://github.com/zahramardani/Smart-Home-Heterogeneous-hardware-) | Original smart-home design archive | Historical design export |

## How the repositories fit together

- **Research:** this repository collects ML2++ artifacts. The main language/compiler implementation lives in [micss-lab/ML-QuadratPP](https://github.com/micss-lab/ML-QuadratPP).
- **Engineering portfolio:** `river_prediction` hosts the forecasting service, SQL example and small retrieval demonstration. Larger RAG and microservice prototypes live under this repository's [portfolio directory](portfolio/README.md).
- **Earlier work:** `river_prediction1` contains the Django prototype. The two IoT repositories preserve original project/design exports.

Stable repository names and existing artifact paths are retained so links from papers, CVs and earlier work continue to resolve.
