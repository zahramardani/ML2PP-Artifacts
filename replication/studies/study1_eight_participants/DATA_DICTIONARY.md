# Data dictionary

## Common fields

- `participant_id`: thesis pseudonym (`P1`--`P8`), not a real identity
- `use_case`: river flow, smart-home energy, or solar power
- `model_family`: model family assigned in the staged study
- `*_min`: reported effort in minutes
- `NA`: not separately recorded

## Qualifiers

- `exact`: reported as a point value in the thesis
- `approximate`: rounded or approximate session timing
- `lower_bound`: the true value may be larger
- `upper_bound`: for a negative change, the actual reduction may be larger
- `included in total`: not recorded as a separate additive component
- `included in preprocessing`: debugging was folded into preprocessing

## Completion

- `complete`: participant completed the Stage 3 task
- `partial`: participant did not complete every required Stage 3 task

Partial-completion timing must not be interpreted as equivalent evidence to
completed-task timing.

## Rating directions

In `stage3_summary.csv`:

- `error_frequency`: 0--3; larger means more frequent errors
- `error_clarity`: 1--5; larger means clearer errors
- `debug_effort`: 1--5; larger means harder
- `code_quality`, `maintainability`, `flexibility`: 1--5; larger is better
- `satisfaction`: 1--5; larger is more satisfied

The full questionnaire wording and additional item-level results are
documented in the thesis questionnaire appendix. This public dataset is a
curated evidence table, not a raw questionnaire export.
