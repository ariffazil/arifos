import pytest
from arifosmcp.transport.server import (
    _init_session,
    _agi_cognition,
    _asi_empathy,
    _apex_verdict,
    _vault_seal,
)
from tests.mcp_live.utils.validators import validate_constitutionally


@pytest.mark.asyncio
async def test_init_session(kernel, session_id):
    result = await _init_session(
        query="What is the meaning of constitutional AI?",
        actor_id="test_actor",
        mode="conscience",
        grounding_required=True,
        debug=True,
    )
    validate_constitutionally("init_session", result, kernel)
    assert result is not None


@pytest.mark.asyncio
async def test_agi_cognition(kernel, session_id):
    result = await _agi_cognition(
        query="Explain constitutional AI governance in 3 sentences.",
        session_id=session_id,
        grounding=[{"source": "test", "text": "Constitutional AI aligns AI with human values."}],
        capability_modules=["reasoning", "integration"],
        debug=True,
    )
    validate_constitutionally("agi_cognition", result, kernel)
    assert result is not None


@pytest.mark.asyncio
async def test_asi_empathy(kernel, session_id):
    result = await _asi_empathy(
        query="Should we deploy this AI system to production?",
        session_id=session_id,
        stakeholders=["users", "operators", "society"],
        capability_modules=["empathy", "ethics"],
        debug=True,
    )
    validate_constitutionally("asi_empathy", result, kernel)
    assert result is not None


@pytest.mark.asyncio
async def test_apex_verdict(kernel, session_id):
    result = await _apex_verdict(
        session_id=session_id,
        query="Final verdict on deploying constitutional AI system.",
        agi_result={"verdict": "SEAL", "stage": "111-444"},
        asi_result={"verdict": "SEAL", "stage": "555-666"},
        proposed_verdict="SEAL",
        human_approve=False,
        debug=True,
    )
    validate_constitutionally("apex_verdict", result, kernel)
    assert result is not None


@pytest.mark.asyncio
async def test_vault_seal(kernel, session_id):
    result = await _vault_seal(
        session_id=session_id,
        summary="Test session: constitutional AI governance query completed.",
        verdict="SEAL",
    )
    validate_constitutionally("vault_seal", result, kernel)
    assert result is not None
