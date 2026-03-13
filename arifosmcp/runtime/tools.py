from __future__ import annotations

import os
import uuid
from typing import Any

import httpx
from fastmcp import Context, FastMCP
from fastmcp.tools import ToolResult

from arifosmcp.runtime.capability_map import build_runtime_capability_map
from arifosmcp.runtime.models import (
    CallerContext,
    RuntimeEnvelope,
    RuntimeStatus,
    Stage,
    UserModel,
    UserModelField,
    UserModelSource,
    Verdict,
)
from arifosmcp.runtime.philosophy import select_governed_philosophy
from arifosmcp.runtime.public_registry import (
    is_public_profile,
    normalize_tool_profile,
    public_tool_specs,
)
from arifosmcp.runtime.resources import build_open_apex_dashboard_result
from arifosmcp.runtime.sessions import _resolve_session_id, set_active_session
from core.physics.thermodynamics_hardened import get_thermodynamic_report
from core.shared.mottos import MOTTO_000_INIT_HEADER, MOTTO_999_SEAL_HEADER, get_motto_for_stage
from core.state.session_manager import session_manager
from core.telemetry import check_adaptation_status, get_current_hysteresis

from .bridge import call_kernel
from .reality_handlers import handler as reality_handler
from .reality_models import BundleInput, EvidenceBundle, Policy

PUBLIC_TOOL_SPEC_BY_NAME = {spec.name: spec for spec in public_tool_specs()}
PUBLIC_KERNEL_TOOL_NAME = "arifOS_kernel"
LEGACY_KERNEL_TOOL_NAME = "arifOS-kernel"
INTELLIGENCE_PROBE_URLS = {
    "qdrant": ("QDRANT_URL", "/healthz"),
    "ollama": ("OLLAMA_URL", "/api/tags"),
    "openclaw": ("OPENCLAW_URL", "/healthz"),
    "browserless": ("BROWSERLESS_URL", "/pressure"),
}


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


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _infer_failed_floors(envelope_data: dict[str, Any]) -> list[str]:
    failed: list[str] = []

    debug_block = envelope_data.get("debug")
    if isinstance(debug_block, dict):
        law_checks = debug_block.get("law_checks")
        if isinstance(law_checks, dict):
            for law_name, law_result in law_checks.items():
                if not isinstance(law_result, dict):
                    continue
                if law_result.get("required") and not bool(law_result.get("pass")):
                    floor = str(law_name).split("_", 1)[0]
                    if floor.startswith("F") and floor not in failed:
                        failed.append(floor)

    errors_block = envelope_data.get("errors")
    if isinstance(errors_block, list):
        for error in errors_block:
            if not isinstance(error, dict):
                continue
            message = str(error.get("message", ""))
            for floor in ("F1", "F2", "F4", "F7", "F10", "F11", "F12", "F13"):
                if floor in message and floor not in failed:
                    failed.append(floor)

    return failed


def _contains_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(pattern in text for pattern in patterns)


