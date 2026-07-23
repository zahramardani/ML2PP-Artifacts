# River-flow dataset

## Thesis file

`Tejo_system_45.csv`

## Scope

- Period: 13 January 2003 to 20 March 2004
- Observations: 433 daily timestamps
- Input stations: Castelo de Bode and Fratel
- Forecast target: Almourol
- Physical variable: river discharge
- Expected unit: m³/s (verify against the original export)
- Forecast horizon: three days
- Look-back window: 20 daily observations
- Split: 80% training / 20% test, in chronological order

## Required logical schema

| ML2++ role | Canonical name |
|---|---|
| Timestamp | timestamp |
| Input | castelo_bode_discharge |
| Input | fratel_discharge |
| Target | almourol_discharge |

The original column labels may differ. Preserve the original file and document any canonical renaming in a preprocessing script.

## Thesis preprocessing

1. Parse and sort timestamps.
2. Align the three station series over their common period.
3. Resample to daily cadence if required.
4. Fill missing observations using interpolation and backward filling as reported by the retained implementation.
5. Apply the chronological 80/20 split.
6. Fit preprocessing operations on the training partition only.
7. Construct 20-step input windows and three-step targets.

## Availability

The exact CSV is not currently deposited. It appears to originate from the Portuguese hydrological application context associated with LNEC/SNIRH. Confirm the exact owner, export query, and redistribution permission before committing it. If redistribution is restricted, provide an acquisition/export script or query record plus a checksum instead.