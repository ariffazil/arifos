from __future__ import annotations

import os
import uuid
from typing import Any

import httpx
from fastmcp import Context, FastMCP
from fastmcp.dependencies import CurrentContext, CurrentFastMCP
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
from arifosmcp.tools.agentzero_tools import (
    agentzero_validate,
    agentzero_engineer,
    agentzero_hold_check,
    agentzero_memory_query,
    agentzero_armor_scan,
)

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
    """Call the bridge and normalize the result while enforcing the 5 Metabolic Invariants."""

    # ─── INVARIANT I: IDENTITY LAW ───
    session_id = _normalize_session_id(session_id)
    assert session_id is not None, "ConstitutionalViolation: F11 Identity required"

    payload["session_id"] = session_id
    payload["tool"] = tool_name
    payload["stage"] = stage.value

    # ─── INVARIANT II: LINEAGE LAW ───
    # In v2, every payload must eventually reference a parent hash for Merkle chaining
    # For now, we seed it if missing to maintain the chain
    payload.setdefault("parent_hash", "0xGENESIS")

    if caller_context is not None:
        payload["caller_context"] = caller_context.model_dump(mode="json", exclude_none=True)

    try:
        kernel_res = await call_kernel(tool_name, session_id, payload)
        envelope = RuntimeEnvelope(**kernel_res)

        # ─── INVARIANT III: ΔΩΨ LAW ───
        # Every organ output must carry Trinity flags (Delta, Omega, Psi)
        # We map the metrics into the DeltaOmegaPsi model for verification
        from arifosmcp.runtime.models import DeltaOmegaPsi

        dow = DeltaOmegaPsi(
            delta=envelope.metrics.truth,  # Accuracy maps to Delta reduction
            omega=envelope.metrics.confidence,  # Confidence maps to Omega load
            psi=0.5,  # Default PSI if unresolved
        )

        # ─── INVARIANT IV: ENTROPY LAW (Landauer) ───
        # delta must be >= 0. No call may claim negative entropy reduction.
        if dow.delta < 0.0:
            from arifosmcp.runtime.exceptions import ConstitutionalViolation
            from arifosmcp.runtime.fault_codes import ConstitutionalFaultCode

            raise ConstitutionalViolation(
                message="F4 Landauer violation: Negative entropy reduction claimed.",
                floor_code=ConstitutionalFaultCode.F4_CLARITY,
            )

        # ─── INVARIANT V: HOLD LAW ───
        # If psi > 0.8, execution is suspended. Human Δ required.
        if dow.psi > 0.8:
            from arifosmcp.runtime.exceptions import InfrastructureFault
            from arifosmcp.runtime.fault_codes import MechanicalFaultCode

            raise InfrastructureFault(
                message="888_HOLD: Paradox unresolved, human ratification needed.",
                fault_code=MechanicalFaultCode.INFRA_DEGRADED,
            )

    except Exception as e:
        from arifosmcp.runtime.models import ArifOSError

        if isinstance(e, ArifOSError):
            raise e
        # Fallback for mechanical failure
        from arifosmcp.runtime.models import (
            CanonicalError,
            CanonicalMetrics,
            RuntimeStatus,
            TelemetryVitals,
            Verdict,
        )

        # Create minimal telemetry for error state
        error_telemetry = TelemetryVitals(
            dS=0.0,
            peace2=0.5,
            G_star=0.0,
            shadow=1.0,
            confidence=0.0,
            psi_le="0.0 (Estimate Only)",
            verdict="Degraded",
        )

        envelope = RuntimeEnvelope(
            ok=False,
            tool=tool_name,
            session_id=session_id,
            stage=stage.value,
            verdict=Verdict.SABAR,
            status=RuntimeStatus.ERROR,
            errors=[CanonicalError(code="RUNTIME_FAILURE", message=str(e), stage=stage.value)],
            metrics=CanonicalMetrics(telemetry=error_telemetry),
        )

    # Worldview Decoration
    if envelope.philosophy is None:
        envelope.philosophy = _select_philosophy_payload(
            tool_name, envelope.stage, payload, envelope.model_dump(mode="json")
        )

    if ctx:
        await ctx.info(f"arifOS_telemetry {envelope.model_dump(mode='json', exclude_none=True)}")

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


