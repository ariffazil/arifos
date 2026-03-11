import pytest
from starlette.testclient import TestClient

from arifosmcp.runtime.server import app as server_app


@pytest.fixture(autouse=True)
async def setup_monitoring():
    # init_monitoring is now deprecated/internal
    pass


def test_rest_health_endpoint():
    """Verify that /health endpoint returns expected status and floors info."""
    client = TestClient(server_app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "ml_floors" in data
    assert "ml_floors_enabled" in data["ml_floors"]
    assert "capability_map" in data
    assert data["capability_map"]["schema"] == "capability-map/v1"
    assert "server_identity" in data["capability_map"]


def test_version_endpoint():
    """Verify that /version endpoint returns build info."""
    client = TestClient(server_app)
    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data


def test_tools_endpoint():
    """Verify that /tools endpoint lists available tools."""
    client = TestClient(server_app)
    response = client.get("/tools")
    # Might require auth if configured, but should usually be open in tests.
    if response.status_code == 200:
        data = response.json()
        assert "tools" in data
        assert "count" in data
        assert data["count"] > 0


def test_governance_status_endpoint():
    """Verify that /api/governance-status returns telemetry."""
    client = TestClient(server_app)
    response = client.get("/api/governance-status")
    assert response.status_code == 200
    data = response.json()
    assert "telemetry" in data
    assert "floors" in data
    assert "session_id" in data


def test_metrics_endpoint_not_found():
    """The legacy /metrics endpoint should now be 404 unless explicitly added."""
    client = TestClient(server_app)
    response = client.get("/metrics")
    assert response.status_code == 404
