# ML2++ thesis use cases and repository artifacts

| Use case | Cadence | Input → horizon | Executed families | Repository material |
|---|---|---|---|---|
| River flow | Daily | 20 steps → 3 days | LSTM, GRU | DSL models, Python reference pipeline, configuration, reported metrics |
| Smart-home energy | Minute | ordered series → 3 minutes | ARIMA(1,1,1), Holt–Winters | DSL models, Python reference pipeline, configuration, reported metrics |
| Solar power | Hourly | 24 steps → 2 hours | XGBoost, Prophet | DSL models, Python reference pipeline, configuration, reported metrics |

The repository also documents:

- the six-part DSML (`data`, `preprocessing`, `time_series`, `model`,
  `evaluation`, and `visualization`);
- chronological splitting and training-only preprocessing;
- flattened versus sequential temporal representations;
- horizon-specific prediction binding to IoT/CPS properties;
- generation provenance levels and run manifests;
- user-study questionnaire instruments;
- dataset acquisition and data-protection constraints.

The Python examples are transparent companions reconstructed from the
configurations reported in the thesis. They are not claimed to be the exact
historical generated files unless a run folder contains a verified manifest
and original hashes.
