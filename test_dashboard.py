"""
Pruebas básicas para validar el dashboard HTML
"""
from pathlib import Path
import pytest


def test_dashboard_file_exists():
    """Verifica que el archivo dashboard.html existe"""
    dashboard_path = Path(__file__).parent / "dashboard.html"
    assert dashboard_path.exists(), "dashboard.html no encontrado"


def test_dashboard_has_required_html_elements():
    """Verifica que el HTML tenga elementos básicos"""
    dashboard_path = Path(__file__).parent / "dashboard.html"
    with open(dashboard_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Verificar elementos HTML
    assert "<!DOCTYPE html>" in html
    assert "<title>Revista Expats - API Metrics Dashboard</title>" in html
    assert "id=\"lastUpdate\"" in html
    assert "id=\"totalRequests\"" in html
    assert "id=\"agentBars\"" in html
    assert "id=\"alertsContainer\"" in html
    assert "id=\"endpointsContainer\"" in html
    assert "id=\"exportFormat\"" in html
    assert "id=\"exportEndpoint\"" in html
    assert "id=\"exportHours\"" in html
    assert "id=\"exportPreview\"" in html


def test_dashboard_has_js_functions():
    """Verifica que el HTML tenga las funciones JavaScript necesarias"""
    dashboard_path = Path(__file__).parent / "dashboard.html"
    with open(dashboard_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Verificar funciones clave
    assert "async function fetchMetrics()" in html
    assert "function updateSummary(metrics)" in html
    assert "function updateAgents(metrics)" in html
    assert "function updateAlerts(metrics)" in html
    assert "function updateEndpoints(metrics)" in html
    assert "function refreshMetrics()" in html
    assert "function updateTimestamp()" in html
    assert "function updateExportEndpointOptions(metrics)" in html
    assert "function buildExportQuery(formatOverride = null)" in html
    assert "async function downloadMetricsExport()" in html
    assert "async function previewMetricsExport()" in html


def test_dashboard_api_integration():
    """Verifica que el HTML haga fetch a los endpoints correctos"""
    dashboard_path = Path(__file__).parent / "dashboard.html"
    with open(dashboard_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Verificar que hace fetch a /api/metrics
    assert "fetch('/api/metrics')" in html
    assert "fetch(`/api/export/metrics?${params.toString()}`)" in html

    # Verificar parámetros de refresh
    assert "REFRESH_INTERVAL = 5000" in html  # 5 segundos


def test_dashboard_has_styling():
    """Verifica que el dashboard tenga estilos CSS"""
    dashboard_path = Path(__file__).parent / "dashboard.html"
    with open(dashboard_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Verificar clases CSS en estilos
    assert ".card {" in html
    assert ".endpoint-table {" in html
    assert ".alert-box {" in html
    assert ".metric-pill {" in html
    assert ".export-controls {" in html
    assert ".export-preview {" in html


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
