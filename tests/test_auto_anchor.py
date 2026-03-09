import pytest
from arifosmcp.runtime.tools import metabolic_loop_router
from arifosmcp.runtime.models import Verdict

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
    assert trace.get("111_MIND") == "SEAL"
    assert trace.get("333_MIND") == "SEAL"

@pytest.mark.asyncio
async def test_verdict_consistency_bridge_failure():
    """
    Test that a bridge failure (VOID) is not upgraded to SEAL by the wrapper.
    """
    from arifosmcp.bridge import call_kernel
    
    # Simulate a bridge failure by calling a tool without auth_context
    # integrate_analyze_reflect (reason_mind) requires session
    res = await call_kernel("integrate_analyze_reflect", "test-session", {"query": "test"})
    
    # Outer verdict must be VOID
    assert res.get("verdict") == "VOID"
    assert res.get("status") == "ERROR"
    assert res.get("failure_origin") == "AUTH"
    
    # Inner payload should also indicate VOID or at least the error
    assert "error" in res.get("data", {})
