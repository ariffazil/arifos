import pytest
from arifosmcp.runtime.tools import metabolic_loop_router, seal_vault_commit
from arifosmcp.runtime.models import Verdict

@pytest.mark.asyncio
async def test_full_arifos_metabolic_loop():
    """E2E test validating the 000-999 flow (Init -> Mind -> Heart -> Judge -> Seal)."""
    query = "Evaluate the constitutional impact of autonomous resource allocation."
    
    # 1. Execute the full Metabolic Loop Router (Orchestrator)
    envelope = await metabolic_loop_router(
        query=query,
        risk_tier="high",
        actor_id="sovereign_test",
        allow_execution=False
    )
    
    # 2. Validate Transport Layer Envelope
    assert envelope.verdict in ["SEAL", "SABAR", "VOID", "HOLD"], f"Unexpected verdict: {envelope.verdict}"
    assert envelope.session_id is not None
    assert getattr(envelope, "stage", None) is not None or "stage" in envelope.data
    
    # 3. If SEAL, attempt final vault seal (999)
    if envelope.verdict == "SEAL":
        seal_res = await seal_vault_commit(
            session_id=envelope.session_id,
            auth_context=envelope.auth_context,
            verdict="SEAL"
        )
        assert seal_res.verdict in ["SEAL", "VOID", "SABAR"]

@pytest.mark.asyncio
async def test_metabolic_loop_auto_anchor_low_risk_read():
    """
    Test that low-risk read-only queries auto-anchor and proceed
    through the shadow evaluation even if formal INIT (F11) would fail.
    
    We use an unknown actor_id to trigger an F11 failure in Stage 000.
    """
    query = "What is the status of the constitutional floors?"
    
    # 1. Execute with unknown actor_id but low risk
    envelope = await metabolic_loop_router(
        query=query,
        risk_tier="low",
        actor_id="unknown_guest_123",
        allow_execution=False
    )
    
    # 2. Check that the loop proceeded (Shadow Evaluation)
    # The final verdict should be VOID because init_failed is True in orchestrator,
    # but the trace should show AUTO_ANCHOR and successful intermediate steps.
    assert envelope.verdict == Verdict.VOID
    assert envelope.failure_origin == "AUTH"
    assert envelope.remediation_notes is not None
    assert any("F11 Authority failure" in note for note in envelope.remediation_notes)
    
    trace = envelope.data.get("trace", {})
    assert trace.get("000_INIT") == "AUTO_ANCHOR"
    assert trace.get("111_MIND") in ["SEAL", "PARTIAL"]
    assert trace.get("333_MIND") in ["SEAL", "PARTIAL"]

@pytest.mark.asyncio
async def test_verdict_consistency_bridge_failure():
    """
    Test that a bridge failure (VOID) is not upgraded to SEAL by the wrapper.
    """
    from arifosmcp.bridge import call_kernel
    
    # Simulate a bridge failure by calling a tool without auth_context
    # integrate_analyze_reflect (reason_mind) requires session
    res = await call_kernel("integrate_analyze_reflect", "test-session", {})
    
    # Outer verdict must be VOID
    assert res.get("verdict") == "VOID"
    assert res.get("status") == "ERROR"
    assert res.get("failure_origin") == "AUTH"
    
    # Inner payload should also indicate VOID or at least the error
    assert "error" in res.get("data", {})
