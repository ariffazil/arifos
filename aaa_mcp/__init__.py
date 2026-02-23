"""Legacy compatibility package.

External/public interface is now `arifos_aaa_mcp` (canonical 13-tool surface).

This `aaa_mcp` package remains as internal/legacy wiring.
"""

from __future__ import annotations

import warnings
from typing import Any


__version__ = "2026.02.23-AAA-BRIDGE"

__all__ = ["mcp"]


_LEGACY_EXPORTS = {
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
    "anchor",
    "reason",
    "integrate",
    "respond",
    "validate",
    "align",
    "forge",
    "audit",
    "seal",
}


def __getattr__(name: str) -> Any:
    if name == "mcp":
        import importlib

        aaa = importlib.import_module("arifos_aaa_mcp.server")
        return getattr(aaa, "mcp")
    if name in _LEGACY_EXPORTS:
        warnings.warn(
            f"aaa_mcp.{name} is deprecated; use arifos_aaa_mcp canonical tools instead",
            DeprecationWarning,
            stacklevel=2,
        )
        import importlib

        legacy = importlib.import_module("aaa_mcp.server")
        return getattr(legacy, name)
    raise AttributeError(name)
