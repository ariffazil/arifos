"""Phase 3 contracts for arifOS AAA MCP.

Provides lightweight input guards and session continuity checks
without changing transport/runtime dependencies.
"""

from __future__ import annotations

from typing import Any

REQUIRES_SESSION = {
    "reason_mind",
    "recall_memory",
    "simulate_heart",
    "critique_thought",
    "apex_judge",
    "eureka_forge",
    "seal_vault",
}


TOOL_INPUT_CONTRACTS: dict[str, dict[str, str]] = {
    "anchor_session": {"query": "str", "actor_id": "str", "session_id": "str"},
    "reason_mind": {"query": "str", "session_id": "str"},
    "recall_memory": {
        "current_thought_vector": "str",
        "session_id": "str",
    },
    "simulate_heart": {"query": "str", "session_id": "str"},
    "critique_thought": {"plan": "dict", "session_id": "str"},
    "apex_judge": {"session_id": "str", "query": "str"},
    "eureka_forge": {
        "session_id": "str",
        "command": "str",
    },
    "seal_vault": {"session_id": "str", "summary": "str"},
    "search_reality": {"query": "str", "session_id": "str"},
    "ingest_evidence": {"source_type": "str", "target": "str"},
    "audit_rules": {"audit_scope": "str", "session_id": "str"},
    "check_vital": {},
}


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
    return None
