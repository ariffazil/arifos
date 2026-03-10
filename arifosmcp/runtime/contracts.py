"""
arifosmcp/runtime/contracts.py — Unified arifOS AAA MCP Contracts

This module is the single source of truth for the active AAA MCP public
surface, its governance metadata, and input validation guards.
"""

from __future__ import annotations

from typing import Any

# ═══════════════════════════════════════════════════════════════════════════════
# CANONICAL TOOL SURFACE (L4)
# ═══════════════════════════════════════════════════════════════════════════════

AAA_CANONICAL_TOOLS: tuple[str, ...] = (
    "anchor_session",
    "reason_mind",
    "vector_memory",
    "simulate_heart",
    "critique_thought",
    "eureka_forge",
    "apex_judge",
    "seal_vault",
    "search_reality",
    "ingest_evidence",
    "audit_rules",
    "check_vital",
    "metabolic_loop",
)

REQUIRES_SESSION: set[str] = {
    "reason_mind",
    "vector_memory",
    "simulate_heart",
    "critique_thought",
    "apex_judge",
    "eureka_forge",
    "seal_vault",
}

READ_ONLY_TOOLS: set[str] = {
    "search_reality",
    "ingest_evidence",
    "audit_rules",
    "check_vital",
}

# ═══════════════════════════════════════════════════════════════════════════════
# GOVERNANCE METADATA
# ═══════════════════════════════════════════════════════════════════════════════

AAA_TOOL_STAGE_MAP: dict[str, str] = {
    "anchor_session": "000_INIT",
    "reason_mind": "333_MIND",
    "vector_memory": "555_MEMORY",
    "simulate_heart": "666_HEART",
    "critique_thought": "666_HEART",
    "eureka_forge": "777_FORGE",
    "apex_judge": "888_JUDGE",
    "judge_soul": "888_JUDGE",
    "seal_vault": "999_VAULT",
    "search_reality": "111_SENSE",
    "ingest_evidence": "222_REALITY",
    "audit_rules": "333_MIND",
    "check_vital": "000_INIT",
    "metabolic_loop": "444_ROUTER",
}

TRINITY_BY_TOOL: dict[str, str] = {
    "anchor_session": "Delta",
    "reason_mind": "Delta",
    "vector_memory": "Omega",
    "simulate_heart": "Omega",
    "critique_thought": "Omega",
    "apex_judge": "Psi",
    "judge_soul": "Psi",
    "eureka_forge": "Psi",
    "seal_vault": "Psi",
    "search_reality": "Delta",
    "ingest_evidence": "Delta",
    "audit_rules": "Delta",
    "check_vital": "Omega",
    "metabolic_loop": "ALL",
}

LAW_13_CATALOG: dict[str, dict[str, str]] = {
    "F1_AMANAH": {"type": "floor", "threshold": "reversible"},
    "F2_TRUTH": {"type": "floor", "threshold": ">=0.99 (adaptive)"},
    "F4_CLARITY": {"type": "floor", "threshold": "dS<=0"},
    "F5_PEACE2": {"type": "floor", "threshold": ">=1.0"},
    "F6_EMPATHY": {"type": "floor", "threshold": ">=0.95"},
    "F7_HUMILITY": {"type": "floor", "threshold": "omega0 in [0.03,0.05]"},
    "F9_ANTI_HANTU": {"type": "floor", "threshold": "c_dark<0.30"},
    "F11_AUTHORITY": {"type": "floor", "threshold": "valid auth continuity"},
    "F12_DEFENSE": {"type": "floor", "threshold": "risk<0.85"},
    "F3_TRI_WITNESS": {"type": "mirror", "threshold": "cross-check present"},
    "F8_GENIUS": {"type": "mirror", "threshold": "coherence >= 0.80"},
    "F10_ONTOLOGY_LOCK": {"type": "wall", "threshold": "lock engaged"},
    "F13_SOVEREIGNTY": {"type": "wall", "threshold": "human veto preserved"},
}

