"""
arifosmcp/runtime/contracts.py — Unified arifOS MCP Contracts

Public/main contract:
  - the 11-mega-tool surface defined in arifosmcp.runtime.public_registry
"""

from __future__ import annotations
from typing import Any
from .public_registry import public_tool_names, CANONICAL_PUBLIC_TOOLS, EXPECTED_TOOL_COUNT

# ═══════════════════════════════════════════════════════════════════════════════
# 11-TOOL CONTRACT ENFORCEMENT
# ═══════════════════════════════════════════════════════════════════════════════

_import_time_names = frozenset(public_tool_names())
_expected_names = CANONICAL_PUBLIC_TOOLS

assert len(_import_time_names) == EXPECTED_TOOL_COUNT, (
    f"CRITICAL: contracts.py sees {len(_import_time_names)} tools, "
    f"expected {EXPECTED_TOOL_COUNT}. Registry drift detected!"
)
assert _import_time_names == _expected_names, (
    f"CRITICAL: Tool name mismatch in contracts.py.\n"
    f"Expected: {sorted(_expected_names)}\n"
    f"Got: {sorted(_import_time_names)}"
)

# ═══════════════════════════════════════════════════════════════════════════════
# TOOL SURFACES
# ═══════════════════════════════════════════════════════════════════════════════

AAA_PUBLIC_TOOLS: tuple[str, ...] = public_tool_names()

AAA_CANONICAL_TOOLS: tuple[str, ...] = AAA_PUBLIC_TOOLS

REQUIRES_SESSION: frozenset[str] = frozenset({
    "arifOS_kernel",
    "agi_mind",
    "asi_heart",
    "apex_soul",
    "vault_ledger",
    "engineering_memory",
    "physics_reality",
    "math_estimator",
    "code_engine",
    "architect_registry",
})

READ_ONLY_TOOLS: set[str] = {
    "physics_reality",
    "math_estimator",
    "architect_registry",
}

# ═══════════════════════════════════════════════════════════════════════════════
# GOVERNANCE METADATA
# ═══════════════════════════════════════════════════════════════════════════════

AAA_TOOL_STAGE_MAP: dict[str, str] = {
    "init_anchor": "000_INIT",
    "anchor_session": "000_INIT",
    "arifOS_kernel": "444_ROUTER",
    "metabolic_loop": "444_ROUTER",
    "apex_soul": "888_JUDGE",
    "apex_judge": "888_JUDGE",
    "vault_ledger": "999_VAULT",
    "seal_vault": "999_VAULT",
    "vault_seal": "999_VAULT",
    "agi_mind": "333_MIND",
    "reason_mind": "333_MIND",
    "agi_reason": "333_MIND",
    "asi_heart": "666_HEART",
    "asi_simulate": "666_HEART",
    "asi_critique": "666_HEART",
    "engineering_memory": "555_MEMORY",
    "physics_reality": "111_SENSE",
    "math_estimator": "444_ROUTER",
    "code_engine": "M-3_EXEC",
    "architect_registry": "M-4_ARCH",
}

TRINITY_BY_TOOL: dict[str, str] = {
    "init_anchor": "PSI Ψ",
    "arifOS_kernel": "DELTA/PSI",
    "apex_soul": "PSI Ψ",
    "vault_ledger": "PSI Ψ",
    "agi_mind": "DELTA Δ",
    "asi_heart": "OMEGA Ω",
    "engineering_memory": "OMEGA Ω",
    "physics_reality": "DELTA Δ",
    "math_estimator": "DELTA Δ",
    "code_engine": "ALL",
    "architect_registry": "DELTA Δ",
}

AAA_TOOL_ALIASES: dict[str, str] = {
    "init": "init_anchor",
    "revoke": "init_anchor",
    "kernel": "arifOS_kernel",
    "status": "arifOS_kernel",
    "judge": "apex_soul",
    "seal": "vault_ledger",
    "reason": "agi_mind",
}

