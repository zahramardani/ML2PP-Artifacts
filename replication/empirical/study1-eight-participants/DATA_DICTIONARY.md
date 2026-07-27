# Data dictionary

## Identifiers and categories

- `participant_id`: pseudonymous dissertation label P1--P8.
- `use_case`: river flow, smart-home energy, or solar power.
- Expertise fields: Beginner, Intermediate, Advanced, or Expert.
- `model_family`: model families assigned or explored in the staged study.

## Effort fields

All effort values are reported visible effort in minutes.

- `stage1_minutes`: manual Python implementation total.
- `stage2_minutes`: IoT-template understanding, adaptation, and execution total.
- `combined_baseline_minutes`: Stage 1 + Stage 2 for the observed route.
- `stage3_minutes`: guided ML2++ modelling/review plus extra-learning total.
- `change_s3_minus_baseline_minutes`: Stage 3 minus combined baseline. Negative
  values indicate less reported time in Stage 3.
- `stage3_completion`: `complete` or `partial`.

## Qualifiers

- `exact`: reported without an uncertainty marker.
- `lower_bound`: true value may be greater than or equal to the recorded value.
- `upper_bound`: algebraic consequence of a lower-bound baseline; for a negative
  change, the true value may be more negative.
- `approximate`: rounded or reconstructed from session timing.
- `NA`: not separately recorded or included in the reported total.

## Stage 3 rating scales

- Error frequency: 0--3.
- Error clarity, debug effort, generated-code quality, maintainability,
  flexibility, and satisfaction: 1--5 in the directions documented by the
  administered questionnaire and dissertation.
- Debug time is already included in modelling/review time and must not be added
  again to the Stage 3 total.

## Interpretation constraints

The stages were sequential, not randomised, and used heterogeneous use cases.
Stage 3 used prepared models. Partial completions must not be pooled with complete
runs as equivalent evidence. These CSV files support audit and secondary
descriptive analysis, not causal or population-level claims.
