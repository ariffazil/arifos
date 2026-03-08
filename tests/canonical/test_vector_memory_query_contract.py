"""Contract guard: vector_memory input must stay on `query` (not legacy names)."""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

from aaa_mcp.protocol.schemas import get_input_schema
from arifos_aaa_mcp.server import vector_memory


ROOT = Path(__file__).resolve().parents[2]
REST_FILE = ROOT / "aaa_mcp" / "rest.py"


def _load_rest_tool_schemas() -> dict[str, dict]:
    module = ast.parse(REST_FILE.read_text(encoding="utf-8"))
    for node in module.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "TOOL_SCHEMAS":
                return ast.literal_eval(node.value)
    raise AssertionError("TOOL_SCHEMAS not found in aaa_mcp/rest.py")


def test_runtime_signature_uses_query_only() -> None:
    params = list(inspect.signature(vector_memory).parameters.keys())
    assert "query" in params
    assert "current_thought_vector" not in params


def test_protocol_schema_uses_query_only() -> None:
    schema = get_input_schema("vector_memory")
    assert schema is not None
    properties = schema.get("properties", {})
    assert "query" in properties
    assert "current_thought_vector" not in properties


def test_rest_schema_uses_query_only() -> None:
    schemas = _load_rest_tool_schemas()
    vector_args = schemas["vector_memory"]["args"]
    assert "query" in vector_args
    assert "current_thought_vector" not in vector_args
