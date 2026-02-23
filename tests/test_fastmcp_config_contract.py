"""Contract tests for FastMCP declarative project configuration."""

from __future__ import annotations

import json
from pathlib import Path


def test_fastmcp_json_exists_and_is_valid_json() -> None:
    config_path = Path("fastmcp.json")
    assert config_path.exists(), "fastmcp.json is required for portable FastMCP execution"

    config = json.loads(config_path.read_text(encoding="utf-8"))
    assert isinstance(config, dict)
    assert config.get("$schema", "").startswith("https://gofastmcp.com/public/schemas/fastmcp.json/")


def test_fastmcp_json_has_required_sections() -> None:
    config = json.loads(Path("fastmcp.json").read_text(encoding="utf-8"))

    source = config.get("source", {})
    assert source.get("type") == "filesystem"
    assert source.get("path") == "arifos_aaa_mcp/server.py"
    assert source.get("entrypoint") == "mcp"

    deployment = config.get("deployment", {})
    assert deployment.get("transport") == "http"
    assert deployment.get("path") == "/mcp/"
    assert int(deployment.get("port")) == 8080


def test_fastmcp_source_entrypoint_is_importable() -> None:
    from arifos_aaa_mcp.server import mcp

    assert hasattr(mcp, "run")
