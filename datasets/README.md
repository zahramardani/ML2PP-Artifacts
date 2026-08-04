# ML2++ validation datasets

This directory contains the checked processed CSV inputs used by the three thesis technical-validation use cases and provides one-page PDF data cards. The source links remain authoritative for the original data cards and applicable terms.

| Use case | Processed file | Cadence | Target | Documentation | Original source |
|---|---|---|---|---|---|
| River-flow forecasting | `river-flow/use_case_1_river_flow_observed.csv` | Daily | Generic discharge series; target inconsistency must be resolved | `river-flow/use_case_1_river_flow.pdf` | [Portuguese SNIRH](https://snirh.apambiente.pt/) |
| Smart-home energy forecasting | `smart-home-energy/use_case_2_smart_home_energy.csv` | One minute | `use_kW` | `smart-home-energy/use_case_2_smart_home_energy.pdf` | [Kaggle data card](https://www.kaggle.com/datasets/taranvee/smart-home-dataset-with-weather-information) |
| Solar-power forecasting | `solar-power/use_case_3_solar_power_hourly.csv` | Hourly | `DC_POWER` | `solar-power/use_case_3_solar_power.pdf` | [Kaggle data card](https://www.kaggle.com/datasets/anikannal/solar-power-generation-data) |

## Validation outcome

- River: 13,715 observed midnight records before 7 August 2022. A complete daily index contains 13,734 timestamps, so 19 calendar dates are absent. Six non-daily test rows dated 9 July 2025 and three empty columns found in the supplied file were excluded.
- Smart home: 4,200 observations from 1 January 2016 05:00 through 4 January 2016 02:59, with a complete one-minute sequence and no missing values or duplicate timestamps.
- Solar: 796 observed hourly records from 15 May through 17 June 2020. A complete hourly index has 816 timestamps, revealing 20 absent hours. Night-time zero production is preserved.

The three CSVs are processed research subsets. Their data-quality and provenance boundaries are documented in the corresponding subdirectory README and PDF data card.
