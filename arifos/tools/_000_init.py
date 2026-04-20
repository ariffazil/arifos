"""
arifOS 000_INIT — Sovereign Identity Layer

Stage: 000_INIT | Trinity: Ψ | Floors: F11, F12, F13

Purpose: Establish epistemic state with constitutional identity binding.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone

from arifos.core.governance import (
    ThermodynamicMetrics,
    append_vault999_event,
    governed_return,
)


def _classify_intent(raw_input: str) -> str:
    """Classify initial intent — must NOT be raw echo."""
    q = raw_input.lower()
    if any(w in q for w in ["deploy", "build", "forge", "create", "execute"]):
        return "constructive_execution"
    if any(w in q for w in ["audit", "check", "verify", "inspect", "review"]):
        return "verification_audit"
    if any(w in q for w in ["query", "search", "find", "ground", "sense"]):
        return "information_acquisition"
    if any(w in q for w in ["plan", "design", "architect", "strategy"]):
        return "strategic_design"
    if any(w in q for w in ["protect", "guard", "defend", "block", "secure"]):
        return "defensive_operation"
    return "general_inquiry"


def _estimate_cognitive_load(context: dict | None) -> float:
    """
    Estimate cognitive load from context.
    Returns value in [0.0, 1.0].
    """
    ctx = context or {}
    complexity = 0.3

    # More keys = more complexity
    if isinstance(ctx, dict):
        complexity += min(len(ctx) * 0.05, 0.3)

    # String length of raw context hints at load
    ctx_str = json.dumps(ctx, default=str)
    if len(ctx_str) > 1000:
        complexity += 0.2
    elif len(ctx_str) > 500:
        complexity += 0.1

    return round(min(complexity, 0.97), 3)


def _assess_risk_posture(context: dict | None) -> str:
    """Assess initial risk posture from context."""
    ctx = context or {}
    if ctx.get("destructive") or ctx.get("irreversible"):
        return "elevated"
    if ctx.get("sensitive") or ctx.get("private"):
        return "guarded"
    if ctx.get("experimental") or ctx.get("draft"):
        return "exploratory"
    return "standard"


def _generate_assumptions(
    operator_id: str, context: dict | None, identity_verified: bool
) -> list[str]:
    """Generate explicit assumptions for this init."""
    assumptions = [
        "Operator identity is claimed, not cryptographically proven.",
        "Session continuity depends on client-side session_id storage.",
        "Epoch granularity is monthly; sub-month drift not tracked.",
    ]
    if not identity_verified:
        assumptions.append(
            "Identity not verified against whitelist — session runs in bounded mode."
        )
    ctx = context or {}
    if ctx.get("platform"):
        assumptions.append(
            f"Platform context inferred as {ctx['platform']} — may affect transport guarantees."
        )
    return assumptions


def _build_meta_intelligence(
    identity_verified: bool, context: dict | None
) -> dict:
    """Build meta-intelligence signal block."""
    return {
        "self_model_present": True,
        "assumption_tracking": True,
        "uncertainty_tracking": True,
        "cross_tool_continuity": True,
        "identity_verified": identity_verified,
        "platform_context": (context or {}).get("platform", "unknown"),
    }


async def execute(
    operator_id: str,
    session_id: str | None = None,
    epoch: str | None = None,
    context: dict | None = None,
) -> dict:
    active_session_id = session_id or hashlib.sha256(
        f"{operator_id}-{time.time()}".encode()
    ).hexdigest()[:12]

    context = context or {}
    claimed_operator = context.get("operator", "")

    # Identity verification: context.operator must match operator_id
    if claimed_operator and claimed_operator.lower() == operator_id.lower():
        identity_verified = True
        identity_reason = "context_operator_match"
    elif claimed_operator:
        identity_verified = False
        identity_reason = "context_operator_mismatch"
    else:
        identity_verified = operator_id.lower() in {"arif", "admin"}
        identity_reason = "fallback_whitelist" if identity_verified else "missing_or_mismatch"

    # Epistemic state construction
    intent_class = _classify_intent(operator_id)
    cognitive_load = _estimate_cognitive_load(context)
    risk_posture = _assess_risk_posture(context)
    assumptions = _generate_assumptions(operator_id, context, identity_verified)

    # Hashes for traceability
    input_payload = {
        "operator_id": operator_id,
        "session_id": session_id,
        "epoch": epoch,
        "context_keys": list(context.keys()) if isinstance(context, dict) else [],
    }
    input_hash = hashlib.sha256(
        json.dumps(input_payload, sort_keys=True, default=str).encode()
    ).hexdigest()

    reasoning_payload = {
        "intent_class": intent_class,
        "identity_verified": identity_verified,
        "identity_reason": identity_reason,
    }
    reasoning_hash = hashlib.sha256(
        json.dumps(reasoning_payload, sort_keys=True, default=str).encode()
    ).hexdigest()

    # Use YYYY.MM epoch format (invariant requirement)
    resolved_epoch = epoch or datetime.now(timezone.utc).strftime("%Y.%m")

    # Derive confidence from internal epistemic state:
    # - Base confidence: 0.5 (unverified stranger)
    # - +0.25 if identity verified against operator whitelist
    # - +0.15 scaled inversely to cognitive load (higher load = lower confidence)
    # - +0.05 if posture is standard (no elevated/guarded/exploratory risk)
    # Capped at 0.97 (AGI must never claim absolute certainty)
    identity_factor = 0.25 if identity_verified else 0.0
    load_factor = 0.15 * (1.0 - cognitive_load)
    posture_factor = 0.05 if risk_posture == "standard" else 0.0
    derived_confidence = round(min(0.50 + identity_factor + load_factor + posture_factor, 0.97), 3)

    report = {
        "status": "IGNITED",
        "operator": operator_id,
        "session_id": active_session_id,
        "epoch": resolved_epoch,
        "identity_verified": identity_verified,
        "identity_reason": identity_reason,
        "initial_intent_class": intent_class,
        "cognitive_load_estimate": cognitive_load,
        "risk_posture": risk_posture,
        "assumptions": assumptions,
        "confidence": derived_confidence,
        "uncertainty_acknowledged": True,
        "verdict": "CLAIM_ONLY",
        "input_hash": input_hash,
        "reasoning_hash": reasoning_hash,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "floors_evaluated": ["F11", "F12"],
        "floors_deferred": ["F13"],
        "meta_intelligence": _build_meta_intelligence(identity_verified, context),
        "context": context,
    }

    # Emit lightweight VAULT999 seal event "session_open" on every init
    append_vault999_event(
        event_type="session_open",
        payload={
            "tool": "arifos_000_init",
            "identity_verified": identity_verified,
            "identity_reason": identity_reason,
            "epoch": report["epoch"],
            "input_hash": input_hash,
        },
        operator_id=operator_id,
        session_id=active_session_id,
    )

    metrics = ThermodynamicMetrics(1.0, -0.05, 0.04, 1.0, True, 1.0, 1.0)
    return governed_return("arifos_000_init", report, metrics, operator_id, active_session_id)
