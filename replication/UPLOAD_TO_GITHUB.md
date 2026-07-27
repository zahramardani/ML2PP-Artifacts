# Manual GitHub upload

1. Extract the delivered ZIP file.
2. Open `https://github.com/micss-lab/ML-QuadratPP`.
3. Create a branch such as `thesis-replication-package`.
4. Upload the extracted `replication/` directory while preserving its paths.
5. Commit with the message `Add thesis reproducibility package`.
6. Open a draft pull request and ask the supervisors to check provenance,
   dataset licences, and participant-data exclusions.

Do not describe the package as complete merely because the folder has been
uploaded. First replace every thesis-transcribed model with the byte-exact
executed model, add the generated sources and logs, add point-level prediction
files and split indices, lock dependencies, and create a verified run manifest
for all five runs.
