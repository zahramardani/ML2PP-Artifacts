from __future__ import annotations

import argparse
import json
import statistics
import time
from pathlib import Path

from app.rag import Retriever, load_documents


def reciprocal_rank(retrieved_sources: list[str], expected_sources: set[str]) -> float:
    for rank, source in enumerate(retrieved_sources, start=1):
        if source in expected_sources:
            return 1.0 / rank
    return 0.0


def evaluate(dataset_path: Path, docs_dir: Path, backend: str, k: int) -> dict:
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    retriever = Retriever(load_documents(docs_dir), backend=backend)
    rows, latencies = [], []

    for item in dataset:
        expected = set(item["expected_sources"])
        start = time.perf_counter()
        results = retriever.search(item["question"], top_k=k)
        latency_ms = (time.perf_counter() - start) * 1000.0
        latencies.append(latency_ms)

        retrieved_sources = [r.chunk.source for r in results]
        unique_retrieved = set(retrieved_sources)
        relevant_retrieved = unique_retrieved.intersection(expected)

        hit = 1.0 if relevant_retrieved else 0.0
        precision = len([s for s in retrieved_sources if s in expected]) / max(len(results), 1)
        recall = len(relevant_retrieved) / max(len(expected), 1)
        rr = reciprocal_rank(retrieved_sources, expected)

        rows.append({
            "id": item["id"],
            "question": item["question"],
            "expected_sources": sorted(expected),
            "retrieved_sources": retrieved_sources,
            f"hit@{k}": hit,
            f"precision@{k}": round(precision, 4),
            f"recall@{k}": round(recall, 4),
            "reciprocal_rank": round(rr, 4),
            "latency_ms": round(latency_ms, 3),
        })

    ordered = sorted(latencies)
    p95_index = max(0, min(len(ordered) - 1, int(0.95 * len(ordered) + 0.999999) - 1))
    summary = {
        "backend": backend,
        "k": k,
        "n_questions": len(rows),
        f"hit_rate@{k}": round(statistics.mean(r[f"hit@{k}"] for r in rows), 4),
        f"precision@{k}": round(statistics.mean(r[f"precision@{k}"] for r in rows), 4),
        f"recall@{k}": round(statistics.mean(r[f"recall@{k}"] for r in rows), 4),
        "mrr": round(statistics.mean(r["reciprocal_rank"] for r in rows), 4),
        "avg_retrieval_latency_ms": round(statistics.mean(latencies), 3),
        "p95_retrieval_latency_ms": round(ordered[p95_index], 3),
    }
    return {"summary": summary, "details": rows}


def main():
    parser = argparse.ArgumentParser(description="Evaluate RAG retrieval quality.")
    parser.add_argument("--dataset", default="evaluation/questions.json")
    parser.add_argument("--docs", default="data/sample_docs")
    parser.add_argument("--backend", choices=["lexical", "semantic"], default="lexical")
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--output", default="evaluation/results_retrieval.json")
    args = parser.parse_args()

    report = evaluate(Path(args.dataset), Path(args.docs), args.backend, args.k)
    Path(args.output).write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("\nRetrieval evaluation")
    print("--------------------")
    for key, value in report["summary"].items():
        print(f"{key}: {value}")
    print(f"\nDetailed report written to: {args.output}")


if __name__ == "__main__":
    main()
