import json
import tempfile
from pathlib import Path

from main import export_metrics
from metrics_storage import MetricsDB
import main


class TestExportEndpoint:
    def setup_method(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.tmp.close()
        self.db = MetricsDB(self.tmp.name)
        self.db.save_snapshot({
            "endpoints": {
                "/api/query": {
                    "request_count": 10,
                    "error_count": 1,
                    "latency_samples": [10, 20, 30]
                }
            },
            "query_agent_counts": {"bot": 3},
            "alerts": []
        })
        main.metrics_db = self.db

    def teardown_method(self):
        Path(self.tmp.name).unlink(missing_ok=True)

    def test_export_csv_response(self):
        response = export_metrics(format="csv", hours=24)
        assert response.status_code == 200
        assert response.media_type == "text/csv"
        content_disposition = response.headers.get("content-disposition", "")
        assert "attachment; filename=" in content_disposition
        assert b"timestamp,endpoint" in response.body

    def test_export_json_response(self):
        response = export_metrics(format="json", hours=24)
        assert response.status_code == 200
        assert response.media_type == "application/json"
        payload = json.loads(response.body.decode("utf-8"))
        assert "export_metadata" in payload
        assert payload["export_metadata"]["period_hours"] == 24

    def test_export_html_response(self):
        response = export_metrics(format="html", hours=24)
        assert response.status_code == 200
        assert response.media_type == "text/html"
        assert b"Metrics Export Report" in response.body

    def test_export_invalid_format(self):
        response = export_metrics(format="xlsx", hours=24)
        assert response.status_code == 400
        payload = json.loads(response.body.decode("utf-8"))
        assert "Invalid format" in payload["error"]

    def test_export_invalid_hours_defaults_to_24(self):
        response = export_metrics(format="json", hours=999)
        payload = json.loads(response.body.decode("utf-8"))
        assert payload["export_metadata"]["period_hours"] == 24

    def test_export_db_not_initialized(self):
        main.metrics_db = None
        response = export_metrics(format="csv", hours=24)
        assert response.status_code == 503
        payload = json.loads(response.body.decode("utf-8"))
        assert payload["error"] == "Database not initialized"
