from app.retriever import Retriever


def test_retriever_finds_relevant_chunk_for_pricing_question():
    retriever = Retriever()
    results = retriever.retrieve("How much does the Pro tier cost?", top_k=3)
    assert results, "expected at least one retrieved chunk"
    top_chunk, top_score = results[0]
    assert top_chunk.doc_id == "pricing.md"
    assert top_score > 0


def test_retriever_returns_empty_for_blank_query():
    retriever = Retriever()
    assert retriever.retrieve("   ") == []


def test_retriever_respects_top_k():
    retriever = Retriever()
    results = retriever.retrieve("storage encryption security", top_k=2)
    assert len(results) <= 2