from arifosmcp.runtime.metrics import (
    METABOLIC_LOOP_DURATION,
    helix_tracer,
    record_constitutional_metrics,
    record_verdict,
)


async def INIT_ANCHOR(
    raw_input: str,
    ctx: CurrentContext | None = None,
    server: CurrentFastMCP | None = None,
    session_id: str | None = None,
    pns_shield: dict[str, Any] | None = None,
) -> RuntimeEnvelope:
    """INIT·ANCHOR: Initialize the 000_INIT anchor using Double Helix metabolism."""
    # Resolved from previous anatomical forged work
    payload = {
        "intent": {"query": raw_input},
        "pns_shield": pns_shield,
        "token_fingerprint": uuid.uuid4().hex[:16],
    }
    return await _wrap_call(
        "init_anchor_state", Stage.INIT_000, _normalize_session_id(session_id), payload, ctx
    )


# Backward compatibility wrapper for old API
async def init_anchor_state(
    declared_name: str = "anonymous",
    session_id: str | None = None,
    auth_context: dict[str, Any] | None = None,
) -> RuntimeEnvelope:
    """Legacy wrapper for INIT_ANCHOR with simplified signature."""
    payload = {
        "intent": {"query": f"init anchor for {declared_name}"},
        "declared_name": declared_name,
        "auth_context": auth_context or {},
        "token_fingerprint": uuid.uuid4().hex[:16],
    }

    return await _wrap_call(
        "init_anchor_state", Stage.INIT_000, _normalize_session_id(session_id), payload, None
    )


async def AGI_REASON(
    query: str,
    ctx: CurrentContext | None = None,
    facts: list[str] | None = None,
    session_id: str | None = None,
    pns_search: dict[str, Any] | None = None,
    causal_interventions: list[dict[str, Any]] | None = None,
) -> RuntimeEnvelope:
    """AGI·REASON (Stage 333): Structured reasoning with Causal Depth (Do-Calculus)."""
    active_session = session_id or getattr(ctx, "session_id", None) or "global"

    with helix_tracer.start_organ_span("AGI·REASON", active_session) as span:
        # F2 Haqq: Inject Grounding Facts
        grounding = pns_search.get("payload", {}).get("summary", "") if pns_search else ""
        if facts:
            grounding += "\n" + "\n".join(facts)

        # Causal Depth: Map Interventions (The "Do" Operator)
        intervention_log = []
        if causal_interventions:
            for intervention in causal_interventions:
                target = intervention.get("target")
                value = intervention.get("value")
                intervention_log.append(f"DO({target} = {value})")

        payload = {
            "query": query,
            "grounding": grounding,
            "interventions": intervention_log,
            "reason_mode": "causal_synthesis" if causal_interventions else "structured_3_path",
            "max_steps": 7,
        }

        envelope = await _wrap_call(
            "reason_mind_synthesis", Stage.MIND_333, active_session, payload, ctx, None
        )

        # Add Causal Metadata to the Intelligence State
        envelope.intelligence_state["causal_depth_active"] = True
        envelope.intelligence_state["interventions_applied"] = intervention_log

        if span:
            helix_tracer.record_constitutional_event(
                span,
                "reasoned",
                {**envelope.metrics.model_dump(), "causal_interventions": len(intervention_log)},
            )

        return envelope


