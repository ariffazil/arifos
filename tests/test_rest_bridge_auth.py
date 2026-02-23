from __future__ import annotations

from starlette.testclient import TestClient

import aaa_mcp.rest as rest


async def _noop() -> dict:
    return {"ok": True}


def test_rest_bridge_requires_bearer_when_configured(monkeypatch) -> None:
    monkeypatch.setenv("ARIFOS_API_KEY", "dev-token")
    monkeypatch.delenv("ARIFOS_DEV_MODE", raising=False)

    rest.TOOLS["noop"] = _noop

    client = TestClient(rest.app)
    r = client.post("/mcp", json={"tool": "noop", "arguments": {}})
    assert r.status_code == 401
    assert r.json().get("error") == "invalid_request"


def test_rest_bridge_accepts_valid_bearer(monkeypatch) -> None:
    monkeypatch.setenv("ARIFOS_API_KEY", "dev-token")
    monkeypatch.delenv("ARIFOS_DEV_MODE", raising=False)

    rest.TOOLS["noop"] = _noop

    client = TestClient(rest.app)
    r = client.post(
        "/mcp",
        json={"tool": "noop", "arguments": {}},
        headers={"Authorization": "Bearer dev-token"},
    )
    assert r.status_code == 200
    assert r.json()["status"] == "success"
    assert r.json()["tool"] == "noop"


def test_rest_bridge_dev_mode_bypasses_auth(monkeypatch) -> None:
    monkeypatch.setenv("ARIFOS_API_KEY", "dev-token")
    monkeypatch.setenv("ARIFOS_DEV_MODE", "true")

    client = TestClient(rest.app)
    r = client.get("/tools")
    assert r.status_code == 200