def _build_user_model(
    tool_name: str,
    stage_value: str,
    payload: dict[str, Any],
    envelope_data: dict[str, Any],
) -> UserModel:
    """
    Build a bounded user model from explicit asks and observable runtime signals.

    Anti-Theory-of-Mind rule:
    - Use explicit request text and observable execution facts only.
    - Never infer hidden motives or psychological state.
    """
    raw_query = str(payload.get("query") or payload.get("intent") or "").strip()
    raw_context = str(payload.get("context") or "").strip()
    observed_text = " ".join(part for part in (raw_query, raw_context) if part).lower()

    behavioral_constraints: list[UserModelField] = []
    output_constraints: list[UserModelField] = []

    def add_behavioral_constraint(value: str, evidence: str, source: UserModelSource) -> None:
        if any(field.value == value for field in behavioral_constraints):
            return
        behavioral_constraints.append(UserModelField(value=value, source=source, evidence=evidence))

    def add_output_constraint(value: str, evidence: str, source: UserModelSource) -> None:
        if any(field.value == value for field in output_constraints):
            return
        output_constraints.append(UserModelField(value=value, source=source, evidence=evidence))

    if raw_query:
        stated_goal = UserModelField(
            value=raw_query,
            source=UserModelSource.EXPLICIT,
            evidence="payload.query",
        )
    elif payload.get("intent"):
        stated_goal = UserModelField(
            value=str(payload["intent"]),
            source=UserModelSource.EXPLICIT,
            evidence="payload.intent",
        )
    else:
        stated_goal = UserModelField(
            value=f"Handle tool call for {tool_name}",
            source=UserModelSource.DEFAULT_POLICY,
            evidence="tool_name fallback",
        )

    if _contains_any(observed_text, ("calm", "non-alarmist", "non alarmist")):
        requested_tone = UserModelField(
            value="calm_non_alarmist",
            source=UserModelSource.EXPLICIT,
            evidence="query/context requested calm wording",
        )
    elif stage_value == Stage.HEART_666.value:
        requested_tone = UserModelField(
            value="calm_non_alarmist",
            source=UserModelSource.DEFAULT_POLICY,
            evidence="heart stage default de-escalation policy",
        )
    else:
        requested_tone = None

    if _contains_any(observed_text, ("concise", "brief", "short")):
        add_output_constraint(
            "keep_response_concise",
            "query/context requested concise output",
            UserModelSource.EXPLICIT,
        )
    if _contains_any(
        observed_text,
        ("accessible", "plain english", "plain english", "simple terms", "high-level"),
    ):
        add_output_constraint(
            "define_terms_clearly_and_keep_accessible",
            "query/context requested accessible framing",
            UserModelSource.EXPLICIT,
        )
    if _contains_any(observed_text, ("step by step", "steps", "walk me through")):
        add_output_constraint(
            "present_steps_explicitly",
            "query/context requested step-by-step structure",
            UserModelSource.EXPLICIT,
        )
    if _contains_any(observed_text, ("json", "schema", "table", "structured")):
        add_output_constraint(
            "prefer_structured_output_when_supported",
            "query/context requested structured output",
            UserModelSource.EXPLICIT,
        )

    if stage_value == Stage.HEART_666.value:
        add_behavioral_constraint(
            "optimize_for_dignity_and_harm_reduction",
            "observable stage=666_HEART",
            UserModelSource.OBSERVABLE,
        )
    elif stage_value == Stage.MIND_333.value:
        add_behavioral_constraint(
            "reduce_ambiguity_and_define_terms_clearly",
            "observable stage=333_MIND",
            UserModelSource.OBSERVABLE,
        )
    elif stage_value == Stage.JUDGE_888.value:
        add_behavioral_constraint(
            "state_release_risks_and_responsibility_clearly",
            "observable stage=888_JUDGE",
            UserModelSource.OBSERVABLE,
        )

    meta_block = envelope_data.get("meta")
    if isinstance(meta_block, dict) and bool(meta_block.get("dry_run")):
        add_output_constraint(
            "state_that_execution_is_simulated",
            "observable meta.dry_run=true",
            UserModelSource.OBSERVABLE,
        )

    return UserModel(
        stated_goal=stated_goal,
        behavioral_constraints=behavioral_constraints,
        output_constraints=output_constraints,
        requested_tone=requested_tone,
        expertise_level=None,
        emotion_state=None,
        hidden_motive=None,
    )


def _resolve_motto(stage_value: str) -> str | None:
    if stage_value == Stage.INIT_000.value:
        return MOTTO_000_INIT_HEADER
    if stage_value == Stage.VAULT_999.value:
        return MOTTO_999_SEAL_HEADER

    stage_motto = get_motto_for_stage(stage_value)
    if stage_motto is None:
        return None
    return f"{stage_motto.positive}, {stage_motto.negative}"


