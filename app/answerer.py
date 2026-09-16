"""Extractive answer synthesis with citations.

No generative LLM call is used, so the demo has zero external
dependencies and zero API keys: the "answer" is composed directly from
the retrieved, cited passages. This keeps the demo fully deterministic
and inspectable, which is often preferable for a grounded-QA demo.
"""
from __future__ import annotations

from dataclasses import dataclass

from app.retriever import Chunk


@dataclass
class Citation:
    doc_id: str
    title: str
    snippet: str
    score: float


@dataclass
class Answer:
    answer: str
    citations: list[Citation]


def synthesize_answer(query: str, retrieved: list[tuple[Chunk, float]]) -> Answer:
    if not retrieved:
        return Answer(
            answer="I couldn't find anything relevant to that question in the knowledge base.",
            citations=[],
        )

    citations = [
        Citation(doc_id=chunk.doc_id, title=chunk.title, snippet=chunk.text, score=round(float(score), 4))
        for chunk, score in retrieved
    ]

    # Compose the answer out of the retrieved sentences themselves, each
    # tagged with an inline citation marker back to its source document.
    sentences_with_markers = [f"{c.snippet} [{c.doc_id}]" for c in citations]
    answer_text = " ".join(sentences_with_markers)

    return Answer(answer=answer_text, citations=citations)
