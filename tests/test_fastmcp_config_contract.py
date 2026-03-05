"""Contract tests: fastmcp.json configuration validity."""

from __future__ import annotations

import json
from pathlib import Path


def _load(name: str) -> dict:
    return json.loads(Path(name).read_text(encoding="utf-8"))


def test_fastmcp_json_exists() -> None:
    assert Path("fastmcp.json").exists()


def test_fastmcp_json_required_keys() -> None:
    config = _load("fastmcp.json")
    assert "source" in config, "fastmcp.json missing 'source'"
    assert "deployment" in config, "fastmcp.json missing 'deployment'"
    assert "environment" in config, "fastmcp.json missing 'environment'"


def test_fastmcp_json_source_path_exists() -> None:
    config = _load("fastmcp.json")
    source_path = config["source"]["path"]
    assert Path(source_path).exists(), f"fastmcp.json source path not found: {source_path}"


def test_fastmcp_json_pins_fastmcp_version() -> None:
    config = _load("fastmcp.json")
    deps = config.get("environment", {}).get("dependencies", [])
    pinned = [d for d in deps if d.startswith("fastmcp==")]
    assert pinned, "fastmcp.json must pin an exact fastmcp version (fastmcp==x.y.z)"


def test_fastmcp_json_http_transport() -> None:
    config = _load("fastmcp.json")
    transport = config.get("deployment", {}).get("transport")
    assert transport == "http", f"Expected transport='http', got {transport!r}"


def test_fastmcp_json_mcp_path() -> None:
    config = _load("fastmcp.json")
    path = config.get("deployment", {}).get("path")
    assert path is not None, "fastmcp.json deployment.path must be set"
    assert "mcp" in path.lower(), f"Expected path to contain 'mcp', got {path!r}"
