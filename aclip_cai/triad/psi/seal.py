"""
aclip_cai/triad/psi/seal.py — Stage 999 Vault
Commit to VAULT999 + Phoenix-72.
"""

from ...core.kernel import kernel


async def seal(
    session_id: str,
    task_summary: str,
    was_modified: bool = True,
    verdict: str | None = None,
) -> dict:
    """
    STAGE 999: Immutability.
    Seal the session and commit to the vault.

    Args:
        verdict: Pre-verified verdict from the Amanah Handshake (apex_judge
                 governance_token). When supplied, the kernel audit still runs
                 for observability but the vault records the Judge-signed verdict,
                 not the audit re-evaluation.
    """
    # Run a final audit on the summary (observability — always executes)
    audit_res = kernel.audit(action=task_summary, context="FINAL_SEAL", severity="high")

    # If a Judge-signed verdict was passed, it is authoritative.
    # The kernel audit serves as a cross-check only.
    final_verdict = verdict if verdict is not None else audit_res.verdict.value

    # Log the final seal with the authoritative verdict
    kernel.vault.log_witness(
        session_id=session_id,
        agent_id="JUDGE",
        stage="999_SEAL",
        statement=task_summary,
        verdict=final_verdict,
    )

    # Phoenix-72 logic — only activate on clean SEAL
    if was_modified and final_verdict == "SEAL":
        kernel.amendment.request_amendment(
            ref=session_id, change_summary=task_summary, sovereign_required=True
        )

    return {
        "verdict": final_verdict,
        "audit_cross_check": audit_res.verdict.value,
        "status": "sealed" if final_verdict == "SEAL" else "partial",
        "vault_id": f"V999-{session_id[:8]}",
        "cooling": "Phoenix-72 initialized" if was_modified else "None",
    }
