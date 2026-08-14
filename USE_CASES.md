# ML2++ thesis use cases and repository artifacts

The human-readable use-case name **Smart Energy** is used in thesis-facing documentation. Stable technical paths and identifiers such as `smart-home-energy`, `use_kW`, and `datasets/smart-home-energy/` are retained where changing them would break artifact references.

| Use case | Cadence | Input context → horizon | Final Chapter 5 configurations | Repository material |
|---|---|---|---|---|
| River flow | Daily | 20 days → 3 days | LSTM, GRU | Final thesis-transcribed DSL models, river input data, aggregate causal-audit metrics |
| Smart Energy | Minute | ordered minute series → 3 minutes | ARIMA(1,1,1), additive damped Holt–Winters (period 60) | Final thesis-transcribed DSL models, preprocessing/checksum material, aggregate causal-audit metrics |
| Solar power | Hourly | 20 hours → 2 hours | XGBoost, Prophet | Final thesis-transcribed DSL models, hourly `DC_POWER` data, aggregate causal-audit metrics |

## Model-specification coverage

The run-specific `model/` directories under `replication/runs/` now contain thesis-transcribed specifications aligned with the six final Chapter 5 technical-validation listings:

- River flow: LSTM and GRU;
- Smart Energy: ARIMA(1,1,1) and Holt–Winters;
- Solar power: XGBoost and Prophet.

This is **complete specification coverage for the three Chapter 5 use cases (6/6 configurations)**. It is not a claim that the repository is a complete byte-exact numerical replication package. See `replication/PACKAGE_STATUS.json` for the remaining provenance material.

The repository also documents:

- the six-part DSML (`data`, `preprocessing`, `time_series`, `model`, `evaluation`, and `visualization`);
- chronological evaluation and the causal-audit boundary;
- flattened versus sequential temporal representations;
- horizon-specific prediction binding to IoT/CPS properties;
- generation provenance levels and run manifests;
- user-study questionnaire instruments;
- dataset acquisition and data-protection constraints.

The Python examples are transparent companion workflows reconstructed for inspection and learning. They must not be treated as byte-exact generated sources or as substitutes for the final causal-audit executions unless a run folder contains verified provenance and matching hashes.
