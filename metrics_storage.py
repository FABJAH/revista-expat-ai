# metrics_storage.py - Persistent metrics database layer
import sqlite3
import json
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional


class MetricsDB:
    """SQLite-based persistent metrics storage with history and trends."""

    def __init__(self, db_path: str = "metrics.db"):
        """Initialize database connection and create schema if needed."""
        self.db_path = Path(db_path)
        self.lock = threading.Lock()
        self.create_tables()

    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def create_tables(self) -> None:
        """Create database schema if not exists."""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Main metrics snapshot table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics_snapshot (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                endpoint TEXT NOT NULL,
                request_count INTEGER DEFAULT 0,
                error_count INTEGER DEFAULT 0,
                latency_avg_ms REAL,
                latency_p95_ms REAL,
                error_rate_pct REAL
            )
            """)

            # Agent counts table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                agent_name TEXT NOT NULL,
                count INTEGER DEFAULT 0
            )
            """)

            # Alerts history table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                endpoint TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                message TEXT,
                value REAL
            )
            """)

            # Create indexes for faster queries
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_snapshot_timestamp "
                "ON metrics_snapshot(timestamp)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_snapshot_endpoint "
                "ON metrics_snapshot(endpoint)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_agent_timestamp "
                "ON agent_metrics(timestamp)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_alerts_timestamp "
                "ON alerts_history(timestamp)"
            )

            conn.commit()
            conn.close()

    def save_snapshot(self, metrics: Dict) -> None:
        """
        Save a complete metrics snapshot to database.

        Args:
            metrics: Dict with endpoints, query_agent_counts, alerts from
                     main.py get_metrics_snapshot()
        """
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Save endpoint metrics
            endpoints = metrics.get("endpoints", {})
            for endpoint, data in endpoints.items():
                error_rate = 0.0
                if data.get("request_count", 0) > 0:
                    error_rate = (data.get("error_count", 0) /
                                  data.get("request_count")) * 100

                latency_avg = None
                latency_p95 = None
                if data.get("latency_samples"):
                    samples = data["latency_samples"]
                    latency_avg = sum(samples) / len(samples)
                    sorted_samples = sorted(samples)
                    idx = int(len(sorted_samples) * 0.95)
                    latency_p95 = sorted_samples[min(idx,
                                                      len(sorted_samples)-1)]

                cursor.execute("""
                INSERT INTO metrics_snapshot
                (endpoint, request_count, error_count, latency_avg_ms,
                 latency_p95_ms, error_rate_pct)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    endpoint,
                    data.get("request_count", 0),
                    data.get("error_count", 0),
                    latency_avg,
                    latency_p95,
                    error_rate
                ))

            # Save agent counts
            agents = metrics.get("query_agent_counts", {})
            for agent_name, count in agents.items():
                cursor.execute("""
                INSERT INTO agent_metrics (agent_name, count)
                VALUES (?, ?)
                """, (str(agent_name), count))

            # Save alerts
            alerts = metrics.get("alerts", [])
            for alert in alerts:
                cursor.execute("""
                INSERT INTO alerts_history
                (endpoint, alert_type, message, value)
                VALUES (?, ?, ?, ?)
                """, (
                    alert.get("endpoint"),
                    alert.get("type"),
                    alert.get("message"),
                    alert.get("value")
                ))

            conn.commit()
            conn.close()

    def get_history(self, hours: int = 24,
                    endpoint: Optional[str] = None) -> Dict:
        """
        Retrieve metrics history for a time period.

        Args:
            hours: Number of hours to look back (default 24)
            endpoint: Optional endpoint filter

        Returns:
            Dict with endpoints containing list of records
        """
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()

            cutoff_time = datetime.utcnow() - timedelta(hours=hours)

            if endpoint:
                cursor.execute("""
                SELECT * FROM metrics_snapshot
                WHERE timestamp >= ? AND endpoint = ?
                ORDER BY timestamp ASC
                """, (cutoff_time.isoformat(), endpoint))
            else:
                cursor.execute("""
                SELECT * FROM metrics_snapshot
                WHERE timestamp >= ?
                ORDER BY timestamp ASC
                """, (cutoff_time.isoformat(),))

            rows = cursor.fetchall()
            conn.close()

            # Organize by endpoint
            history = {}
            for row in rows:
                ep = row["endpoint"]
                if ep not in history:
                    history[ep] = []

                history[ep].append({
                    "timestamp": row["timestamp"],
                    "request_count": row["request_count"],
                    "error_count": row["error_count"],
                    "latency_avg_ms": row["latency_avg_ms"],
                    "latency_p95_ms": row["latency_p95_ms"],
                    "error_rate_pct": row["error_rate_pct"]
                })

            return history

    def get_trends(self, endpoint: str,
                   hours: int = 24) -> Dict:
        """
        Calculate trends for an endpoint.

        Args:
            endpoint: Endpoint name
            hours: Number of hours to analyze

        Returns:
            Dict with peak values, averages, and trends
        """
        history = self.get_history(hours=hours, endpoint=endpoint)

        if endpoint not in history or not history[endpoint]:
            return {
                "endpoint": endpoint,
                "message": "No data available",
                "data": []
            }

        records = history[endpoint]

        # Calculate statistics
        latencies = [r["latency_p95_ms"] for r in records
                     if r["latency_p95_ms"] is not None]
        error_rates = [r["error_rate_pct"] for r in records]

        peak_latency = max(latencies) if latencies else None
        avg_latency = sum(latencies) / len(latencies) if latencies else None
        peak_error_rate = max(error_rates) if error_rates else None
        avg_error_rate = sum(error_rates) / len(error_rates) if error_rates \
            else None

        # Find peak error moment
        peak_error_record = max(records, key=lambda x: x["error_rate_pct"],
                                default=None)

        return {
            "endpoint": endpoint,
            "period_hours": hours,
            "statistics": {
                "latency": {
                    "peak_ms": peak_latency,
                    "average_ms": avg_latency
                },
                "error_rate": {
                    "peak_pct": peak_error_rate,
                    "average_pct": avg_error_rate
                },
                "total_measurements": len(records)
            },
            "peak_error_moment": peak_error_record,
            "data": records
        }

    def get_agent_history(self, hours: int = 24) -> Dict:
        """
        Get agent activity history.

        Args:
            hours: Number of hours to look back

        Returns:
            Dict with agent counts over time
        """
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()

            cutoff_time = datetime.utcnow() - timedelta(hours=hours)

            cursor.execute("""
            SELECT * FROM agent_metrics
            WHERE timestamp >= ?
            ORDER BY timestamp ASC
            """, (cutoff_time.isoformat(),))

            rows = cursor.fetchall()
            conn.close()

            # Organize by agent
            history = {}
            for row in rows:
                agent = row["agent_name"]
                if agent not in history:
                    history[agent] = []

                history[agent].append({
                    "timestamp": row["timestamp"],
                    "count": row["count"]
                })

            return history

    def get_alerts_history(self, hours: int = 24,
                          alert_type: Optional[str] = None) -> List[Dict]:
        """
        Get alerts history.

        Args:
            hours: Number of hours to look back
            alert_type: Optional filter by alert type (error_rate, latency)

        Returns:
            List of alert records
        """
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()

            cutoff_time = datetime.utcnow() - timedelta(hours=hours)

            if alert_type:
                cursor.execute("""
                SELECT * FROM alerts_history
                WHERE timestamp >= ? AND alert_type = ?
                ORDER BY timestamp DESC
                """, (cutoff_time.isoformat(), alert_type))
            else:
                cursor.execute("""
                SELECT * FROM alerts_history
                WHERE timestamp >= ?
                ORDER BY timestamp DESC
                """, (cutoff_time.isoformat(),))

            rows = cursor.fetchall()
            conn.close()

            return [dict(row) for row in rows]

    def cleanup_old_data(self, days: int = 30) -> int:
        """
        Delete records older than specified days (maintenance task).

        Args:
            days: Minimum age of records to delete

        Returns:
            Number of rows deleted
        """
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()

            cutoff_time = datetime.utcnow() - timedelta(days=days)

            deleted = 0
            for table in ["metrics_snapshot", "agent_metrics",
                         "alerts_history"]:
                cursor.execute(f"""
                DELETE FROM {table} WHERE timestamp < ?
                """, (cutoff_time.isoformat(),))
                deleted += cursor.rowcount

            conn.commit()
            conn.close()

            return deleted

    def export_to_csv(self, endpoint: Optional[str] = None,
                      hours: int = 24) -> str:
        """
        Export metrics to CSV format.

        Args:
            endpoint: Optional endpoint filter (if None, exports all)
            hours: Number of hours to look back

        Returns:
            CSV string with header row and data
        """
        history = self.get_history(hours=hours, endpoint=endpoint)

        csv_lines = [
            "timestamp,endpoint,request_count,error_count,"
            "latency_avg_ms,latency_p95_ms,error_rate_pct"
        ]

        for ep in sorted(history.keys()):
            for record in history[ep]:
                csv_lines.append(
                    f"{record['timestamp']},"
                    f"{ep},"
                    f"{record['request_count']},"
                    f"{record['error_count']},"
                    f"{record['latency_avg_ms']},"
                    f"{record['latency_p95_ms']},"
                    f"{record['error_rate_pct']}"
                )

        return "\n".join(csv_lines)

    def export_to_json(self, endpoint: Optional[str] = None,
                       hours: int = 24) -> Dict:
        """
        Export metrics to JSON format.

        Args:
            endpoint: Optional endpoint filter (if None, exports all)
            hours: Number of hours to look back

        Returns:
            Dict with metadata and metrics array
        """
        history = self.get_history(hours=hours, endpoint=endpoint)

        return {
            "export_metadata": {
                "export_timestamp": datetime.utcnow().isoformat(),
                "period_hours": hours,
                "endpoint_filter": endpoint,
                "total_records": sum(len(records) for records
                                     in history.values())
            },
            "metrics": history
        }

    def export_summary_report(self, hours: int = 24) -> str:
        """
        Export a summary report in HTML format with statistics.

        Args:
            hours: Number of hours to look back

        Returns:
            HTML string with summary table and key metrics
        """
        history = self.get_history(hours=hours)

        if not history:
            return ("<html><body><p>No metrics data available</p>"
                    "</body></html>")

        # Calculate summary statistics
        total_requests = 0
        total_errors = 0
        avg_latency_values = []
        p95_latency_values = []
        error_rates = []

        for endpoint_records in history.values():
            for record in endpoint_records:
                total_requests += record.get("request_count", 0)
                total_errors += record.get("error_count", 0)
                if record.get("latency_avg_ms") is not None:
                    avg_latency_values.append(record["latency_avg_ms"])
                if record.get("latency_p95_ms") is not None:
                    p95_latency_values.append(record["latency_p95_ms"])
                if record.get("error_rate_pct") is not None:
                    error_rates.append(record["error_rate_pct"])

        avg_latency = (sum(avg_latency_values) / len(avg_latency_values)
                       if avg_latency_values else 0)
        avg_p95_latency = (sum(p95_latency_values) /
                           len(p95_latency_values)
                           if p95_latency_values else 0)
        avg_error_rate = (sum(error_rates) / len(error_rates)
                          if error_rates else 0)

        # Build HTML report
        html = f"""<html>
<head>
    <title>Metrics Export Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .summary {{ background-color: #f0f0f0; padding: 15px;
                   border-radius: 5px; margin-bottom: 20px; }}
        .metric {{ display: inline-block; margin-right: 30px; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #333; }}
        .metric-label {{ font-size: 12px; color: #666; }}
        table {{ border-collapse: collapse; width: 100%;
                margin-top: 20px; }}
        th {{ background-color: #4CAF50; color: white; padding: 10px;
             text-align: left; }}
        td {{ border: 1px solid #ddd; padding: 8px; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        tr:hover {{ background-color: #f5f5f5; }}
    </style>
</head>
<body>
    <h1>Metrics Export Report</h1>
    <p>Generated: {datetime.utcnow().isoformat()}</p>
    <p>Period: Last {hours} hours</p>

    <div class="summary">
        <h2>Summary Statistics</h2>
        <div class="metric">
            <div class="metric-value">{total_requests}</div>
            <div class="metric-label">Total Requests</div>
        </div>
        <div class="metric">
            <div class="metric-value">{total_errors}</div>
            <div class="metric-label">Total Errors</div>
        </div>
        <div class="metric">
            <div class="metric-value">{avg_error_rate:.2f}%</div>
            <div class="metric-label">Avg Error Rate</div>
        </div>
        <div class="metric">
            <div class="metric-value">{avg_latency:.2f}ms</div>
            <div class="metric-label">Avg Latency</div>
        </div>
        <div class="metric">
            <div class="metric-value">{avg_p95_latency:.2f}ms</div>
            <div class="metric-label">Avg P95 Latency</div>
        </div>
    </div>

    <h2>Per-Endpoint Metrics</h2>
    <table>
        <thead>
            <tr>
                <th>Endpoint</th>
                <th>Requests</th>
                <th>Errors</th>
                <th>Error Rate %</th>
                <th>Avg Latency (ms)</th>
                <th>P95 Latency (ms)</th>
            </tr>
        </thead>
        <tbody>
"""

        for endpoint in sorted(history.keys()):
            records = history[endpoint]
            if records:
                latest = records[-1]  # Most recent record
                html += f"""            <tr>
                <td>{endpoint}</td>
                <td>{latest.get('request_count', 0)}</td>
                <td>{latest.get('error_count', 0)}</td>
                <td>{latest.get('error_rate_pct', 0):.2f}%</td>
                <td>{latest.get('latency_avg_ms', 0):.2f}</td>
                <td>{latest.get('latency_p95_ms', 0):.2f}</td>
            </tr>
"""

        html += """        </tbody>
    </table>
</body>
</html>
"""

        return html
