# Time-series forecasting validation

Time-series forecasting must preserve temporal order during evaluation. Randomly shuffling future observations into a training set can leak information from the future into model development and lead to unrealistically optimistic metrics.

Useful evaluation strategies include chronological train-test splits and rolling-origin or walk-forward evaluation.

A persistence or naive forecast is an important baseline. A complex model should be compared with a simple baseline to show whether added complexity produces useful predictive value.

Common point-forecast metrics include MAE and RMSE. MAE is directly interpretable in the target unit and is less sensitive to large errors than RMSE. RMSE penalizes large errors more strongly.

Lag features encode historical observations as model inputs. Forecast horizon describes how far into the future the model predicts. Multi-step forecasting can be direct, recursive, or multi-output depending on the model and application.

Data leakage can occur not only in train-test splitting but also during preprocessing. Scaling, imputation, feature selection, and aggregation must be fitted or constructed without using information that would not have been available at prediction time.
