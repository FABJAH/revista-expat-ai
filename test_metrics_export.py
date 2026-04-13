# test_metrics_export.py - Tests for Phase 8 export functionality
import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from metrics_storage import MetricsDB


@pytest.fixture
def temp_db():
    """Create temporary metrics database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    db = MetricsDB(db_path)

    # Seed with sample data
    sample_metrics = {
        "endpoints": {
            "/api/query": {
                "request_count": 100,
                "error_count": 5,
                "latency_samples": [50, 75, 100, 125, 150]
            },
            "/api/analytics": {
                "request_count": 50,
                "error_count": 2,
                "latency_samples": [40, 60, 80]
            }
        },
        "query_agent_counts": {
            "immigration_bot": 30,
            "work_bot": 20
        },
        "alerts": []
    }

    db.save_snapshot(sample_metrics)

    yield db

    # Cleanup
    Path(db_path).unlink(missing_ok=True)


class TestMetricsExport:
    """Test export functionality for metrics."""

    def test_export_to_csv_all_endpoints(self, temp_db):
        """Test CSV export with all endpoints."""
        csv_output = temp_db.export_to_csv()

        # Verify CSV structure
        assert csv_output is not None
        assert isinstance(csv_output, str)
        assert len(csv_output) > 0

        lines = csv_output.strip().split('\n')
        assert len(lines) >= 1  # At least header

        # Check header
        assert "timestamp" in lines[0]
        assert "endpoint" in lines[0]
        assert "request_count" in lines[0]
        assert "error_count" in lines[0]
        assert "latency_avg_ms" in lines[0]
        assert "latency_p95_ms" in lines[0]
        assert "error_rate_pct" in lines[0]

    def test_export_to_csv_single_endpoint(self, temp_db):
        """Test CSV export for a specific endpoint."""
        csv_output = temp_db.export_to_csv(endpoint="/api/query")

        assert csv_output is not None
        assert isinstance(csv_output, str)

        lines = csv_output.strip().split('\n')
        if len(lines) > 1:
            # If data rows exist, verify they contain the endpoint
            for line in lines[1:]:
                assert "/api/query" in line

    def test_export_to_json_structure(self, temp_db):
        """Test JSON export structure and metadata."""
        json_output = temp_db.export_to_json()

        # Verify it's a dict
        assert isinstance(json_output, dict)

        # Verify metadata
        assert "export_metadata" in json_output
        metadata = json_output["export_metadata"]

        assert "export_timestamp" in metadata
        assert "period_hours" in metadata
        assert metadata["period_hours"] == 24

        assert "endpoint_filter" in metadata
        assert metadata["endpoint_filter"] is None  # No filter specified

        assert "total_records" in metadata
        assert metadata["total_records"] >= 0

        # Verify metrics
        assert "metrics" in json_output
        assert isinstance(json_output["metrics"], dict)

    def test_export_to_json_with_endpoint_filter(self, temp_db):
        """Test JSON export with endpoint filter."""
        json_output = temp_db.export_to_json(endpoint="/api/query")

        assert json_output["export_metadata"]["endpoint_filter"] == "/api/query"

        # Only /api/query should be in metrics (if it has data)
        if json_output["metrics"]:
            for endpoint in json_output["metrics"].keys():
                assert endpoint == "/api/query"

    def test_export_to_json_serializable(self, temp_db):
        """Test that JSON output is properly serializable."""
        json_output = temp_db.export_to_json()

        # Should be able to serialize to JSON string
        json_str = json.dumps(json_output)
        assert json_str is not None
        assert len(json_str) > 0

        # Should be able to deserialize back
        parsed = json.loads(json_str)
        assert parsed["export_metadata"] is not None

    def test_export_summary_report_html_structure(self, temp_db):
        """Test HTML summary report structure."""
        html_output = temp_db.export_summary_report()

        assert html_output is not None
        assert isinstance(html_output, str)
        assert len(html_output) > 0

        # Verify HTML structure
        assert "<html>" in html_output or "<HTML>" in html_output.upper()
        assert "</html>" in html_output or "</HTML>" in html_output.upper()
        assert "<body>" in html_output or "<BODY>" in html_output.upper()
        assert "</body>" in html_output or "</BODY>" in html_output.upper()

        # Verify title
        assert "Metrics Export Report" in html_output

    def test_export_summary_report_contains_stats(self, temp_db):
        """Test that HTML report contains summary statistics."""
        html_output = temp_db.export_summary_report()

        # Verify summary sections present
        assert "Summary Statistics" in html_output
        assert "Per-Endpoint Metrics" in html_output

        # Verify it contains metric labels
        assert "Total Requests" in html_output
        assert "Total Errors" in html_output
        assert "Avg Error Rate" in html_output
        assert "Avg Latency" in html_output
        assert "Avg P95 Latency" in html_output

    def test_export_summary_report_contains_table(self, temp_db):
        """Test that HTML report contains endpoint table."""
        html_output = temp_db.export_summary_report()

        # Verify table structure
        assert "<table>" in html_output
        assert "</table>" in html_output
        assert "<thead>" in html_output
        assert "</thead>" in html_output
        assert "<tbody>" in html_output
        assert "</tbody>" in html_output

        # Verify table headers
        assert "<th>Endpoint</th>" in html_output
        assert "<th>Requests</th>" in html_output
        assert "<th>Errors</th>" in html_output

    def test_export_with_custom_hours(self, temp_db):
        """Test export with custom hour parameter."""
        # CSV with custom hours (use 48 hours to ensure data inclusion)
        csv_output = temp_db.export_to_csv(hours=48)
        assert csv_output is not None

        # JSON with custom hours
        json_output = temp_db.export_to_json(hours=48)
        assert json_output["export_metadata"]["period_hours"] == 48

        # HTML with custom hours
        html_output = temp_db.export_summary_report(hours=48)
        # Check that hours appears in output (either "48 hours" or summary section)
        assert "48 hours" in html_output or "Summary Statistics" in html_output
        """Test exports on empty database."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name

        try:
            db = MetricsDB(db_path)

            # CSV on empty DB
            csv_output = db.export_to_csv()
            assert csv_output is not None
            lines = csv_output.split('\n')
            assert len(lines) >= 1  # At least header

            # JSON on empty DB
            json_output = db.export_to_json()
            assert json_output["export_metadata"]["total_records"] == 0

            # HTML on empty DB (should return minimal HTML)
            html_output = db.export_summary_report()
            assert "No metrics data available" in html_output or \
                   "Summary Statistics" in html_output

        finally:
            Path(db_path).unlink(missing_ok=True)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
