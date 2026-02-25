"""
aclip_cai/triad/omega/align.py — Stage 666 Align
Ethics and Anti-Hantu alignment.
"""

from ...core.kernel import kernel


async def align(session_id: str, action: str) -> dict:
    """
    STAGE 666: The Alignment Axis.
    Enforce F9 (Anti-Hantu) and F10 (Ontology) strictly.
    """
    audit_res = kernel.audit(action=action, context="ALIGNMENT_CHECK", severity="medium")

    # Audit specifically for F9/F10
    f9_pass = audit_res.floor_results.get("F9").passed if "F9" in audit_res.floor_results else True
    f10_pass = (
        audit_res.floor_results.get("F10").passed if "F10" in audit_res.floor_results else True
    )

    if not (f9_pass and f10_pass):
        return {
            "verdict": "VOID",
            "reason": "Ontological or Consciousness breach detected.",
            "status": "blocked",
        }

    return {
        "verdict": audit_res.verdict.value,
        "recommendation": audit_res.recommendation,
        "status": "aligned",
    }
