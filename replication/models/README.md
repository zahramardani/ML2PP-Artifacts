# Model specification coverage and provenance boundary

The six run-specific `model/` directories under `replication/runs/` contain specifications transcribed and aligned to the final Chapter 5 technical-validation listings dated 2026-08-14:

| Use case | Specifications |
|---|---|
| River flow | LSTM, GRU |
| Smart Energy | ARIMA(1,1,1), Holt–Winters |
| Solar power | XGBoost, Prophet |

Therefore, the repository has **6/6 thesis-listing model specifications across all three technical-validation use cases**.

These files provide declaration/model-specification evidence. They are deliberately labelled as transcriptions and are **not** asserted to be the byte-exact model files that produced the reported executions. Do not convert this specification-completeness statement into a claim of complete numerical replication.

A byte-exact archived executed model, when available, should preserve at minimum:

- dataset reference and timestamp semantics;
- input and output feature roles;
- preprocessing operations;
- lag/window and forecasting horizon;
- algorithm and every supplied parameter, in the grammar-supported order;
- prediction-result properties and evaluation metrics;
- visualization directives; and
- runtime binding/configuration.

The remaining requirements for full replication are tracked in `../PACKAGE_STATUS.json`.
