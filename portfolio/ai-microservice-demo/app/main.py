from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .db import SessionLocal, PredictionLog, init_db
from .llm import explain_with_llm
from .model import predict_anomaly
from .schemas import SensorReading, PredictionResponse, ExplanationRequest


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="AI Microservice Demo",
    version="1.0.0",
    description="Portfolio microservice demonstrating REST APIs, ML inference, persistence, containers and deployability.",
    lifespan=lifespan,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(reading: SensorReading, db: Session = Depends(get_db)) -> PredictionResponse:
    anomaly, score, level = predict_anomaly(reading.temperature, reading.vibration, reading.load)
    result = PredictionResponse(anomaly=anomaly, anomaly_score=score, risk_level=level)
    db.add(PredictionLog(
        temperature=reading.temperature,
        vibration=reading.vibration,
        load=reading.load,
        anomaly=anomaly,
        anomaly_score=score,
        risk_level=level,
    ))
    db.commit()
    return result


@app.post("/explain")
def explain(request: ExplanationRequest) -> dict:
    return {"explanation": explain_with_llm(request.model_dump())}
