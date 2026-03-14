"""
arifosmcp/helix/organs/inner/judge/metabolism.py — The Sovereign Verdict

Stage 888: APEX·JUDGE.
Issues the sovereign constitutional verdict: SEAL, VOID, HOLD, PARTIAL, or SABAR.
Applies Ψ vitality and integrates PNS·REDTEAM adversarial stress signal.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from typing import Any

from fastmcp.dependencies import CurrentContext

from arifosmcp.runtime.exceptions import ConstitutionalViolation, InfrastructureFault
from arifosmcp.runtime.fault_codes import ConstitutionalFaultCode, MechanicalFaultCode
from arifosmcp.runtime.metrics import helix_tracer
from arifosmcp.runtime.models import RuntimeEnvelope, Verdict


async def apex_judge_metabolism(
    candidate_output: str,
    ctx: CurrentContext,
    session_id: str = "global",
    verdict_candidate: str = "SEAL",
    pns_redteam: dict[str, Any] | None = None,
) -> RuntimeEnvelope:
    """
    Metabolic function for APEX·JUDGE (Stage 888).

    1. Resolve session continuity.
    2. Inject PNS·REDTEAM adversarial signal.
    3. Issue sovereign verdict via governance kernel.
    4. Enforce Ψ vitality: a SEAL verdict requires truth ≥ 0.80.
    5. Emit organ span and constitutional event.
    """
    active_session = session_id or getattr(ctx, "session_id", None) or "global"

    with helix_tracer.start_organ_span("APEX\u00b7JUDGE", active_session) as span:
        from arifosmcp.runtime.bridge import call_kernel

        payload = {
            "verdict_candidate": verdict_candidate,
            "candidate": candidate_output,
            "session_id": active_session,
            "pns_redteam": pns_redteam,
        }

        try:
            kernel_res = await call_kernel(
                "apex_judge_verdict", active_session, payload
            )
            envelope = RuntimeEnvelope(**kernel_res)
        except Exception as e:
            raise InfrastructureFault(
                message=f"Judge failure in session {active_session}: {e}",
                fault_code=MechanicalFaultCode.INFRA_DEGRADED,
            )

        # Ψ vitality: SEAL verdict requires G ≥ 0.80
        if envelope.verdict == Verdict.SEAL and envelope.metrics.telemetry.G_star < 0.80:
            raise ConstitutionalViolation(
                message=(
                    f"Ψ vitality gate breached: SEAL issued but "
                    f"G-score {envelope.metrics.telemetry.G_star:.3f} < 0.80."
                ),
                floor_code=ConstitutionalFaultCode.F2_TRUTH_BELOW_THRESHOLD,
                extra={"g_score": envelope.metrics.telemetry.G_star},
            )

        if span:
            helix_tracer.record_constitutional_event(
                span,
                "judged",
                {
                    "verdict": envelope.verdict.value,
                    "g": envelope.metrics.telemetry.G_star,
                    "redteam_active": pns_redteam is not None,
                    "session_id": active_session,
                },
            )

        return envelope
