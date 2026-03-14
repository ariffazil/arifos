"""
arifosmcp/helix/organs/inner/critique/metabolism.py — The Self-Auditor

Stage 666B: ASI·CRITIQUE.
Evaluates draft output for blind spots, uncertainty, and floor compliance.
Applies F7 Humility gate and integrates PNS·HEALTH + PNS·FLOOR signals.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from typing import Any

from fastmcp.dependencies import CurrentContext

from arifosmcp.runtime.exceptions import ConstitutionalViolation, InfrastructureFault
from arifosmcp.runtime.fault_codes import ConstitutionalFaultCode, MechanicalFaultCode
from arifosmcp.runtime.metrics import helix_tracer
from arifosmcp.runtime.models import RuntimeEnvelope


async def asi_critique_metabolism(
    draft_output: str,
    ctx: CurrentContext,
    session_id: str = "global",
    pns_health: dict[str, Any] | None = None,
    pns_floor: dict[str, Any] | None = None,
) -> RuntimeEnvelope:
    """
    Metabolic function for ASI·CRITIQUE (Stage 666B).

    1. Resolve session continuity.
    2. Inject PNS·HEALTH and PNS·FLOOR signals into the audit payload.
    3. Execute thought audit against the governance kernel.
    4. Enforce F7 Humility gate (confidence must stay in [0.03, 0.05]).
    5. Emit organ span and constitutional event.
    """
    active_session = session_id or getattr(ctx, "session_id", None) or "global"

    with helix_tracer.start_organ_span("ASI·CRITIQUE", active_session) as span:
        from arifosmcp.runtime.bridge import call_kernel

        payload = {
            "thought_id": "current_thought",
            "draft_output": draft_output,
            "session_id": active_session,
            "pns_health": pns_health,
            "pns_floor": pns_floor,
        }

        try:
            kernel_res = await call_kernel(
                "critique_thought_audit", active_session, payload
            )
            envelope = RuntimeEnvelope(**kernel_res)
        except Exception as e:
            raise InfrastructureFault(
                message=f"Critique failure in session {active_session}: {e}",
                fault_code=MechanicalFaultCode.INFRA_DEGRADED,
            )

        # F7 Humility gate: confidence must stay in [0.03, 0.05]
        omega = envelope.metrics.telemetry.confidence
        if omega < 0.03 or omega > 0.05:
            raise ConstitutionalViolation(
                message=(
                    f"F7 Humility gate breached: confidence {omega:.4f} outside "
                    f"[0.03, 0.05]. Draft may be overconfident or paralysed."
                ),
                floor_code=ConstitutionalFaultCode.F2_TRUTH_BELOW_THRESHOLD,
                extra={"omega": omega},
            )

        if span:
            helix_tracer.record_constitutional_event(
                span,
                "critiqued",
                {
                    "omega": omega,
                    "pns_health_active": pns_health is not None,
                    "pns_floor_active": pns_floor is not None,
                    "session_id": active_session,
                },
            )

        return envelope
