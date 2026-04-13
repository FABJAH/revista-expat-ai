"""
Test suite for metrics_storage.py persistent database layer
"""
import sqlite3
import tempfile
from pathlib import Path
import pytest
from datetime import datetime, timedelta
from metrics_storage import MetricsDB


class TestMetricsStorage:
    """Tests for MetricsDB class"""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing"""
        temp_dir = tempfile.mkdtemp()
        db_path = Path(temp_dir) / "test_metrics.db"
        db = MetricsDB(str(db_path))
        yield db
        # Cleanup
        if db_path.exists():
            db_path.unlink()

    def test_create_database_schema(self, temp_db):
        """Verify database schema is created correctly"""
        conn = temp_db.get_connection()
        cursor = conn.cursor()

        # Check tables exist
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        tables = {row[0] for row in cursor.fetchall()}

        assert "metrics_snapshot" in tables
        assert "agent_metrics" in tables
        assert "alerts_history" in tables

        # Check indexes exist
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='index'"
        )
        indexes = {row[0] for row in cursor.fetchall()}

        assert "idx_snapshot_timestamp" in indexes
        assert "idx_snapshot_endpoint" in indexes

        conn.close()

    def test_save_and_retrieve_snapshot(self, temp_db):
        """Test saving and retrieving metrics snapshot"""
        # Create sample metrics
        metrics = {
            "endpoints": {
                "/api/query": {
                    "request_count": 100,
                    "error_count": 5,
                    "latency_samples": [10, 20, 30, 40, 50]
                },
                "/api/health": {
                    "request_count": 200,
                    "error_count": 0,
                    "latency_samples": [5, 5, 5, 5, 5]
                }
            },
            "query_agent_counts": {
                "Legal": 10,
                "Healthcare": 5
            },
            "alerts": [
                {
                    "endpoint": "/api/query",
                    "type": "error_rate",
                    "message": "Error rate 5%",
                    "value": 5.0
                }
            ]
        }

        # Save snapshot
        temp_db.save_snapshot(metrics)

        # Retrieve and verify
        history = temp_db.get_history(hours=24)

        assert "/api/query" in history
        assert "/api/health" in history
        assert len(history["/api/query"]) == 1
        assert len(history["/api/health"]) == 1

        # Verify values
        query_record = history["/api/query"][0]
        assert query_record["request_count"] == 100
        assert query_record["error_count"] == 5
        assert query_record["error_rate_pct"] == 5.0

    def test_get_history_with_time_filter(self, temp_db):
        """Test retrieving history with time filtering"""
        # Create metrics from different times
        old_time = datetime.utcnow() - timedelta(hours=48)
        new_time = datetime.utcnow()

        metrics_old = {
            "endpoints": {
                "/api/query": {
                    "request_count": 50,
                    "error_count": 2,
                    "latency_samples": [10, 20, 30]
                }
            },
            "query_agent_counts": {},
            "alerts": []
        }

        metrics_new = {
            "endpoints": {
                "/api/query": {
                    "request_count": 100,
                    "error_count": 5,
                    "latency_samples": [20, 30, 40]
                }
            },
            "query_agent_counts": {},
            "alerts": []
        }

        # Manually insert old record
        conn = temp_db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO metrics_snapshot
        (timestamp, endpoint, request_count, error_count,
         latency_avg_ms, latency_p95_ms, error_rate_pct)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            old_time.isoformat(), "/api/query", 50, 2,
            20.0, 30.0, 4.0
        ))
        conn.commit()
        conn.close()

        temp_db.save_snapshot(metrics_new)

        # Test 24h filter (should get only new)
        history_24h = temp_db.get_history(hours=24)
        assert len(history_24h["/api/query"]) == 1
        assert history_24h["/api/query"][0]["request_count"] == 100

        # Test 72h filter (should get both)
        history_72h = temp_db.get_history(hours=72)
        assert len(history_72h["/api/query"]) == 2

    def test_trends_calculation(self, temp_db):
        """Test trend analysis calculation"""
        # Create multiple samples
        for i in range(5):
            metrics = {
                "endpoints": {
                    "/api/query": {
                        "request_count": 100 + i*10,
                        "error_count": 5 + i,
                        "latency_samples": [10 + i*5, 20 + i*5, 30 + i*5]
                    }
                },
                "query_agent_counts": {},
                "alerts": []
            }
            temp_db.save_snapshot(metrics)

        # Get trends
        trends = temp_db.get_trends("/api/query", hours=24)

        assert trends["endpoint"] == "/api/query"
        assert "statistics" in trends
        assert "latency" in trends["statistics"]
        assert "peak_ms" in trends["statistics"]["latency"]
        assert "average_ms" in trends["statistics"]["latency"]
        assert trends["statistics"]["total_measurements"] == 5

        # Verify peak latency calculation
        peak_lat = trends["statistics"]["latency"]["peak_ms"]
        assert peak_lat > 20  # Should be 40 (30 + 4*5)

    def test_agent_metrics_history(self, temp_db):
        """Test agent metrics tracking"""
        for i in range(3):
            metrics = {
                "endpoints": {},
                "query_agent_counts": {
                    "Legal": 10 + i,
                    "Healthcare": 5 + i
                },
                "alerts": []
            }
            temp_db.save_snapshot(metrics)

        # Retrieve agent history
        history = temp_db.get_agent_history(hours=24)

        assert "Legal" in history
        assert "Healthcare" in history
        assert len(history["Legal"]) == 3
        assert len(history["Healthcare"]) == 3

        # Verify ordering by timestamp
        assert history["Legal"][0]["count"] == 10
        assert history["Legal"][1]["count"] == 11
        assert history["Legal"][2]["count"] == 12


class TestMetricsStorageIntegration:
    """Integration tests with main.py"""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database"""
        temp_dir = tempfile.mkdtemp()
        db_path = Path(temp_dir) / "test_metrics.db"
        db = MetricsDB(str(db_path))
        yield db
        if db_path.exists():
            db_path.unlink()

    def test_background_persistence_task(self, temp_db):
        """Test that save_metrics_to_db preserves data correctly"""
        # Simulate what main.py does
        sample_snapshot = {
            "window_size": 200,
            "endpoints": {
                "/api/query": {
                    "requests": 100,
                    "errors": 5,
                    "error_rate_pct": 5.0,
                    "latency_avg_ms": 25.0,
                    "latency_p95_ms": 40.0,
                    "samples": 5
                }
            },
            "query_agent_counts": {
                "Legal": 8,
                "Healthcare": 3
            },
            "alerts": [
                {
                    "endpoint": "/api/query",
                    "type": "error_rate",
                    "message": "Error rate exceeded",
                    "value": 5.0
                }
            ]
        }

        # Save multiple snapshots
        for _ in range(5):
            # Convert to MetricsDB format
            metrics = {
                "endpoints": {
                    ep: {
                        "request_count": data["requests"],
                        "error_count": data["errors"],
                        "latency_samples": [data["latency_avg_ms"]]
                    } for ep, data in sample_snapshot["endpoints"].items()
                },
                "query_agent_counts": sample_snapshot["query_agent_counts"],
                "alerts": sample_snapshot["alerts"]
            }
            temp_db.save_snapshot(metrics)

        # Verify persistence
        history = temp_db.get_history(hours=24)
        assert "/api/query" in history
        assert len(history["/api/query"]) == 5

        # Verify agent counts
        agent_history = temp_db.get_agent_history(hours=24)
        assert len(agent_history["Legal"]) == 5

        # Verify alerts
        alerts = temp_db.get_alerts_history(hours=24)
        assert len(alerts) == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
