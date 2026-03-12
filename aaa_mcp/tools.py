"""
aaa_mcp.tools - legacy compatibility wrappers.

This module exists only for older integrations that still import the historical
AAA tool names. It is not the public/main MCP contract. Model-facing clients
should use arifosmcp.runtime.public_registry and the 8-tool public surface.
"""

from __future__ import annotations

from typing import Any

from arifosmcp.runtime.models import CallerContext
from arifosmcp.runtime.tools import (
    assess_heart_impact,
    audit_rules,
    bootstrap_identity,
    check_vital,
    critique_thought_audit,
    init_anchor_state,
    ingest_evidence,
    integrate_analyze_reflect,
    open_apex_dashboard,
    quantum_eureka_forge,
    reason_mind_synthesis,
    seal_vault_commit,
    search_reality,
    session_memory,
)


async def anchor_session(
    intent: dict[str, Any] | None = None,
    math: dict[str, Any] | None = None,
    governance: dict[str, Any] | None = None,
    auth_token: str | None = None,
    session_id: str = "global",
    actor_id: str = "anonymous",
) -> dict[str, Any]:
    """000 INIT - Session anchor. Bootstrap a governed session."""
    # Support both old and new parameter styles
    if intent is None:
        intent = {"query": "INIT", "actor_id": actor_id}
    
    result = await init_anchor_state(
        intent=intent,
        math=math,
        governance=governance,
        auth_token=auth_token,
        session_id=session_id,
    )
    return result.model_dump(mode="json")


async def reason_mind(
    query: str,
    session_id: str,
    logic_path: str = "",
    auth_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """222-333 MIND - Reasoning and synthesis."""
    result = await reason_mind_synthesis(
        session_id=session_id,
        query=query or logic_path,
        auth_context=auth_context or {},
    )
    return result.model_dump(mode="json")


async def recall_memory(
    session_id: str,
    operation: str = "retrieve",
    content: str | None = None,
    auth_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """555 MEMORY - Session memory operations."""
    result = await session_memory(
        session_id=session_id,
        operation=operation,
        content=content,
        auth_context=auth_context or {},
    )
    return result.model_dump(mode="json")


async def simulate_heart(
    action_impact: str,
    session_id: str,
    auth_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """555-666 HEART - Impact assessment and empathy."""
    result = await assess_heart_impact(
        session_id=session_id,
        scenario=action_impact,
        auth_context=auth_context or {},
    )
    return result.model_dump(mode="json")


async def critique_thought(
    thought_id: str,
    session_id: str,
    auth_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """666B CRITIQUE - Thought audit."""
    result = await critique_thought_audit(
        session_id=session_id,
        thought_id=thought_id,
        auth_context=auth_context or {},
    )
    return result.model_dump(mode="json")


async def apex_judge(
    session_id: str,
    verdict_candidate: str = "SEAL",
    reason_summary: str | None = None,
    auth_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """888 JUDGE - APEX verdict rendering."""
    result = await quantum_eureka_forge(
        session_id=session_id,
        intent=reason_summary or "APEX Judgment",
        auth_context=auth_context or {},
    )
    return result.model_dump(mode="json")


async def eureka_forge(
    proposal: str,
    session_id: str,
    auth_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """777 FORGE - Eureka proposal forging."""
    result = await quantum_eureka_forge(
        session_id=session_id,
        intent=proposal,
        auth_context=auth_context or {},
    )
    return result.model_dump(mode="json")


async def seal_vault(
    verdict: dict[str, Any] | str,
    session_id: str,
    auth_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """999 VAULT - Immutable ledger seal."""
    verdict_str = verdict.get("verdict", "SEAL") if isinstance(verdict, dict) else str(verdict)
    result = await seal_vault_commit(
        session_id=session_id,
        verdict=verdict_str,
        auth_context=auth_context or {},
    )
    return result.model_dump(mode="json")


async def fetch_content(
    url: str,
    session_id: str = "global",
) -> dict[str, Any]:
    """Fetch content from URL."""
    result = await ingest_evidence(
        url=url,
    )
    return result.model_dump(mode="json")


async def inspect_file(
    path: str,
    session_id: str = "global",
) -> dict[str, Any]:
    """File inspection."""
    # Delegates to runtime capability map or filesystem tools
    from arifosmcp.runtime.capability_map import build_runtime_capability_map
    return {
        "ok": True,
        "tool": "inspect_file",
        "session_id": session_id,
        "path": path,
        "capability_map": build_runtime_capability_map(),
    }


# Re-export working tools directly
search_reality = search_reality
audit_rules = audit_rules
check_vital = check_vital
open_apex_dashboard = open_apex_dashboard

__all__ = [
    "anchor_session",
    "reason_mind",
    "recall_memory",
    "simulate_heart",
    "critique_thought",
    "apex_judge",
    "eureka_forge",
    "seal_vault",
    "search_reality",
    "fetch_content",
    "inspect_file",
    "audit_rules",
    "check_vital",
    "open_apex_dashboard",
]
