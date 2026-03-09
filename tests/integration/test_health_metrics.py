import pytest
from starlette.testclient import TestClient

from arifosmcp.transport.infrastructure.monitoring import init_monitoring
from arifosmcp.transport.rest import app as rest_app
from arifosmcp.transport.streamable_http_server import app as streamable_app


@pytest.fixture(autouse=True)
async def setup_monitoring():
    await init_monitoring()


def test_rest_health_governance_metrics():
    """Verify that rest.py health endpoint returns governance metrics."""
    client = TestClient(rest_app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "governance_metrics" in data
    assert "avg_genius_g" in data["governance_metrics"]
    assert "avg_landauer_risk" in data["governance_metrics"]
    assert "avg_vault_lag_ms" in data["governance_metrics"]
    assert "health_checks" in data
    assert "postgres" in data["health_checks"]


def test_streamable_health_governance_metrics():
    """Verify that streamable_http_server.py health endpoint returns governance metrics."""
    client = TestClient(streamable_app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "governance_metrics" in data
    assert "avg_landauer_risk" in data["governance_metrics"]
    assert "health_checks" in data
    assert "redis" in data["health_checks"]


def test_metrics_endpoint_aggregation():
    """Verify that the /metrics endpoint returns basic telemetry counters."""
    client = TestClient(rest_app)
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "requests_total" in data
    assert "errors" in data


def test_rest_bridge_rejects_mcp_transport_path():
    """The legacy REST bridge must not impersonate a compliant MCP endpoint."""
    client = TestClient(rest_app)
    response = client.get("/mcp")
    assert response.status_code == 410
    data = response.json()
    assert data["error"] == "deprecated_transport_surface"
    assert data["recommended_endpoint"] == "/mcp"
