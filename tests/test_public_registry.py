from __future__ import annotations

import json
from pathlib import Path

from arifosmcp.runtime.public_registry import build_mcp_manifest, build_server_json

ROOT = Path(__file__).resolve().parents[1]


def test_server_json_matches_registry() -> None:
    server_json = json.loads((ROOT / "spec" / "server.json").read_text(encoding="utf-8"))
    assert server_json == build_server_json()


def test_mcp_manifest_matches_registry() -> None:
    manifest_json = json.loads((ROOT / "spec" / "mcp-manifest.json").read_text(encoding="utf-8"))
    assert manifest_json == build_mcp_manifest()