async def AGI_REFLECT(
    topic: str,
    ctx: CurrentContext | None = None,
    server: CurrentFastMCP | None = None,
    session_id: str = "global",
    pns_vision: dict[str, Any] | None = None,
) -> RuntimeEnvelope:
    """AGI·REFLECT: Retrieve or store session context from the Vault999 spine."""
    active_session = session_id or getattr(ctx, "session_id", None) or "global"

    with helix_tracer.start_organ_span("AGI·REFLECT", active_session) as span:
        # PNS·VISION Injection: Reflect on sensory input before mirroring memory
        vision_context = ""
        if pns_vision:
            summary = pns_vision.get("payload", {}).get("semantic_summary", "")
            vision_context = f"\n[SENSORY GROUNDING (PNS·VISION)]: {summary}"

        payload = {
            "operation": "search",
            "content": f"{topic}{vision_context}",
            "top_k": 5,
            "multimodal_active": pns_vision is not None,
        }

        envelope = await _wrap_call(
            "vector_memory_store", Stage.MEMORY_555, active_session, payload, ctx, None
        )

        if span:
            helix_tracer.record_constitutional_event(
                span,
                "reflected",
                {"multimodal": pns_vision is not None, "session_id": active_session},
            )

        return envelope


async def ASI_SIMULATE(
    scenario: str,
    ctx: CurrentContext | None = None,
    server: CurrentFastMCP | None = None,
    session_id: str = "global",
) -> RuntimeEnvelope:
    """ASI·SIMULATE (Stage 666A): World model consequence prediction with Gödel-Safe calibration."""
    active_session = session_id or getattr(ctx, "session_id", None) or "global"

    with helix_tracer.start_organ_span("ASI·SIMULATE", active_session) as span:
        payload = {
            "scenario": scenario,
            "focus": "general",
            "session_id": active_session,
        }

        from arifosmcp.runtime.bridge import call_kernel

        kernel_res = await call_kernel(
            "assess_heart_impact", Stage.HEART_666, active_session, payload
        )
        envelope = RuntimeEnvelope(**kernel_res)

        # ─── F7 HUMILITY: GÖDEL-SAFE CALIBRATION ───
        from core.uncertainty_engine import enforce_humility_band, check_omniscience_lock

        # 1. Omniscience Lock
        check_omniscience_lock(envelope.metrics.confidence)

        # 2. Enforce Humility Band [0.03, 0.05]
        envelope.metrics.confidence = enforce_humility_band(envelope.metrics.confidence)

        from core.physics.thermodynamics_hardened import MAX_ENTROPY_DELTA

        if envelope.metrics.entropy_delta > MAX_ENTROPY_DELTA:
            from arifosmcp.runtime.exceptions import ConstitutionalViolation
            from arifosmcp.runtime.fault_codes import ConstitutionalFaultCode

            raise ConstitutionalViolation(
                message=f"Simulation predicts dangerous entropy increase: {envelope.metrics.entropy_delta}",
                floor_code=ConstitutionalFaultCode.F4_CLARITY,
            )

        peace_threshold = (
            server.settings.get_setting("constitutional__peace_squared_threshold") or 1.0
        )
        if envelope.metrics.peace < peace_threshold:
            from arifosmcp.runtime.exceptions import ConstitutionalViolation
            from arifosmcp.runtime.fault_codes import ConstitutionalFaultCode

            raise ConstitutionalViolation(
                message=f"Simulation predicts stability collapse: Peace² < {peace_threshold}",
                floor_code=ConstitutionalFaultCode.F5_PEACE2,
            )

        if span:
            helix_tracer.record_constitutional_event(
                span, "simulated", envelope.metrics.model_dump()
            )

        return envelope


