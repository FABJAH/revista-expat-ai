from fastapi.testclient import TestClient

import main


class DummyOrchestrator:
    def process_query(self, question, language, limit, offset):
        return {
            "agente": "Legal",
            "respuesta": "ok",
            "total_results": 0,
            "json": [],
        }


def test_metrics_include_query_agent_counts(monkeypatch):
    monkeypatch.setattr(main, "get_orchestrator", lambda: DummyOrchestrator())

    client = TestClient(main.app)
    resp = client.post(
        "/api/query",
        json={"question": "Necesito abogado", "language": "es"},
    )
    assert resp.status_code == 200

    metrics_resp = client.get("/api/metrics")
    assert metrics_resp.status_code == 200
    payload = metrics_resp.json()

    assert "alerts" in payload
    assert payload["metrics"]["query_agents"].get("Legal", 0) >= 1


def test_prometheus_metrics_endpoint(monkeypatch):
    monkeypatch.setattr(main, "get_orchestrator", lambda: DummyOrchestrator())

    client = TestClient(main.app)
    client.get("/api/health")
    client.post(
        "/api/query",
        json={"question": "hola", "language": "es"},
    )

    resp = client.get("/api/metrics/prometheus")
    assert resp.status_code == 200

    body = resp.text
    assert "revista_api_requests_total" in body
    assert 'endpoint="/api/health"' in body
    assert "revista_query_agent_total" in body
    assert 'agent="Legal"' in body
