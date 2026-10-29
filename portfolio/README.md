# Engineering Portfolio

Independent software demonstrations by **Zahra Mardani Korani**.

[All projects](../PROJECTS.md) · [Research artifacts](../README.md)

## Choose a project

| Project | Main components | Guide |
|---|---|---|
| AI microservice | FastAPI, Isolation Forest, SQLAlchemy, SQLite/PostgreSQL, Go gateway, Docker, Kubernetes/Helm templates | [README](ai-microservice-demo/README.md) |
| ML2++ RAG Copilot | Document chunking, TF-IDF retrieval, optional local embeddings, optional LLM generation, evaluation scripts | [README](ml2pp-rag-copilot/README.md) |
| Forecasting API | XGBoost, persistence baseline, FastAPI, Docker and monitoring helpers | [Separate repository](https://github.com/zahramardani/river_prediction) |
| SQL station analytics | SQLite, CTEs, window functions and gap-aware lag checks | [SQL project](https://github.com/zahramardani/river_prediction/tree/main/sql/station_analytics) |

## Run one application at a time

Each application has its own requirements and relative data paths. From this repository's root, enter the selected application directory before following its setup guide:

```bash
cd portfolio/ai-microservice-demo
```

or:

```bash
cd portfolio/ml2pp-rag-copilot
```

Use a separate virtual environment for each application. Both FastAPI examples use port 8000 by default, so stop one before starting the other on that port.

The RAG Copilot supports retrieval without a paid API. Generated answers require a configured provider key. The microservice provides local explanations when an LLM key is absent. See each README for commands and configuration.

## Scope

These are small portfolio prototypes with their own tests and CI workflows. Deployment manifests show packaging approaches; they do not establish that a managed cloud service was deployed. Demonstration outputs remain separate from ML2++ dissertation evidence.


<!-- BEGIN FOLDER GUIDE -->
## Folder guide

Application prototypes with their own setup guides, dependencies and tests, alongside the research artifacts.

[Parent folder](../) · [Repository overview](../README.md) · [All projects](https://github.com/zahramardani/ML2PP-Artifacts/blob/main/PROJECTS.md)

### Contents

| Item | What it is |
|---|---|
| [ai-microservice-demo/](ai-microservice-demo/) | The FastAPI anomaly-detection demonstration, database integration, Go gateway and deployment packaging. |
| [ml2pp-rag-copilot/](ml2pp-rag-copilot/) | The document-retrieval API, optional generated answers, sample documents, evaluation scripts and tests. |

**Start here:** [ai-microservice-demo/](ai-microservice-demo/).

<!-- END FOLDER GUIDE -->
