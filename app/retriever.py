"""TF-IDF based retriever over the synthetic document set.

Retrieval ranks whole documents (not individual sentences) with TF-IDF
cosine similarity -- with only a handful of short documents, sentence-
level chunks are too sparse for TF-IDF to distinguish reliably, whereas
whole-document vectors give the model enough signal to rank correctly.
Each match also carries the single most relevant sentence from that
document, used as the citation snippet.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.data.documents import DOCUMENTS

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


@dataclass
class Chunk:
    doc_id: str
    title: str
    text: str


def _split_sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENTENCE_SPLIT.split(text) if s.strip()]


class Retriever:
    """Retrieves the most relevant documents for a query using TF-IDF cosine similarity."""

    def __init__(self) -> None:
        self.documents = DOCUMENTS
        self._doc_vectorizer = TfidfVectorizer(stop_words="english")
        self._doc_matrix = self._doc_vectorizer.fit_transform([d["text"] for d in self.documents])

        # A second, sentence-level index is used only to pick the best
        # citation snippet within a document that has already been
        # selected as relevant.
        self._sentence_vectorizer = TfidfVectorizer(stop_words="english")
        all_sentences = [s for d in self.documents for s in _split_sentences(d["text"])]
        self._sentence_vectorizer.fit(all_sentences)

    def _best_sentence(self, query: str, doc_text: str) -> str:
        sentences = _split_sentences(doc_text)
        if len(sentences) == 1:
            return sentences[0]
        sent_matrix = self._sentence_vectorizer.transform(sentences)
        query_vec = self._sentence_vectorizer.transform([query])
        sims = cosine_similarity(query_vec, sent_matrix)[0]
        best_idx = int(sims.argmax())
        return sentences[best_idx]

    def retrieve(self, query: str, top_k: int = 3) -> list[tuple[Chunk, float]]:
        if not query.strip():
            return []
        query_vec = self._doc_vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self._doc_matrix)[0]
        ranked = sorted(zip(self.documents, scores), key=lambda pair: pair[1], reverse=True)

        results: list[tuple[Chunk, float]] = []
        for doc, score in ranked[:top_k]:
            if score <= 0:
                continue
            snippet = self._best_sentence(query, doc["text"])
            results.append((Chunk(doc_id=doc["doc_id"], title=doc["title"], text=snippet), score))
        return results
