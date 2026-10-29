# RAG Evaluation

This folder evaluates the ML2++ RAG Copilot at two levels.

## 1. Retrieval quality

Run:

```bash
PYTHONPATH=. python -m evaluation.evaluate_retrieval --backend lexical --k 3
```

Metrics:

- **Hit Rate@K** — percentage of questions where at least one expected source appears in the top K.
- **Precision@K** — fraction of retrieved results that are relevant.
- **Recall@K** — fraction of expected relevant sources retrieved.
- **MRR** — Mean Reciprocal Rank; rewards putting the first relevant result close to rank 1.
- **Average / P95 retrieval latency** — retrieval speed.

The reviewed evaluation set is in `questions.json`.

For semantic retrieval:

```bash
pip install -r requirements-semantic.txt
PYTHONPATH=. python -m evaluation.evaluate_retrieval --backend semantic --k 3
```

## 2. Generated-answer quality

`evaluate_generation.py` includes transparent offline checks:

- **Keyword coverage** — simple completeness proxy.
- **Citation correctness** — whether cited sources match reviewed expected sources.
- **Unsupported-number flag** — lightweight hallucination warning for numeric claims not present in context.

These are useful sanity checks, but they are not a substitute for semantic faithfulness evaluation.

For a stronger production evaluation, add:

- **Faithfulness / groundedness**
- **Answer relevance**
- **Context relevance**
- **Citation completeness**

using a reviewed human evaluation set plus an LLM-as-judge or a framework such as RAGAS / DeepEval.

## Current lexical baseline

On the small 8-question reviewed set, the current TF-IDF baseline produced:

- Hit Rate@3: **1.00**
- Recall@3: **1.00**
- MRR: **1.00**
- Precision@3: **0.5417**

These values are only a portfolio baseline on a tiny evaluation set; they are not a production benchmark.

## Why separate retrieval and generation?

A RAG answer can fail because the retriever selected the wrong context, or because the LLM generated a poor answer even after receiving good context. Evaluating the two stages separately makes debugging much easier.

## Interview answer

> I evaluate RAG at two levels. For retrieval I use Hit Rate@K, Precision@K, Recall@K, MRR and latency. For generated answers I check groundedness, answer relevance and citation correctness. I keep retrieval and generation evaluation separate because they fail for different reasons.


<!-- BEGIN FOLDER GUIDE -->
## Folder guide

The existing evaluation questions and scripts for retrieval and generated-answer checks.

[Parent folder](../) · [Repository overview](../../../README.md) · [All projects](https://github.com/zahramardani/ML2PP-Artifacts/blob/main/PROJECTS.md)

### Contents

| Item | What it is |
|---|---|
| [evaluate_generation.py](evaluate_generation.py) | Generated-answer evaluation script. |
| [evaluate_retrieval.py](evaluate_retrieval.py) | Retrieval evaluation script. |
| [questions.json](questions.json) | The question set used by the RAG evaluation scripts. |

**Start here:** [evaluate_generation.py](evaluate_generation.py).

<!-- END FOLDER GUIDE -->
