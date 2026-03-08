from __future__ import annotations

import os
from starlette.testclient import TestClient

from arifos_aaa_mcp.server import create_aaa_mcp_server


def test_rest_bridge_requires_bearer_when_configured(monkeypatch) -> None:
    monkeypatch.setenv("ARIFOS_API_KEY", "dev-token")
    monkeypatch.delenv("ARIFOS_DEV_MODE", raising=False)

    mcp = create_aaa_mcp_server()
    client = TestClient(mcp.http_app())

    r = client.get("/tools")
    assert r.status_code == 401
    assert r.json().get("error") == "invalid_request"

    r = client.post("/tools/reason_mind", json={"query": "test", "session_id": "req-123"})
    assert r.status_code == 401
    assert r.json().get("error") == "invalid_request"


def test_rest_bridge_accepts_valid_bearer(monkeypatch) -> None:
    monkeypatch.setenv("ARIFOS_API_KEY", "dev-token")
    monkeypatch.delenv("ARIFOS_DEV_MODE", raising=False)

    mcp = create_aaa_mcp_server()
    # Mocking out the tool isn't strictly necessary as we can just assert a different error
    # but let's test a valid hit that fails missing params vs missing auth

    client = TestClient(mcp.http_app())
    r = client.post(
        "/tools/reason_mind",
        json={"query": "test"},
        headers={"Authorization": "Bearer dev-token"},
    )
    # The tool returns 500 or 400 for missing args, not 401. Let's just check /tools
    assert r.status_code != 401

    r2 = client.get("/tools", headers={"Authorization": "Bearer dev-token"})
    assert r2.status_code == 200
    assert "tools" in r2.json()


def test_rest_bridge_dev_mode_bypasses_auth(monkeypatch) -> None:
    monkeypatch.setenv("ARIFOS_API_KEY", "dev-token")
    monkeypatch.setenv("ARIFOS_DEV_MODE", "true")

    mcp = create_aaa_mcp_server()
    client = TestClient(mcp.http_app())

    r = client.get("/tools")
    assert r.status_code == 200
    assert "tools" in r.json()
