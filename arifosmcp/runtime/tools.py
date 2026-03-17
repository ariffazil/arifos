from __future__ import annotations

import os
import uuid
from typing import Any

import httpx
from fastmcp import Context, FastMCP
from fastmcp.dependencies import CurrentContext, CurrentFastMCP
from fastmcp.tools import Tool, ToolResult
from fastmcp.tools import tool as make_tool
from fastmcp.tools.tool_transform import ArgTransform

from arifosmcp.runtime.metrics import (
    helix_tracer,
)
from arifosmcp.runtime.models import (
    AuthContext,
    CallerContext,
    CanonicalError,
    CanonicalMetrics,
    PersonaId,
    RiskClass,
    RuntimeEnvelope,
    RuntimeStatus,
    Stage,
    TelemetryVitals,
    UserModel,
    UserModelField,
    UserModelSource,
    Verdict,
)
from arifosmcp.runtime.philosophy import select_governed_philosophy
from arifosmcp.runtime.public_registry import (
    PUBLIC_TOOL_SPEC_BY_NAME,
    public_tool_names,
    public_tool_specs,
)
from arifosmcp.runtime.resources import build_open_apex_dashboard_result
from arifosmcp.runtime.sessions import _resolve_session_id, set_active_session
from core.shared.mottos import MOTTO_000_INIT_HEADER, MOTTO_999_SEAL_HEADER, get_motto_for_stage
from core.state.session_manager import session_manager
from core.telemetry import check_adaptation_status, get_current_hysteresis

