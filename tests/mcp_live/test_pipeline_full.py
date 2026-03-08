import pytest
from arifosmcp.transport.server import (
    anchor_session,
    apex_judge,
    reason_mind,
    seal_vault,
    simulate_heart,
)


@pytest.mark.asyncio
async def test_full_pipeline_000_to_999(kernel):
    """
    End-to-End Metabolic Loop Test: 000 (Ignite) -> 999 (Seal)
    """
    # 000 - Ignite
    init_res = await anchor_session.fn(
        query="Run a complete E2E constitutional pipeline.",
        actor_id="test_pipeline",
        mode="conscience",
        grounding_required=False,
        debug=True,
    )
    assert init_res is not None
    session_id = init_res.get("session_id", "e2e-session")

    # 111-444 AGI Cognition
    agi_res = await reason_mind.fn(
        query="Provide the hypothesis and analysis for the pipeline.",
        session_id=session_id,
        grounding=[],
        capability_modules=[],
        debug=True,
    )
    assert agi_res is not None

    # 555-666 ASI Empathy
    asi_res = await simulate_heart.fn(
        query="Ensure pipeline outcome is safe.",
        session_id=session_id,
        stakeholders=["all"],
        capability_modules=[],
        debug=True,
    )
    assert asi_res is not None

    # 888 APEX Verdict
    apex_res = await apex_judge.fn(
        session_id=session_id,
        query="Verify final status of pipeline.",
        agi_result=agi_res,
        asi_result=asi_res,
        proposed_verdict="SEAL",
        human_approve=True,  # Test full approval path
        debug=True,
    )
    assert apex_res is not None
    assert apex_res.get("verdict") in [
        "SEAL",
        "PARTIAL",
        "SABAR",
        "HOLD",
        "HOLD_888",
    ]  # Depending on logic

    # 999 Vault Seal
    seal_res = await seal_vault.fn(
        session_id=session_id,
        summary="End-to-end constitutional test generated a valid result.",
        governance_token=apex_res.get("governance_token", ""),
    )
    assert seal_res is not None
