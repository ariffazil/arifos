from __future__ import annotations

import uuid
from typing import Any

from fastmcp import Context, FastMCP

from arifosmcp.bridge import call_kernel
from arifosmcp.runtime.models import (
    AuthContext,
    RuntimeEnvelope,
    Stage,
    Telemetry,
    Verdict,
    Witness,
)


def _normalize_session_id(session_id: str) -> str:
    if not session_id or session_id == "global":
        return f"session-{uuid.uuid4().hex[:8]}"
    return session_id


def _normalize_verdict(verdict: Any) -> str:
    verdict_str = str(verdict or "UNSET")
    if verdict_str == "888_HOLD":
        return Verdict.HOLD_888.value
    return verdict_str


def _normalize_auth_context(raw_auth_context: Any) -> dict[str, Any]:
    if isinstance(raw_auth_context, AuthContext):
        return raw_auth_context.model_dump(exclude_none=True)
    if isinstance(raw_auth_context, dict):
        return raw_auth_context
    return {}


async def _wrap_call(
    tool_name: str,
    stage: Stage,
    session_id: str,
    payload: dict[str, Any],
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """Call the bridge and normalize the result into a RuntimeEnvelope."""

    session_id = _normalize_session_id(session_id)
    input_auth_ctx = _normalize_auth_context(payload.get("auth_context"))

    try:
        kernel_res = await call_kernel(tool_name, session_id, payload)

        verdict_str = _normalize_verdict(kernel_res.get("verdict", "UNSET"))
        try:
            verdict = Verdict(verdict_str)
        except ValueError:
            verdict = Verdict.UNSET

        returned_auth_ctx = kernel_res.get("auth_context", input_auth_ctx)
        auth_context = AuthContext(**_normalize_auth_context(returned_auth_ctx))

        envelope = RuntimeEnvelope(
            verdict=verdict,
            stage=stage,
            session_id=str(kernel_res.get("session_id", session_id)),
            telemetry=Telemetry(
                dS=kernel_res.get("telemetry", {}).get("dS", -0.7),
                peace2=kernel_res.get("telemetry", {}).get("peace2", 1.1),
                confidence=kernel_res.get("telemetry", {}).get("confidence", 0.9),
                verdict=kernel_res.get("telemetry", {}).get("verdict", "Alive"),
            ),
            witness=Witness(
                human=kernel_res.get("witness", {}).get("human", 0.0),
                ai=kernel_res.get("witness", {}).get("ai", 0.0),
                earth=kernel_res.get("witness", {}).get("earth", 0.0),
            ),
            auth_context=auth_context,
            data=kernel_res.get("payload", kernel_res),
        )
    except Exception as e:
        envelope = RuntimeEnvelope(
            verdict=Verdict.VOID,
            stage=stage,
            session_id=session_id,
            data={"error": str(e), "stage": "BRIDGE_FAILURE"},
        )

    if ctx:
        await ctx.info(f"arifOS_telemetry {envelope.model_dump_json()}")

    return envelope


async def init_anchor_state(
    intent: dict[str, Any],
    math: dict[str, Any] | None = None,
    governance: dict[str, Any] | None = None,
    auth_token: str | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """000 INIT - Session anchor. Bootstrap a governed session and mint continuity context."""
    payload = {
        "intent": intent,
        "math": math,
        "governance": governance,
        "auth_token": auth_token,
    }
    return await _wrap_call("init_anchor_state", Stage.INIT, "global", payload, ctx)


async def integrate_analyze_reflect(
    session_id: str,
    query: str,
    auth_context: dict[str, Any],
    max_subquestions: int = 3,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """111 FRAME - Integrate, analyze, reflect. Frame the problem before deep reasoning."""
    payload = {
        "query": query,
        "auth_context": auth_context,
        "max_subquestions": max_subquestions,
    }
    return await _wrap_call("integrate_analyze_reflect", Stage.MIND_111, session_id, payload, ctx)


async def reason_mind_synthesis(
    session_id: str,
    query: str,
    auth_context: dict[str, Any],
    reason_mode: str = "default",
    max_steps: int = 7,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """333 REASON - Mind synthesis. Run multi-step governed reasoning for the active session."""
    payload = {
        "query": query,
        "auth_context": auth_context,
        "reason_mode": reason_mode,
        "max_steps": max_steps,
    }
    return await _wrap_call("reason_mind_synthesis", Stage.MIND_333, session_id, payload, ctx)


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
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """444 ROUTE - Metabolic loop router. Orchestrate the full 000-999 APEX-G pipeline."""
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
    }
    return await _wrap_call("metabolic_loop_router", Stage.ROUTER, "global", payload, ctx)


async def vector_memory_store(
    session_id: str,
    operation: str,
    auth_context: dict[str, Any],
    content: str | None = None,
    memory_ids: list[str] | None = None,
    top_k: int = 5,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """555 MEMORY - Vector memory store. Store, recall, search, or forget BBB memory."""
    payload = {
        "operation": operation,
        "content": content,
        "memory_ids": memory_ids,
        "top_k": top_k,
        "auth_context": auth_context,
    }
    return await _wrap_call("vector_memory_store", Stage.MEMORY, session_id, payload, ctx)


async def assess_heart_impact(
    session_id: str,
    scenario: str,
    auth_context: dict[str, Any],
    heart_mode: str = "general",
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """666A HEART - Impact assessment. Evaluate empathy, care, and stakeholder harm."""
    payload = {"scenario": scenario, "focus": heart_mode, "auth_context": auth_context}
    return await _wrap_call("assess_heart_impact", Stage.HEART, session_id, payload, ctx)


async def critique_thought_audit(
    session_id: str,
    thought_id: str,
    auth_context: dict[str, Any],
    critique_mode: str = "overall",
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """666B CRITIQUE - Thought audit. Run adversarial critique against a prior reasoning artifact."""
    payload = {
        "thought_id": thought_id,
        "critique_focus": critique_mode,
        "auth_context": auth_context,
    }
    return await _wrap_call("critique_thought_audit", Stage.HEART, session_id, payload, ctx)


async def quantum_eureka_forge(
    session_id: str,
    intent: str,
    auth_context: dict[str, Any],
    eureka_type: str = "concept",
    materiality: str = "idea_only",
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """777 FORGE - Eureka proposal. Forge a sandboxed discovery or implementation proposal."""
    payload = {
        "intent": intent,
        "eureka_type": eureka_type,
        "materiality": materiality,
        "auth_context": auth_context,
    }
    return await _wrap_call("quantum_eureka_forge", Stage.APEX, session_id, payload, ctx)


async def apex_judge_verdict(
    session_id: str,
    verdict_candidate: str,
    auth_context: dict[str, Any],
    reason_summary: str | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """888 JUDGE - APEX verdict. Render the sovereign constitutional judgment for a session."""
    payload = {
        "verdict_candidate": verdict_candidate,
        "reason_summary": reason_summary,
        "auth_context": auth_context,
    }
    return await _wrap_call("apex_judge_verdict", Stage.JUDGE, session_id, payload, ctx)


async def seal_vault_commit(
    session_id: str,
    auth_context: dict[str, Any],
    verdict: str = "SEAL",
    payload_ref: str | None = None,
    payload_hash: str | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """999 SEAL - Vault commit. Append an immutable session verdict to VAULT999."""
    payload = {
        "summary": f"Commit for session {session_id}",
        "verdict": verdict,
        "payload_ref": payload_ref,
        "payload_hash": payload_hash,
        "auth_context": auth_context,
    }
    return await _wrap_call("seal_vault_commit", Stage.VAULT, session_id, payload, ctx)


def register_tools(mcp: FastMCP) -> None:
    """Register all 10 APEX-G tools."""

    mcp.tool()(init_anchor_state)
    mcp.tool()(integrate_analyze_reflect)
    mcp.tool()(reason_mind_synthesis)
    mcp.tool()(metabolic_loop_router)
    mcp.tool()(vector_memory_store)
    mcp.tool()(assess_heart_impact)
    mcp.tool()(critique_thought_audit)
    mcp.tool()(quantum_eureka_forge)
    mcp.tool()(apex_judge_verdict)
    mcp.tool()(seal_vault_commit)


__all__ = [
    "apex_judge_verdict",
    "assess_heart_impact",
    "critique_thought_audit",
    "init_anchor_state",
    "integrate_analyze_reflect",
    "metabolic_loop_router",
    "quantum_eureka_forge",
    "reason_mind_synthesis",
    "register_tools",
    "seal_vault_commit",
    "vector_memory_store",
]
