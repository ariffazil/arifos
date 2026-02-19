import pytest
from aaa_mcp.rest import app as rest_app
from aaa_mcp.streamable_http_server import app as streamable_app
from aaa_mcp.infrastructure.monitoring import init_monitoring
from starlette.testclient import TestClient


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
    """Verify that the /metrics endpoint aggregates internal and global stats."""
    client = TestClient(rest_app)
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "governance_stats" in data
    assert "legacy_stats" in data
    assert "avg_latency_ms" in data
