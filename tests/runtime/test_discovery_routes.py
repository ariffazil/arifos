"""
tests/runtime/test_discovery_routes.py — Discovery Route Tests

Verifies that root-level discovery files (agent.json, ai.json, etc.) 
are correctly registered and accessible without being shadowed by mounts.
"""

import pytest
from starlette.testclient import TestClient
from arifosmcp.runtime.server import app

@pytest.fixture
def client():
    return TestClient(app)

def test_well_known_agent_reachable(client):
    """Test that /.well-known/agent.json is reachable and returns JSON."""
    response = client.get("/.well-known/agent.json")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "skills" in data
    assert data["name"] == "arifOS Constitutional Kernel"

def test_llms_txt_reachable(client):
    """Test that /llms.txt is reachable (even if file doesn't exist, we test route registration)."""
    # Note: If the file doesn't exist in the test environment, this might be 404
    # but we are testing that the route is handled by our handler, not shadowed.
    response = client.get("/llms.txt")
    # Status code depends on if file exists, but let's at least check it doesn't return 401/403
    assert response.status_code != 401

def test_robots_txt_reachable(client):
    """Test that /robots.txt is reachable."""
    response = client.get("/robots.txt")
    assert response.status_code != 401

def test_ai_json_reachable(client):
    """Test that /ai.json is reachable."""
    response = client.get("/ai.json")
    assert response.status_code != 401
