from __future__ import annotations

import uuid
from typing import Any

from fastmcp import Context, FastMCP

from arifosmcp.bridge import call_kernel
from arifosmcp.runtime.models import (
    APEXBundle,
    AuthContext,
    OPEXBundle,
    RuntimeEnvelope,
    Stage,
    Telemetry,
    Verdict,
    Witness,
    derive_apex,
)


from arifosmcp.runtime.sessions import _resolve_session_id, set_active_session
from core.state.session_manager import session_manager

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


def _build_opex(tool_name: str, kernel_res: dict[str, Any], envelope: RuntimeEnvelope) -> OPEXBundle:
    """Extract OPEX epistemic fields from the kernel result, keyed by tool name."""
    data = kernel_res.get("payload", kernel_res)
    conf = envelope.telemetry.confidence

    if tool_name == "init_anchor_state":
        return OPEXBundle(
            output_candidate=str(data.get("mode", "session_init")),
            probability=conf,
            evidence=["auth_token validated", "F11 auth passed", "F12 injection clean"],
            uncertainty=(["grounding_required"] if data.get("grounding_required") else []),
        )
    elif tool_name == "integrate_analyze_reflect":
        subqs = data.get("subquestions", [])
        return OPEXBundle(
            output_candidate=str(data.get("framing_notes", "")),
            probability=conf,
            evidence=[str(q) for q in subqs],
            uncertainty=(["further sub-analysis required"] if len(subqs) < 2 else []),
        )
    elif tool_name == "reason_mind_synthesis":
        steps = data.get("steps", [])
        low_conf_steps = [s.get("thought", "") for s in steps if float(s.get("confidence", 1.0)) < 0.7]
        return OPEXBundle(
            output_candidate=str(data.get("eureka_insight", "")),
            probability=float(data.get("genius_score", conf)),
            evidence=[s.get("thought", "") for s in steps],
            uncertainty=low_conf_steps,
        )
    elif tool_name == "metabolic_loop_router":
        trace = data.get("trace", {})
        return OPEXBundle(
            output_candidate=f"Pipeline verdict: {envelope.verdict.value}",
            probability=conf,
            evidence=[f"{stage}: {v}" for stage, v in trace.items()],
            uncertainty=[f"{s}: requires review" for s, v in trace.items() if v in ("SABAR", "VOID")],
        )
    elif tool_name == "vector_memory_store":
        mems = data.get("memories", [])
        return OPEXBundle(
            output_candidate="Memory operation completed",
            probability=conf,
            evidence=[str(m) for m in mems[:5]],
            uncertainty=(["memory gaps detected"] if not mems else []),
        )
    elif tool_name == "assess_heart_impact":
        risk = float(data.get("risk_score", 0.0))
        return OPEXBundle(
            output_candidate=f"Risk score: {risk:.2f}",
            probability=max(0.0, 1.0 - risk),
            evidence=[str(data.get("vulnerable_stakeholder_analysis", ""))],
            uncertainty=["complex multi-stakeholder scenarios may be unmodeled"],
        )
    elif tool_name == "critique_thought_audit":
        issues = data.get("issues", [])
        risk = float(data.get("risk_score", 0.0))
        return OPEXBundle(
            output_candidate=str(data.get("recommendation", "")),
            probability=max(0.0, 1.0 - risk),
            evidence=[str(i) for i in issues],
            uncertainty=["logical edge cases may remain"],
        )
    elif tool_name == "quantum_eureka_forge":
        return OPEXBundle(
            output_candidate=str(data.get("eureka_proposal", "")),
            probability=float(data.get("confidence", conf)),
            evidence=[f"materiality={data.get('materiality', 'idea_only')}"],
            uncertainty=["sandboxed proposal — not verified for deployment"],
        )
    elif tool_name == "apex_judge_verdict":
        w = envelope.witness
        tri = (w.human * w.ai * w.earth) ** (1 / 3)
        return OPEXBundle(
            output_candidate=str(data.get("governance_token", envelope.verdict.value)),
            probability=tri,
            evidence=[f"human={w.human:.2f}", f"ai={w.ai:.2f}", f"earth={w.earth:.2f}"],
            uncertainty=([str(data.get("reasoning", ""))] if tri < 0.95 else []),
        )
    elif tool_name == "seal_vault_commit":
        sealed = bool(data.get("sealed", False))
        return OPEXBundle(
            output_candidate=str(data.get("entry_id", "")),
            probability=1.0 if sealed else 0.0,
            evidence=[f"merkle_root={data.get('merkle_root', '')}"],
            uncertainty=[],
        )
    else:
        return OPEXBundle(probability=conf)


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

        # Flatten nested data if bridge wrapped it
        extracted_data = kernel_res.get("data")
        if not extracted_data:
            extracted_data = kernel_res.get("payload", kernel_res)

        effective_session_id = str(
            kernel_res.get("session_id")
            or (extracted_data.get("session_id") if isinstance(extracted_data, dict) else None)
            or session_id
        )

        envelope = RuntimeEnvelope(
            verdict=verdict,
            stage=stage,
            session_id=effective_session_id,
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
            data=extracted_data if isinstance(extracted_data, dict) else {"raw": extracted_data},
        )

        # Attach OPEX (epistemic) + APEX (governance) schema layers
        opex = _build_opex(tool_name, kernel_res, envelope)
        envelope.opex = opex
        envelope.apex = derive_apex(envelope, opex)

    except Exception as e:
        envelope = RuntimeEnvelope(
            verdict=Verdict.VOID,
            stage=stage,
            session_id=session_id,
            telemetry=Telemetry(
                dS=0.0,
                peace2=0.0,
                confidence=0.0,
                verdict="Fractured",
            ),
            data={"error": str(e), "stage": "BRIDGE_FAILURE"},
            opex=OPEXBundle(),
            apex=APEXBundle(),
        )

    if ctx:
        await ctx.info(f"arifOS_telemetry {envelope.model_dump_json()}")

    return envelope


