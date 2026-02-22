"""Single source of truth for legacy/canonical protocol tool naming.

Internal protocol graph/schemas still use legacy stage-oriented names.
Public MCP surface uses canonical 5-organ names.
"""

from __future__ import annotations

from typing import Dict

# Internal protocol names used across tool_graph/schemas/capabilities.
LEGACY_TOOL_NAMES = {
    "init_gate",
    "agi_sense",
    "agi_think",
    "agi_reason",
    "asi_empathize",
    "asi_align",
    "apex_verdict",
    "vault_seal",
    "reality_search",
    "trinity_forge",
    "tool_router",
    "vault_query",
    "truth_audit",
    "simulate_transfer",
}

# Public canonical names from aaa_mcp.server.
CANONICAL_PUBLIC_TO_LEGACY: Dict[str, str] = {
    "init_session": "init_gate",
    "agi_cognition": "agi_reason",
    "asi_empathy": "asi_empathize",
    "apex_verdict": "apex_verdict",
    "vault_seal": "vault_seal",
    "search": "reality_search",
}

# Verb aliases used by legacy clients.
MCP_VERB_TO_LEGACY: Dict[str, str] = {
    "anchor": "init_gate",
    "reason": "agi_think",
    "integrate": "agi_reason",
    "respond": "agi_reason",
    "validate": "asi_empathize",
    "align": "asi_align",
    "forge": "apex_verdict",
    "audit": "apex_verdict",
    "seal": "vault_seal",
}

# Reverse map for observability/reporting where needed.
LEGACY_TO_CANONICAL_PUBLIC: Dict[str, str] = {
    v: k for k, v in CANONICAL_PUBLIC_TO_LEGACY.items()
}


def resolve_protocol_tool_name(name: str) -> str:
    """Normalize tool identifier to legacy protocol key."""
    if name in LEGACY_TOOL_NAMES:
        return name
    if name in CANONICAL_PUBLIC_TO_LEGACY:
        return CANONICAL_PUBLIC_TO_LEGACY[name]
    return MCP_VERB_TO_LEGACY.get(name, name)


__all__ = [
    "CANONICAL_PUBLIC_TO_LEGACY",
    "LEGACY_TO_CANONICAL_PUBLIC",
    "MCP_VERB_TO_LEGACY",
    "LEGACY_TOOL_NAMES",
    "resolve_protocol_tool_name",
]
