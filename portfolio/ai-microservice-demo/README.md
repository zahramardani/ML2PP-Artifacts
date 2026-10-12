# AI Microservice Portfolio Demo

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
