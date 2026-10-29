# Study 1: Eight-Participant Evaluation

This directory contains a public, de-identified representation of the
exploratory Stage 1--Stage 3 evaluation reported in the ML2++ PhD thesis.

## Study design

- **Participants:** eight, identified only as `P1`--`P8`
- **Stage 1:** manual Python forecasting workflow
- **Stage 2:** reuse of the Stage 1 workflow in an IoT-oriented template
- **Stage 3:** guided adaptation and execution of a prepared ML2++ model
- **Timing:** Stage 3 was conducted approximately 40 days after Stages 1--2
- **Design:** exploratory staged within-participant comparison; the stages
  were not randomised or counterbalanced

Stage 3 measured guided model adaptation, not greenfield DSML authoring.
Five participants completed Stage 3 and three completed it partially.

## Public files

- `participant_profiles.csv`: broad, de-identified participant background
- `stage1_stage2_effort.csv`: step-level Stage 1 and Stage 2 effort
- `stage3_summary.csv`: Stage 3 timing, completion, DSL size, and ratings
- `combined_effort.csv`: participant-level comparison used in the thesis
- `DATA_DICTIONARY.md`: field definitions and uncertainty conventions
- `RESTRICTED_DATA_NOTICE.md`: materials intentionally excluded from GitHub

## Interpretation

The data support an exploratory conclusion: among the five participants who
completed Stage 3, four used less time than on the cumulative Stage 1 +
Stage 2 route, while one used slightly more time. This is not evidence of a
general productivity effect. The sample is small, tasks and expertise are
heterogeneous, order was fixed, and some timings are approximate or lower
bounds.

## Privacy

No names, email addresses, signatures, consent forms, raw scans, file
metadata, or participant free-text responses are included. Participant
identifiers are pseudonyms used consistently in the thesis.


<!-- BEGIN FOLDER GUIDE -->
## Folder guide

The existing Study 1 documentation, questionnaire files and artifacts from manual coding, IoT integration and ML2++ adaptation.

[Parent folder](../) · [Repository overview](../../../README.md) · [All projects](https://github.com/zahramardani/ML2PP-Artifacts/blob/main/PROJECTS.md)

### Contents

| Item | What it is |
|---|---|
| [questionnaire_responses/](questionnaire_responses/) | Questionnaire PDF folders organized by the existing participant IDs P1 through P8. |
| [step1-manual-coding/](step1-manual-coding/) | The source archives and upload-status documentation deposited for the manual Python workflow stage. |
| [step2-iot-integration/](step2-iot-integration/) | The source archives and upload-status documentation deposited for the IoT-integration stage. |
| [step3-ml2-integration/](step3-ml2-integration/) | The deposited ThingML models, Java and Python sources and Maven build file from the ML2++ adaptation stage. |
| [DATA_DICTIONARY.md](DATA_DICTIONARY.md) | Existing definitions of study fields and measurement conventions. |
| [RESTRICTED_DATA_NOTICE.md](RESTRICTED_DATA_NOTICE.md) | Existing notice describing restricted study material. |

**Start here:** [DATA_DICTIONARY.md](DATA_DICTIONARY.md).

<!-- END FOLDER GUIDE -->
