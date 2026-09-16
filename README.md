# RAG Knowledge Assistant (v4)

A small, self-contained retrieval-augmented generation (RAG) demo: ask a
natural-language question and get back an answer that is *grounded* in
retrieved source passages, with an explicit citation back to the
document each passage came from.

> **v4 in a rotating series of small daily AI builds.** This entry's specific twist is a two-stage retrieval design: TF-IDF ranks whole documents first, then a second TF-IDF pass picks the single best-matching sentence inside the winning document to use as the citation snippet. This keeps citations short and precise even though ranking happens at the document level. See [ai-build-log](https://github.com/tanu-11sharma/ai-build-log) for the full series.

## Why this project

RAG is one of the most common patterns in production AI applications
today: instead of trusting a model's parametric memory, you retrieve
relevant context from your own documents and answer strictly from that
context. This demo implements the full pipeline — chunking, retrieval,
and cited answer synthesis — end to end, without requiring any external
LLM API key, so it's easy to run and inspect.

The "answering" step here is deliberately extractive (it composes the
answer directly from the retrieved sentences, each tagged with its
source) rather than generative, which keeps the whole demo
deterministic, dependency-free, and trivially testable — while still
demonstrating the retrieval + citation mechanics that generative RAG
systems rely on.

## How it works

1. A small synthetic knowledge base (`app/data/documents.py`) describes
   a fictional product, "Aurora Cloud Storage" (pricing, security, sync
   behavior, sharing, and limits).
2. `app/retriever.py` splits each document into sentence-level chunks
   and builds a TF-IDF index over them (scikit-learn).
3. On a query, the retriever ranks chunks by cosine similarity and
   returns the top-k matches.
4. `app/answerer.py` composes a cited answer directly from the
   retrieved chunks — each sentence is tagged with `[doc_id]`.
5. `app/main.py` exposes this as a small FastAPI service.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

## Example usage

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How much does the Pro tier cost?"}'
```

Example response:

```json
{
  "question": "How much does the Pro tier cost?",
  "answer": "The Pro tier costs $9 per month and includes 500GB of storage, versioned backups, and priority support. [pricing.md]",
  "citations": [
    {
      "doc_id": "pricing.md",
      "title": "Aurora Cloud Storage Pricing",
      "snippet": "The Pro tier costs $9 per month and includes 500GB of storage, versioned backups, and priority support.",
      "score": 0.4123
    }
  ]
}
```

Interactive API docs are also available at `http://127.0.0.1:8000/docs`
once the server is running.

## Test

```bash
pytest
```

## Notes / disclaimer

This is a demo built with synthetic, self-authored sample data about a
fictional product. It performs no real trading, medical, legal, or
financial actions, and it does not call out to any live external
system — everything runs locally against the bundled sample documents.
