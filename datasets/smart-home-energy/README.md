# Use Case 2 - smart-home energy dataset

## Checked processed file (publication pending)

`use_case_2_smart_home_energy.csv`

- 4,200 one-minute observations
- period: 1 January 2016 05:00 through 4 January 2016 02:59
- target: `use_kW`, derived from the source variable `use [kW]`
- range: 0.13 to 0.96 kW; mean approximately 0.611 kW
- no missing timestamps, missing target values, or duplicate timestamps
- forecast horizon: three minutes
- executed model families: ARIMA(1,1,1) and additive Holt-Winters
- source: https://www.kaggle.com/datasets/taranvee/smart-home-dataset-with-weather-information

The thesis uses a chronological 80/20 split: 3,360 fitting observations and 840 held-out observations, yielding 838 complete three-step test origins. Holt-Winters uses a 60-observation seasonal cycle. The subset spans only about 70 hours, so it does not support a reliable 1,440-minute daily-seasonality benchmark. The PDF data card is public; the CSV is prepared locally pending explicit redistribution confirmation.
