"""
aclip_cai/triad/delta/reason.py — Stage 222 Reasoning
Logical causal tracing and structural breakdown.
"""

from ...core.kernel import kernel


async def reason(session_id: str, hypothesis: str, evidence: list[str]) -> dict:
    """
    STAGE 222: Logical De-entropy.
    Trace the logic from evidence to hypothesis.
    """
    # Run constitutional audit
    audit_res = kernel.audit(
        action=f"HYPOTHESIS: {hypothesis}\nEVIDENCE: {', '.join(evidence)}",
        context="REASONING_PIPELINE",
        severity="medium",
    )

    # Update Thermo Budget (ΔS reduction)
    kernel.thermo.update_budget(session_id=session_id, delta_s=audit_res.delta_s)

    # Log to Vault
    kernel.vault.log_witness(
        session_id=session_id,
        agent_id="ARCHITECT",
        stage="222_REASON",
        statement=hypothesis,
        verdict=audit_res.verdict.value,
    )

    return {
        "verdict": audit_res.verdict.value,
        "delta_s": audit_res.delta_s,
        "recommendation": audit_res.recommendation,
        "status": "metabolized",
    }
