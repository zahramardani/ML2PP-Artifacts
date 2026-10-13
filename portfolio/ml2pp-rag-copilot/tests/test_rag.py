from app.rag import Chunk, Retriever, build_grounded_prompt, chunk_text


def test_chunking_overlap():
    text = "A" * 1200
    chunks = chunk_text(text, "demo.txt", chunk_size=500, overlap=100)
    assert len(chunks) >= 3
    assert chunks[0].source == "demo.txt"
    assert chunks[0].chunk_id == 0


def test_lexical_retrieval_finds_leakage_chunk():
    chunks = [
        Chunk("Random shuffling can create future data leakage in time series.", "validation.md", 0),
        Chunk("A DSL can define syntax and semantics for a modeling language.", "dsl.md", 0),
    ]
    retriever = Retriever(chunks, backend="lexical")
    results = retriever.search("How can random splitting leak future information?", top_k=1)

    assert results[0].chunk.source == "validation.md"
    assert results[0].score > 0


def test_prompt_contains_sources_and_question():
    result_chunks = [
        type("R", (), {
            "chunk": Chunk("Chronological splits preserve temporal order.", "validation.md", 0),
            "score": 0.8,
        })()
    ]
    prompt = build_grounded_prompt("Why chronological split?", result_chunks)
    assert "validation.md" in prompt
    assert "Why chronological split?" in prompt
    assert "ONLY the supplied context" in prompt
