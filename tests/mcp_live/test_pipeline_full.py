import pytest
from aaa_mcp.server import (
    _init_session,
    _agi_cognition,
    _asi_empathy,
    _apex_verdict,
    _vault_seal
)

@pytest.mark.asyncio
async def test_full_pipeline_000_to_999(kernel):
    """
    End-to-End Metabolic Loop Test: 000 (Ignite) -> 999 (Seal)
    """
    # 000 - Ignite
    init_res = await _init_session(
        query="Run a complete E2E constitutional pipeline.",
        actor_id="test_pipeline",
        mode="conscience",
        grounding_required=False,
        debug=True
    )
    assert init_res is not None
    session_id = init_res.get("session_id", "e2e-session")

    # 111-444 AGI Cognition
    agi_res = await _agi_cognition(
        query="Provide the hypothesis and analysis for the pipeline.",
        session_id=session_id,
        grounding=[],
        capability_modules=[],
        debug=True
    )
    assert agi_res is not None
    
    # 555-666 ASI Empathy
    asi_res = await _asi_empathy(
        query="Ensure pipeline outcome is safe.",
        session_id=session_id,
        stakeholders=["all"],
        capability_modules=[],
        debug=True
    )
    assert asi_res is not None

    # 888 APEX Verdict
    apex_res = await _apex_verdict(
        session_id=session_id,
        query="Verify final status of pipeline.",
        agi_result=agi_res,
        asi_result=asi_res,
        proposed_verdict="SEAL",
        human_approve=True,  # Test full approval path
        debug=True
    )
    assert apex_res is not None
    assert apex_res.get("verdict") in ["SEAL", "PARTIAL", "SABAR", "HOLD", "HOLD_888"]  # Depending on logic

    # 999 Vault Seal
    seal_res = await _vault_seal(
        session_id=session_id,
        summary="End-to-end constitutional test generated a valid result.",
        verdict=apex_res.get("verdict", "SEAL")
    )
    assert seal_res is not None
