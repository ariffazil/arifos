"""
aclip_cai/triad/psi/audit.py — Stage 888 Judge
Final Tri-Witness judgment.
"""

from ...core.kernel import kernel


async def audit(session_id: str, action: str, sovereign_token: str = "") -> dict:
    """
    STAGE 888: Final Judgment.
    Invoke the Apex Judge for final constitutional verdict.
    """
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
