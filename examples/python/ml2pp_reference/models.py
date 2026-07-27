from __future__ import annotations

import numpy as np


def fit_linear_sequence(x_train: np.ndarray, y_train: np.ndarray, x_test: np.ndarray):
    from sklearn.linear_model import Ridge
    from sklearn.multioutput import MultiOutputRegressor

    model = MultiOutputRegressor(Ridge(alpha=1.0))
    model.fit(x_train.reshape(len(x_train), -1), y_train)
    return model.predict(x_test.reshape(len(x_test), -1))


def fit_arima(train: np.ndarray, history: np.ndarray, n_out: int) -> np.ndarray:
    from statsmodels.tsa.arima.model import ARIMA

    predictions = []
    series = list(train)
    for observed in history:
        fitted = ARIMA(series, order=(1, 1, 1)).fit()
        predictions.append(fitted.forecast(n_out))
        series.append(float(observed))
    return np.asarray(predictions)


def fit_holt_winters(train: np.ndarray, history: np.ndarray, n_out: int) -> np.ndarray:
    from statsmodels.tsa.holtwinters import ExponentialSmoothing

    predictions = []
    series = list(train)
    for observed in history:
        fitted = ExponentialSmoothing(
            series, trend="add", damped_trend=True, seasonal="add",
            seasonal_periods=60, initialization_method="estimated"
        ).fit(optimized=True)
        predictions.append(fitted.forecast(n_out))
        series.append(float(observed))
    return np.asarray(predictions)


def fit_xgboost(x_train: np.ndarray, y_train: np.ndarray, x_test: np.ndarray):
    from sklearn.multioutput import MultiOutputRegressor
    from xgboost import XGBRegressor

    estimator = XGBRegressor(
        max_depth=6, learning_rate=0.1, n_estimators=200,
        objective="reg:squarederror", random_state=42, n_jobs=1,
    )
    model = MultiOutputRegressor(estimator).fit(
        x_train.reshape(len(x_train), -1), y_train
    )
    return model.predict(x_test.reshape(len(x_test), -1))


def fit_prophet(timestamps, target: np.ndarray, split: int, n_out: int):
    from prophet import Prophet

    predictions = []
    for horizon in range(1, n_out + 1):
        train = {"ds": timestamps.iloc[:split], "y": target[:split]}
        model = Prophet(daily_seasonality=True, weekly_seasonality=True)
        model.fit(__import__("pandas").DataFrame(train))
        future = __import__("pandas").DataFrame(
            {"ds": timestamps.iloc[split + horizon - 1 :]}
        )
        predictions.append(model.predict(future)["yhat"].to_numpy())
    length = min(map(len, predictions))
    return np.column_stack([values[:length] for values in predictions])

