"""Contract tests for FastMCP dev/prod profile files."""

from __future__ import annotations

import json
from pathlib import Path


def _load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_profile_files_exist() -> None:
    assert Path("dev.fastmcp.json").exists()
    assert Path("prod.fastmcp.json").exists()


def test_profiles_pin_fastmcp_exact_version() -> None:
    for file_name in ("fastmcp.json", "dev.fastmcp.json", "prod.fastmcp.json"):
        config = _load(file_name)
        deps = config.get("environment", {}).get("dependencies", [])
        assert "fastmcp==3.0.2" in deps


def test_dev_and_prod_transports() -> None:
    dev = _load("dev.fastmcp.json")
    prod = _load("prod.fastmcp.json")

    assert dev.get("deployment", {}).get("transport") == "stdio"
    assert dev.get("deployment", {}).get("log_level") == "DEBUG"

    assert prod.get("deployment", {}).get("transport") == "http"
    assert prod.get("deployment", {}).get("path") == "/mcp/"
