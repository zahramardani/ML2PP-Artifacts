# Use Case 3 - solar-power dataset

## Checked processed file (publication pending)

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

The thesis preprocessing fills consistently non-producing night-time gaps with zero, interpolates short daytime gaps, and applies forward/backward propagation to remaining gaps. Because two-sided interpolation and backward filling can use future information, the reported results are retrospective positive-path validation rather than leakage-free online forecasting evidence. The PDF data card is public; the CSV is prepared locally pending explicit redistribution confirmation.
