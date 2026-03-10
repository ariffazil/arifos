from __future__ import annotations

import uuid
from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.tools import ToolResult

from arifosmcp.runtime.models import CallerContext, RuntimeEnvelope, Stage
from arifosmcp.runtime.resources import build_open_apex_dashboard_result
from arifosmcp.runtime.sessions import _resolve_session_id, set_active_session
from core.state.session_manager import session_manager

from .bridge import call_kernel


def _normalize_session_id(session_id: str | None) -> str:
    """
    Resolve session_id using the centralized registry.
    F11: Ensures identity and authority boundaries are preserved.
    """
    resolved = _resolve_session_id(session_id)
    if not resolved:
        resolved = f"session-{uuid.uuid4().hex[:8]}"
        # Register with core manager to prevent null context in kernel
        session_manager.create_session(owner="anonymous", session_id=resolved)
        # Update active session pointer
        set_active_session(resolved)

    return resolved


def _normalize_verdict(verdict: Any) -> str:
    verdict_str = str(verdict or "VOID")
    # Mapping legacy or human strings to canonical enum
    from core.shared.verdict_contract import normalize_verdict

    return normalize_verdict(333, verdict_str).value


async def _wrap_call(
    tool_name: str,
    stage: Stage,
    session_id: str,
    payload: dict[str, Any],
    ctx: Context | None = None,
    caller_context: CallerContext | None = None,
) -> RuntimeEnvelope:
    """Call the bridge and normalize the result into a RuntimeEnvelope."""

    session_id = _normalize_session_id(session_id)
    # Ensure payload has session_id and routing metadata
    payload["session_id"] = session_id
    payload["tool"] = tool_name
    payload["stage"] = stage.value

    # Propagate caller_context into payload for bridge/kernel tracing
    if caller_context is not None:
        payload["caller_context"] = caller_context.model_dump(mode="json", exclude_none=True)

    try:
        # call_kernel now returns a dictionary matching the Canonical Schema
        kernel_res = await call_kernel(tool_name, session_id, payload)

        # Merge additional runtime metadata if not already present
        if "meta" not in kernel_res:
            from datetime import datetime, timezone

            kernel_res["meta"] = {
                "schema_version": "1.0.0",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "debug": bool(payload.get("debug")),
                "dry_run": bool(payload.get("dry_run")),
            }

        # Carry caller_context into envelope from payload or argument
        if "caller_context" not in kernel_res and caller_context is not None:
            kernel_res["caller_context"] = caller_context.model_dump(mode="json", exclude_none=True)

        # Initialize the envelope model (v1.0.0 Schema)
        envelope = RuntimeEnvelope(**kernel_res)

    except Exception as e:
        # Fallback for bridge or validation failure
        from arifosmcp.runtime.models import CanonicalError, CanonicalMeta, RuntimeStatus, Verdict

        envelope = RuntimeEnvelope(
            ok=False,
            tool=tool_name,
            session_id=session_id,
            stage=stage.value,
            verdict=Verdict.SABAR,
            status=RuntimeStatus.ERROR,
            errors=[
                CanonicalError(
                    code="RUNTIME_FAILURE",
                    message=str(e),
                    stage=stage.value,
                    recoverable=True,
                )
            ],
            meta=CanonicalMeta(debug=bool(payload.get("debug"))),
            auth_context=payload.get("auth_context"),
            caller_context=caller_context,
        )

    if ctx:
        # Filter down for UX telemetry (remove raw payload in logs)
        log_data = envelope.model_dump(exclude_none=True)
        if not payload.get("debug"):
            log_data.pop("payload", None)
            log_data.pop("debug", None)
        await ctx.info(f"arifOS_telemetry {log_data}")

    return envelope


# ─── Persona resolution helper ──────────────────────────────────────────────

_PERSONA_WHITELIST = {"architect", "engineer", "auditor", "validator"}


def _resolve_caller_context(
    caller_context: CallerContext | None,
    requested_persona: str | None,
) -> CallerContext:
    """
    Resolve the final CallerContext for a tool call.

    The LLM may suggest a persona via ``requested_persona`` (advisory hint).
    The server governs the final ``persona_id``; unknown hints are silently
    ignored and fall back to the default (engineer).

    F9 compliance: AI declares execution role, never inherits human sovereignty.
    """
    from arifosmcp.runtime.models import PersonaId

    base = caller_context or CallerContext()

    if requested_persona and requested_persona.lower() in _PERSONA_WHITELIST:
        governed_persona = PersonaId(requested_persona.lower())
        base = base.model_copy(update={"persona_id": governed_persona})

    return base


