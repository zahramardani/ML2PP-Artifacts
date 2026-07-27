# Provenance of reported numerical results

`reported_metrics.csv` is a machine-readable transcription of the aggregate
metric tables in the revised dissertation. The values are documentation
evidence, not a reconstruction from original point-level predictions.

The file distinguishes the executed XGBoost solar rows from the preliminary
Prophet-compatible reference rows. Prophet must not be counted as one of the
five completed official-backend configurations.

To make these results independently reproducible, add the original timestamp,
target, prediction, horizon, split-membership and forecast-origin records for
each run. Then include the exact analysis script used to calculate MAE, RMSE,
MSE, R-squared, persistence RMSE and any relative improvement.
