# SolarProphet_Chapter5 — retained run evidence

- Run ID: `ML2RUN_672b6608ffe4419b`
- Model: `ProphetImpl`
- Target: `DC_POWER`
- Preflight: `PASS`
- Training rows: 636
- Held-out rows: 160; 159 complete two-step forecast origins per horizon
- Dataset SHA-256: `f6c949d3489737fef7459df6d0fd5831b1669574b8f8cc1bafae96e81d1baf3a`
- Generated train-script SHA-256: `3accd2096419298580f5ba1eae14871f6a28f92cba3fcca4efda1f151b9ca736`
- Overall generated evaluation: RMSE = `1185.9249432120557`, `n_test=318`

## Horizon metrics

```csv
Horizon,Samples,MAE,RMSE,MAPE_percent,sMAPE_percent,R2
t+1,159,737.8975530179993,1192.1426702375863,32.75069934466794,102.26498221475178,0.8907056972130352
t+2,159,724.8775400274728,1179.6744447786566,32.293243112421415,103.18646945614353,0.8934200638646654
```

## Generated PNG outputs recorded by the plot manifest

- `acf_DC_POWER.png`
- `forecast_vs_actual_horizon_t_plus_01.png`
- `forecast_vs_actual_horizon_t_plus_02.png`
- `lag_DC_POWER.png`
- `line_DC_POWER.png`

The generated audit records chronological splitting, test-partition exclusion from selection, exclusion of originally missing targets, and no common-period internal interpolation. `FULL_RUN_SHA256.txt` records the hashes of the complete retained local run directory.
