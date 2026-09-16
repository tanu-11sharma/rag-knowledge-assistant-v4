from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_ask_returns_grounded_answer_with_citations():
    resp = client.post("/ask", json={"question": "What encryption does Aurora use?"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["citations"], "expected at least one citation"
    assert body["citations"][0]["doc_id"] == "security.md"
    assert "[security.md]" in body["answer"]


def test_ask_with_no_match_returns_fallback_message():
    resp = client.post("/ask", json={"question": "xyzzy nonsense query zzz"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["citations"] == []
    assert "couldn't find" in body["answer"].lower()


def test_ask_rejects_empty_question():
    resp = client.post("/ask", json={"question": ""})
    assert resp.status_code == 422
