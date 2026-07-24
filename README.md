# ML2++ Research Artifacts

Research artifacts for **ML2++: A Model-Driven Engineering Framework for Time-Series Forecasting in IoT and Cyber-Physical Systems**.

ML2++ is a domain-specific modeling language and model-driven engineering framework for defining time-series forecasting workflows in IoT and cyber-physical systems. It provides textual and graphical editors based on a shared metamodel and generates executable forecasting artifacts.

## Artifact structure

| Directory | Contents |
|---|---|
| `language/` | Shared EMF/Ecore metamodel, Textula/Xtext, and Sirius Web artifacts |
| `generators/` | Xtend transformations and model-to-code generation resources |
| `use-cases/` | ML2++ model instances and resources for evaluated IoT/CPS scenarios |
| `datasets/` | Redistributable data, metadata, schemas, and acquisition instructions |
| `experiments/` | Configurations, execution instructions, and expected results |
| `evaluation/` | Study instruments, anonymized results, and analysis materials |
| `generated-artifacts/` | Representative generated Python/Java code and outputs |
| `docs/` | Tutorials, architecture material, screenshots, and supplementary documentation |
| `publications/` | Publication-specific supplementary material |

## Reproducibility checklist

Each use case or experiment should identify:

1. the ML2++ model instance;
2. data provenance and preprocessing steps;
3. software and dependency versions;
4. generation and execution commands;
5. train/validation/test splits;
6. random seeds, where applicable;
7. evaluation metrics and expected outputs.

Large, restricted, or third-party datasets must not be committed directly. Add metadata and acquisition or reconstruction instructions instead.

## Related implementation

The principal implementation is maintained in [`ML-QuadratPP`](https://github.com/arminmoin/ML-QuadratPP). Thesis results should reference the exact implementation revision used. The pinned revision is:

`4253f75e7f3b3f94620d79e672e4db52b477d32c`

## Author

**Zahra Mardani Korani**  
LNEC/CICTI and Iscte-IUL/ISTA/ISTAR

Supervisors: João Carlos Ferreira, Armin Moin, and Alberto Rodrigues da Silva.

## Citation and licensing

Final citation metadata and licenses will be added after confirmation of the thesis and publication metadata. Third-party datasets retain their original terms and licenses.
