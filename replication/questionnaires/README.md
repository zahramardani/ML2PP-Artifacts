# Questionnaire artefacts

`questionnaire_instruments.tex` contains the complete Stage 1--Stage 4
instrument appendix extracted from the revised dissertation source, including
instructions, response scales and scale directions. It contains no participant
responses.

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

`stage4_questionnaire_public_deidentified_responses.csv` is a PUBLIC
respondent-level release for the 40 analysed Stage 4 responses. It contains the
structured analytical variables used to reproduce the principal Stage 4 item,
construct, Python-effort, and workload summaries. Public respondent IDs
(`S4-PUB-001`--`S4-PUB-040`) are assigned for the release and row order does not
preserve the original submission sequence.

The public respondent-level file is de-identified before release. Fields that
can directly or indirectly identify a participant, and verbatim free-text
fields that may contain identifying details, are not included in the public
row-level file. Aggregate demographic/context counts and de-identified
qualitative summaries remain available through the dissertation and aggregate
CSV. The respondent-level release supports independent checking of the main
numerical Stage 4 summaries.

The extraction can be repeated with
`scripts/export_questionnaire_appendix.py` after the dissertation source is
updated.

Do not commit direct participant identifiers, unredacted free-text answers,
session recordings, or directly identifying participant-level logs without
documented consent and a data-protection review.
