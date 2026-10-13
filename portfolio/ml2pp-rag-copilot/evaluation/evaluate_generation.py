from __future__ import annotations

import json
import re
from pathlib import Path


def keyword_coverage(answer: str, expected_keywords: list[str]) -> float:
    if not expected_keywords:
        return 1.0
    answer_lower = answer.lower()
    hits = sum(1 for kw in expected_keywords if kw.lower() in answer_lower)
    return hits / len(expected_keywords)


def citation_correctness(cited_sources: list[str], expected_sources: list[str]) -> float:
    if not cited_sources:
        return 0.0
    expected = set(expected_sources)
    correct = sum(1 for src in cited_sources if src in expected)
    return correct / len(cited_sources)


def contains_unsupported_numbers(answer: str, context: str) -> bool:
    answer_nums = set(re.findall(r"\b\d+(?:\.\d+)?%?\b", answer))
    context_nums = set(re.findall(r"\b\d+(?:\.\d+)?%?\b", context))
    return bool(answer_nums - context_nums)


def evaluate_saved_answers(path: str = "evaluation/saved_answers.json") -> dict:
    records = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = []
    for r in records:
        rows.append({
            "id": r["id"],
            "keyword_coverage": round(keyword_coverage(r["answer"], r.get("expected_answer_keywords", [])), 4),
            "citation_correctness": round(citation_correctness(r.get("cited_sources", []), r.get("expected_sources", [])), 4),
            "unsupported_number_flag": contains_unsupported_numbers(r["answer"], r.get("context", "")),
        })

    if not rows:
        return {"summary": {}, "details": []}

    summary = {
        "avg_keyword_coverage": round(sum(r["keyword_coverage"] for r in rows) / len(rows), 4),
        "avg_citation_correctness": round(sum(r["citation_correctness"] for r in rows) / len(rows), 4),
        "unsupported_number_rate": round(sum(1 for r in rows if r["unsupported_number_flag"]) / len(rows), 4),
    }
    return {"summary": summary, "details": rows}


if __name__ == "__main__":
    example = Path("evaluation/saved_answers.json")
    if not example.exists():
        raise SystemExit("Create evaluation/saved_answers.json from RAG outputs first. See evaluation/README.md.")
    report = evaluate_saved_answers(str(example))
    Path("evaluation/results_generation.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))
