# SolarXGBoost_Chapter5 — retained run evidence

- Run ID: `ML2RUN_c172ec1499ab509c`
- Model: `XGBoostImpl`
- Target: `DC_POWER`
- Preflight: `PASS`
- Training origins: 595
- Held-out origins: 159
- Dataset SHA-256: `f6c949d3489737fef7459df6d0fd5831b1669574b8f8cc1bafae96e81d1baf3a`
- Generated train-script SHA-256: `2e7e4b9428194985869d7d5d0ea3fa90e4b9457a9e11ff3d8f4b1222d69e30cf`
- Overall generated evaluation: RMSE = `1173.24778314502`, `n_test=318`
- Search mode: `hyperparameter_tuning:RANDOM_SEARCH`
- Held-out test data used for selection: `false`

## Selected training-side configuration

```text
max_depth=2
learning_rate=0.05
n_estimators=300
subsample=0.8
colsample_bytree=1.0
min_child_weight=1
reg_lambda=2
reg_alpha=0
gamma=0
booster=gbtree
```

## Horizon metrics

```csv
Horizon,Samples,MAE,RMSE,MAPE_percent,sMAPE_percent,R2
t+1,159,599.4861531475681,1049.1750941624903,33.882469331406504,104.76467127124978,0.9153480428916065
t+2,159,784.8951622907099,1285.399682238384,37.56479926229849,104.7451342999916,0.8734600993196638
```

## Generated PNG outputs recorded by the plot manifest

- `acf_DC_POWER.png`
- `forecast_vs_actual_horizon_t_plus_01.png`
- `forecast_vs_actual_horizon_t_plus_02.png`
- `lag_DC_POWER.png`
- `line_DC_POWER.png`
- `line_rolling_mean.png`
- `line_rolling_std.png`

The retained selection record states that selection used training-side validation/CV and reserved the held-out test partition for final evaluation. `FULL_RUN_SHA256.txt` records the hashes of the complete retained local run directory.