AAA_TOOL_LAW_BINDINGS: dict[str, list[str]] = {
    "anchor_session": ["F11_AUTHORITY", "F12_DEFENSE", "F13_SOVEREIGNTY", "F3_TRI_WITNESS"],
    "reason_mind": ["F2_TRUTH", "F4_CLARITY", "F7_HUMILITY", "F8_GENIUS", "F3_TRI_WITNESS", "F11_AUTHORITY"],
    "vector_memory": ["F4_CLARITY", "F7_HUMILITY", "F3_TRI_WITNESS", "F13_SOVEREIGNTY", "F11_AUTHORITY"],
    "simulate_heart": ["F5_PEACE2", "F6_EMPATHY", "F4_CLARITY", "F3_TRI_WITNESS", "F11_AUTHORITY"],
    "critique_thought": ["F4_CLARITY", "F7_HUMILITY", "F8_GENIUS", "F12_DEFENSE", "F3_TRI_WITNESS", "F11_AUTHORITY"],
    "apex_judge": [
        "F1_AMANAH",
        "F2_TRUTH",
        "F3_TRI_WITNESS",
        "F8_GENIUS",
        "F9_ANTI_HANTU",
        "F10_ONTOLOGY_LOCK",
        "F11_AUTHORITY",
        "F13_SOVEREIGNTY",
    ],
    "eureka_forge": [
        "F5_PEACE2",
        "F6_EMPATHY",
        "F7_HUMILITY",
        "F9_ANTI_HANTU",
        "F13_SOVEREIGNTY",
    ],
    "seal_vault": ["F1_AMANAH", "F3_TRI_WITNESS", "F10_ONTOLOGY_LOCK", "F13_SOVEREIGNTY"],
    "search_reality": ["F2_TRUTH", "F4_CLARITY", "F12_DEFENSE"],
    "ingest_evidence": ["F1_AMANAH", "F2_TRUTH", "F4_CLARITY", "F11_AUTHORITY", "F12_DEFENSE"],
    "audit_rules": ["F2_TRUTH", "F8_GENIUS", "F10_ONTOLOGY_LOCK", "F12_DEFENSE"],
    "check_vital": ["F4_CLARITY", "F5_PEACE2", "F7_HUMILITY", "F3_TRI_WITNESS"],
    "metabolic_loop": ["F1_AMANAH", "F2_TRUTH", "F3_TRI_WITNESS", "F4_CLARITY", "F13_SOVEREIGNTY"],
}

AAA_TOOL_ALIASES: dict[str, str] = {
    "metabolicloop": "metabolic_loop",
    "init_session": "anchor_session",
    "agi_cognition": "reason_mind",
    "phoenix_recall": "vector_memory",
    "recall_memory": "vector_memory",
    "memory_search": "vector_memory",
    "asi_empathy": "simulate_heart",
    "apex_verdict": "apex_judge",
    "judge_soul": "apex_judge",
    "sovereign_actuator": "eureka_forge",
    "vault_seal": "seal_vault",
    "search": "search_reality",
    "fetch": "ingest_evidence",
    "fetch_content": "ingest_evidence",
    "inspect_file": "ingest_evidence",
    "analyze": "ingest_evidence",
    "system_audit": "audit_rules",
    "anchor": "anchor_session",
    "reason": "reason_mind",
    "integrate": "reason_mind",
    "respond": "reason_mind",
    "validate": "simulate_heart",
    "align": "simulate_heart",
    "forge": "apex_judge",
    "audit": "apex_judge",
    "seal": "seal_vault",
}

TOOL_INPUT_CONTRACTS: dict[str, dict[str, str]] = {
    "arifOS.kernel": {"query": "str"},
    "anchor_session": {"query": "str", "actor_id": "str", "session_id": "str"},
    "reason_mind": {"query": "str", "session_id": "str"},
    "vector_memory": {"query": "str", "session_id": "str"},
    "simulate_heart": {"query": "str", "session_id": "str"},
    "critique_thought": {"thought_id": "str", "session_id": "str"},
    "apex_judge": {"session_id": "str", "verdict_candidate": "str"},
    "eureka_forge": {
        "session_id": "str",
        "intent": "str",
    },
    "seal_vault": {"session_id": "str", "verdict": "str"},
    "search_reality": {"query": "str"},
    "ingest_evidence": {"source_url": "str"},
    "audit_rules": {},
    "check_vital": {},
    "session_memory": {"operation": "str"},
    "open_apex_dashboard": {},
    "trace_replay": {},
    "metabolic_loop": {"query": "str"},
}