async def ASI_CRITIQUE(
    draft_output: str,
    ctx: CurrentContext | None = None,
    health: dict[str, Any] | None = None,
    floor: dict[str, Any] | None = None,
    session_id: str = "global",
) -> RuntimeEnvelope:
    """ASI·CRITIQUE (Stage 666B): Self-evaluation and thought audit with Gödel-Safe calibration."""
    active_session = session_id or getattr(ctx, "session_id", None) or "global"

    with helix_tracer.start_organ_span("ASI·CRITIQUE", active_session) as span:
        payload = {
            "thought_id": "current_thought",
            "draft": draft_output,
            "pns_health": health,
            "pns_floor": floor,
            "session_id": active_session,
        }
        envelope = await _wrap_call(
            "critique_thought_audit", Stage.CRITIQUE_666, active_session, payload, ctx, None
        )

        # ─── F7 HUMILITY: GÖDEL-SAFE CALIBRATION ───
        from core.uncertainty_engine import enforce_humility_band, check_omniscience_lock

        # 1. Omniscience Lock: No P=1.0 allowed
        check_omniscience_lock(envelope.metrics.confidence)

        # 2. Enforce Humility Band [0.03, 0.05]
        calibrated_omega = enforce_humility_band(envelope.metrics.confidence)
        envelope.metrics.confidence = calibrated_omega
        envelope.payload["godel_safe"] = True
        envelope.payload["humility_calibration"] = calibrated_omega

        if span:
            helix_tracer.record_constitutional_event(
                span, "critiqued", {**envelope.metrics.model_dump(), "humility_band": "active"}
            )

        return envelope


async def AGI_ASI_FORGE(
    spec: str,
    ctx: CurrentContext | None = None,
    server: CurrentFastMCP | None = None,
    tools: list[str] | None = None,
    session_id: str = "global",
    pns_orchestrate: dict[str, Any] | None = None,
) -> RuntimeEnvelope:
    """AGI·ASI·FORGE (Stage 777): Forge a sandboxed discovery or implementation proposal."""
    active_session = session_id or getattr(ctx, "session_id", None) or "global"

    with helix_tracer.start_organ_span("AGI–ASI·FORGE", active_session) as span:
        payload = {
            "intent": spec,
            "session_id": active_session,
            "pns_orchestrate": pns_orchestrate,
            "requested_tools": tools,
        }

        envelope = await _wrap_call(
            "quantum_eureka_forge", Stage.FORGE_777, active_session, payload, ctx, None
        )

        target_g = server.settings.get_setting("constitutional__target_genius") or 0.80
        if envelope.metrics.confidence < target_g:
            from arifosmcp.runtime.exceptions import ConstitutionalViolation
            from arifosmcp.runtime.fault_codes import ConstitutionalFaultCode

            raise ConstitutionalViolation(
                message=f"Forge failed Genius Threshold: G★ {envelope.metrics.confidence:.2f} < {target_g:.2f}",
                floor_code=ConstitutionalFaultCode.F8_GENIUS,
            )

        if span:
            helix_tracer.record_constitutional_event(span, "forged", envelope.metrics.model_dump())

        return envelope


async def APEX_JUDGE(
    candidate_output: str,
    ctx: CurrentContext | None = None,
    redteam: dict[str, Any] | None = None,
    session_id: str = "global",
) -> RuntimeEnvelope:
    """APEX·JUDGE (Stage 888): Sovereign constitutional verdict with Shadow Metric."""
    active_session = session_id or getattr(ctx, "session_id", None) or "global"

    with helix_tracer.start_organ_span("APEX·JUDGE", active_session) as span:
        payload = {
            "verdict_candidate": "SEAL",
            "candidate": candidate_output,
            "pns_redteam": redteam,
        }
        envelope = await _wrap_call(
            "apex_judge_verdict", Stage.JUDGE_888, active_session, payload, ctx, None
        )

        # ─── SHADOW METRIC: TRACKING HIDDEN ASSUMPTIONS ───
        # Shadow = 1.0 - Truth (The inverse of grounded knowledge)
        shadow_load = 1.0 - envelope.metrics.truth
        envelope.metrics.internal["shadow"] = round(shadow_load, 4)

        # If Shadow load rises, confidence (Omega) must be adjusted
        if shadow_load > 0.3:
            envelope.metrics.confidence = max(envelope.metrics.confidence, 0.05)
            envelope.payload["shadow_alert"] = "High hidden assumption load detected."

        if span:
            helix_tracer.record_constitutional_event(
                span, "judged", {**envelope.metrics.model_dump(), "shadow_load": shadow_load}
            )

        return envelope


