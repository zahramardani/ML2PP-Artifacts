from __future__ import annotations

import os
from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.rag import Retriever, build_grounded_prompt, load_documents

load_dotenv()

app = FastAPI(
    title="ML2++ RAG Copilot",
    version="1.0.0",
    description="Portfolio-ready RAG API for forecasting and ML2++ knowledge.",
)


class QueryRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    top_k: int = Field(default=3, ge=1, le=10)


class SourceItem(BaseModel):
    source: str
    chunk_id: int
    score: float
    text: str


class RetrieveResponse(BaseModel):
    question: str
    backend: str
    results: list[SourceItem]


class AnswerResponse(BaseModel):
    question: str
    answer: str
    mode: str
    sources: list[SourceItem]


@lru_cache(maxsize=1)
def get_retriever() -> Retriever:
    docs_dir = Path(os.getenv("DOCS_DIR", "data/sample_docs"))
    backend = os.getenv("RETRIEVER_BACKEND", "lexical")
    chunks = load_documents(docs_dir)
    return Retriever(chunks, backend=backend)


def serialize_results(results):
    return [
        SourceItem(
            source=r.chunk.source,
            chunk_id=r.chunk.chunk_id,
            score=round(r.score, 4),
            text=r.chunk.text,
        )
        for r in results
    ]


def generate_answer(prompt: str) -> tuple[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return (
            "OPENAI_API_KEY is not configured. Retrieval succeeded; "
            "inspect the returned source chunks to see the grounded context.",
            "retrieval-only",
        )

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-6-luna"),
        input=[{"role": "user", "content": prompt}],
    )
    return response.output_text, "llm+rag"


@app.get("/health")
def health():
    retriever = get_retriever()
    return {
        "status": "ok",
        "backend": retriever.backend,
        "chunks": len(retriever.chunks),
    }


@app.post("/retrieve", response_model=RetrieveResponse)
def retrieve(req: QueryRequest):
    retriever = get_retriever()
    results = retriever.search(req.question, top_k=req.top_k)
    return RetrieveResponse(
        question=req.question,
        backend=retriever.backend,
        results=serialize_results(results),
    )


@app.post("/ask", response_model=AnswerResponse)
def ask(req: QueryRequest):
    retriever = get_retriever()
    results = retriever.search(req.question, top_k=req.top_k)
    prompt = build_grounded_prompt(req.question, results)
    answer, mode = generate_answer(prompt)

    return AnswerResponse(
        question=req.question,
        answer=answer,
        mode=mode,
        sources=serialize_results(results),
    )
