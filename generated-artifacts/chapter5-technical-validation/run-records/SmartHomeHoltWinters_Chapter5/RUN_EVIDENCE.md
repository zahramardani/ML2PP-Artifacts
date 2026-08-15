# SmartHomeHoltWinters_Chapter5 — retained run evidence

- Run ID: `ML2RUN_3b520673ebbef3f6`
- Model: `HWESImpl`
- Target: `use_kW`
- Preflight: `PASS`
- Training rows: 3,360
- Held-out rows: 840; 838 complete three-step forecast origins per horizon
- Dataset SHA-256: `a3c6ee0c68c5eb6f6cae5c5cf7c695fa8f0399de9983e3a8fe585bfa6350ef33`
- Generated train-script SHA-256: `ba5a2bc041f1bc546d6b00cb7960434b57b11f38acf192adcfbbcbce6995f8c5`
- Overall generated evaluation: RMSE = `0.07685372990574026`, `n_test=2514`

## Horizon metrics

```csv
Horizon,Samples,MAE,RMSE,MAPE_percent,sMAPE_percent,R2
t+1,838,0.02156892578542473,0.030208819356368672,3.659457133011379,3.696922568622411,0.9754480193005896
t+2,838,0.049992910718834285,0.06854760445694484,8.547314573386856,8.68422750321172,0.873361475364309
t+3,838,0.08232482394899647,0.11003699631297623,14.274065765410715,14.494410801718324,0.6728877361909987
```

## Generated PNG outputs recorded by the plot manifest

- `acf_use_kW.png`
- `forecast_vs_actual_horizon_t_plus_01.png`
- `forecast_vs_actual_horizon_t_plus_02.png`
- `forecast_vs_actual_horizon_t_plus_03.png`
- `line_use_kW.png`

The generated audit records chronological splitting, training-side fitting of data-dependent preprocessing state, test exclusion from selection, and removal of target blocks that cross the split boundary. `FULL_RUN_SHA256.txt` records the hashes of the complete retained local run directory.
