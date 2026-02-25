"""
aclip_cai/triad/psi/seal.py — Stage 999 Vault
Commit to VAULT999 + Phoenix-72.
"""

from ...core.kernel import kernel


async def seal(session_id: str, task_summary: str, was_modified: bool = True) -> dict:
    """
    STAGE 999: Immutability.
    Seal the session and commit to the vault.
    """
    # Run a final audit on the summary
    audit_res = kernel.audit(action=task_summary, context="FINAL_SEAL", severity="high")

    # Log the final seal
    kernel.vault.log_witness(
        session_id=session_id,
        agent_id="JUDGE",
        stage="999_SEAL",
        statement=task_summary,
        verdict=audit_res.verdict.value,
    )

    # Phoenix-72 logic
    if was_modified and audit_res.verdict.value == "SEAL":
        kernel.amendment.request_amendment(
            ref=session_id, change_summary=task_summary, sovereign_required=True
        )

    return {
        "verdict": audit_res.verdict.value,
        "status": "sealed" if audit_res.verdict.value == "SEAL" else "partial",
        "vault_id": f"V999-{session_id[:8]}",
        "cooling": "Phoenix-72 initialized" if was_modified else "None",
    }