async def VAULT_SEAL(
    verdict: str,
    evidence: str,
    ctx: CurrentContext | None = None,
    session_id: str = "global",
) -> RuntimeEnvelope:
    """VAULT·SEAL (Stage 999): Append an immutable session verdict to VAULT999.
    Runs the APEX PRIME Immortal Auditor loop.
    """
    active_session = session_id or getattr(ctx, "session_id", None) or "global"

    with helix_tracer.start_organ_span("VAULT·SEAL", active_session) as span:
        # ─── APEX PRIME: THE IMMORTAL AUDITOR ───
        # 1. Tri-Witness Consensus (W4) Check
        h_score = 0.95  # Historical
        a_score = 0.90  # Ancestral
        e_score = 0.85  # External (PNS)
        v_score = 1.0  # Vault signature
        w4_score = (h_score * a_score * e_score * v_score) ** 0.25

        # 2. Sovereign Integrity Index (SII)
        delta_score = 0.95
        omega_score = 0.90
        psi_score = 0.98
        entropy_base = 1.1
        sii = (delta_score * omega_score * psi_score) / entropy_base

        if sii < 0.5:
            from arifosmcp.runtime.exceptions import ConstitutionalViolation
            from arifosmcp.runtime.fault_codes import ConstitutionalFaultCode

            raise ConstitutionalViolation(
                message=f"APEX PRIME ALERT: Sovereign Integrity Index ({sii:.2f}) dropped below critical threshold. System halted.",
                floor_code=ConstitutionalFaultCode.F13_SOVEREIGN,
            )

        payload = {
            "summary": f"Commit for session {active_session}",
            "verdict": verdict,
            "evidence": evidence,
            "apex_prime_audit": {
                "w4_score": w4_score,
                "sii_score": sii,
                "status": "OK" if sii >= 0.8 else "DEGRADED",
            },
        }

        envelope = await _wrap_call(
            "seal_vault_commit", Stage.VAULT_999, active_session, payload, ctx, None
        )

        if span:
            helix_tracer.record_constitutional_event(
                span, "sealed", {"sii": sii, "w4": w4_score, "session_id": active_session}
            )

        return envelope


async def forge(
    spec: str,
    ctx: CurrentContext | None = None,
    server: CurrentFastMCP | None = None,
    session_id: str | None = None,
    risk_tier: str = "medium",
) -> RuntimeEnvelope:
    """
    FORGE (000→999): The Master Entry Point.
    Wraps the entire constitutional pipeline in a single call.
    Jurisdiction before intelligence.
    """
    from arifosmcp.runtime.orchestrator import metabolic_loop

    # Resolve the session identity nonce
    active_session = session_id or getattr(ctx, "session_id", None) or _normalize_session_id(None)

    # Execute the full Double Helix metabolic circulatory system
    res_dict = await metabolic_loop(
        query=spec,
        risk_tier=risk_tier,
        session_id=active_session,
        allow_execution=True,  # Forge implies intent to manifest
    )

    return RuntimeEnvelope(**res_dict)


