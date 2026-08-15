# RiverForecastLSTM_Chapter5 — retained run evidence

This file reproduces the small text-based records retained in the supplied executed run directory. Larger generated sources, point-level prediction CSVs, PNG plots, model/checkpoint files, and Maven outputs are covered by `FULL_RUN_SHA256.txt`.

## `run_metadata.json`

```json
{
  "run_id": "ML2RUN_dd3ced1e34f8c5bd",
  "generated_at_utc": "2026-08-15T19:25:11.862048+00:00",
  "compiler_profile": "ML2++ PythonJava compiler V12 DSL-strict execution",
  "model": "LSTMImpl",
  "autoML": "OFF",
  "hyperparameter_tuning": "OFF",
  "dataset_path": "/home/zahra/test/flow_dataset.csv",
  "dataset_sha256": "cf58d90c5cbf4632a0a8ab679f13ebe8cf73cb35ba741e57925df7d8075fb23b",
  "generated_train_script_sha256": "d9dc1a363cc9da3bb4022ae187e0ad59196afd7310799358c117c5e7e49fd581",
  "python": "3.10.12 (main, Jun 22 2026, 18:55:27) [GCC 11.4.0]",
  "platform": "Linux-6.8.0-101-generic-x86_64-with-glibc2.35",
  "packages": {
    "numpy": "2.2.6",
    "pandas": "2.3.3",
    "scikit-learn": "1.7.2",
    "scipy": "1.15.3",
    "statsmodels": "0.14.6",
    "pmdarima": null,
    "tensorflow": "2.21.0",
    "keras": "3.12.4",
    "xgboost": "3.2.0",
    "prophet": "1.4.0",
    "optuna": null,
    "arch": null
  },
  "assurance_artifacts": [
    "ml_preflight_report.json",
    "leakage_audit.json",
    "model_evaluation.json",
    "plots/plots_manifest.json"
  ]
}
```

## `ml_preflight_report.json`

```json
{
  "status": "PASS",
  "dataset_path": "/home/zahra/test/flow_dataset.csv",
  "model": "LSTMImpl",
  "target": "almourol_discharge",
  "train_samples": 10230,
  "test_samples": 2261,
  "checks": [
    {"name":"dataset_readable","passed":true,"detail":"/home/zahra/test/flow_dataset.csv","severity":"error"},
    {"name":"raw_rows_available","passed":true,"detail":"raw_rows=13716","severity":"error"},
    {"name":"processed_rows_available","passed":true,"detail":"processed_rows=13128","severity":"error"},
    {"name":"chronological_index_monotonic","passed":true,"detail":"processed index must be monotonic","severity":"error"},
    {"name":"train_cutoff_defined","passed":true,"detail":"cutoff=2014-08-23 00:00:00","severity":"error"},
    {"name":"nonempty_train_partition","passed":true,"detail":"train=10230","severity":"error"},
    {"name":"nonempty_test_partition","passed":true,"detail":"test=2261","severity":"error"},
    {"name":"feature_shape_compatible","passed":true,"detail":"X_train=(10230, 20, 3), X_test=(2261, 20, 3)","severity":"error"},
    {"name":"target_train_alignment","passed":true,"detail":"X_train=10230, y_train=10230","severity":"error"},
    {"name":"target_test_alignment","passed":true,"detail":"X_test=2261, y_test=2261","severity":"error"},
    {"name":"window_lag_valid","passed":true,"detail":"lag=20","severity":"error"},
    {"name":"forecast_steps_valid","passed":true,"detail":"steps=3","severity":"error"},
    {"name":"window_history_sufficient","passed":true,"detail":"train=10230, lag=20","severity":"warning"},
    {"name":"seasonal_cycles_sufficient","passed":true,"detail":"available_cycles=511.50, period=20","severity":"warning"},
    {"name":"deep_learning_sample_size","passed":true,"detail":"train_samples=10230; fewer than 100 may be unstable","severity":"warning"}
  ],
  "warnings": []
}
```

## `leakage_audit.json`

```json
{
  "chronological_split": true,
  "split_policy": "first_80_percent_train_last_20_percent_test",
  "training_cutoff": "2014-08-23 00:00:00",
  "label_encoders_fit_on_training_only": true,
  "feature_scalers_fit_on_training_only": true,
  "advanced_imputer_fit_on_training_only": true,
  "outlier_thresholds_fit_on_training_only": true,
  "test_partition_excluded_from_tuning": true,
  "test_partition_excluded_from_early_stopping": true,
  "window_targets_crossing_partition_boundary_skipped": true,
  "originally_missing_targets_excluded_from_training_and_scoring": true,
  "rolling_features_use_past_only_shift": false,
  "causal_missing_value_policy_for_sequential_data": false,
  "common_period_threshold_semantics": "maximum consecutive missing observations per feature within each retained common period",
  "common_period_internal_interpolation_enabled": true,
  "sequence_tensor_preserved": true,
  "assurance_scope": "compiler-generated pipeline controls; not a formal proof of absence of all domain-specific leakage"
}
```

## `model_evaluation.json`

```json
{"metric":"MSE","value":33004.80422203925,"n_test":6783}
```

## `plots/diagnostics/forecast_metrics_by_horizon.csv`

```csv
Horizon,Samples,MAE,RMSE,MAPE_percent,sMAPE_percent,R2
t+1,2261,71.52117215318103,158.8375257863574,51.60627856466212,38.51357244846624,0.5335948146885693
t+2,2261,91.48154730441243,184.06121645948414,65.02792626305327,47.27172161564827,0.37748791469066945
t+3,2261,101.79034106518199,199.7661674649662,71.87692065307387,51.06661895327275,0.2777085636097463
```

## `plots/plots_manifest.json`

```json
[
 {"file":"forecast_vs_actual_horizon_t_plus_01.png","category":"forecasting","phase":"train","model":"LSTMImpl"},
 {"file":"forecast_vs_actual_horizon_t_plus_02.png","category":"forecasting","phase":"train","model":"LSTMImpl"},
 {"file":"forecast_vs_actual_horizon_t_plus_03.png","category":"forecasting","phase":"train","model":"LSTMImpl"},
 {"file":"heatmap.png","category":"preprocessing","phase":"train","model":"LSTMImpl"},
 {"file":"line_almourol_discharge.png","category":"preprocessing","phase":"train","model":"LSTMImpl"},
 {"file":"line_castelo_bode_discharge.png","category":"preprocessing","phase":"train","model":"LSTMImpl"},
 {"file":"line_fratel_discharge.png","category":"preprocessing","phase":"train","model":"LSTMImpl"},
 {"file":"training_loss.png","category":"overfitting","phase":"train","model":"LSTMImpl"}
]
```
