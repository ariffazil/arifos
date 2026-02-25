"""Legacy compatibility package.

External/public interface is now `arifos_aaa_mcp` (canonical 13-tool surface).

This `aaa_mcp` package remains as internal/legacy wiring.
"""

from __future__ import annotations

import warnings
from typing import Any

__version__ = "2026.02.23-CANONICAL-13"

__all__ = ["mcp"]


# All legacy/mid-gen names resolve to canonical UX names.
_OLD_TO_NEW = {
    # Mid-gen kernel names → canonical
    "init_session": "anchor_session",
    "agi_cognition": "reason_mind",
    "phoenix_recall": "recall_memory",
    "asi_empathy": "simulate_heart",
    "apex_verdict": "judge_soul",
    "sovereign_actuator": "forge_hand",
    "vault_seal": "seal_vault",
    "search": "search_reality",
    "fetch": "fetch_content",
    "analyze": "inspect_file",
    "system_audit": "audit_rules",
    # Legacy 9-verb surface → canonical
    "anchor": "anchor_session",
    "reason": "reason_mind",
    "integrate": "reason_mind",
    "respond": "reason_mind",
    "validate": "simulate_heart",
    "align": "simulate_heart",
    "forge": "judge_soul",
    "audit": "judge_soul",
    "seal": "seal_vault",
    # Canonical names → self (for pass-through)
    "anchor_session": "anchor_session",
    "reason_mind": "reason_mind",
    "recall_memory": "recall_memory",
    "simulate_heart": "simulate_heart",
    "critique_thought": "critique_thought",
    "judge_soul": "judge_soul",
    "forge_hand": "forge_hand",
    "seal_vault": "seal_vault",
    "search_reality": "search_reality",
    "fetch_content": "fetch_content",
    "inspect_file": "inspect_file",
    "audit_rules": "audit_rules",
    "check_vital": "check_vital",
}


def __getattr__(name: str) -> Any:
    if name == "mcp":
        import importlib

        aaa = importlib.import_module("arifos_aaa_mcp.server")
        return aaa.mcp
    if name in _OLD_TO_NEW:
        warnings.warn(
            f"aaa_mcp.{name} is deprecated; use arifos_aaa_mcp canonical tools instead",
            DeprecationWarning,
            stacklevel=2,
        )
        import importlib

        legacy = importlib.import_module("aaa_mcp.server")
        return getattr(legacy, _OLD_TO_NEW[name])
    raise AttributeError(name)
