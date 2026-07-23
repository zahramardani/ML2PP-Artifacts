# ML2++ datasets

This directory documents the datasets used by the three ML2++ technical-validation use cases.

## Dataset catalogue

| Use case | Expected file | Status in this repository | Target | Cadence |
|---|---|---|---|---|
| River-flow forecasting | `river-flow/Tejo_system_45.csv` | Raw file not yet deposited | Almourol discharge | Daily |
| Smart-home energy forecasting | `smart-home-energy/HomeC_selected.csv` | Raw file not yet deposited | Household energy consumption | Hourly after resampling |
| Solar-power forecasting | `solar-power/solar_generation.csv` | Exact thesis file not yet deposited | DC power | Hourly after resampling |

The exact raw/processed CSV files were not present in the retained workspace used to prepare this repository. Similar sample files must not be renamed or presented as the thesis datasets. Add each exact file only after its provenance and redistribution permission have been verified.

## Required evidence when adding a dataset

For each deposited file, record:

1. original source and data owner;
2. acquisition or export date;
3. licence or redistribution permission;
4. original and processed filenames;
5. column names, units, timestamp format, and timezone;
6. preprocessing history;
7. chronological train/test indices;
8. SHA-256 checksum.

The detailed specifications are in the three use-case subdirectories.