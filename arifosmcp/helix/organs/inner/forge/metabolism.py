"""
arifosmcp/helix/organs/inner/forge/metabolism.py — The Synthesis Engine

Stage 777: AGI·ASI·FORGE.
Synthesizes solutions and generates artifacts under constitutional governance.
Applies F11 execution gate and integrates PNS·ORCHESTRATE routing.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from typing import Any

from fastmcp.dependencies import CurrentContext

from arifosmcp.runtime.exceptions import InfrastructureFault
from arifosmcp.runtime.fault_codes import MechanicalFaultCode
from arifosmcp.runtime.metrics import helix_tracer
from arifosmcp.runtime.models import RuntimeEnvelope


async def agi_asi_forge_metabolism(
    spec: str,
    ctx: CurrentContext,
    session_id: str = "global",
    pns_orchestrate: dict[str, Any] | None = None,
    tools: list[str] | None = None,
) -> RuntimeEnvelope:
    """
    Metabolic function for AGI·ASI·FORGE (Stage 777).

    1. Resolve session continuity.
    2. Inject PNS·ORCHESTRATE routing signal.
    3. Execute forge synthesis via governance kernel.
    4. Emit organ span and constitutional event.
    """
    active_session = session_id or getattr(ctx, "session_id", None) or "global"

    with helix_tracer.start_organ_span("AGI\u2013ASI\u00b7FORGE", active_session) as span:
        from arifosmcp.runtime.bridge import call_kernel

        orchestrate_payload = pns_orchestrate or {}
        if tools:
            orchestrate_payload = {**orchestrate_payload, "tools": tools}

        payload = {
            "intent": spec,
            "session_id": active_session,
            "pns_orchestrate": orchestrate_payload,
        }

        try:
            kernel_res = await call_kernel(
                "quantum_eureka_forge", active_session, payload
            )
            envelope = RuntimeEnvelope(**kernel_res)
        except Exception as e:
            raise InfrastructureFault(
                message=f"Forge failure in session {active_session}: {e}",
                fault_code=MechanicalFaultCode.INFRA_DEGRADED,
            )

        if span:
            helix_tracer.record_constitutional_event(
                span,
                "forged",
                {
                    "g": envelope.metrics.truth,
                    "ds": envelope.metrics.entropy_delta,
                    "tools_active": bool(tools),
                    "session_id": active_session,
                },
            )

        return envelope
