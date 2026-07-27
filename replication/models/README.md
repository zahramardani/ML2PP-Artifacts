# Exact model instances required

Do not copy a tutorial model into this directory and call it an executed model
unless it is byte-for-byte the model used for the reported run.

The exact archived model should declare, at minimum:

- the dataset reference and timestamp semantics;
- input and output feature roles;
- preprocessing operations;
- lag/window and forecasting horizon;
- algorithm and every parameter supplied to it;
- prediction-result properties and evaluation metrics;
- visualization directives; and
- the runtime binding/configuration.

Use the run-specific `model/` directories described in the parent README.
