from __future__ import annotations

import ast
from pathlib import Path

from arifosmcp.transport.protocol.aaa_contract import AAA_CANONICAL_TOOLS
from arifosmcp.transport.protocol.schemas import CANONICAL_TOOL_INPUT_SCHEMAS


CANONICAL_TO_RUNTIME_FN = {
    "anchor_session": "_init_session",
    "reason_mind": "_agi_cognition",
    "vector_memory": "_phoenix_recall",
    "simulate_heart": "_asi_empathy",
    "critique_thought": "_critique_thought",
    "apex_judge": "_apex_verdict",
    "eureka_forge": "_sovereign_actuator",
    "seal_vault": "_vault_seal",
    "search_reality": "_search",
    "ingest_evidence": "_ingest_evidence",
    "audit_rules": "_system_audit",
    "check_vital": "_check_vital",
    "metabolic_loop": "_metabolic_loop",
}

_SERVER_PATH = Path(__file__).resolve().parents[2] / "arifosmcp" / "transport" / "server.py"
_SERVER_AST = ast.parse(_SERVER_PATH.read_text(encoding="utf-8"))
_FUNC_NODES = {
    node.name: node
    for node in _SERVER_AST.body
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
}


def _function_node(tool_name: str) -> ast.FunctionDef | ast.AsyncFunctionDef:
    fn_name = CANONICAL_TO_RUNTIME_FN[tool_name]
    assert fn_name in _FUNC_NODES, f"Runtime function {fn_name} not found"
    return _FUNC_NODES[fn_name]


def _runtime_param_names(tool_name: str) -> list[str]:
    fn = _function_node(tool_name)
    return [arg.arg for arg in fn.args.args] + [arg.arg for arg in fn.args.kwonlyargs]


def _runtime_required_param_names(tool_name: str) -> list[str]:
    fn = _function_node(tool_name)
    required: list[str] = []

    # Positional-or-keyword args: defaults apply to the last N args.
    pos_args = fn.args.args
    pos_defaults = fn.args.defaults
    required_pos_count = len(pos_args) - len(pos_defaults)
    required.extend(arg.arg for arg in pos_args[:required_pos_count])

    # Keyword-only args: defaults aligned one-to-one in kw_defaults.
    for kw_arg, kw_default in zip(fn.args.kwonlyargs, fn.args.kw_defaults):
        if kw_default is None:
            required.append(kw_arg.arg)

    return required


def test_canonical_schema_covers_full_runtime_signature() -> None:
    for tool_name in AAA_CANONICAL_TOOLS:
        schema = CANONICAL_TOOL_INPUT_SCHEMAS[tool_name]
        schema_props = set(schema.get("properties", {}).keys())
        runtime_params = set(_runtime_param_names(tool_name))
        assert runtime_params.issubset(
            schema_props
        ), f"Schema for {tool_name} missing params: {sorted(runtime_params - schema_props)}"


def test_canonical_schema_required_matches_runtime_required() -> None:
    for tool_name in AAA_CANONICAL_TOOLS:
        schema = CANONICAL_TOOL_INPUT_SCHEMAS[tool_name]
        schema_required = set(schema.get("required", []))
        runtime_required = set(_runtime_required_param_names(tool_name))
        assert runtime_required.issubset(schema_required), (
            f"Schema required mismatch for {tool_name}; "
            f"missing required fields: {sorted(runtime_required - schema_required)}"
        )
