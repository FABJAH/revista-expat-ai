# test_api_export.py - Tests for Phase 8 API export endpoints
import json
import pytest
import tempfile
from pathlib import Path
from datetime import datetime

# Import after ensuring metrics_storage exists
from metrics_storage import MetricsDB


class TestExportMethods:
    """Test export methods directly (for API validation)."""

    @pytest.fixture
    def temp_db(self):
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

    def test_export_csv_output_valid(self, temp_db):
        """Test CSV export produces valid output."""
        csv_output = temp_db.export_to_csv()

        assert csv_output is not None
        assert isinstance(csv_output, str)
        assert len(csv_output) > 0
        assert "timestamp,endpoint,request_count" in csv_output

    def test_export_csv_with_endpoint_filter(self, temp_db):
        """Test CSV export with endpoint filter."""
        csv_output = temp_db.export_to_csv(endpoint="/api/query")

        assert csv_output is not None
        assert "timestamp,endpoint,request_count" in csv_output

    def test_export_json_output_valid(self, temp_db):
        """Test JSON export produces valid output."""
        json_output = temp_db.export_to_json()

        assert json_output is not None
        assert isinstance(json_output, dict)
        assert "export_metadata" in json_output
        assert "metrics" in json_output

    def test_export_json_with_endpoint_filter(self, temp_db):
        """Test JSON export with endpoint filter."""
        json_output = temp_db.export_to_json(endpoint="/api/query")

        assert json_output["export_metadata"]["endpoint_filter"] == "/api/query"

    def test_export_json_serializable_to_string(self, temp_db):
        """Test JSON export can be serialized to string."""
        json_output = temp_db.export_to_json()
        json_str = json.dumps(json_output, default=str)

        assert json_str is not None
        assert len(json_str) > 0

    def test_export_html_output_valid(self, temp_db):
        """Test HTML export produces valid output."""
        html_output = temp_db.export_summary_report()

        assert html_output is not None
        assert isinstance(html_output, str)
        assert "<html>" in html_output.lower()
        assert "</html>" in html_output.lower()
        assert "Metrics Export Report" in html_output

    def test_export_html_contains_table(self, temp_db):
        """Test HTML export contains table with metrics."""
        html_output = temp_db.export_summary_report()

        assert "<table>" in html_output
        assert "<thead>" in html_output
        assert "<tbody>" in html_output
        assert "Endpoint" in html_output
        assert "Requests" in html_output

    def test_export_methods_with_custom_hours(self, temp_db):
        """Test export methods accept hours parameter."""
        csv = temp_db.export_to_csv(hours=12)
        json_data = temp_db.export_to_json(hours=12)
        html = temp_db.export_summary_report(hours=12)

        assert csv is not None
        assert json_data["export_metadata"]["period_hours"] == 12
        assert html is not None

    def test_export_csv_encoding_utf8(self, temp_db):
        """Test CSV export can be encoded to UTF-8."""
        csv_output = temp_db.export_to_csv()
        encoded = csv_output.encode("utf-8")

        assert encoded is not None
        assert len(encoded) > 0

    def test_export_html_encoding_utf8(self, temp_db):
        """Test HTML export can be encoded to UTF-8."""
        html_output = temp_db.export_summary_report()
        encoded = html_output.encode("utf-8")

        assert encoded is not None
        assert len(encoded) > 0

    def test_export_json_as_string_contains_data(self, temp_db):
        """Test JSON export as string contains expected data."""
        json_output = temp_db.export_to_json()
        json_str = json.dumps(json_output, default=str, indent=2)

        assert "export_timestamp" in json_str
        assert "period_hours" in json_str
        assert "metrics" in json_str

    def test_export_empty_database(self):
        """Test exports on empty database."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name

        try:
            db = MetricsDB(db_path)

            # CSV on empty DB
            csv = db.export_to_csv()
            assert csv is not None
            assert "timestamp,endpoint" in csv

            # JSON on empty DB
            json_data = db.export_to_json()
            assert json_data["export_metadata"]["total_records"] == 0

            # HTML on empty DB
            html = db.export_summary_report()
            assert html is not None

        finally:
            Path(db_path).unlink(missing_ok=True)

    def test_export_csv_can_be_used_for_download(self, temp_db):
        """Test CSV export - validate it's suitable for download."""
        csv_output = temp_db.export_to_csv()
        # Simulate encoding for file download
        csv_bytes = csv_output.encode("utf-8")
        filename = "metrics_export_test.csv"

        assert len(csv_bytes) > 0
        assert b"timestamp" in csv_bytes
        assert filename.endswith(".csv")

    def test_export_json_can_be_used_for_download(self, temp_db):
        """Test JSON export - validate it's suitable for download."""
        json_output = temp_db.export_to_json()
        json_str = json.dumps(json_output, default=str)
        json_bytes = json_str.encode("utf-8")
        filename = "metrics_export_test.json"

        assert len(json_bytes) > 0
        assert b"export_metadata" in json_bytes
        assert filename.endswith(".json")

    def test_export_html_can_be_used_for_download(self, temp_db):
        """Test HTML export - validate it's suitable for download."""
        html_output = temp_db.export_summary_report()
        html_bytes = html_output.encode("utf-8")
        filename = "metrics_report_test.html"

        assert len(html_bytes) > 0
        assert b"Metrics Export Report" in html_bytes
        assert filename.endswith(".html")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
