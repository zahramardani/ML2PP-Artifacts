from pydantic import BaseModel, Field


class SensorReading(BaseModel):
    temperature: float = Field(..., ge=-50, le=150)
    vibration: float = Field(..., ge=0, le=100)
    load: float = Field(..., ge=0, le=1000)


class PredictionResponse(BaseModel):
    anomaly: bool
    anomaly_score: float
    risk_level: str


class ExplanationRequest(BaseModel):
    reading: SensorReading
    prediction: PredictionResponse