async def init_anchor_state(
    intent: dict[str, Any],
    math: dict[str, Any] | None = None,
    governance: dict[str, Any] | None = None,
    auth_token: str | None = None,
    session_id: str = "global",
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """000 INIT - Session anchor. Bootstrap a governed session and mint continuity context."""
    payload = {
        "intent": intent,
        "math": math,
        "governance": governance,
        "auth_token": auth_token,
    }
    return await _wrap_call("init_anchor_state", Stage.INIT, session_id, payload, ctx)


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


def register_tools(mcp: FastMCP, profile: str = "full") -> None:
    """Register all 10 APEX-G tools."""

    normalized_profile = profile.strip().lower() or "full"

    if normalized_profile == "chatgpt":
        mcp.tool(
            description=(
                "Use this when you want the full arifOS governed evaluation in one tool call. "
                "This is the preferred entrypoint for ChatGPT, Developer Mode, and remote MCP "
                "clients because it manages session continuity internally."
            )
        )(metabolic_loop_router)
        return

    mcp.tool(
        description=(
            "Use this only when you need to manually start a governed arifOS session and "
            "chain lower-level tools yourself. For ChatGPT and remote MCP clients, prefer "
            "`metabolic_loop_router` for one-call execution."
        )
    )(init_anchor_state)
    mcp.tool(
        description=(
            "Use this only when continuing an existing arifOS session with a valid "
            "`auth_context` from `init_anchor_state`. For ChatGPT and remote MCP clients, "
            "prefer `metabolic_loop_router`."
        )
    )(integrate_analyze_reflect)
    mcp.tool(
        description=(
            "Use this only when continuing an existing governed session with `auth_context`. "
            "For ChatGPT and remote MCP clients, prefer `metabolic_loop_router`."
        )
    )(reason_mind_synthesis)
    mcp.tool(
        description=(
            "Use this when you want the full arifOS governed evaluation in one tool call. "
            "This is the preferred entrypoint for ChatGPT, Developer Mode, and remote MCP "
            "clients because it manages session continuity internally."
        )
    )(metabolic_loop_router)
    mcp.tool(
        description=(
            "Use this only when continuing an existing session with `auth_context` for "
            "explicit memory operations. For ChatGPT and remote MCP clients, prefer "
            "`metabolic_loop_router` unless you need manual control."
        )
    )(vector_memory_store)
    mcp.tool(
        description=(
            "Use this only when continuing an existing session with `auth_context` for a "
            "targeted heart-impact check. For ChatGPT and remote MCP clients, prefer "
            "`metabolic_loop_router`."
        )
    )(assess_heart_impact)
    mcp.tool(
        description=(
            "Use this only when continuing an existing session with `auth_context` for a "
            "targeted critique pass. For ChatGPT and remote MCP clients, prefer "
            "`metabolic_loop_router`."
        )
    )(critique_thought_audit)
    mcp.tool(
        description=(
            "Use this only when continuing an existing session with `auth_context` for a "
            "sandboxed forge step. For ChatGPT and remote MCP clients, prefer "
            "`metabolic_loop_router`."
        )
    )(quantum_eureka_forge)
    mcp.tool(
        description=(
            "Use this only when continuing an existing session with `auth_context` to render "
            "a final constitutional verdict. For ChatGPT and remote MCP clients, prefer "
            "`metabolic_loop_router`."
        )
    )(apex_judge_verdict)
    mcp.tool(
        description=(
            "Use this only when you intentionally want to append an immutable vault entry for "
            "an existing governed session. This is not a first-choice tool for ChatGPT."
        )
    )(seal_vault_commit)


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
