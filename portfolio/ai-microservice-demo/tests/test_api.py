from fastapi.testclient import TestClient
from app.main import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


def test_predict():
    with TestClient(app) as client:
        response = client.post("/predict", json={"temperature": 61, "vibration": 4.8, "load": 460})
        assert response.status_code == 200
        body = response.json()
        assert set(body) == {"anomaly", "anomaly_score", "risk_level"}
        assert body["risk_level"] in {"low", "medium", "high"}


def test_explain_without_external_key():
    with TestClient(app) as client:
        prediction = client.post("/predict", json={"temperature": 95, "vibration": 13, "load": 850}).json()
        response = client.post("/explain", json={
            "reading": {"temperature": 95, "vibration": 13, "load": 850},
            "prediction": prediction,
        })
        assert response.status_code == 200
        assert "explanation" in response.json()
