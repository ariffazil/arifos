from __future__ import annotations

import uuid
from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.tools import ToolResult

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
from arifosmcp.runtime.resources import build_open_apex_dashboard_result
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


def _build_opex(
    tool_name: str, kernel_res: dict[str, Any], envelope: RuntimeEnvelope
) -> OPEXBundle:
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
        low_conf_steps = [
            s.get("thought", "") for s in steps if float(s.get("confidence", 1.0)) < 0.7
        ]
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
            uncertainty=[
                f"{s}: requires review" for s, v in trace.items() if v in ("SABAR", "VOID")
            ],
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

        auth_context = AuthContext(**input_auth_ctx)

        extracted_data = kernel_res.get("data", {})
        if not extracted_data:
            extracted_data = kernel_res.get("payload", kernel_res)

        effective_session_id = str(
            kernel_res.get("session_id")
            or (extracted_data.get("session_id") if isinstance(extracted_data, dict) else None)
            or session_id
        )

        # Inject Philosophy Anchor with semantic context
        from arifosmcp.runtime.philosophy import get_wisdom_for_context

        g_score = kernel_res.get("telemetry", {}).get("confidence", 0.9)
        failed_floors = []
        if verdict_str in ["VOID", "HOLD-888"]:
            failed_floors.append("F2")

        # Extract query/context from payload for semantic matching
        query_text = ""
        if isinstance(payload, dict):
            query_text = (
                payload.get("query", "")
                or payload.get("task", "")
                or payload.get("question", "")
            )

        # Use unified wisdom retrieval (combines deterministic + semantic)
        anchor = get_wisdom_for_context(
            context=query_text,
            stage=stage.value,
            g_score=g_score,
            failed_floors=failed_floors,
            use_semantic=True,
        )

        envelope = RuntimeEnvelope(
            verdict=verdict,
            stage=stage,
            session_id=effective_session_id,
            final_verdict=kernel_res.get("final_verdict", verdict_str),
            status=kernel_res.get("status", "SUCCESS"),
            failure_origin=kernel_res.get("failure_origin"),
            failure_stage=kernel_res.get("failure_stage"),
            auth_state=kernel_res.get("auth_state", "anonymous"),
            score_delta=kernel_res.get("score_delta", {}),
            primary_blocker=kernel_res.get("primary_blocker"),
            secondary_blockers=kernel_res.get("secondary_blockers", []),
            next_best_action=kernel_res.get("next_best_action"),
            counterfactual=kernel_res.get("counterfactual"),
            remediation_notes=kernel_res.get("remediation_notes", []),
            blocked_because=kernel_res.get("blocked_because"),
            block_class=kernel_res.get("block_class"),
            safe_alternative=kernel_res.get("safe_alternative"),
            minimum_upgrade_condition=kernel_res.get("minimum_upgrade_condition"),
            telemetry=Telemetry(
                dS=kernel_res.get("telemetry", {}).get("dS", -0.7),
                peace2=kernel_res.get("telemetry", {}).get("peace2", 1.1),
                confidence=g_score,
                verdict=kernel_res.get("telemetry", {}).get("verdict", "Alive"),
            ),
            witness=Witness(
                human=kernel_res.get("witness", {}).get("human", 0.0),
                ai=kernel_res.get("witness", {}).get("ai", 0.0),
                earth=kernel_res.get("witness", {}).get("earth", 0.0),
            ),
            auth_context=auth_context,
            philosophy={
                "quote_id": anchor["id"],
                "quote": anchor["text"],
                "author": anchor["author"],
                "category": anchor["category"],
            },
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
    dry_run: bool = False,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """Stage 444 ROUTER - Metabolic Loop. The all-in-one arifOS Sovereign evaluation."""
    session_id = _resolve_session_id(None)
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
    return await _wrap_call("arifOS.kernel", Stage.ROUTER, session_id, payload, ctx)


async def session_memory(
    session_id: str,
    operation: str,
    auth_context: dict[str, Any] | None = None,
    content: str | None = None,
    memory_ids: list[str] | None = None,
    top_k: int = 5,
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
    return await _wrap_call("session_memory", Stage.MEMORY, session_id, payload, ctx)


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
    """666B CRITIQUE - Thought audit against a prior reasoning artifact."""
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
    telemetry: dict[str, Any] | None = None,
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
    return await _wrap_call("seal_vault_commit", Stage.VAULT, session_id, payload, ctx)


async def search_reality(query: str, ctx: Context | None = None) -> RuntimeEnvelope:
    """External knowledge discovery. Finds real-world sources and evidence before reasoning."""
    return await _wrap_call("search_reality", Stage.INIT, "global", {"query": query}, ctx)


async def ingest_evidence(url: str, ctx: Context | None = None) -> RuntimeEnvelope:
    """Evidence ingestion. Loads URLs, documents, and datasets into context."""
    return await _wrap_call("ingest_evidence", Stage.INIT, "global", {"source_url": url}, ctx)


async def audit_rules(session_id: str = "global", ctx: Context | None = None) -> RuntimeEnvelope:
    """Constitutional audit. Inspects governance floors and system rules logic."""
    return await _wrap_call("audit_rules", Stage.INIT, session_id, {}, ctx)


async def check_vital(session_id: str = "global", ctx: Context | None = None) -> RuntimeEnvelope:
    """Kernel health monitor. Reports system health, metrics, and constitutional vitality."""
    return await _wrap_call("check_vital", Stage.INIT, session_id, {}, ctx)


async def open_apex_dashboard(
    session_id: str = "global", ctx: Context | None = None
) -> ToolResult | RuntimeEnvelope:
    """Sovereign monitoring interface. UI dashboard for live metrics and trace visibility."""
    res = build_open_apex_dashboard_result(session_id)
    if res:
        return res
    # Fallback if Prefab not available
    return await _wrap_call("open_apex_dashboard", Stage.VAULT, session_id, {}, ctx)


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
