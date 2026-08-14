# Questionnaire artefacts

`questionnaire_instruments.tex` contains the complete Stage 1--Stage 4
instrument appendix extracted verbatim from the revised dissertation source,
including instructions, response scales and scale directions. It contains no
participant responses.

`stage4_quick_start_tutorial.pdf` is the real-user Quick-Start document used
for the Stage 4 guided study. It contains Tasks 1--13 for the ML2++ editor and
the prepared Tejo river-flow model. Almourol is the forecasting target; Fratel
and Castelo de Bode provide the other station series, while lagged Almourol
values are also supplied in the model's historical input window.

`stage4_questionnaire_public_aggregate.csv` contains the privacy-reviewed
aggregate Stage 4 results used in the dissertation tables, including 130
questionnaire invitations, 40 valid analysed responses, the 30.8% invitation-
to-analysed-response yield, descriptive statistics, confidence-interval
half-widths, construct internal-consistency coefficients, and aggregate
categorical counts. It contains no participant-level rows, direct identifiers,
identifying dates, or verbatim free-text responses.

The extraction can be repeated with
`scripts/export_questionnaire_appendix.py` after the dissertation source is
updated.

Do not commit participant names, email addresses, unredacted free-text
answers, session recordings, or participant-level logs without documented
consent and a data-protection review. Aggregate evidence should state the
valid-response rule and the number excluded at each stage.
