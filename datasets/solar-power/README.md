# Use Case 3 - solar-power dataset

## Checked processed file

`use_case_3_solar_power_hourly.csv`

- 796 observed hourly timestamps
- period: 15 May through 17 June 2020
- target: `DC_POWER`
- 20 absent timestamps relative to a complete 816-hour index
- 358 physical zero observations retained
- forecast horizon: two hours
- executed model families: XGBoost and Prophet
- source: https://www.kaggle.com/datasets/anikannal/solar-power-generation-data

The target is the arithmetic hourly mean of available Plant 1 inverter-level `DC_POWER` observations. It is not total plant energy and not grid-injected AC power.

The thesis preprocessing fills consistently non-producing night-time gaps with zero, interpolates short daytime gaps, and applies forward/backward propagation to remaining gaps. Because two-sided interpolation and backward filling can use future information, the reported results are retrospective positive-path validation rather than leakage-free online forecasting evidence. The checked CSV and its PDF data card are deposited in this directory.


<!-- BEGIN FOLDER GUIDE -->
## Folder guide

The deposited hourly solar-power CSV and its existing data card and provenance documentation.

[Parent folder](../) · [Repository overview](../../README.md) · [All projects](https://github.com/zahramardani/ML2PP-Artifacts/blob/main/PROJECTS.md)

### Contents

| Item | What it is |
|---|---|
| [use_case_3_solar_power.pdf](use_case_3_solar_power.pdf) | Existing PDF data card for this use-case dataset. |
| [use_case_3_solar_power_hourly.csv](use_case_3_solar_power_hourly.csv) | The deposited CSV data table named use_case_3_solar_power_hourly.csv. |

**Start here:** [use_case_3_solar_power.pdf](use_case_3_solar_power.pdf).

<!-- END FOLDER GUIDE -->
