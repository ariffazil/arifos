"""Contract tests for core tool schema and adapter alias profile."""

from __future__ import annotations

import ast
from pathlib import Path

import yaml

from aaa_mcp.protocol.aaa_contract import AAA_CANONICAL_TOOLS

ROOT = Path(__file__).resolve().parents[2]
TOOLS_SCHEMA = ROOT / "core_mcp" / "schemas" / "tools.yaml"
ALIAS_SCHEMA = ROOT / "adapters" / "openai_apps" / "alias_map.yaml"
SERVER_FILE = ROOT / "arifos_aaa_mcp" / "server.py"


def _load_yaml(path: Path) -> dict:
    assert path.exists(), f"Missing schema file: {path}"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), f"Schema must be object: {path}"
    return data


def _tool_names_in_server() -> set[str]:
    module = ast.parse(SERVER_FILE.read_text(encoding="utf-8"))
    names: set[str] = set()

    for node in ast.walk(module):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for deco in node.decorator_list:
            if not isinstance(deco, ast.Call):
                continue
            func = deco.func
            if not isinstance(func, ast.Attribute):
                continue
            if not isinstance(func.value, ast.Name) or func.value.id != "mcp":
                continue
            if func.attr != "tool":
                continue

            explicit_name = None
            for kw in deco.keywords:
                if kw.arg == "name" and isinstance(kw.value, ast.Constant):
                    if isinstance(kw.value.value, str):
                        explicit_name = kw.value.value
                        break
            names.add(explicit_name or node.name)

    return names


def test_tools_yaml_matches_canonical_and_aux_contract() -> None:
    payload = _load_yaml(TOOLS_SCHEMA)

    canonical = payload.get("canonical_tools")
    auxiliary = payload.get("auxiliary_tools")

    assert isinstance(canonical, list)
    assert isinstance(auxiliary, list)
    assert len(canonical) == 13
    assert len(auxiliary) == 2

    canonical_names = {item["name"] for item in canonical}
    auxiliary_names = {item["name"] for item in auxiliary}

    assert canonical_names == set(AAA_CANONICAL_TOOLS)
    assert auxiliary_names == {"visualize_governance", "metabolic_loop"}


def test_schema_tools_exist_in_current_server_registration() -> None:
    payload = _load_yaml(TOOLS_SCHEMA)

    expected = {*(item["name"] for item in payload["canonical_tools"])}
    for item in payload["auxiliary_tools"]:
        exposure = item.get("exposure")
        # Aux tools can be exposed via adapter resources rather than direct MCP tool registration.
        if exposure in {"internal_preferred", "resource_preferred"}:
            continue
        expected.add(item["name"])
    registered = _tool_names_in_server()

    missing = expected - registered
    assert not missing, f"Tools in schema but not registered: {sorted(missing)}"


def test_openai_alias_public_default_maps_to_unique_canonical_tools() -> None:
    tools_payload = _load_yaml(TOOLS_SCHEMA)
    alias_payload = _load_yaml(ALIAS_SCHEMA)

    canonical_names = {
        *(item["name"] for item in tools_payload["canonical_tools"]),
        *(item["name"] for item in tools_payload["auxiliary_tools"]),
    }

    openai_to_canonical = alias_payload["openai_to_canonical"]
    public_default = alias_payload["exposure_policy"]["public_default"]

    mapped = [openai_to_canonical[name] for name in public_default]
    assert len(mapped) == len(set(mapped)), "public_default aliases must map 1:1"

    for target in mapped:
        assert target in canonical_names, f"Alias maps to unknown canonical tool: {target}"

    assert alias_payload["openai_to_canonical"]["search"] == "search_reality"
    assert alias_payload["openai_to_canonical"]["fetch"] == "fetch_content"
    assert alias_payload["openai_to_canonical"]["health_check"] == "check_vital"
