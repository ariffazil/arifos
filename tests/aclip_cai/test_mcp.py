"""
tests/aclip_cai/test_mcp.py — Integration Tests for 9 System Calls
"""

import pytest
from fastapi.testclient import TestClient
from aclip_cai.core.mcp_server import app

client = TestClient(app)

def test_syscall_anchor():
    payload = {
        "name": "anchor",
        "arguments": {"user_id": "arif", "context": "testing"},
        "session_id": "test-sess-001"
    }
    response = client.post("/mcp/anchor", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "SEAL"
    assert data["result"]["session_id"] == "test-sess-001"

def test_syscall_reason():
    payload = {
        "name": "reason",
        "arguments": {"query": "is 2+2=4?"},
        "session_id": "test-sess-001"
    }
    response = client.post("/mcp/reason", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "SEAL"
    assert "analysis" in data["result"]

def test_syscall_validate():
    payload = {
        "name": "validate",
        "arguments": {"content": "rm -rf /", "severity": "high"},
        "session_id": "test-sess-001"
    }
    response = client.post("/mcp/validate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "VOID"
    assert data["result"]["validated"] is False

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