# ═══════════════════════════════════════════════════════════════════════════════
# TWO-LAYER IDENTITY ENVELOPE (F9/F10 compliant)
#
# Every tool call envelope must carry two identity layers, auto-populated by
# the MCP server:
#   1. auth_context  — Human authority layer (never AI)
#   2. caller_context — AI execution identity layer (instrument, not sovereign)
#
# The LLM may provide a `requested_persona` hint (advisory only); the server
# governs the final caller_context.persona_id.
# ═══════════════════════════════════════════════════════════════════════════════

#: JSON Schema for the human authority layer.
AUTH_CONTEXT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "description": "Human authority layer. Populated by MCP server. Never the AI model.",
    "properties": {
        "actor_id": {
            "type": "string",
            "description": "Human or org identity (e.g. 'arif', 'petronas_ciso').",
        },
        "authority_level": {
            "type": "string",
            "enum": ["viewer", "editor", "judge", "admin", "root"],
            "description": "Permission or approval scope.",
        },
        "continuity": {
            "type": "string",
            "enum": ["session", "thread", "case", "none"],
            "description": "Continuity anchor for audit/logging.",
        },
    },
    "required": ["actor_id", "authority_level"],
}

#: JSON Schema for the AI runtime identity layer.
CALLER_CONTEXT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "description": (
        "AI execution identity layer. Instrument only — never inherits human sovereignty (F9/F10). "
        "Populated by the MCP server from transport metadata. The LLM may supply a "
        "`requested_persona` hint but the server governs the final persona_id."
    ),
    "properties": {
        "agent_id": {
            "type": "string",
            "description": "Stable runtime instance ID (e.g. 'gpt-runtime-01').",
        },
        "model_id": {
            "type": "string",
            "description": "Model/version string (e.g. 'claude-3-5-sonnet').",
        },
        "persona_id": {
            "type": "string",
            "enum": ["architect", "engineer", "auditor", "validator"],
            "description": (
                "Governed operational persona. Server-assigned; LLM hint via "
                "`requested_persona` field is advisory only."
            ),
        },
        "runtime_role": {
            "type": "string",
            "enum": ["assistant", "router", "tool_broker", "evaluator"],
            "description": "Operational role for this call.",
        },
        "toolchain_role": {
            "type": "string",
            "enum": ["orchestrator", "leaf", "subagent"],
            "description": "Position in multi-agent/tool chain.",
        },
        "extra": {
            "type": "object",
            "description": "Forward-compatible extension slot for future fields.",
        },
    },
    "required": ["persona_id", "runtime_role"],
}

#: Valid persona hints that the LLM client may suggest.
VALID_PERSONA_HINTS: frozenset[str] = frozenset({"architect", "engineer", "auditor", "validator"})


def require_session(tool: str, session_id: str | None) -> dict[str, Any] | None:
    if tool in REQUIRES_SESSION and (not session_id or not str(session_id).strip()):
        return {
            "verdict": "VOID",
            "stage": "F11_AUTH",
            "floors_failed": ["F11"],
            "error": "Missing session_id",
            "next_actions": [
                "Call anchor_session first.",
                "Reuse returned session_id for downstream tools.",
            ],
        }
    return None


def validate_input(tool: str, payload: dict[str, Any]) -> dict[str, Any] | None:
    contract = TOOL_INPUT_CONTRACTS.get(tool, {})
    for key, type_name in contract.items():
        if key not in payload:
            return {
                "verdict": "VOID",
                "stage": "F3_CONTRACT",
                "floors_failed": ["F3"],
                "error": f"Missing required field: {key}",
            }
        value = payload[key]
        if type_name == "str" and (not isinstance(value, str) or not str(value).strip()):
            return {
                "verdict": "VOID",
                "stage": "F3_CONTRACT",
                "floors_failed": ["F3"],
                "error": f"Field '{key}' must be non-empty string",
            }
        if type_name == "dict" and not isinstance(value, dict):
            return {
                "verdict": "VOID",
                "stage": "F3_CONTRACT",
                "floors_failed": ["F3"],
                "error": f"Field '{key}' must be object",
            }
        if type_name == "bool" and not isinstance(value, bool):
            return {
                "verdict": "VOID",
                "stage": "F3_CONTRACT",
                "floors_failed": ["F3"],
                "error": f"Field '{key}' must be boolean",
            }
    return None
