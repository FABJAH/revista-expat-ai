from fastapi.testclient import TestClient

import main


class DummyOrchestrator:
    def process_query(self, question, language, limit, offset):
        return {
            "agente": "Dummy",
            "respuesta": f"ok: {question}",
            "total_results": 0,
            "json": [],
        }


def test_metrics_endpoint_reports_api_activity(monkeypatch):
    monkeypatch.setattr(main, "get_orchestrator", lambda: DummyOrchestrator())

    client = TestClient(main.app)

    # Genera tráfico API en endpoints distintos
    health_resp = client.get("/api/health")
    assert health_resp.status_code == 200

    query_resp = client.post(
        "/api/query",
        json={"question": "hola", "language": "es"},
    )
    assert query_resp.status_code == 200

    metrics_resp = client.get("/api/metrics")
    assert metrics_resp.status_code == 200

    payload = metrics_resp.json()
    assert payload["status"] == "ok"
    assert "metrics" in payload

    endpoints = payload["metrics"]["endpoints"]
    assert "/api/health" in endpoints
    assert "/api/query" in endpoints
    assert endpoints["/api/health"]["requests"] >= 1
    assert endpoints["/api/query"]["requests"] >= 1
    assert endpoints["/api/query"]["latency_avg_ms"] >= 0
