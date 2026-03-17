import json
from arifosmcp.runtime.public_registry import build_server_json, build_mcp_manifest
from pathlib import Path

ROOT = Path("c:/arifosmcp")
spec_dir = ROOT / "spec"

server_json = build_server_json()
(spec_dir / "server.json").write_text(json.dumps(server_json, indent=2), encoding="utf-8")

manifest_json = build_mcp_manifest()
(spec_dir / "mcp-manifest.json").write_text(json.dumps(manifest_json, indent=2), encoding="utf-8")

print("Updated spec files.")
