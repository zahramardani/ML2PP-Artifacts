# AI Microservice Portfolio Demo

[Portfolio index](../README.md) · [All projects](../../PROJECTS.md)

Run the commands below from `portfolio/ai-microservice-demo` inside the repository. From the repository root:

```bash
cd portfolio/ai-microservice-demo
```

A compact portfolio project showing how an ML capability can be packaged as a production-oriented service. It was created to demonstrate skills relevant to modern AI/software engineering roles: REST APIs, Python, relational persistence, containerization, Kubernetes/Helm, CI, testing, basic Go, and optional LLM integration.

## What it demonstrates

- **FastAPI REST API** with `/health`, `/predict`, and `/explain` endpoints
- **Small Go gateway service** with health/proxy endpoints to demonstrate basic hands-on Go and microservice composition
- **Machine learning inference** using a deterministic Isolation Forest anomaly detector
- **SQLAlchemy persistence** with SQLite locally and PostgreSQL in Docker Compose
- **Docker + Docker Compose** for reproducible local deployment
- **Kubernetes manifests + Helm chart** for deployment packaging
- **GitHub Actions CI** running automated tests and Go vet
- **Optional LangChain/OpenAI integration** for natural-language explanations when `OPENAI_API_KEY` is configured
- Unit/API tests with `pytest`

## Architecture

Client -> Go gateway -> FastAPI -> ML model -> prediction log database
                              -> optional LangChain/OpenAI explanation

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` for the generated OpenAPI UI.

## Run tests

```bash
pytest -q
```

## Docker Compose

```bash
docker compose up --build
```

This starts the FastAPI service, a small Go gateway, and PostgreSQL. The API is available at `http://localhost:8000`; the Go gateway is at `http://localhost:8080`.

## Example request

```bash
curl -X POST http://localhost:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"temperature": 95, "vibration": 13, "load": 850}'
```

## Kubernetes / Helm

Raw manifests are in `k8s/`. A minimal Helm chart is in `helm/`.

```bash
helm install ai-demo ./helm
```

Replace the placeholder image repository in `helm/values.yaml` before deploying.

## Scope

This is intentionally a small portfolio demonstration rather than a production system. A production version would add authentication, migrations, secrets management, tracing/metrics, structured logging, rate limiting, model registry/versioning, and a managed database.


<!-- BEGIN FOLDER GUIDE -->
## Folder guide

The FastAPI anomaly-detection demonstration, database integration, Go gateway and deployment packaging.

[Parent folder](../) · [Repository overview](../../README.md) · [All projects](https://github.com/zahramardani/ML2PP-Artifacts/blob/main/PROJECTS.md)

### Contents

| Item | What it is |
|---|---|
| [.github/](.github/) | A workflow definition packaged inside the microservice example. GitHub discovers runnable workflows under the repository-root .github/workflows directory; consult those root definitions for the active configuration. |
| [app/](app/) | The Python API, input/output schemas, model, persistence helpers and optional explanation integration. |
| [go-gateway/](go-gateway/) | The small Go HTTP gateway packaged with the AI microservice demonstration. |
| [helm/](helm/) | Chart metadata, configurable values and Kubernetes templates for the microservice example. |
| [k8s/](k8s/) | Standalone Deployment and Service YAML files packaged with the microservice demonstration. |
| [tests/](tests/) | Tests for the microservice demonstration's API behavior. |
| [.env.example](.env.example) | Example environment-variable configuration. |
| [.gitignore](.gitignore) | Patterns excluding local caches, environments or generated outputs from new commits. |
| [docker-compose.yml](docker-compose.yml) | Local multi-service Docker Compose configuration. |
| [Dockerfile](Dockerfile) | Container-image build instructions for this application. |
| [pytest.ini](pytest.ini) | Pytest collection and import-path settings. |
| [requirements.txt](requirements.txt) | Python dependency list for this component. |

**Start here:** [.github/](.github/).

<!-- END FOLDER GUIDE -->
