from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import os

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass(frozen=True)
class Chunk:
    text: str
    source: str
    chunk_id: int


@dataclass(frozen=True)
class SearchResult:
    chunk: Chunk
    score: float


def chunk_text(text: str, source: str, chunk_size: int = 900, overlap: int = 150) -> list[Chunk]:
    """Split text into overlapping character chunks."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must satisfy 0 <= overlap < chunk_size")

    clean = " ".join(text.split())
    if not clean:
        return []

    chunks: list[Chunk] = []
    start = 0
    chunk_id = 0

    while start < len(clean):
        end = min(start + chunk_size, len(clean))
        chunks.append(Chunk(text=clean[start:end], source=source, chunk_id=chunk_id))
        chunk_id += 1
        if end == len(clean):
            break
        start = end - overlap

    return chunks


def load_documents(directory: str | Path) -> list[Chunk]:
    directory = Path(directory)
    chunks: list[Chunk] = []
    for path in sorted(directory.rglob("*")):
        if path.suffix.lower() not in {".md", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8")
        chunks.extend(chunk_text(text, source=path.name))
    return chunks


class Retriever:
    """
    Two retrieval modes:
      - lexical: TF-IDF cosine similarity; fast and deterministic.
      - semantic: Sentence Transformer embeddings + cosine similarity.
    """

    def __init__(self, chunks: Iterable[Chunk], backend: str = "lexical"):
        self.chunks = list(chunks)
        if not self.chunks:
            raise ValueError("At least one document chunk is required.")

        self.backend = backend.lower()
        texts = [c.text for c in self.chunks]

        if self.backend == "lexical":
            self.vectorizer = TfidfVectorizer(stop_words="english")
            self.matrix = self.vectorizer.fit_transform(texts)
            self.encoder = None
            self.embeddings = None

        elif self.backend == "semantic":
            from sentence_transformers import SentenceTransformer

            model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
            self.encoder = SentenceTransformer(model_name)
            self.embeddings = self.encoder.encode(
                texts,
                normalize_embeddings=True,
                show_progress_bar=False,
            )
            self.vectorizer = None
            self.matrix = None

        else:
            raise ValueError("backend must be 'lexical' or 'semantic'")

    def search(self, query: str, top_k: int = 3) -> list[SearchResult]:
        if not query.strip():
            return []

        top_k = max(1, min(top_k, len(self.chunks)))

        if self.backend == "lexical":
            query_vec = self.vectorizer.transform([query])
            scores = cosine_similarity(query_vec, self.matrix)[0]
        else:
            query_vec = self.encoder.encode(
                [query],
                normalize_embeddings=True,
                show_progress_bar=False,
            )
            scores = np.dot(self.embeddings, query_vec[0])

        order = np.argsort(scores)[::-1][:top_k]
        return [
            SearchResult(chunk=self.chunks[i], score=float(scores[i]))
            for i in order
        ]


def build_grounded_prompt(question: str, results: list[SearchResult]) -> str:
    context_blocks = []
    for i, result in enumerate(results, start=1):
        context_blocks.append(
            f"[SOURCE {i}: {result.chunk.source} | chunk {result.chunk.chunk_id}]\n"
            f"{result.chunk.text}"
        )

    context = "\n\n".join(context_blocks)

    return f"""You are a technical assistant for ML, time-series forecasting, and ML2++.

Answer the user's question using ONLY the supplied context.
If the context is insufficient, say that clearly.
Do not invent project results, metrics, or implementation details.
At the end, list the source filenames you used.

CONTEXT
-------
{context}

QUESTION
--------
{question}
"""
