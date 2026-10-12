from functools import lru_cache
import numpy as np
from sklearn.ensemble import IsolationForest


@lru_cache(maxsize=1)
def get_model() -> IsolationForest:
    rng = np.random.default_rng(42)
    normal = np.column_stack([
        rng.normal(60, 6, 400),
        rng.normal(5, 1.2, 400),
        rng.normal(450, 60, 400),
    ])
    model = IsolationForest(n_estimators=120, contamination=0.05, random_state=42)
    model.fit(normal)
    return model


def predict_anomaly(temperature: float, vibration: float, load: float) -> tuple[bool, float, str]:
    model = get_model()
    x = np.array([[temperature, vibration, load]], dtype=float)
    raw = float(model.decision_function(x)[0])
    anomaly = bool(model.predict(x)[0] == -1)
    score = round(max(0.0, min(1.0, 0.5 - raw)), 4)
    if score >= 0.65:
        level = "high"
    elif score >= 0.4:
        level = "medium"
    else:
        level = "low"
    return anomaly, score, level
