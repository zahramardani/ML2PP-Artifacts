# Solar-power dataset

## Thesis file

`solar_generation.csv`

## Scope

- Domain: photovoltaic generation
- Inputs: ambient temperature, module temperature, and irradiation
- Forecast target: DC power
- Technical-validation cadence: hourly after resampling
- Forecast horizon: three hourly steps
- Look-back window: 20 observations
- Split: 80% training / 20% test, in chronological order
- Model configuration: XGBoost, random state 42

## Required logical schema

| ML2++ role | Canonical name |
|---|---|
| Timestamp | timestamp |
| Input | ambient_temperature |
| Input | module_temperature |
| Input | irradiation |
| Target | DC_POWER |

## Thesis preprocessing

1. Parse and sort timestamps.
2. Retain night-time zero production as a physically valid observation.
3. Resample to hourly cadence.
4. Interpolate short missing intervals.
5. Apply documented outlier handling.
6. Create persistent lag and rolling-window features.
7. Apply the chronological 80/20 split.
8. Flatten the previous 20 observations for the XGBoost regressor.

## Availability

The exact `solar_generation.csv` used by the thesis is not currently deposited. A file named `Plant_1_Generation_Data_seconds.csv` exists in the broader implementation checkout, but its schema and identity do not match the four-variable thesis declaration; it must not be substituted without a documented, reproducible join/transformation and provenance check. Confirm the original source and redistribution licence before adding the exact dataset.