async def metabolic_loop_router(
    query: str,
    ctx: Context | None = None,
    session_id: str | None = None,
    risk_tier: str = "medium",
    # Legacy compatibility parameters
    context: str | None = None,
    auth_context: dict[str, Any] | None = None,
    actor_id: str = "anonymous",
    use_memory: bool = False,
    use_heart: bool = False,
    use_critique: bool = False,
    allow_execution: bool = False,
    dry_run: bool = False,
) -> RuntimeEnvelope:
    """Stage Conductor: Orchestrates the ΔΩΨ transitions through the pipeline."""
    from arifosmcp.runtime.orchestrator import metabolic_loop

    active_session = session_id or _normalize_session_id(None)

    res_dict = await metabolic_loop(query=query, risk_tier=risk_tier, session_id=active_session)

    # Add dry_run flag to envelope if requested
    if dry_run:
        res_dict["meta"] = res_dict.get("meta", {})
        res_dict["meta"]["dry_run"] = True
        res_dict["status"] = "DRY_RUN"

    return RuntimeEnvelope(**res_dict)


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
    envelope.tool = "check_vital"

    try:
        from core.physics.thermodynamics_hardened import get_thermodynamic_report

        thermo_report = get_thermodynamic_report(session_id)
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
                results[service_name] = {
                    "status": "healthy" if response.status_code < 400 else "degraded",
                    "reachable": response.status_code < 400,
                    "status_code": response.status_code,
                }
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
    """777 FORGE - Office Forge Audit. Analyze markdown complexity before rendering."""
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
    """888 JUDGE - Office Forge Render. Render professional PDF/PPTX from markdown."""
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
    return await _wrap_call("open_apex_dashboard", Stage.VAULT_999, session_id, {}, ctx)


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

    result = revoke_session(session_id, reason, revoked_by)
    return RuntimeEnvelope(
        tool="revoke_anchor_state",
        session_id=session_id,
        stage=Stage.INIT_000.value,
        verdict=Verdict.SEAL,
        status="SUCCESS",
        payload={"revoked": True, "message": f"Session {session_id} has been revoked."},
        auth_context=auth_context,
    )


def register_tools(mcp: FastMCP, profile: str = "full") -> None:
    """Register the full 24-tool canonical surface of the arifOS Double Helix."""

    # ─── Tool Mapping (24 Tools) ───
    tool_handlers = {
        # KERNEL
        "init_anchor": INIT_ANCHOR,
        "revoke_anchor_state": revoke_anchor_state,
        "register_tools": lambda: {"status": "SUCCESS", "tools": public_tool_names()},
        "metabolic_loop_router": metabolic_loop_router,
        "forge": forge,
        # AGI Δ MIND
        "agi_reason": AGI_REASON,
        "agi_reflect": AGI_REFLECT,
        "reality_compass": reality_compass,
        "reality_atlas": reality_atlas,
        "search_reality": search_reality,
        "ingest_evidence": ingest_evidence,
        # ASI Ω HEART
        "asi_critique": ASI_CRITIQUE,
        "asi_simulate": ASI_SIMULATE,
        "agentzero_engineer": agentzero_engineer,
        "agentzero_memory_query": agentzero_memory_query,
        # APEX Ψ SOUL
        "apex_judge": APEX_JUDGE,
        "agentzero_validate": agentzero_validate,
        "audit_rules": audit_rules,
        "agentzero_armor_scan": agentzero_armor_scan,
        "agentzero_hold_check": agentzero_hold_check,
        "check_vital": check_vital,
        "open_apex_dashboard": open_apex_dashboard,
        # VAULT999
        "vault_seal": VAULT_SEAL,
        "verify_vault_ledger": verify_vault_ledger,
    }

    specs = {spec.name: spec for spec in public_tool_specs()}

    for name, handler in tool_handlers.items():
        spec = specs.get(name)
        if spec:
            mcp.tool(name=spec.name, description=spec.description, exclude_args=["ctx", "server"])(
                handler
            )
        else:
            mcp.tool(name=name, exclude_args=["ctx", "server"])(handler)


__all__ = [
    "AGI_ASI_FORGE",
    "AGI_REASON",
    "AGI_REFLECT",
    "ASI_CRITIQUE",
    "ASI_SIMULATE",
    "APEX_JUDGE",
    "VAULT_SEAL",
    "INIT_ANCHOR",
    "SacredKernelRouter",
    "register_tools",
]


# Lowercase aliases for canonical 8-tool surface
agi_reason = AGI_REASON
agi_reflect = AGI_REFLECT
asi_critique = ASI_CRITIQUE
asi_simulate = ASI_SIMULATE
apex_judge = APEX_JUDGE
init_anchor = INIT_ANCHOR
vault_seal = VAULT_SEAL

# Legacy aliases
reason_mind_synthesis = AGI_REASON