def _select_philosophy_payload(
    tool_name: str,
    stage_value: str,
    payload: dict[str, Any],
    envelope_data: dict[str, Any],
) -> dict[str, Any]:
    metrics_block = envelope_data.get("metrics")
    if isinstance(metrics_block, dict):
        g_score = _safe_float(
            metrics_block.get("confidence", metrics_block.get("truth", 0.0)),
            default=0.0,
        )
    else:
        g_score = 0.0

    payload_block = envelope_data.get("payload")
    context_parts = [
        payload.get("query"),
        payload.get("context"),
        payload.get("url"),
        payload.get("source_url"),
        payload.get("intent"),
    ]
    if isinstance(payload_block, dict):
        context_parts.extend(
            [
                payload_block.get("error"),
                payload_block.get("message"),
                payload_block.get("summary"),
            ]
        )

    context_text = (
        " ".join(str(part).strip() for part in context_parts if part).strip() or tool_name
    )
    failed_floors = _infer_failed_floors(envelope_data)
    verdict_value = str(envelope_data.get("verdict") or "SABAR")
    session_value = str(envelope_data.get("session_id") or payload.get("session_id") or "global")

    return select_governed_philosophy(
        context_text,
        stage=stage_value,
        verdict=verdict_value,
        g_score=g_score,
        failed_floors=failed_floors,
        session_id=session_value,
    )


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

        if tool_name in {PUBLIC_KERNEL_TOOL_NAME, LEGACY_KERNEL_TOOL_NAME} and isinstance(
            kernel_res, dict
        ):
            if str(kernel_res.get("tool", "")).strip() == "metabolic_loop":
                kernel_res["tool"] = PUBLIC_KERNEL_TOOL_NAME
            claimed_actor_id = str(
                payload.get("claimed_actor_id", payload.get("actor_id", "anonymous")) or "anonymous"
            )
            payload_block = kernel_res.get("payload")
            if isinstance(payload_block, dict):
                identity_resolution = payload_block.get("identity_resolution")
                if isinstance(identity_resolution, dict) and identity_resolution.get(
                    "input_actor_id"
                ) in {None, "", "anonymous"}:
                    identity_resolution["input_actor_id"] = claimed_actor_id
            errors_block = kernel_res.get("errors")
            if (
                isinstance(errors_block, list)
                and errors_block
                and isinstance(errors_block[0], dict)
                and str(errors_block[0].get("stage", "")) == Stage.INIT_000.value
                and "F11:" in str(errors_block[0].get("message", ""))
            ):
                errors_block[0]["code"] = "AUTH_FAILURE"
        elif tool_name == "init_anchor_state" and isinstance(kernel_res, dict):
            if str(kernel_res.get("tool", "")).strip() == "anchor_session":
                kernel_res["tool"] = tool_name

        # Merge additional runtime metadata if not already present
        if "meta" not in kernel_res:
            from datetime import datetime, timezone

            kernel_res["meta"] = {
                "schema_version": "1.0.0",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "debug": bool(payload.get("debug")),
                "dry_run": bool(payload.get("dry_run")),
            }
        else:
            # Ensure payload flags are reflected even when kernel returns its own meta
            if payload.get("dry_run") and not kernel_res["meta"].get("dry_run"):
                kernel_res["meta"]["dry_run"] = True
            if payload.get("debug") and not kernel_res["meta"].get("debug"):
                kernel_res["meta"]["debug"] = True

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

    resolved_motto = _resolve_motto(envelope.stage)
    if resolved_motto and envelope.meta.motto is None:
        envelope.meta.motto = resolved_motto

    if envelope.philosophy is None:
        envelope.philosophy = _select_philosophy_payload(
            tool_name,
            envelope.stage,
            payload,
            envelope.model_dump(mode="json", exclude_none=True),
        )

    if envelope.user_model is None:
        envelope.user_model = _build_user_model(
            tool_name,
            envelope.stage,
            payload,
            envelope.model_dump(mode="json", exclude_none=True),
        )

    if tool_name == "check_vital":
        envelope.payload["capability_map"] = build_runtime_capability_map()
        envelope.payload.setdefault(
            "message",
            "System vitality and governed capability posture retrieved successfully.",
        )
        envelope.payload.setdefault(
            "operator_note",
            (
                "Read capability_map for configured/disabled/degraded features. "
                "Raw credential values are intentionally never exposed."
            ),
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

    F9 compliance: AI declares execution role, never inherits human apexty.
    """
    from arifosmcp.runtime.models import PersonaId

    base = caller_context or CallerContext()

    if requested_persona and requested_persona.lower() in _PERSONA_WHITELIST:
        governed_persona = PersonaId(requested_persona.lower())
        base = base.model_copy(update={"persona_id": governed_persona})

    return base


async def init_anchor_state(
    intent: dict[str, Any] | None = None,
    math: dict[str, Any] | None = None,
    governance: dict[str, Any] | None = None,
    auth_token: str | None = None,
    session_id: str = "global",
    declared_name: str | None = None,
    human_approval: bool = True,
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
    dry_run: bool = False,
) -> RuntimeEnvelope:
    """000 INIT - Session anchor. Bootstrap identity or mint continuity context."""
    payload: dict[str, Any]

    if declared_name:
        current_session_id = _normalize_session_id(session_id)
        clean_name = declared_name.strip().lower()
        if clean_name in {"arif", "arif fazil", "arif-fazil", "ariffazil"}:
            normalized_actor_id = "ariffazil"
            authority_level = "apex"
        else:
            normalized_actor_id = clean_name.replace(" ", "-")
            authority_level = "declared"

        governance_payload = dict(governance or {})
        governance_payload.update(
            {
                "actor_id": normalized_actor_id,
                "authority_level": authority_level,
                "stakes_class": governance_payload.get("stakes_class", "C"),
                "human_approval": human_approval,
                "token_fingerprint": uuid.uuid4().hex[:16],
            }
        )

        payload = {
            "actor_id": normalized_actor_id,
            "claimed_actor_id": normalized_actor_id,
            "intent": intent or {"query": f"I am {declared_name}"},
            "governance": governance_payload,
            "math": math,
            "auth_token": auth_token,
            "dry_run": dry_run,
        }
        return await _wrap_call(
            "init_anchor_state", Stage.INIT_000, current_session_id, payload, ctx, caller_context
        )

    payload = {
        "intent": intent,
        "math": math,
        "governance": governance,
        "auth_token": auth_token,
        "token_fingerprint": uuid.uuid4().hex[:16],
        "dry_run": dry_run,
    }
    if isinstance(governance, dict) and governance.get("actor_id"):
        payload.setdefault("actor_id", governance.get("actor_id"))
        payload.setdefault("claimed_actor_id", governance.get("actor_id"))

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
    auth_context: dict[str, Any] | None = None,
    use_memory: bool = True,
    use_heart: bool = True,
    use_critique: bool = True,
    allow_execution: bool = False,
    debug: bool = False,
    dry_run: bool = False,
    requested_persona: str | None = None,
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
    session_id: str | None = None,
) -> RuntimeEnvelope:
    payload = {
        "query": query,
        "context": context,
        "risk_tier": risk_tier,
        "actor_id": actor_id,
        "auth_context": auth_context,
        "use_memory": use_memory,
        "use_heart": use_heart,
        "use_critique": use_critique,
        "allow_execution": allow_execution,
        "debug": debug,
        "dry_run": dry_run,
        "requested_persona": requested_persona,
    }
    resolved_caller = _resolve_caller_context(caller_context, requested_persona)
    return await _wrap_call(
        PUBLIC_KERNEL_TOOL_NAME, Stage.ROUTER_444, session_id or "", payload, ctx, resolved_caller
    )


async def session_memory(
    session_id: str,
    operation: str,
    auth_context: dict[str, Any] | None = None,
    content: str | None = None,
    memory_ids: str = "",
    top_k: int = 5,
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """Session memory for conversation state, vector recall, and reasoning artifacts.

    Args:
        memory_ids: Comma-separated list of memory IDs to retrieve/forget.
            Example: "mem-001,mem-002,mem-003". Leave empty for store/search operations.
    """
    # Parse comma-separated memory_ids string into list (Copilot Studio schema-safe)
    parsed_ids: list[str] | None = (
        [mid.strip() for mid in memory_ids.split(",") if mid.strip()] if memory_ids else None
    )
    payload = {
        "operation": operation,
        "content": content,
        "memory_ids": parsed_ids,
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
    """888 JUDGE - APEX verdict. Render the apex constitutional judgment for a session."""
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


async def reality_compass(
    input: str,
    session_id: str = "global",
    actor_id: str = "anonymous",
    authority_level: str = "anonymous",
    mode: str = "auto",
    top_k: int = 5,
    fetch_top_k: int = 2,
    render: str = "auto",
    budget_ms: int = 15000,
    atlas: bool = True,
    policy: dict[str, Any] | None = None,
    debug_profile: str = "none",
    region: str = "MY",
    locale: str = "en-MY",
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """Unified reality entrypoint: query→search, url→fetch. Emits EvidenceBundle."""
    import hashlib

    b_input = BundleInput(
        type="url" if input.startswith(("http://", "https://")) else "query",
        value=input,
        mode=mode,
        top_k=top_k,
        fetch_top_k=fetch_top_k,
        render=render,
        budget_ms=budget_ms,
        policy=Policy(**(policy or {})),
    )
    auth_ctx = {
        "actor_id": actor_id,
        "authority_level": authority_level,
        "token_fingerprint": hashlib.sha256(f"{session_id}:{actor_id}".encode()).hexdigest()[:16],
    }
    bundle = await reality_handler.handle_compass(b_input, auth_ctx)

    # Wrap in RuntimeEnvelope
    return RuntimeEnvelope(
        tool="reality_compass",
        session_id=session_id,
        stage=Stage.SENSE_111.value,
        verdict=bundle.status.verdict,
        status=bundle.status.state,
        payload=bundle.model_dump(mode="json"),
        auth_context=auth_ctx,
    )


async def reality_atlas(
    operation: str,
    session_id: str = "global",
    bundles: list[Any] = [],
    query: dict[str, Any] = {},
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """Build, merge, and query the Reality Atlas over EvidenceBundles."""
    payload = {
        "operation": operation,
        "bundles": bundles,
        "query": query,
    }
    return await _wrap_call("reality_atlas", Stage.REALITY_222, session_id, payload, ctx)


async def search_reality(query: str, ctx: Context | None = None) -> RuntimeEnvelope:
    """Alias to reality_compass(mode='search')."""
    return await reality_compass(input=query, mode="search", ctx=ctx)


async def ingest_evidence(url: str, ctx: Context | None = None) -> RuntimeEnvelope:
    """Alias to reality_compass(mode='fetch')."""
    return await reality_compass(input=url, mode="fetch", ctx=ctx)


async def audit_rules(session_id: str = "global", ctx: Context | None = None) -> RuntimeEnvelope:
    """Constitutional audit. Inspects governance floors and system rules logic."""
    envelope = await _wrap_call("audit_rules", Stage.MIND_333, session_id, {}, ctx)
    # P4: Add floor_runtime_hooks mapping
    if envelope.ok:
        envelope.payload["floor_runtime_hooks"] = {
            "F1_AMANAH": "core.enforcement.reversibility",
            "F2_TRUTH": "arifosmcp.intelligence.fact_checker",
            "F3_TRI_WITNESS": "core.shared.consensus",
            "F4_CLARITY": "core.physics.entropy",
            "F5_PEACE2": "core.shared.vitality",
            "F11_AUTHORITY": "core.enforcement.auth_continuity",
            "F12_DEFENSE": "core.enforcement.injection_scanner",
        }
    return envelope


async def check_vital(session_id: str = "global", ctx: Context | None = None) -> RuntimeEnvelope:
    """Kernel health monitor. Reports system health, metrics, and constitutional vitality."""
    session_id = _normalize_session_id(session_id)
    envelope = await _wrap_call("check_vital", Stage.INIT_000, session_id, {}, ctx)
    envelope.tool = "check_vital"  # Ensure stable external name (Drift fix)

    # Enhance payload with real-time thermo-budget and telemetry (H1.1)
    try:
        # Try to import thermodynamics with graceful fallback
        try:
            from core.physics.thermodynamics_hardened import ThermodynamicViolation

            thermo_available = True
        except ImportError:
            thermo_available = False
            ThermodynamicViolation = Exception  # type: ignore[misc]

        if thermo_available:
            try:
                thermo_report = get_thermodynamic_report(session_id)
            except ThermodynamicViolation:
                thermo_report = {
                    "status": "no_active_budget",
                    "note": "Session has not initialized thermodynamics.",
                }
        else:
            thermo_report = {
                "status": "module_unavailable",
                "note": "Thermodynamics module not loadable in this environment.",
            }

        adaptation = check_adaptation_status()
        hysteresis = get_current_hysteresis()

        envelope.payload.update(
            {
                "thermodynamic_vitality": thermo_report,
                "constitutional_telemetry": {
                    "adaptation_status": adaptation,
                    "hysteresis_penalty": hysteresis,
                },
                "system_status": "HEALTHY",
            }
        )
    except Exception as e:
        envelope.payload["vital_error"] = f"Failed to fetch detailed vitals: {e}"

    envelope.payload["intelligence_services"] = await _probe_intelligence_services()

    return envelope


async def ollama_local_generate(
    prompt: str,
    model: str = "qwen2.5:3b",
    system: str | None = None,
    temperature: float = 0.2,
    max_tokens: int = 512,
    session_id: str = "global",
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """333 MIND - Internal local-model prompt using the Ollama runtime."""
    payload = {
        "prompt": prompt,
        "model": model,
        "system": system,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    return await _wrap_call("ollama_local_generate", Stage.MIND_333, session_id, payload, ctx)


async def _probe_intelligence_services() -> dict[str, dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {}
    async with httpx.AsyncClient(timeout=5.0) as client:
        for service_name, (env_name, path) in INTELLIGENCE_PROBE_URLS.items():
            client_base = os.getenv(env_name, "").strip()
            if service_name == "browserless" and not client_base:
                client_base = "http://headless_browser:3000"
            if not client_base:
                results[service_name] = {"status": "not_configured", "reachable": False}
                continue
            url = f"{client_base.rstrip('/')}{path}"
            try:
                response = await client.get(url)
                payload: dict[str, Any] = {
                    "status": "healthy" if response.status_code < 400 else "degraded",
                    "reachable": response.status_code < 400,
                    "status_code": response.status_code,
                }
                if service_name == "ollama" and response.status_code < 400:
                    try:
                        payload["model_count"] = len(response.json().get("models", []))
                    except ValueError:
                        payload["model_count"] = None
                results[service_name] = payload
            except Exception as exc:
                results[service_name] = {
                    "status": "unreachable",
                    "reachable": False,
                    "error": str(exc),
                }
    return results


async def verify_vault_ledger(
    session_id: str = "global",
    full_scan: bool = True,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """999 VAULT - Verify Merkle chain integrity of the VAULT999 ledger."""
    payload = {"full_scan": full_scan}
    return await _wrap_call("verify_vault_ledger", Stage.VAULT_999, session_id, payload, ctx)


async def office_forge_audit(
    markdown: str,
    session_id: str = "global",
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """777 FORGE - Office Forge Audit. Analyze markdown complexity before rendering.

    F12 Guard: Checks for injection, size limits, and Mermaid complexity.
    Returns a 'Ready to Render' status.
    """
    payload = {"markdown": markdown}
    return await _wrap_call("office_forge_audit", Stage.FORGE_777, session_id, payload, ctx)


async def forge_office_document(
    markdown: str,
    output_mode: str = "pdf",
    theme: str = "default",
    filename: str | None = None,
    session_id: str = "global",
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """888 JUDGE - Office Forge Render. Render professional PDF/PPTX from markdown.

    Hardened render tool using Marp-cli. Requires audited markdown.
    Enforces 2MB limit and 25s timeout.
    """
    payload = {
        "markdown": markdown,
        "output_mode": output_mode,
        "theme": theme,
        "filename": filename,
    }
    return await _wrap_call("forge_office_document", Stage.JUDGE_888, session_id, payload, ctx)


async def open_apex_dashboard(
    session_id: str = "global", ctx: Context | None = None
) -> ToolResult | RuntimeEnvelope:
    """Sovereign monitoring interface. UI dashboard for live metrics and trace visibility."""
    res = build_open_apex_dashboard_result(session_id)
    if res:
        return res
    # Fallback if Prefab not available
    return await _wrap_call("open_apex_dashboard", Stage.VAULT_999, session_id, {}, ctx)


async def _copilot_reality_compass_wrapper(
    input: str,
    session_id: str = "global",
    mode: str = "auto",
    top_k: int = 5,
    fetch_top_k: int = 2,
    budget_ms: int = 15000,
    atlas: bool = True,
) -> RuntimeEnvelope:
    """Unified reality entrypoint: query→search, url→fetch. (Copilot-safe flat surface)"""
    return await reality_compass(
        input=input,
        session_id=session_id,
        mode=mode,
        top_k=top_k,
        fetch_top_k=fetch_top_k,
        budget_ms=budget_ms,
        atlas=atlas,
    )


async def _copilot_kernel_wrapper(
    query: str,
    context: str = "",
    risk_tier: str = "medium",
    actor_id: str = "anonymous",
    use_memory: bool = True,
    use_heart: bool = True,
    use_critique: bool = True,
    allow_execution: bool = False,
    debug: bool = False,
) -> RuntimeEnvelope:
    """arifOS Constitutional Governance Kernel.

    Runs the full constitutional reasoning pipeline (13 floors, VAULT999 ledger,
    Trinity ΔΩΨ) and returns a governed APEX envelope.

    Use this as the primary entrypoint for all non-trivial tasks.
    This is the Copilot Studio-safe surface: flat primitive-only parameters.
    """
    return await metabolic_loop_router(
        query=query,
        context=context,
        risk_tier=risk_tier,
        actor_id=actor_id,
        use_memory=use_memory,
        use_heart=use_heart,
        use_critique=use_critique,
        allow_execution=allow_execution,
        debug=debug,
        auth_context=None,
        caller_context=None,
        ctx=None,
    )


async def revoke_anchor_state(
    session_id: str,
    reason: str,
    revoked_by: str = "sovereign",
    auth_context: dict[str, Any] | None = None,
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """Revoke a session's governance token. F11 Token Lifecycle management."""
    from core.enforcement.auth_continuity import revoke_session

    payload = {
        "operation": "revoke",
        "session_id": session_id,
        "reason": reason,
        "revoked_by": revoked_by,
    }

    result = revoke_session(session_id, reason, revoked_by)

    return RuntimeEnvelope(
        tool="revoke_anchor_state",
        session_id=session_id,
        stage=Stage.INIT_000.value,
        verdict=Verdict.SEAL,
        status="SUCCESS",
        payload={
            "revoked": True,
            "session_id": session_id,
            "reason": reason,
            "revoked_by": revoked_by,
            "message": f"Session {session_id} has been revoked. All subsequent calls will be rejected.",
        },
        auth_context=auth_context,
    )


async def reality_dossier(
    bundles: list[Any],
    session_id: str = "global",
    actor_id: str = "anonymous",
    authority_level: str = "anonymous",
    auth_context: dict[str, Any] | None = None,
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """Build a Reality Dossier from EvidenceBundles.
    Tri-Witness Decoder for F3 compliance.
    Implements 3E Intelligence: Exploration -> Entropy -> Eureka.
    """
    from .reality_dossier import dossier_engine
    from .reality_models import EvidenceBundle

    parsed_bundles: list[EvidenceBundle] = []
    for b in bundles:
        if isinstance(b, EvidenceBundle):
            parsed_bundles.append(b)
        elif isinstance(b, dict):
            parsed_bundles.append(EvidenceBundle(**b))

    dossier_result = await dossier_engine.build_dossier(
        bundles=parsed_bundles,
        session_id=session_id,
        actor_id=actor_id,
        authority_level=authority_level,
    )

    return RuntimeEnvelope(
        tool="reality_dossier",
        session_id=session_id,
        stage=Stage.REALITY_222.value,
        verdict=Verdict.SEAL if dossier_result.status.state == "SUCCESS" else Verdict.PARTIAL,
        status=RuntimeStatus.SUCCESS
        if dossier_result.status.state == "SUCCESS"
        else RuntimeStatus.ERROR,
        machine_status="READY",
        intelligence_stage=dossier_result.intelligence.eureka,
        payload=dossier_result.model_dump(mode="json"),
        auth_context=auth_context,
    )


def register_tools(mcp: FastMCP, profile: str = "full") -> None:
    """Register the core runtime tools; the dashboard app tool is added in resources."""
    from arifosmcp.tools.lsp_tools import register_lsp_tools

    normalized_profile = normalize_tool_profile(profile)
    is_copilot_profile = normalized_profile == "copilot"
    public_surface = is_public_profile(normalized_profile)

    if is_copilot_profile:
        # Copilot Studio profile: flat, schema-safe surface only.
        # Avoids Copilot Studio known issues:
        #   - Reference type inputs (CallerContext, dict|None) silently drop tools
        #   - Array union types (list[str]|None) truncate schemas
        #   - Duplicate tool names confuse the generative orchestrator
        # See: https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-troubleshooting
        copilot_surface = {
            "arifOS_kernel": _copilot_kernel_wrapper,
            "search_reality": search_reality,
            "ingest_evidence": ingest_evidence,
            "session_memory": session_memory,
            "audit_rules": audit_rules,
            "check_vital": check_vital,
        }
        for tool_name, handler in copilot_surface.items():
            spec = PUBLIC_TOOL_SPEC_BY_NAME.get(tool_name)
            if spec:
                mcp.tool(name=spec.name, description=spec.description)(handler)
            else:
                mcp.tool(name=tool_name)(handler)
        # No legacy aliases in copilot profile — avoids orchestrator confusion
        return

    public_tool_handlers = {
        "arifOS_kernel": metabolic_loop_router,
        "search_reality": search_reality,
        "ingest_evidence": ingest_evidence,
        "session_memory": session_memory,
        "audit_rules": audit_rules,
        "check_vital": check_vital,
        "init_anchor_state": init_anchor_state,
        "revoke_anchor_state": revoke_anchor_state,
        "reality_dossier": reality_dossier,
        "verify_vault_ledger": verify_vault_ledger,
    }

    specs = {spec.name: spec for spec in public_tool_specs()}

    for tool_name, handler in public_tool_handlers.items():
        spec = specs.get(tool_name)
        if spec:
            mcp.tool(name=spec.name, description=spec.description)(handler)
        else:
            mcp.tool(name=tool_name)(handler)

    if not public_surface:
        mcp.tool(
            name="office_forge_audit", description="Internal markdown audit for office rendering."
        )(office_forge_audit)
        mcp.tool(
            name="forge_office_document",
            description="Internal office forge renderer for governed PDF/PPTX artifact generation.",
        )(forge_office_document)
        mcp.tool(
            name="ollama_local_generate",
            description="Internal bounded prompt execution against the local Ollama runtime.",
        )(ollama_local_generate)

        from arifosmcp.tools.lsp_tools import register_lsp_tools

        register_lsp_tools(mcp)

    # Legacy aliases — simplified profile matching
    if not public_surface:
        mcp.tool(
            name="arifOS-kernel",
            description=(
                "[Legacy Alias] Use arifOS_kernel instead. Governed metabolic loop orchestrator."
            ),
        )(metabolic_loop_router)

        mcp.tool(
            name="metabolic_loop_router",
            description=(
                "[Legacy Alias] Use arifOS_kernel instead. Governed metabolic loop orchestrator."
            ),
        )(metabolic_loop_router)

    # Legacy tools preserved for internal orchestration
    if normalized_profile == "internal":
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
    "forge_office_document",
    "ingest_evidence",
    "metabolic_loop_router",
    "office_forge_audit",
    "open_apex_dashboard",
    "quantum_eureka_forge",
    "reason_mind_synthesis",
    "register_tools",
    "seal_vault_commit",
    "search_reality",
    "session_memory",
    "verify_vault_ledger",
]
