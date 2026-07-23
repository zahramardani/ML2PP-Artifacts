# Smart-home energy dataset

## Thesis file

`HomeC_selected.csv`

## Scope

- Domain: residential/household energy consumption
- Forecast target: `energy_consumption`
- Input: historical `energy_consumption`
- Technical-validation cadence: hourly after resampling
- Forecast horizon: three hourly steps
- Split: 80% training / 20% test, in chronological order
- Model configuration: SARIMA with seasonal period 24

## Required logical schema

| ML2++ role | Canonical name |
|---|---|
| Timestamp | timestamp |
| Input and target | energy_consumption |

## Thesis preprocessing

1. Parse and sort timestamps.
2. Resample the selected consumption series to hourly cadence.
3. Interpolate short missing intervals.
4. Preserve chronological order.
5. Apply the chronological 80/20 split.
6. Run stationarity and seasonality diagnostics.

The hourly technical-validation configuration is distinct from the minute-level configuration used by some participants in the staged evaluation. They must not be mixed or described as the same execution.

## Availability

The exact selected CSV is not currently deposited. Before adding it, identify the original household-energy source, selection procedure, original variable name and unit, time range, timezone, and redistribution licence. Deposit either the lawful processed file with provenance or exact acquisition and transformation instructions.