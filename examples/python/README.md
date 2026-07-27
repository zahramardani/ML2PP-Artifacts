# ML2++ Python reference examples

This directory provides compact, runnable Python companions for the three
technical-validation use cases described in the PhD thesis:

1. multivariate river-flow forecasting (daily, 20 input steps, 3 horizons);
2. smart-home energy forecasting (minute-level, 3 horizons);
3. photovoltaic generation forecasting (hourly, 2 horizons).

The scripts are reference implementations of the thesis workflow, not
byte-exact reconstructions of the original generated artifacts. By default
they use deterministic synthetic data, so the workflow can be tested without
redistributing restricted or unavailable source datasets. A user-owned CSV
can be supplied with `--csv`.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r examples/python/requirements.txt

python examples/python/run_usecase.py river --output artifacts/river
python examples/python/run_usecase.py energy --output artifacts/energy
python examples/python/run_usecase.py solar --output artifacts/solar
```

Each run writes:

- `predictions.csv` with observations and horizon-specific predictions;
- `metrics.csv` with MAE, MSE, RMSE and R²;
- `run_config.json` with the resolved configuration;
- `forecast.png` with an observed-versus-predicted plot.

## CSV schemas

- River: `timestamp,disch1,disch2,disch3`; `disch3` is the target.
- Energy: `timestamp,energy`.
- Solar: `timestamp,ac_power`.

The split is chronological. Scaling is fitted on training data only.
Synthetic outputs must never be presented as the dissertation's reported
experimental results.

