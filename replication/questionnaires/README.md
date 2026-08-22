# Questionnaire artefacts

`questionnaire_instruments.tex` contains the complete Stage 1--Stage 4
instrument appendix extracted verbatim from the revised dissertation source,
including instructions, response scales and scale directions. It contains no
participant responses.

`stage4_quick_start_tutorial.pdf` is the real-user Quick-Start document used
for the Stage 4 guided study reported in Chapter 6. It contains Tasks 1--13 for
the ML2++ editor and the prepared Tejo river-flow model. Almourol is the
forecasting target; Fratel and Castelo de Bode provide the other station
series, while lagged Almourol values are also supplied in the model's
historical input window.

For an explicit Chapter 6 / Stage 4 entry point, see
[`../studies/stage4-quick-start/README.md`](../studies/stage4-quick-start/README.md).

`stage4_questionnaire_public_aggregate.csv` contains the privacy-reviewed
aggregate Stage 4 results used in the dissertation tables, including 130
questionnaire invitations, 40 valid analysed responses, the 30.8% invitation-
to-analysed-response yield, descriptive statistics, confidence-interval
half-widths, construct internal-consistency coefficients, and aggregate
categorical counts.

`stage4_questionnaire_public_deidentified_responses.csv` contains 40
respondent-level rows for the structured analytical variables used to
reproduce the principal Stage 4 item, construct, Python-effort, and workload
summaries. Public respondent IDs (`S4-PUB-001`--`S4-PUB-040`) are newly assigned
for this release and are not the administered identifiers. Row order is not
the original submission order.

To reduce re-identification risk, the public respondent-level file excludes
participant names/direct identifiers, timestamps and exact dates,
session/device/background/demographic/browser fields, and fields that can
contain verbatim or user-supplied free text (B6, C6, G3, G4, and H6). Aggregate
demographic/context counts and qualitative summaries remain available through
the aggregate evidence reported in the dissertation and the aggregate CSV.
The respondent-level release therefore supports independent checking of the
main numerical Stage 4 summaries without exposing direct identifiers or
verbatim qualitative responses.

SHA-256 for `stage4_questionnaire_public_deidentified_responses.csv`:
`6ede4619c0c08e7562a558c9672c322bdb706992a33d5e1d7ca0f9907585bd0a`.

The extraction can be repeated with
`scripts/export_questionnaire_appendix.py` after the dissertation source is
updated.

Do not commit participant names, email addresses, unredacted free-text
answers, session recordings, or directly identifying participant-level logs
without documented consent and a data-protection review.
