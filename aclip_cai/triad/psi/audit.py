"""
aclip_cai/triad/psi/audit.py — Stage 888 Judge
Final Tri-Witness judgment.

SAMPLING INTEGRATION (v2026.3):
When FastMCP Context is provided, uses ctx.sample() for governed LLM reasoning.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ...core.kernel import kernel
from .._utils import serialize_floor_concerns

if TYPE_CHECKING:
    from fastmcp import Context


_SAMPLING_ENABLED = True

try:
    from ...core.constitutional_sampling import (
        sample_audit,
        AuditResult,
        SamplingConfig,
    )
except ImportError:
    _SAMPLING_ENABLED = False


async def audit(
    session_id: str,
    action: str,
    sovereign_token: str = "",
    ctx: "Context | None" = None,
    use_sampling: bool = True,
    agi_result: dict[str, Any] | None = None,
    asi_result: dict[str, Any] | None = None,
    temperature: float = 0.2,
) -> dict[str, Any]:
    """
    STAGE 888: Final Judgment.
    Invoke the Apex Judge for final constitutional verdict.

    SAMPLING INTEGRATION:
    When ctx is provided, uses constitutional sampling for LLM judgment.
    """
    if ctx is not None and use_sampling and _SAMPLING_ENABLED:
        return await _audit_with_sampling(
            session_id, action, sovereign_token, ctx, agi_result, asi_result, temperature
        )
    return await _audit_with_kernel(session_id, action, sovereign_token)


async def _audit_with_sampling(
    session_id: str,
    action: str,
    sovereign_token: str,
    ctx: "Context",
    agi_result: dict[str, Any] | None,
    asi_result: dict[str, Any] | None,
    temperature: float,
) -> dict[str, Any]:
    """AUDIT using FastMCP sampling with constitutional governance."""
    try:
        config = SamplingConfig(temperature=temperature, max_tokens=2048)
        result: AuditResult = await sample_audit(
            ctx=ctx,
            query=action,
            agi_result=agi_result,
            asi_result=asi_result,
            config=config,
        )

        return {
            "verdict": result.verdict.value,
            "pass_rate": result.pass_rate,
            "truth_score": result.truth_score,
            "humility_omega": result.humility_omega,
            "floors_passed": result.floors_passed,
            "floors_failed": result.floors_failed,
            "sampling_mode": True,
            "recommendation": result.recommendation,
            "status": "judged",
            "floor_concerns": serialize_floor_concerns(result.floor_concerns),
        }
    except Exception:
        return await _audit_with_kernel(session_id, action, sovereign_token)


async def _audit_with_kernel(
    session_id: str,
    action: str,
    sovereign_token: str,
) -> dict[str, Any]:
    """AUDIT using kernel.audit() structural checks (fallback)."""
    # Enforce F11 (Authority) and F3 (Consensus)
    severity = "irreversible" if sovereign_token == "888_APPROVED" else "high"

    audit_res = kernel.audit(
        action=action, context=f"SOVEREIGN_TOKEN={sovereign_token}", severity=severity
    )

    # Log to Vault
    kernel.vault.log_witness(
        session_id=session_id,
        agent_id="JUDGE",
        stage="888_JUDGE",
        statement=action[:150],
        verdict=audit_res.verdict.value,
    )

    return {
        "verdict": audit_res.verdict.value,
        "pass_rate": audit_res.pass_rate,
        "recommendation": audit_res.recommendation,
        "status": "judged",
    }
