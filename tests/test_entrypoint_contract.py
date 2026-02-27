"""Entrypoint and transport contract tests for aaa_mcp."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


class _StubMCP:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def run(self, **kwargs: Any) -> None:
        self.calls.append(kwargs)


def _run_cli_mode(monkeypatch, mode: str) -> _StubMCP:
    import aaa_mcp.__main__ as cli

    stub = _StubMCP()
    monkeypatch.setattr(cli, "check_fastmcp_version", lambda: 2)
    monkeypatch.setattr("arifos_aaa_mcp.server.create_aaa_mcp_server", lambda: stub)
    monkeypatch.setattr(sys, "argv", ["aaa_mcp", mode])
    cli.main()
    return stub


def test_cli_modes_use_public_constructor_and_transport(monkeypatch) -> None:
    stub_stdio = _run_cli_mode(monkeypatch, "stdio")
    assert stub_stdio.calls[-1]["transport"] == "stdio"

    stub_sse = _run_cli_mode(monkeypatch, "sse")
    assert stub_sse.calls[-1]["transport"] == "sse"

    stub_http = _run_cli_mode(monkeypatch, "http")
    assert stub_http.calls[-1]["transport"] == "http"


def test_cli_default_mode_is_sse(monkeypatch) -> None:
    import aaa_mcp.__main__ as cli

    stub = _StubMCP()
    monkeypatch.setattr(cli, "check_fastmcp_version", lambda: 2)
    monkeypatch.setattr("arifos_aaa_mcp.server.create_aaa_mcp_server", lambda: stub)
    monkeypatch.setattr(sys, "argv", ["aaa_mcp"])
    cli.main()

    assert stub.calls[-1]["transport"] == "sse"


def test_rest_mode_dispatches_to_rest_main(monkeypatch) -> None:
    import aaa_mcp.__main__ as cli

    called = {"rest": False}
    stub = _StubMCP()
    monkeypatch.setattr(cli, "check_fastmcp_version", lambda: 2)
    monkeypatch.setattr("arifos_aaa_mcp.server.create_aaa_mcp_server", lambda: stub)
    monkeypatch.setattr("aaa_mcp.rest.main", lambda: called.__setitem__("rest", True))
    monkeypatch.setattr(sys, "argv", ["aaa_mcp", "rest"])

    cli.main()

    assert called["rest"] is True


def test_unknown_mode_exits_with_code_2(monkeypatch) -> None:
    import aaa_mcp.__main__ as cli

    monkeypatch.setattr(cli, "check_fastmcp_version", lambda: 2)
    monkeypatch.setattr("arifos_aaa_mcp.server.create_aaa_mcp_server", lambda: _StubMCP())
    monkeypatch.setattr(sys, "argv", ["aaa_mcp", "bogus-mode"])

    try:
        cli.main()
        raise AssertionError("Expected SystemExit for unknown mode")
    except SystemExit as exc:
        assert exc.code == 2


def test_rest_aliases_map_legacy_names_to_public_canon() -> None:
    from aaa_mcp.rest import TOOL_ALIASES, TOOLS

    canonical = {
        "anchor_session",
        "reason_mind",
        "recall_memory",
        "simulate_heart",
        "critique_thought",
        "apex_judge",
        "eureka_forge",
        "seal_vault",
        "search_reality",
        "fetch_content",
        "inspect_file",
        "audit_rules",
        "check_vital",
    }
    assert canonical.issubset(set(TOOLS.keys()))
    assert TOOL_ALIASES["anchor"] == "anchor_session"
    assert TOOL_ALIASES["reason"] == "reason_mind"
    assert TOOL_ALIASES["validate"] == "simulate_heart"
    assert TOOL_ALIASES["audit"] == "apex_judge"
    assert TOOL_ALIASES["judge_soul"] == "apex_judge"
    assert TOOL_ALIASES["seal"] == "seal_vault"


def test_server_constructor_returns_fastmcp_instance() -> None:
    from aaa_mcp.server import create_unified_mcp_server

    mcp = create_unified_mcp_server()
    assert hasattr(mcp, "run")


def test_dockerfile_uses_public_http_entrypoint() -> None:
    dockerfile = Path("Dockerfile").read_text(encoding="utf-8")
    assert "FROM python:3.12-slim AS build" in dockerfile
    assert "FROM python:3.12-slim AS runtime" in dockerfile
    assert 'CMD ["python", "-m", "arifos_aaa_mcp", "http"]' in dockerfile
