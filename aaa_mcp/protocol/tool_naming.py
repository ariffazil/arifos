"""Single source of truth for legacy/canonical protocol tool naming.

Internal protocol graph/schemas still use legacy stage-oriented names.
Public MCP surface uses canonical UX verb names (13-tool surface).

Three naming generations exist:
  1. Legacy protocol: init_gate, agi_sense, agi_reason, asi_empathize, ...
  2. Mid-gen kernel:  init_session, agi_cognition, asi_empathy, apex_verdict, ...
  3. Canonical UX:    anchor_session, reason_mind, simulate_heart, judge_soul, ...

All public APIs should use generation 3. Generations 1-2 are internal/compat only.
"""

from __future__ import annotations

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
    "phoenix_recall",
    "sovereign_actuator",
    "fetch",
    "analyze",
    "system_audit",
    "sense_health",
    "sense_fs",
}

# Canonical UX names → legacy protocol names (for schema lookups).
CANONICAL_PUBLIC_TO_LEGACY: dict[str, str] = {
    # Canonical UX (generation 3) → legacy protocol (generation 1)
    "anchor_session": "init_gate",
    "reason_mind": "agi_reason",
    "recall_memory": "phoenix_recall",
    "simulate_heart": "asi_empathize",
    "critique_thought": "asi_align",
    "judge_soul": "apex_verdict",
    "forge_hand": "sovereign_actuator",
    "seal_vault": "vault_seal",
    "search_reality": "reality_search",
    "fetch_content": "fetch",
    "inspect_file": "analyze",
    "audit_rules": "system_audit",
    "check_vital": "sense_health",
    # Mid-gen compat (generation 2) → legacy protocol (generation 1)
    "init_session": "init_gate",
    "agi_cognition": "agi_reason",
    "phoenix_recall": "phoenix_recall",
    "asi_empathy": "asi_empathize",
    "apex_verdict": "apex_verdict",
    "sovereign_actuator": "sovereign_actuator",
    "vault_seal": "vault_seal",
    "search": "reality_search",
    "fetch": "fetch",
    "analyze": "analyze",
    "system_audit": "system_audit",
    "sense_health": "sense_health",
    "sense_fs": "sense_fs",
}

# Legacy 9-verb aliases → legacy protocol names.
MCP_VERB_TO_LEGACY: dict[str, str] = {
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
LEGACY_TO_CANONICAL_PUBLIC: dict[str, str] = {
    v: k
    for k, v in CANONICAL_PUBLIC_TO_LEGACY.items()
    if not any(
        k == mid
        for mid in (
            "init_session",
            "agi_cognition",
            "phoenix_recall",
            "asi_empathy",
            "apex_verdict",
            "sovereign_actuator",
            "vault_seal",
            "search",
            "fetch",
            "analyze",
            "system_audit",
            "sense_health",
            "sense_fs",
        )
    )
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
