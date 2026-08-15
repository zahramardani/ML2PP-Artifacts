# RiverForecastGRU_Chapter5 — retained run evidence

- Run ID: `ML2RUN_08456d77a0581444`
- Model: `GRUImpl`
- Target: `almourol_discharge`
- Preflight: `PASS`
- Training windows: 10,230
- Held-out windows: 2,261
- Dataset SHA-256: `cf58d90c5cbf4632a0a8ab679f13ebe8cf73cb35ba741e57925df7d8075fb23b`
- Generated train-script SHA-256: `600e25058674809213782e2c12f7adc99e9c77b5cd4345b9e35ae5bb8634dd4e`
- Overall generated evaluation: MSE = `32604.631327806997`, `n_test=6783`

## Horizon metrics

```csv
Horizon,Samples,MAE,RMSE,MAPE_percent,sMAPE_percent,R2
t+1,2261,72.00692400168444,161.34504291024405,49.13235081448325,39.96412894801962,0.5187525991130191
t+2,2261,90.19954741387282,182.71070361477135,62.339428657444095,47.36700297771669,0.38658952022593773
t+3,2261,99.3611602867393,195.95527524490805,69.37585777632776,50.73372599452612,0.3050036730747845
```

## Leakage/preflight controls retained in the run

The generated records state chronological 80/20 splitting, a cutoff of `2014-08-23 00:00:00`, training-only fitting of feature scalers/imputation/outlier thresholds, held-out-test exclusion from tuning and early stopping, skipped target blocks crossing the partition boundary, and exclusion of originally missing targets from fitting/scoring. The common-period audit also records internal interpolation enabled, so the complete river missing-value path is not described as fully causal.

## Generated PNG outputs recorded by the plot manifest

- `forecast_vs_actual_horizon_t_plus_01.png`
- `forecast_vs_actual_horizon_t_plus_02.png`
- `forecast_vs_actual_horizon_t_plus_03.png`
- `heatmap.png`
- `line_almourol_discharge.png`
- `line_castelo_bode_discharge.png`
- `line_fratel_discharge.png`
- `training_loss.png`

`FULL_RUN_SHA256.txt` records the hashes of the complete retained local run directory, including generated source, point-level prediction CSVs, PNGs, model/checkpoint files, and Maven outputs.
