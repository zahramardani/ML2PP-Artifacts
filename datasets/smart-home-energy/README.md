# Use Case 2 - smart-home energy dataset

## Corrected reproducible dataset

The previously deposited `use_case_2_smart_home_energy.csv` was removed on 13 August 2026 after validation showed that it had been derived from the source `humidity` column while being labelled `use_kW`.

The corrected dataset is generated reproducibly with:

```bash
python -m pip install reportlab
python datasets/smart-home-energy/preprocess_smart_home.py
```

The generated output is `use_case_2_smart_home_energy.csv` with:

- 4,200 one-minute observations
- period: 1 January 2016 05:00:00 through 4 January 2016 02:59:00 UTC
- target: `use_kW`, derived from the original source variable `use [kW]`
- raw source cadence used for this artifact: one second
- aggregation: arithmetic mean of each consecutive 60 raw `use [kW]` observations
- raw target observations used: first 252,000 observations (4,200 complete one-minute blocks)
- target range: 0.000800 to 4.302675 kW
- target mean: 0.775213 kW
- no missing output timestamps, missing target values, or duplicate output timestamps
- forecast horizon documented for the use case: three minutes
- model families documented for the use case: ARIMA(1,1,1) and additive Holt-Winters
- corrected CSV SHA-256: `8211344ec98cff4287496c3daeadd7217c586d18d6b2ca68fe5bb856efd7e7dc`
- SHA-256 of the selected 252,000 `(epoch_second,use [kW])` source pairs: `fd0e874c6c7766fec60bd7c4f2b697ace85e0d558bba33a9dc2fad29b8ef3801`

## Provenance

- authoritative original data card: https://www.kaggle.com/datasets/taranvee/smart-home-dataset-with-weather-information
- public reconstruction stream used by the script: https://data.yotahub.com/2024-1/datahub-2024-1-home.csv.gz
- public mirror conversion script: https://github.com/machbase/datahub/blob/bbfb34f51c905743099dde49a684138cac964284/dataset/2024/01.Smart%20Home%20Dataset/conv/convert.py

The Kaggle data card is the authoritative original source. The Yotahub/Machbase stream is a public converted copy used only to make the transformation reproducible without Kaggle credentials. The preprocessing script validates the source schema, the first target observation, and one-second timestamp continuity before constructing the one-minute series.

The processed target is household power use in kW. It is not humidity and is not a weather variable.

## Correction note

The superseded CSV must not be used as household-energy evidence. Numerical forecasting results produced from that file require rerunning on the corrected `use [kW]` dataset before they can be described as household-energy forecasting results.

`use_case_2_smart_home_energy.pdf` has been regenerated from the corrected target definition and provenance.
