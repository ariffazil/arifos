"""Contract tests for root `server.py` entrypoint hardening."""

from __future__ import annotations

from typing import Any

import server


class _StubMCP:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def run(self, **kwargs: Any) -> None:
        self.calls.append(kwargs)


def test_normalize_mode_falls_back_to_default_for_invalid_value() -> None:
    assert server._normalize_mode("invalid-mode") == "sse"


def test_safe_env_port_falls_back_for_non_numeric(monkeypatch) -> None:
    monkeypatch.setenv("PORT", "not-a-port")
    assert server._safe_env_port() == 8080


def test_main_stdio_uses_stdio_transport(monkeypatch) -> None:
    stub = _StubMCP()
    monkeypatch.setattr("aaa_mcp.server.create_unified_mcp_server", lambda: stub)

    server.main(["--mode", "stdio"])

    assert stub.calls[-1] == {"transport": "stdio"}


def test_main_rest_sets_host_port_and_dispatches(monkeypatch) -> None:
    called = {"rest": False}
    monkeypatch.setattr("aaa_mcp.rest.main", lambda: called.__setitem__("rest", True))

    server.main(["--mode", "rest", "--host", "127.0.0.1", "--port", "9090"])

    assert called["rest"] is True


def test_main_rejects_out_of_range_port() -> None:
    try:
        server.main(["--mode", "sse", "--port", "70000"])
        raise AssertionError("Expected SystemExit for invalid port")
    except SystemExit as exc:
        assert "invalid port" in str(exc)
