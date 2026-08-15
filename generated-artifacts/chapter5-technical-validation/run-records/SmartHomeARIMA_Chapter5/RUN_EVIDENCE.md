# SmartHomeARIMA_Chapter5 — retained run evidence

- Run ID: `ML2RUN_0bff91e91c1d2114`
- Model: `ARIMAImpl`
- Target: `use_kW`
- Preflight: `PASS`
- Training rows: 3,360
- Held-out rows: 840; 838 complete three-step forecast origins per horizon
- Dataset SHA-256: `a3c6ee0c68c5eb6f6cae5c5cf7c695fa8f0399de9983e3a8fe585bfa6350ef33`
- Generated train-script SHA-256: `a088600f322dd7b22e42c619a1ffcca68f3e2ae7e20ca99270c3be0da86bcc23`
- Overall generated evaluation: RMSE = `0.07039295377347571`, `n_test=2514`

## Horizon metrics

```csv
Horizon,Samples,MAE,RMSE,MAPE_percent,sMAPE_percent,R2
t+1,838,0.019140362611532236,0.027495271985839516,3.2154953323785893,3.2387976941165415,0.9796607436582623
t+2,838,0.044268063316859126,0.06276027350946337,7.485732332008239,7.548350887358717,0.893842438655978
t+3,838,0.07280600902137399,0.10084969960444168,12.510622314226422,12.495386264217224,0.7252304574683079
```

## Generated PNG outputs recorded by the plot manifest

- `forecast_vs_actual_horizon_t_plus_01.png`
- `forecast_vs_actual_horizon_t_plus_02.png`
- `forecast_vs_actual_horizon_t_plus_03.png`

The generated audit records chronological splitting, training-side fitting of data-dependent preprocessing state, test exclusion from selection, and removal of target blocks that cross the split boundary. `FULL_RUN_SHA256.txt` records the hashes of the complete retained local run directory.