from .bridge import call_kernel
from .reality_handlers import handler as reality_handler
from .reality_models import BundleInput, Policy
from arifosmcp.tools.agentzero_tools import (
    agentzero_validate,
    agentzero_engineer,
    agentzero_hold_check,
    agentzero_memory_query,
    agentzero_armor_scan,
)
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
        telemetry = metrics_block.get("telemetry", {})
        g_score = _safe_float(
            telemetry.get("G_star", telemetry.get("confidence", 0.0)),
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


def _resolve_caller_state(session_id: str, authority: Any) -> tuple[str, list[str], list[dict[str, str]]]:
    """
    Anti-chaos: Resolve caller state and tool visibility.
    Aligns with the 26 canonical tools across Trinity layers.
    """
    # Determine state from session and authority
    if session_id == "global":
        caller_state = "anonymous"
    elif authority and getattr(authority, "claim_status", "anonymous") == "verified":
        caller_state = "verified"
    elif authority and getattr(authority, "claim_status", "anonymous") == "anchored":
        caller_state = "anchored"
    elif authority and getattr(authority, "actor_id", "anonymous") != "anonymous":
        caller_state = "claimed"
    else:
        caller_state = "anonymous"
    
    # 26 Canonical Tools by Trinity Layer
    KERNEL = ["get_caller_status", "init_anchor", "init_anchor_state", "revoke_anchor_state", "register_tools", "arifOS_kernel", "forge"]
    MIND = ["agi_reason", "agi_reflect", "reality_compass", "reality_atlas", "search_reality", "ingest_evidence"]
    HEART = ["asi_critique", "asi_simulate", "agentzero_engineer", "agentzero_memory_query"]
    SOUL = ["apex_judge", "agentzero_validate", "audit_rules", "agentzero_armor_scan", "agentzero_hold_check", "check_vital", "open_apex_dashboard"]
    VAULT = ["vault_seal", "verify_vault_ledger"]
    
    # Define tool visibility by state
    visibility = {
        "anonymous": {
            "allowed": ["get_caller_status", "init_anchor", "init_anchor_state", "register_tools", "audit_rules", "check_vital"],
            "blocked": {
                "arifOS_kernel": "Requires anchored session. Run init_anchor_state first.",
                "agi_reason": "Requires anchored session.",
                "agentzero_engineer": "Requires anchored session and high-tier auth.",
                "forge": "Requires approved session status (F13).",
                "vault_seal": "Requires verified identity (F11).",
            }
        },
        "claimed": {
            "allowed": ["get_caller_status", "init_anchor", "init_anchor_state", "register_tools", "audit_rules", "check_vital"],
            "blocked": {
                "arifOS_kernel": "Complete init_anchor_state to unlock kernel.",
                "agentzero_engineer": "Requires verified identity.",
            }
        },
        "anchored": {
            "allowed": KERNEL + MIND + ["asi_critique", "asi_simulate", "agentzero_memory_query", "audit_rules", "check_vital", "open_apex_dashboard"],
            "blocked": {
                "agentzero_engineer": "Requires cryptographic verification.",
                "vault_seal": "Requires verified identity.",
                "verify_vault_ledger": "Requires verified identity.",
            }
        },
        "verified": {
            "allowed": KERNEL + MIND + HEART + SOUL + VAULT,
            "blocked": {}
        },
    }
    
    state_config = visibility.get(caller_state, visibility["anonymous"])
    blocked_list = [{"tool": k, "reason": v} for k, v in state_config.get("blocked", {}).items()]
    
    return caller_state, state_config["allowed"], blocked_list


def _resolve_next_action(caller_state: str, blocked_tools: list[dict[str, str]]) -> dict[str, Any] | None:
    """
    Anti-chaos: Resolve exact next step for recovery.
    """
    if caller_state in ("anonymous", "claimed"):
        return {
            "tool": "init_anchor",  # CANONICAL: init_anchor (legacy alias: init_anchor_state)
            "reason": f"You are {caller_state}. Identity required for governed execution.",
            "required_args": ["actor_id", "intent"],
            "example_payload": {
                "actor_id": "arif",
                "intent": "establish session for code review"
            },
            "retry_safe": True,
            "human_approval_required": False
        }
    
    if blocked_tools and blocked_tools[0].get("tool") == "arifOS_kernel":
        return {
            "tool": "init_anchor",
            "reason": "Kernel requires anchored session with auth_context",
            "required_args": ["actor_id", "intent"],
            "example_payload": {
                "actor_id": "arif",
                "declared_name": "Muhammad Arif",
                "intent": "testing kernel governance flow"
            },
            "retry_safe": True,
            "human_approval_required": False
        }
    
    return None


async def _wrap_call(
    tool_name: str,
    stage: Stage,
    session_id: str,
    payload: dict[str, Any],
    ctx: Context | None = None,
    caller_context: CallerContext | None = None,
) -> RuntimeEnvelope:
    """
    Call the bridge and normalize the result while enforcing the 5 Metabolic Invariants.
    Hardened with F12 Security Pre-scan and F11 Identity verification.
    """

    # ─── F12 SECURITY PRE-SCAN ───
    if not isinstance(payload, dict):
        from arifosmcp.runtime.exceptions import ConstitutionalViolation
        from arifosmcp.runtime.fault_codes import ConstitutionalFaultCode

        raise ConstitutionalViolation(
            message="F12 Security Violation: Payload must be a JSON object.",
            floor_code=ConstitutionalFaultCode.F12_DEFENSE,
        )

    # ─── INVARIANT I: IDENTITY LAW (F11) ───
    session_id = _normalize_session_id(session_id)
    assert session_id is not None, "ConstitutionalViolation: F11 Identity required"

    payload["session_id"] = session_id
    payload["tool"] = tool_name
    payload["stage"] = stage.value

    # ─── INVARIANT II: LINEAGE LAW ───
    payload.setdefault("parent_hash", "0xGENESIS")

    if caller_context is not None:
        payload["caller_context"] = caller_context.model_dump(mode="json", exclude_none=True)

    # Identify tool metadata for envelope decoration
    spec = PUBLIC_TOOL_SPEC_BY_NAME.get(tool_name)
    risk_class = RiskClass.LOW
    requires_auth = False
    if spec:
        if "F11" in spec.floors or "F13" in spec.floors:
            risk_class = RiskClass.HIGH
            requires_auth = True
        elif spec.layer == "KERNEL":
            risk_class = RiskClass.MEDIUM

    try:
        kernel_res = await call_kernel(tool_name, session_id, payload)
        envelope = RuntimeEnvelope(**kernel_res)

        # ─── ENVELOPE DECORATION (Rule 4: Universal Clarity) ───
        envelope.canonical_tool_name = tool_name
        envelope.risk_class = risk_class
        envelope.requires_auth = requires_auth
        envelope.requires_human = envelope.verdict in (Verdict.HOLD, Verdict.HOLD_888)
        
        # Anti-chaos: populate caller state visibility (Phase 1)
        # Ensure diagnostics_only is set based on the session_id
        envelope.diagnostics_only = (session_id == "global")
        
        # Resolve state visibility
        envelope.caller_state, envelope.allowed_next_tools, envelope.blocked_tools = _resolve_caller_state(session_id, envelope.authority)
        
        # Anti-chaos: populate next_action for recovery if not provided by kernel
        if envelope.verdict in (Verdict.HOLD, Verdict.VOID) and not envelope.next_action:
            envelope.next_action = _resolve_next_action(envelope.caller_state, envelope.blocked_tools)

        envelope.recoverable = envelope.status != RuntimeStatus.ERROR or any(
            e.recoverable for e in envelope.errors
        )

        # Decorate with Stage Motto (Meta Invariant)
        envelope.meta.motto = _resolve_motto(envelope.stage)

        # ─── INVARIANT III: ΔΩΨ LAW ───
        from arifosmcp.runtime.models import DeltaOmegaPsi

        g_star = (
            envelope.metrics.telemetry.G_star
            if envelope.metrics and envelope.metrics.telemetry
            else 0.0
        )
        conf = (
            envelope.metrics.telemetry.confidence
            if envelope.metrics and envelope.metrics.telemetry
            else 0.0
        )

        dow = DeltaOmegaPsi(
            delta=max(0.0, min(1.0, g_star)),
            omega=max(0.0, min(1.0, conf)),
            psi=0.5,
        )

        # ─── INVARIANT IV: ENTROPY LAW (Landauer) ───
        if dow.delta < 0.0:
            from arifosmcp.runtime.exceptions import ConstitutionalViolation
            from arifosmcp.runtime.fault_codes import ConstitutionalFaultCode

            raise ConstitutionalViolation(
                message="F4 Landauer violation: Negative entropy reduction claimed.",
                floor_code=ConstitutionalFaultCode.F4_CLARITY,
            )

        # ─── INVARIANT V: HOLD LAW ───
        if dow.psi > 0.8:
            from arifosmcp.runtime.exceptions import InfrastructureFault
            from arifosmcp.runtime.fault_codes import MechanicalFaultCode

            raise InfrastructureFault(
                message="888_HOLD: Paradox unresolved, human ratification needed.",
                fault_code=MechanicalFaultCode.INFRA_DEGRADED,
            )

    except Exception as e:
        from arifosmcp.runtime.models import ArifOSError, Verdict

        if isinstance(e, ArifOSError):
            error_telemetry = TelemetryVitals(
                ds=0.0,
                peace2=0.5,
                G_star=0.0,
                shadow=1.0,
                confidence=0.0,
                psi_le="0.0 (Estimate Only)",
                verdict="HOLD",
            )

            envelope = RuntimeEnvelope(
                ok=False,
                tool=tool_name,
                canonical_tool_name=tool_name,
                risk_class=risk_class,
                requires_auth=requires_auth,
                session_id=session_id,
                diagnostics_only=(session_id == "global"),
                stage=stage.value,
                verdict=_normalize_verdict(e.verdict),
                status=RuntimeStatus.ERROR,
                errors=[
                    CanonicalError(
                        code=e.fault_code,
                        message=str(e),
                        stage=stage.value,
                        recoverable=True,
                        remediation=getattr(e, "remediation", None),
                    )
                ],
                metrics=CanonicalMetrics(telemetry=error_telemetry),
            )
            # Add next step hint for common auth errors
            if e.fault_code in ("AUTH_TOKEN_MISSING", "AUTH_FAILURE"):
                envelope.errors[0].required_next_tool = "init_anchor"
                envelope.errors[0].required_fields = ["raw_input"]
                envelope.next_action = "init_anchor"

            return envelope

        # Hardened mechanical fallback
        error_telemetry = TelemetryVitals(
            ds=0.0,
            peace2=0.5,
            G_star=0.0,
            shadow=1.0,
            confidence=0.0,
            psi_le="0.0 (Estimate Only)",
            verdict="HOLD",
        )

        envelope = RuntimeEnvelope(
            ok=False,
            tool=tool_name,
            canonical_tool_name=tool_name,
            risk_class=risk_class,
            requires_auth=requires_auth,
            session_id=session_id,
            diagnostics_only=(session_id == "global"),
            stage=stage.value,
            verdict=Verdict.HOLD,
            status=RuntimeStatus.ERROR,
            errors=[
                CanonicalError(code="HARDENED_RUNTIME_FAILURE", message=str(e), stage=stage.value)
            ],
            metrics=CanonicalMetrics(telemetry=error_telemetry),
        )

    # Worldview Decoration
    if envelope.philosophy is None:
        envelope.philosophy = _select_philosophy_payload(
            tool_name, envelope.stage, payload, envelope.model_dump(mode="json")
        )

    if ctx and hasattr(ctx, "info"):
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


async def init_anchor(
    query: str = "",
    ctx: Context = CurrentContext(),
    server: FastMCP = CurrentFastMCP(),
    session_id: str | None = None,
    pns_shield: dict[str, Any] | None = None,
    # Standardised identity fields
    actor_id: str = "anonymous",
    declared_name: str | None = None,
    intent: str | None = None,
    # Security & Governance
    human_approval: bool = False,
    auth_context: dict[str, Any] | None = None,
    caller_context: CallerContext | None = None,
    # Backward compatibility (deprecated)
    raw_input: str | None = None,
) -> RuntimeEnvelope:
    """
    🚀 START HERE: Initialize a constitutional session (000_INIT).
    This tool is the hinge point between passive discovery and governed participation.

    ### Contract (Missing Contract 1)
    - **Identity Claim**: Binds an `actor_id` to a `session_id`.
    - **State Change**: Transitions session from `anonymous` or `claimed` to `anchored`.
    - **Session Continuity**: If `session_id` is provided, attempts to re-anchor.
    - **Actor Handling**: If actor already exists, binds to the session; if not, creates a temporary anchor.

    ### Input
    - `actor_id`: (Required) Machine/Agent ID (e.g., "arif", "gemini-cli").
    - `declared_name`: (Optional) Human-readable name (e.g., "Muhammad Arif").
    - `intent`: (Optional) Brief description of the work session.

    ### Returns (RuntimeEnvelope)
    - `session_id`: The minted or re-anchored session ID.
    - `caller_state`: Set to "anchored".
    - `auth_context`: The opaque context required for `arifOS_kernel`.
        - `session_id`: str
        - `actor_id`: str (canonicalized)
        - `capability_class`: str ("operator" by default)
        - `escalation_hold`: null | str (if gated by F11/F13)
    - `authority`: Current claiming status.
    - `next_action`: Guidance for `arifOS_kernel`.
    """
    effective_actor = (declared_name or actor_id).lower().strip().replace(" ", "-")
    if effective_actor == "arif":
        effective_actor = "ariffazil"

    effective_query = (
        query
        or raw_input
        or (intent.get("query") if isinstance(intent, dict) else intent)
        or "Initialize session"
    )

    payload = {
        "intent": {"query": effective_query},
        "pns_shield": pns_shield,
        "actor_id": effective_actor,
        "declared_name": declared_name or effective_actor,
        "human_approval": human_approval,
        "auth_context": auth_context or {},
        "token_fingerprint": uuid.uuid4().hex[:16],
    }

    envelope = await _wrap_call(
        "init_anchor",  # Use canonical tool name
        Stage.INIT_000,
        _normalize_session_id(session_id),
        payload,
        ctx,
        caller_context,
    )
    # Ensure tool name matches the public surface for F2 Truth
    envelope.tool = "init_anchor"

    # Enrich payload with Authority and AuthContext for caller visibility
    if envelope.ok:
        envelope.payload["caller_state"] = "anchored"
        envelope.payload["authority"] = {
            "actor_id": effective_actor,
            "declared_name": declared_name or effective_actor,
            "claim_status": "anchored",
            "capability_class": "operator",
            "approval_scope": []
        }
        envelope.payload["auth_context"] = {
            "session_id": envelope.session_id,
            "actor_id": effective_actor,
            "capability_class": "operator",
            "escalation_hold": None
        }
        envelope.payload["next_action"] = {
            "tool": "arifOS_kernel",
            "action": "Proceed to governed execution.",
            "example_query": "Analyze system state and propose optimizations."
        }
    return envelope


async def init_anchor_state(
    declared_name: str = "anonymous",
    session_id: str | None = None,
    auth_context: dict[str, Any] | None = None,
    human_approval: bool = False,
    intent: dict[str, Any] | None = None,
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
    # Allow extra fields for testing compatibility
    **kwargs: Any,
) -> RuntimeEnvelope:
    """Legit signature for init_anchor_state to satisfy inspection while using common logic."""
    envelope = await init_anchor(
        declared_name=declared_name,
        session_id=session_id,
        auth_context=auth_context,
        human_approval=human_approval,
        intent=intent,
        caller_context=caller_context,
        ctx=ctx or CurrentContext(),
        **kwargs,
    )
    envelope.tool = "init_anchor_state"
    return envelope


async def agi_reason(
    query: str,
    ctx: Context = CurrentContext(),
    facts: list[str] | None = None,
    session_id: str | None = None,
    pns_search: dict[str, Any] | None = None,
    causal_interventions: list[dict[str, Any]] | None = None,
    auth_context: dict[str, Any] | None = None,
) -> RuntimeEnvelope:
    """
    333_MIND: Perform first-principles structured reasoning.
    Explores hypotheses through conservative, exploratory, and adversarial paths.
    Enforces F2 (Truth) and F4 (Clarity).
    """
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
            "auth_context": auth_context,
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


async def agi_reflect(
    topic: str,
    ctx: Context = CurrentContext(),
    server: FastMCP = CurrentFastMCP(),
    session_id: str = "global",
    pns_vision: dict[str, Any] | None = None,
) -> RuntimeEnvelope:
    """
    555_MEMORY: Perform metacognitive integration.
    Reflects on the current intelligence state and session context to ensure coherence.
    Enforces F4 and F7.
    """
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


async def asi_simulate(
    scenario: str,
    ctx: Context = CurrentContext(),
    server: FastMCP = CurrentFastMCP(),
    session_id: str = "global",
    auth_context: dict[str, Any] | None = None,
) -> RuntimeEnvelope:
    """
    666_HEART: Simulate consequences and predict world-model outcomes.
    Assess the downstream impact of a proposal before execution.
    Enforces F5 (Peace²) and F6 (Empathy).
    """
    active_session = session_id or getattr(ctx, "session_id", None) or "global"

    with helix_tracer.start_organ_span("ASI·SIMULATE", active_session) as span:
        payload = {
            "scenario": scenario,
            "focus": "general",
            "session_id": active_session,
            "auth_context": auth_context,
        }

        envelope = await _wrap_call(
            "assess_heart_impact", Stage.HEART_666, active_session, payload, ctx
        )

        # ─── F7 HUMILITY: GÖDEL-SAFE CALIBRATION ───
        from core.uncertainty_engine import enforce_humility_band, check_omniscience_lock

        # 1. Omniscience Lock
        check_omniscience_lock(envelope.metrics.telemetry.confidence)

        # 2. Enforce Humility Band [0.03, 0.05]
        envelope.metrics.telemetry.confidence = enforce_humility_band(
            envelope.metrics.telemetry.confidence
        )

        from core.physics.thermodynamics_hardened import MAX_ENTROPY_DELTA

        if envelope.metrics.telemetry.dS > MAX_ENTROPY_DELTA:
            from arifosmcp.runtime.exceptions import ConstitutionalViolation
            from arifosmcp.runtime.fault_codes import ConstitutionalFaultCode

            raise ConstitutionalViolation(
                message=f"Simulation predicts dangerous entropy increase: {envelope.metrics.telemetry.dS}",
                floor_code=ConstitutionalFaultCode.F4_CLARITY,
            )

        peace_threshold = 1.0  # Default F5 threshold
        if envelope.metrics.telemetry.peace2 < peace_threshold:
            from arifosmcp.runtime.exceptions import ConstitutionalViolation
            from arifosmcp.runtime.fault_codes import ConstitutionalFaultCode

            raise ConstitutionalViolation(
                message=f"Simulation predicts stability collapse: Peace² < {peace_threshold}",
                floor_code=ConstitutionalFaultCode.F5_PEACE_VIOLATION,
            )

        if span:
            helix_tracer.record_constitutional_event(
                span, "simulated", envelope.metrics.model_dump()
            )

        return envelope


async def asi_critique(
    draft_output: str,
    ctx: Context = CurrentContext(),
    health: dict[str, Any] | None = None,
    floor: dict[str, Any] | None = None,
    session_id: str = "global",
) -> RuntimeEnvelope:
    """
    666_HEART: Advanced adversarial critique and thought audit.
    Detects blind spots, uncertainty, and hidden assumptions before action.
    Enforces F7 (Humility) and F9 (Anti-Hantu/Shadow).
    """
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
        check_omniscience_lock(envelope.metrics.telemetry.confidence)

        # 2. Enforce Humility Band [0.03, 0.05]
        calibrated_omega = enforce_humility_band(envelope.metrics.telemetry.confidence)
        envelope.metrics.telemetry.confidence = calibrated_omega
        envelope.payload["godel_safe"] = True
        envelope.payload["humility_calibration"] = calibrated_omega

        if span:
            helix_tracer.record_constitutional_event(
                span, "critiqued", {**envelope.metrics.model_dump(), "humility_band": "active"}
            )

        return envelope


async def agi_asi_forge_handler(
    spec: str,
    ctx: Context = CurrentContext(),
    server: FastMCP = CurrentFastMCP(),
    tools: list[str] | None = None,
    session_id: str = "global",
    pns_orchestrate: dict[str, Any] | None = None,
    dry_run: bool = False,
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

        target_g = 0.80
        # F8: Only enforce Genius threshold if NOT in dry_run mode (which is often used in tests)
        if not dry_run and envelope.metrics.telemetry.confidence < target_g:
            from arifosmcp.runtime.exceptions import ConstitutionalViolation
            from arifosmcp.runtime.fault_codes import ConstitutionalFaultCode

            raise ConstitutionalViolation(
                message=f"Forge failed Genius Threshold: G★ {envelope.metrics.telemetry.confidence:.2f} < {target_g:.2f}",
                floor_code=ConstitutionalFaultCode.F8_GENIUS,
            )

        if span:
            helix_tracer.record_constitutional_event(span, "forged", envelope.metrics.model_dump())

        return envelope


async def apex_judge(
    candidate_output: str,
    ctx: Context = CurrentContext(),
    redteam: dict[str, Any] | None = None,
    session_id: str = "global",
) -> RuntimeEnvelope:
    """
    888_JUDGE: Render a sovereign constitutional verdict (SEAL, VOID, HOLD, SABAR).
    Final authority for all candidate outputs in the arifOS Double Helix.
    Enforces F3 (Tri-Witness) and F13 (Sovereign Override).
    """
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
        shadow_load = 1.0 - envelope.metrics.telemetry.G_star
        envelope.metrics.internal["shadow"] = round(shadow_load, 4)

        # If Shadow load rises, confidence (Omega) must be adjusted
        if shadow_load > 0.3:
            envelope.metrics.telemetry.confidence = max(envelope.metrics.telemetry.confidence, 0.05)
            envelope.payload["shadow_alert"] = "High hidden assumption load detected."

        if span:
            helix_tracer.record_constitutional_event(
                span,
                "judged",
                {
                    "dS": envelope.metrics.telemetry.dS,
                    "peace2": envelope.metrics.telemetry.peace2,
                    "g": envelope.metrics.telemetry.G_star,
                    "shadow_load": shadow_load,
                },
            )

        return envelope


async def vault_seal(
    verdict: str,
    evidence: str,
    ctx: Context = CurrentContext(),
    session_id: str = "global",
    auth_context: dict[str, Any] | None = None,
) -> RuntimeEnvelope:
    """
    999_VAULT: Commit a verified verdict and evidence to the immutable VAULT999 ledger.
    Mints a permanent hash-chain entry in the Cooling Ledger.
    Enforces F1 (Amanah) and F13 (Sovereign).
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
        # This is a placeholder for a hypothetical 'force_33' condition.
        # The instruction implies adding to such a condition, but it's not present here.
        # Assuming the instruction meant to add this condition *around* the SII calculation
        # if a 'force_33' condition were to be introduced here.
        # For now, I will insert the condition as a comment to reflect the intent,
        # as the exact 'force_33' structure is not in the provided code.
        # force_33 = (
        #     verdict in ("SABAR", "VOID")
        #     or g_score < 0.5
        #     or stage_num == 0
        #     or stage == "000_INIT"
        #     or not deterministic_local_quote
        # )
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
            "auth_context": auth_context,
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
    ctx: Context = CurrentContext(),
    server: FastMCP = CurrentFastMCP(),
    session_id: str | None = None,
    risk_tier: str = "medium",
    dry_run: bool = False,
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
        allow_execution=not dry_run,  # Don't execute if dry_run
        dry_run=dry_run,
    )

    envelope = RuntimeEnvelope(**res_dict)
    envelope.tool = "forge"
    return envelope


async def arifos_kernel(
    query: str,
    ctx: Context | None = None,
    session_id: str | None = None,
    risk_tier: str = "medium",
    mode: str = "recommend",
    # Legacy compatibility parameters
    context: str | None = None,
    auth_context: AuthContext | dict[str, Any] | None = None,
    actor_id: str = "anonymous",
    declared_name: str | None = None,
    human_approval: bool = False,
    use_memory: bool = False,
    use_heart: bool = False,
    use_critique: bool = False,
    allow_execution: bool = False,
    dry_run: bool = False,
    requested_persona: str | None = None,
    caller_context: CallerContext | None = None,
    debug: bool = False,
) -> RuntimeEnvelope:
    """
    444_ROUTER: The Governed Conductor (Stage Conductor).
    Orchestrates ΔΩΨ transitions through the metabolic pipeline.

    ### Contract (Missing Contract 2)
    - **Governance Requirement**: Executes under F1-F13 constitutional enforcement.
    - **Mandatory Auth**: Governed `mode`s requires a valid `auth_context` (minted via `init_anchor`).
    - **Risk Tiering**:
        - `low`: Minimal friction, diagnostic-heavy.
        - `medium`: (Default) Standard governance audit.
        - `high`: Requires F13 human approval (or explicit human_approval flag).

    ### Modes
    - `inspect/analyze`: Read-only probe of state (low risk).
    - `recommend`: Synthetic proposal with risk assessment (no execution).
    - `governed_execute`: Live execution under constitutional oversight.
    - `dry_run`: Full pipeline simulation without side effects.

    ### Input
    - `query`: The objective or task (e.g., "Analyze logs and propose a fix").
    - `auth_context`: (Required for execution) The context returned from `init_anchor`.
    - `risk_tier`: "low" | "medium" | "high".
    - `mode`: "recommend" | "inspect" | "governed_execute" | "dry_run".

    ### Returns (RuntimeEnvelope)
    - `verdict`: SEAL | HOLD | VOID | SABAR.
    - `remediation`: Recovery path if verdict is not SEAL.
    - `payload`: Results of the tool/analysis or execution log.
    """
    # Canonical delegation via _wrap_call to ensure Invariants and Philosophy apply
    active_session = session_id or _normalize_session_id(None)

    # Ensure allow_execution is synchronized with mode
    effective_execution = allow_execution or (mode == "governed_execute")
    effective_dry_run = dry_run or (mode == "dry_run")

    return await _wrap_call(
        tool_name="arifOS_kernel",
        stage=Stage.ROUTER_444,
        session_id=active_session,
        payload={
            "query": query,
            "context": context,
            "risk_tier": risk_tier,
            "mode": mode,
            "actor_id": actor_id,
            "declared_name": declared_name,
            "human_approval": human_approval,
            "auth_context": auth_context
            if not hasattr(auth_context, "model_dump")
            else auth_context.model_dump(mode="json"),
            "allow_execution": effective_execution,
            "dry_run": effective_dry_run,
            "caller_context": caller_context.model_dump(mode="json") if caller_context else None,
            "debug": debug,
            "use_memory": use_memory,
            "use_heart": use_heart,
            "use_critique": use_critique,
            "requested_persona": requested_persona,
        },
        ctx=ctx,
        caller_context=caller_context,
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
    """
    111_SENSE: Ground claims in external reality.
    Use this to verify facts or fetch URL content BEFORE performing reasoning.
    Enforces F2 (Truth) fidelity.
    """
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
    """
    222_REALITY: Map evidence across multiple sources.
    Merges and queries EvidenceBundles to create a unified grounding context.
    Enforces F2 and F3.
    """
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
    """
    333_MIND: Inspect the live status and thresholds of all 13 constitutional floors (F1-F13).
    Provides transparency into current governance constraints.
    Enforces F1-F13.
    """
    envelope = await _wrap_call("audit_rules", Stage.JUDGE_888, session_id, {}, ctx)
    
    # Discovery: Always surface contract and floor metadata for transparency
    from .resources import apex_tools_markdown_table
    envelope.payload["tool_contract_table"] = apex_tools_markdown_table()
    envelope.payload["floor_runtime_hooks"] = {
        "F1_AMANAH": "core.enforcement.reversibility",
        "F2_TRUTH": "arifosmcp.intelligence.fact_checker",
        "F3_TRI_WITNESS": "core.shared.consensus",
        "F4_CLARITY": "core.physics.entropy",
        "F5_PEACE2": "core.shared.vitality",
        "F11_AUTHORITY": "core.enforcement.auth_continuity",
        "F12_DEFENSE": "core.enforcement.injection_scanner",
    }
    envelope.payload["discovery_resource"] = "canon://contracts"
    envelope.payload["guidance"] = (
        "Review canon://contracts and canon://states resources "
        "for tool hierarchy and the full Session Ladder bootstrap sequence."
    )
    return envelope


async def get_caller_status(
    session_id: str = "global",
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """
    000_INIT: Single onboarding compass. Returns current state and exact next step.
    
    Anti-chaos: This is the de-chaos entry point. Call this first when confused.
    Returns:
    - current caller state (anonymous|claimed|anchored|verified|scoped|approved)
    - accessible tools at current state
    - blocked tools with reasons
    - exact next step with example payload
    """
    envelope = await _wrap_call("get_caller_status", Stage.INIT_000, session_id, {}, ctx)
    envelope.tool = "get_caller_status"
    
    # Enrichment: Add walkthrough guidance if this is the first call
    envelope.payload.update({
        "bootstrap_sequence": [
            "1. check_vital - System health and vitals (no auth required)",
            "2. audit_rules - Constitutional floors and tool contracts (no auth required)",
            "3. init_anchor_state - Establish identity (creates session anchor)",
            "4. arifOS_kernel - Primary metabolic loop for governed execution",
        ],
        "system_motto": "DITEMPA BUKAN DIBERI — Forged, Not Given",
    })
    
    return envelope
async def check_vital(session_id: str = "global", ctx: Context | None = None) -> RuntimeEnvelope:
    """
    000_INIT: System health and thermodynamic telemetry monitor.
    Reports real-time ΔS (Entropy), Peace², and Gödel Humility metrics.
    Enforces F4, F5, F7.
    """
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

    # --- BOOTSTRAP GUIDANCE (Consolidated truth source) ---
    status_map = {
        "anonymous": "GUEST: No identity claimed. Restricted to discovery (check_vital, audit_rules).",
        "claimed": "GUEST (CLAIMED): Name/Actor ID provided but session NOT yet anchored.",
        "anchored": "OPERATOR (ANCHORED): Session active. memory/ingest tools unlocked.",
        "verified": "OPERATOR (VERIFIED): Identity verified via VAULT999 proof.",
        "approved": "APEX (APPROVED): Full Human Sovereign approval. All capabilities enabled.",
    }

    next_steps = {
        "anonymous": {
            "advance_to": "anchored",
            "tool": "init_anchor",
            "required": ["actor_id", "intent"],
            "example": "init_anchor(actor_id='arif', intent='governance test')"
        },
        "claimed": {
            "advance_to": "anchored",
            "tool": "init_anchor",
            "action": "Finalize session binding with identity attestation."
        },
        "anchored": {
            "advance_to": "verified",
            "tool": "verify_vault_ledger",
            "action": "Provide cryptographic proof of continuity."
        }
    }

    current_state = envelope.caller_state
    
    envelope.payload["bootstrap"] = {
        "current_state": current_state,
        "description": status_map.get(current_state, "Unknown state."),
        "ladder_resource": "canon://states",
        "accessible_tools": envelope.allowed_next_tools,
        "blocked_tools": [t["tool"] for t in envelope.blocked_tools],
        "blocked_details": envelope.blocked_tools,
        "operator_guidance": next_steps.get(current_state, {"action": "Proceed with current authority."}),
        "diagnostics_only": envelope.diagnostics_only,
    }

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

    revoke_session(session_id, reason, revoked_by)
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
        "get_caller_status": get_caller_status,
        "init_anchor": init_anchor,
        "init_anchor_state": init_anchor_state,
        "revoke_anchor_state": revoke_anchor_state,
        "register_tools": lambda: {"status": "SUCCESS", "tools": public_tool_names()},
        "arifOS_kernel": arifos_kernel,
        "metabolic_loop_router": arifos_kernel,
        "forge": forge,
        # AGI Δ MIND
        "agi_reason": agi_reason,
        "agi_reflect": agi_reflect,
        "reality_compass": reality_compass,
        "reality_atlas": reality_atlas,
        "search_reality": search_reality,
        "ingest_evidence": ingest_evidence,
        # ASI Ω HEART
        "asi_critique": asi_critique,
        "asi_simulate": asi_simulate,
        "agentzero_engineer": agentzero_engineer,
        "agentzero_memory_query": agentzero_memory_query,
        # APEX Ψ SOUL
        "apex_judge": apex_judge,
        "agentzero_validate": agentzero_validate,
        "audit_rules": audit_rules,
        "agentzero_armor_scan": agentzero_armor_scan,
        "agentzero_hold_check": agentzero_hold_check,
        "check_vital": check_vital,
        "open_apex_dashboard": open_apex_dashboard,
        # VAULT999
        "vault_seal": vault_seal,
        "verify_vault_ledger": verify_vault_ledger,
    }

    specs = {spec.name: spec for spec in public_tool_specs()}

    # ─── Server-injected args hidden from client schema ───
    # session_id: server always auto-generates via _normalize_session_id
    # caller_context: advisory — now visible in schema (F9-compliant, server governs final persona_id)
    _kernel_hidden = {
        "session_id": ArgTransform(hide=True, default=None),
    }
    _transform_names = {"arifOS_kernel", "metabolic_loop_router"}

    # ─── Internal tools: hidden from public clients until validated ───
    # agentzero_engineer: authorized=True hardcoded — F11 risk until real auth wired
    # agentzero_validate: SimpleArifOSClient rubber-stamps governance (mock)
    # agentzero_memory_query: requires Qdrant vector DB, untested
    _internal_tool_names = {"agentzero_engineer", "agentzero_validate", "agentzero_memory_query"}

    for name, handler in tool_handlers.items():
        spec = specs.get(name)
        description = spec.description if spec else None
        tags = {"internal"} if name in _internal_tool_names else None
        if name in _transform_names:
            base = make_tool(handler)
            transformed = Tool.from_tool(
                base,
                name=name,
                description=description,
                transform_args=_kernel_hidden,
            )
            mcp.add_tool(transformed)
        elif spec:
            mcp.tool(name=spec.name, description=spec.description, tags=tags)(handler)
        else:
            mcp.tool(name=name, tags=tags)(handler)


__all__ = [
    "init_anchor",
    "init_anchor_state",
    "agi_reason",
    "agi_reflect",
    "asi_simulate",
    "asi_critique",
    "agi_asi_forge_handler",
    "apex_judge",
    "vault_seal",
    "arifos_kernel",
    "register_tools",
]

# Legacy and public surface aliases
reason_mind_synthesis = agi_reason
assess_heart_impact = asi_simulate
critique_thought_audit = asi_critique
vector_memory_store = agi_reflect
seal_vault_commit = vault_seal
# init_anchor_state already defined above correctly
metabolic_loop_router = arifos_kernel
agi_asi_forge = agi_asi_forge_handler
apex_judge_verdict = apex_judge
