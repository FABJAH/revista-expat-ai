from fastapi.testclient import TestClient

import main


class DummyOrchestrator:
    def __init__(self):
        self.calls = []

    def process_query(self, question, language, limit, offset):
        self.calls.append(
            {
                "question": question,
                "language": language,
                "limit": limit,
                "offset": offset,
            }
        )
        return {
            "agente": "Dummy",
            "respuesta": "ok",
            "total_results": 0,
            "json": [],
        }


def test_query_rejects_non_json_content_type(monkeypatch):
    dummy = DummyOrchestrator()
    monkeypatch.setattr(main, "get_orchestrator", lambda: dummy)

    client = TestClient(main.app)
    resp = client.post(
        "/api/query",
        data="question=hola",
        headers={"Content-Type": "text/plain"},
    )

    assert resp.status_code == 415
    assert "Content-Type" in resp.json()["error"]


def test_query_clamps_limit_offset_and_language(monkeypatch):
    dummy = DummyOrchestrator()
    monkeypatch.setattr(main, "get_orchestrator", lambda: dummy)

    client = TestClient(main.app)
    resp = client.post(
        "/api/query",
        json={
            "question": "Necesito ayuda",
            "language": "fr",
            "limit": 999,
            "offset": 10000,
        },
    )

    assert resp.status_code == 200
    assert len(dummy.calls) == 1
    call = dummy.calls[0]
    assert call["language"] == "es"
    assert call["limit"] == 20
    assert call["offset"] == 1000


def test_analytics_rejects_oversized_payload(monkeypatch):
    dummy = DummyOrchestrator()
    monkeypatch.setattr(main, "get_orchestrator", lambda: dummy)

    client = TestClient(main.app)
    resp = client.post(
        "/api/analytics",
        json={
            "event": "click",
            "data": {"blob": "a" * 9000},
            "session_id": "session_ok",
        },
    )

    assert resp.status_code == 413
    assert "demasiado grande" in resp.json()["error"]


def test_analytics_rejects_too_long_session_id(monkeypatch):
    dummy = DummyOrchestrator()
    monkeypatch.setattr(main, "get_orchestrator", lambda: dummy)

    client = TestClient(main.app)
    resp = client.post(
        "/api/analytics",
        json={
            "event": "click",
            "data": {},
            "session_id": "x" * 129,
        },
    )

    assert resp.status_code == 400
    assert "session_id" in resp.json()["error"]