# Mode definitions for 11 Mega-Tools
TOOL_MODES: dict[str, frozenset[str]] = {
    "init_anchor": frozenset({"init", "revoke", "refresh"}),
    "arifOS_kernel": frozenset({"kernel", "status"}),
    "apex_soul": frozenset({"judge", "rules", "validate", "hold", "armor", "notify"}),
    "vault_ledger": frozenset({"seal", "verify"}),
    "agi_mind": frozenset({"reason", "reflect", "forge"}),
    "asi_heart": frozenset({"critique", "simulate"}),
    "engineering_memory": frozenset({"engineer", "vector_query", "vector_store", "vector_forget", "generate", "query"}),
    "physics_reality": frozenset({"search", "ingest", "compass", "atlas"}),
    "math_estimator": frozenset({"cost", "health", "vitals"}),
    "code_engine": frozenset({"fs", "process", "net", "tail", "replay"}),
    "architect_registry": frozenset({"register", "list", "read"}),
}

# 13 Floors Mapping for Mega-Tools (Using long names for governance_engine)
AAA_TOOL_LAW_BINDINGS: dict[str, list[str]] = {
    "init_anchor": ["F11_AUTHORITY", "F12_DEFENSE", "F13_SOVEREIGNTY"],
    "arifOS_kernel": ["F4_CLARITY", "F11_AUTHORITY"],
    "apex_soul": ["F3_TRI_WITNESS", "F12_DEFENSE", "F13_SOVEREIGNTY"],
    "vault_ledger": ["F1_AMANAH", "F13_SOVEREIGNTY"],
    "agi_mind": ["F2_TRUTH", "F4_CLARITY", "F7_HUMILITY", "F8_GENIUS"],
    "asi_heart": ["F5_PEACE2", "F6_EMPATHY", "F9_ANTI_HANTU"],
    "engineering_memory": ["F11_AUTHORITY", "F2_TRUTH"],
    "physics_reality": ["F2_TRUTH", "F3_TRI_WITNESS"],
    "math_estimator": ["F4_CLARITY", "F5_PEACE2"],
    "code_engine": [],
    "architect_registry": [],
}

LAW_13_CATALOG: dict[str, dict[str, str]] = {
    "F1_AMANAH": {"name": "Amanah", "type": "floor"},
    "F2_TRUTH": {"name": "Truth", "type": "floor"},
    "F3_TRI_WITNESS": {"name": "Tri-Witness", "type": "mirror"},
    "F4_CLARITY": {"name": "Clarity", "type": "floor"},
    "F5_PEACE2": {"name": "Peace2", "type": "floor"},
    "F6_EMPATHY": {"name": "Empathy", "type": "floor"},
    "F7_HUMILITY": {"name": "Humility", "type": "floor"},
    "F8_GENIUS": {"name": "Genius", "type": "mirror"},
    "F9_ANTI_HANTU": {"name": "Dark", "type": "floor"},
    "F10_ONTOLOGY_LOCK": {"name": "Ontology", "type": "floor"},
    "F11_AUTHORITY": {"name": "Authority", "type": "floor"},
    "F12_DEFENSE": {"name": "Injection", "type": "floor"},
    "F13_SOVEREIGNTY": {"name": "Sovereign", "type": "wall"},
}

def require_session(tool: str, session_id: str | None) -> dict[str, Any] | None:
    if tool in REQUIRES_SESSION and (not session_id or not str(session_id).strip()):
        return {
            "verdict": "HOLD",
            "stage": "F11_AUTH",
            "floors_failed": ["F11"],
            "error": "Missing session_id",
            "next_actions": [
                "Call init_anchor with mode='init' first.",
            ],
        }
    return None

def public_tool_input_contracts() -> dict[str, Any]:
    """Mock for compatibility."""
    return {}



def verify_contract() -> dict[str, Any]:
    """Verify the 11-tool contract is intact."""
    checks = {
        "tool_count": len(AAA_PUBLIC_TOOLS) == 11,
        "stage_map": len(AAA_TOOL_STAGE_MAP) >= 11,
        "trinity_map": len(TRINITY_BY_TOOL) == 11,
        "mode_map": len(TOOL_MODES) == 11,
    }
    return {
        "ok": all(checks.values()),
        "checks": checks,
        "tools": list(AAA_PUBLIC_TOOLS),
    }
