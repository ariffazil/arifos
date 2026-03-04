from __future__ import annotations

from importlib import import_module
from typing import Any

# F12: Hard allowlist — only canonical 13 MCP tools may be resolved
_ALLOWED_TOOLS: frozenset[str] = frozenset({
    "anchor_session",
    "reason_mind",
    "recall_memory",
    "simulate_heart",
    "critique_thought",
    "eureka_forge",
    "apex_judge",
    "seal_vault",
    "search_reality",
    "fetch_content",
    "inspect_file",
    "audit_rules",
    "check_vital",
})


def get_tool_adapter(name: str) -> Any:
    if name not in _ALLOWED_TOOLS:
        raise ValueError(f"F12: Tool '{name}' not in allowlist — access denied")
    module = import_module("aaa_mcp.server")
    tool = getattr(module, name)
    return getattr(tool, "fn", tool)
