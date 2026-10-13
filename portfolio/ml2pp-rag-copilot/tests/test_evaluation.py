from evaluation.evaluate_generation import (
    citation_correctness,
    contains_unsupported_numbers,
    keyword_coverage,
)
from evaluation.evaluate_retrieval import reciprocal_rank


def test_reciprocal_rank():
    assert reciprocal_rank(["a.md", "target.md"], {"target.md"}) == 0.5
    assert reciprocal_rank(["a.md"], {"target.md"}) == 0.0


def test_keyword_coverage():
    score = keyword_coverage(
        "Temporal leakage happens when future information enters training.",
        ["future", "leakage", "temporal"],
    )
    assert score == 1.0


def test_citation_correctness():
    assert citation_correctness(["a.md"], ["a.md"]) == 1.0
    assert citation_correctness(["wrong.md"], ["a.md"]) == 0.0


def test_unsupported_number_flag():
    assert contains_unsupported_numbers("RMSE was 12.5", "RMSE was 12.5") is False
    assert contains_unsupported_numbers("RMSE was 12.5", "No metric was reported") is True
