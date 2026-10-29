# Provenance of reported numerical results

[Replication guide](../README.md) · [Reported metrics](reported_metrics.csv) · [Retained Chapter 5 records](../../generated-artifacts/chapter5-technical-validation/README.md)

`reported_metrics.csv` is a machine-readable transcription of reported aggregate results. Its numerical values and existing row labels have been retained; this documentation update does not recompute scores or assert numerical reproduction.

The newer retained Chapter 5 collection includes separate XGBoost and Prophet model instances and text execution records. Consult each record for its run ID, backend, recorded metrics and audit scope. Historical labels in the aggregate CSV must not be used alone to count completed official-backend executions or to identify the newest run evidence.

Independent numerical verification requires the original timestamp, target, prediction, horizon, split-membership and forecast-origin records, together with the exact metric calculation script. Text summaries and full-run checksum lists support traceability but do not supply absent prediction files.

Synthetic outputs from `examples/python/` or `portfolio/` are separate demonstrations and must not be substituted for dissertation results.
