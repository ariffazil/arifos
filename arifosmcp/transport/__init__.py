"""
DEPRECATED: This legacy transport module is deprecated.

arifosmcp/runtime/server.py and FastMCP are the canonical deployment paths
for modern, agnostic MCP clients.

Legacy compatibility package.
External/public interface is now `arifosmcp.runtime` (canonical 13-tool surface).
This `arifosmcp.transport` package remains as internal/legacy wiring.
"""

from __future__ import annotations

import warnings
from typing import Any

__version__ = "2026.03.10"

__all__ = ["mcp"]


class _CompatTool:
    def __init__(self, fn: Any) -> None:
        self.fn = fn

    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return await self.fn(*args, **kwargs)


# All legacy/mid-gen names resolve to canonical UX names.
_OLD_TO_NEW = {
    # Mid-gen kernel names → canonical
    "init_session": "anchor_session",
    "agi_cognition": "reason_mind",
    "phoenix_recall": "vector_memory",
    "recall_memory": "vector_memory",
    "memory_search": "vector_memory",
    "asi_empathy": "simulate_heart",
    "apex_verdict": "apex_judge",
    "sovereign_actuator": "eureka_forge",
    "vault_seal": "seal_vault",
    "search": "search_reality",
    "fetch": "fetch_content",
    "fetch_content": "fetch_content",
    "analyze": "inspect_file",
    "inspect_file": "inspect_file",
    "system_audit": "audit_rules",
    # Legacy 9-verb surface → canonical
    "anchor": "anchor_session",
    "reason": "reason_mind",
    "integrate": "reason_mind",
    "respond": "reason_mind",
    "validate": "simulate_heart",
    "align": "simulate_heart",
    "forge": "apex_judge",
    "audit": "apex_judge",
    "seal": "seal_vault",
    # Canonical names → self (for pass-through)
    "anchor_session": "anchor_session",
    "reason_mind": "reason_mind",
    "vector_memory": "vector_memory",
    "simulate_heart": "simulate_heart",
    "critique_thought": "critique_thought",
    "apex_judge": "apex_judge",
    "eureka_forge": "eureka_forge",
    "seal_vault": "seal_vault",
    "search_reality": "search_reality",
    "ingest_evidence": "ingest_evidence",
    "audit_rules": "audit_rules",
    "check_vital": "check_vital",
    "metabolic_loop": "metabolic_loop",
}


def __getattr__(name: str) -> Any:
    if name == "mcp":
        import importlib

        aaa = importlib.import_module("arifosmcp.runtime.server")
        return aaa.mcp
    if name in _OLD_TO_NEW:
        warnings.warn(
            f"arifosmcp.transport.{name} is deprecated; use arifosmcp.runtime canonical tools instead",
            DeprecationWarning,
            stacklevel=2,
        )
        import importlib

        legacy = importlib.import_module("arifosmcp.transport.server")
        if name == "init_session":

            async def _init_session_compat(
                query: str,
                actor_id: str = "anonymous",
                auth_token: str | None = None,
                mode: str = "conscience",
                grounding_required: bool = True,
                debug: bool = False,
                inject_kernel: bool = False,
                compact_kernel: bool = True,
                template_id: str | None = None,
                auth_context: dict[str, Any] | None = None,
            ) -> Any:
                return await legacy.anchor_session.fn(
                    query=query,
                    actor_id=actor_id,
                    auth_token=auth_token,
                    mode=mode,
                    grounding_required=grounding_required,
                    debug=debug,
                    inject_kernel=inject_kernel,
                    compact_kernel=compact_kernel,
                    template_id=template_id,
                    auth_context=auth_context,
                )

            return _CompatTool(_init_session_compat)

        if name == "system_audit":

            async def _system_audit_compat(
                audit_scope: str = "quick",
                verify_floors: bool = True,
            ) -> Any:
                return await legacy.audit_rules.fn(
                    audit_scope=audit_scope,
                    verify_floors=verify_floors,
                )

            return _CompatTool(_system_audit_compat)

        if name == "search":

            async def _search_compat(query: str, intent: str = "general") -> Any:
                return await legacy.search_reality.fn(query=query, intent=intent)

            return _CompatTool(_search_compat)

        return getattr(legacy, _OLD_TO_NEW[name])
    raise AttributeError(name)
