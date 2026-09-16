"""FastAPI app exposing the RAG knowledge assistant.

POST /ask   -> retrieve relevant passages and return a cited answer
GET  /health -> liveness check
GET  /docs   -> interactive OpenAPI docs (served by FastAPI automatically)
"""
from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.answerer import synthesize_answer
from app.retriever import Retriever

app = FastAPI(
    title="RAG Knowledge Assistant",
    description=(
        "A small retrieval-augmented Q&A demo over a synthetic document "
        "set. Every answer is grounded in retrieved passages with "
        "explicit citations."
    ),
    version="0.1.0",
)

_retriever = Retriever()


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Natural-language question")
    top_k: int = Field(3, ge=1, le=10, description="Number of passages to retrieve")


class CitationResponse(BaseModel):
    doc_id: str
    title: str
    snippet: str
    score: float


class AskResponse(BaseModel):
    question: str
    answer: str
    citations: list[CitationResponse]


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    retrieved = _retriever.retrieve(request.question, top_k=request.top_k)
    result = synthesize_answer(request.question, retrieved)
    return AskResponse(
        question=request.question,
        answer=result.answer,
        citations=[
            CitationResponse(doc_id=c.doc_id, title=c.title, snippet=c.snippet, score=c.score)
            for c in result.citations
        ],
    )
