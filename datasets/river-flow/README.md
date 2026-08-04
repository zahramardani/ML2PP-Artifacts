# Use Case 1 - SNIRH river-flow dataset

## Checked processed file

`use_case_1_river_flow_observed.csv`

- 13,715 observed daily midnight timestamps
- period: 30 December 1984 through 6 August 2022
- variables: `disch1`, `disch2`, `disch3`
- 19 absent timestamps relative to a complete 13,734-day index
- forecast look-back: 20 days
- forecast horizon: three days
- executed model families: LSTM and GRU
- source: https://snirh.apambiente.pt/

The supplied file contained six non-daily test rows dated 9 July 2025 and three empty columns. They were excluded from the checked, execution-aligned input. Observed scientific values were not altered. The checked CSV and its PDF data card are deposited in this directory.

## Provenance boundary

The processed file does not retain the station codes or measurement unit. The intended scenario mentions Albufeira da Aguieira (11H/01A), Albufeira da Raiva (12H/01A), Albufeira de Fronhas (12I/01A), and Acude Ponte de Coimbra (12G/01AE), but no `disch`-column-to-station mapping is claimed.

The thesis narrative describes the third series as target, while an inspected executable listing declares `output_features disch2`. This must be resolved before claiming exact target-level reproduction. The PDF data card documents the issue explicitly.