async def init_anchor_state(
    intent: dict[str, Any],
    math: dict[str, Any] | None = None,
    governance: dict[str, Any] | None = None,
    auth_token: str | None = None,
    session_id: str = "global",
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """000 INIT - Session anchor. Bootstrap a governed session and mint continuity context."""
    payload = {
        "intent": intent,
        "math": math,
        "governance": governance,
        "auth_token": auth_token,
    }
    return await _wrap_call(
        "init_anchor_state", Stage.INIT_000, session_id, payload, ctx, caller_context
    )


async def integrate_analyze_reflect(
    session_id: str,
    query: str,
    auth_context: dict[str, Any],
    max_subquestions: int = 3,
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """111 FRAME - Integrate, analyze, reflect. Frame the problem before deep reasoning."""
    payload = {
        "query": query,
        "auth_context": auth_context,
        "max_subquestions": max_subquestions,
    }
    return await _wrap_call(
        "integrate_analyze_reflect", Stage.SENSE_111, session_id, payload, ctx, caller_context
    )


async def reason_mind_synthesis(
    session_id: str,
    query: str,
    auth_context: dict[str, Any],
    reason_mode: str = "default",
    max_steps: int = 7,
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """333 REASON - Mind synthesis. Run multi-step governed reasoning for the active session."""
    payload = {
        "query": query,
        "auth_context": auth_context,
        "reason_mode": reason_mode,
        "max_steps": max_steps,
    }
    return await _wrap_call(
        "reason_mind_synthesis", Stage.MIND_333, session_id, payload, ctx, caller_context
    )


async def metabolic_loop_router(
    query: str,
    context: str = "",
    risk_tier: str = "medium",
    actor_id: str = "anonymous",
    use_memory: bool = True,
    use_heart: bool = True,
    use_critique: bool = True,
    allow_execution: bool = False,
    debug: bool = False,
    dry_run: bool = False,
    requested_persona: str | None = None,
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """Stage 444 ROUTER - Metabolic Loop. The all-in-one arifOS Sovereign evaluation."""
    session_id = _resolve_session_id(None)

    # Server governs final persona; LLM hint (requested_persona) is advisory only.
    resolved_caller = _resolve_caller_context(caller_context, requested_persona)

    payload = {
        "query": query,
        "context": context,
        "risk_tier": risk_tier,
        "actor_id": actor_id,
        "use_memory": use_memory,
        "use_heart": use_heart,
        "use_critique": use_critique,
        "allow_execution": allow_execution,
        "debug": debug,
        "dry_run": dry_run,
    }
    return await _wrap_call(
        "arifOS.kernel", Stage.ROUTER_444, session_id, payload, ctx, resolved_caller
    )


async def session_memory(
    session_id: str,
    operation: str,
    auth_context: dict[str, Any] | None = None,
    content: str | None = None,
    memory_ids: list[str] | None = None,
    top_k: int = 5,
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """Session memory for conversation state, vector recall, and reasoning artifacts."""
    payload = {
        "operation": operation,
        "content": content,
        "memory_ids": memory_ids,
        "top_k": top_k,
        "auth_context": auth_context or {},
    }
    return await _wrap_call(
        "vector_memory_store", Stage.MEMORY_555, session_id, payload, ctx, caller_context
    )


async def assess_heart_impact(
    session_id: str,
    scenario: str,
    auth_context: dict[str, Any],
    heart_mode: str = "general",
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """666A HEART - Impact assessment. Evaluate empathy, care, and stakeholder harm."""
    payload = {"scenario": scenario, "focus": heart_mode, "auth_context": auth_context}
    return await _wrap_call(
        "assess_heart_impact", Stage.HEART_666, session_id, payload, ctx, caller_context
    )


async def critique_thought_audit(
    session_id: str,
    thought_id: str,
    auth_context: dict[str, Any],
    critique_mode: str = "overall",
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """666B CRITIQUE - Thought audit against a prior reasoning artifact."""
    payload = {
        "thought_id": thought_id,
        "critique_focus": critique_mode,
        "auth_context": auth_context,
    }
    return await _wrap_call(
        "critique_thought_audit", Stage.CRITIQUE_666, session_id, payload, ctx, caller_context
    )


async def quantum_eureka_forge(
    session_id: str,
    intent: str,
    auth_context: dict[str, Any],
    eureka_type: str = "concept",
    materiality: str = "idea_only",
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """777 FORGE - Eureka proposal. Forge a sandboxed discovery or implementation proposal."""
    payload = {
        "intent": intent,
        "eureka_type": eureka_type,
        "materiality": materiality,
        "auth_context": auth_context,
    }
    return await _wrap_call(
        "quantum_eureka_forge", Stage.FORGE_777, session_id, payload, ctx, caller_context
    )


async def apex_judge_verdict(
    session_id: str,
    verdict_candidate: str,
    auth_context: dict[str, Any],
    reason_summary: str | None = None,
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """888 JUDGE - APEX verdict. Render the sovereign constitutional judgment for a session."""
    payload = {
        "verdict_candidate": verdict_candidate,
        "reason_summary": reason_summary,
        "auth_context": auth_context,
    }
    return await _wrap_call(
        "apex_judge_verdict", Stage.JUDGE_888, session_id, payload, ctx, caller_context
    )


async def seal_vault_commit(
    session_id: str,
    auth_context: dict[str, Any],
    verdict: str = "SEAL",
    payload_ref: str | None = None,
    payload_hash: str | None = None,
    telemetry: dict[str, Any] | None = None,
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """999 SEAL - Vault commit. Append an immutable session verdict to VAULT999."""
    payload = {
        "summary": f"Commit for session {session_id}",
        "verdict": verdict,
        "payload_ref": payload_ref,
        "payload_hash": payload_hash,
        "telemetry": telemetry,
        "auth_context": auth_context,
    }
    return await _wrap_call(
        "seal_vault_commit", Stage.VAULT_999, session_id, payload, ctx, caller_context
    )


async def search_reality(query: str, ctx: Context | None = None) -> RuntimeEnvelope:
    """External knowledge discovery. Finds real-world sources and evidence before reasoning."""
    return await _wrap_call("search_reality", Stage.SENSE_111, "global", {"query": query}, ctx)


async def ingest_evidence(url: str, ctx: Context | None = None) -> RuntimeEnvelope:
    """Evidence ingestion. Loads URLs, documents, and datasets into context."""
    return await _wrap_call(
        "ingest_evidence", Stage.REALITY_222, "global", {"source_url": url}, ctx
    )


async def audit_rules(session_id: str = "global", ctx: Context | None = None) -> RuntimeEnvelope:
    """Constitutional audit. Inspects governance floors and system rules logic."""
    return await _wrap_call("audit_rules", Stage.MIND_333, session_id, {}, ctx)


async def check_vital(session_id: str = "global", ctx: Context | None = None) -> RuntimeEnvelope:
    """Kernel health monitor. Reports system health, metrics, and constitutional vitality."""
    return await _wrap_call("check_vital", Stage.INIT_000, session_id, {}, ctx)


async def open_apex_dashboard(
    session_id: str = "global", ctx: Context | None = None
) -> ToolResult | RuntimeEnvelope:
    """Sovereign monitoring interface. UI dashboard for live metrics and trace visibility."""
    res = build_open_apex_dashboard_result(session_id)
    if res:
        return res
    # Fallback if Prefab not available
    return await _wrap_call("open_apex_dashboard", Stage.VAULT_999, session_id, {}, ctx)


def register_tools(mcp: FastMCP, profile: str = "full") -> None:
    """Register the core runtime tools; the dashboard app tool is added in resources."""

    normalized_profile = profile.strip().lower() or "full"

    # 1. arifOS.kernel — Core execution
    mcp.tool(
        name="arifOS.kernel",
        description=(
            "The arifOS Intelligence Kernel. Runs the full constitutional reasoning pipeline. "
            "Use this as the primary entrypoint for non-trivial intelligence tasks."
        ),
    )(metabolic_loop_router)

    # Legacy alias
    mcp.tool(
        name="metabolic_loop_router",
        description=(
            "[Legacy Alias] Use arifOS.kernel instead. Governed metabolic loop orchestrator."
        ),
    )(metabolic_loop_router)

    # 2. search_reality — Discovery
    mcp.tool(
        name="search_reality",
        description="Find real-world sources and factual grounding before reasoning.",
    )(search_reality)

    # 3. ingest_evidence — Intake
    mcp.tool(
        name="ingest_evidence",
        description="Fetch or extract evidence from a URL, document, or file path.",
    )(ingest_evidence)

    # 4. session_memory — Context
    mcp.tool(
        name="session_memory",
        description="Store, retrieve, or forget session context and reasoning artifacts.",
    )(session_memory)

    # 5. audit_rules — Governance
    mcp.tool(
        name="audit_rules",
        description="Inspect the 13 constitutional floors and verify governance logic.",
    )(audit_rules)

    # 6. check_vital — Health
    mcp.tool(
        name="check_vital",
        description="Read-only system health snapshot, reporting diagnostics and vitality signals.",
    )(check_vital)

    # Legacy tools preserved for internal orchestration
    if normalized_profile != "chatgpt":
        mcp.tool(description="000 INIT - Session anchor.")(init_anchor_state)
        mcp.tool(description="111 FRAME - Problem framing.")(integrate_analyze_reflect)
        mcp.tool(description="333 REASON - Mind synthesis.")(reason_mind_synthesis)
        mcp.tool(description="666A HEART - Impact assessment.")(assess_heart_impact)
        mcp.tool(description="666B CRITIQUE - Thought audit.")(critique_thought_audit)
        mcp.tool(description="777 FORGE - Eureka proposal.")(quantum_eureka_forge)
        mcp.tool(description="888 JUDGE - APEX verdict.")(apex_judge_verdict)
        mcp.tool(description="999 SEAL - Vault commit.")(seal_vault_commit)


__all__ = [
    "audit_rules",
    "check_vital",
    "ingest_evidence",
    "metabolic_loop_router",
    "open_apex_dashboard",
    "quantum_eureka_forge",
    "reason_mind_synthesis",
    "register_tools",
    "seal_vault_commit",
    "search_reality",
    "session_memory",
]
