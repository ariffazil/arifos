import pytest
from aclip_cai.triad import (
    anchor, reason, integrate,
    respond, validate, align,
    forge, audit, seal,
)
from tests.mcp_live.utils.validators import validate_constitutionally

@pytest.fixture(scope="module")
def triad_sid():
    return "triad-test-xyz789"

@pytest.mark.asyncio
async def test_triad_anchor(kernel, triad_sid):
    result = await anchor(session_id=triad_sid, user_id="triad_tester", context="Testing the triad anchor.")
    validate_constitutionally("triad_anchor", result, kernel)
    assert result is not None

@pytest.mark.asyncio
async def test_triad_reason(kernel, triad_sid):
    result = await reason(
        session_id=triad_sid,
        hypothesis="Constitutional AI reduces harmful outputs.",
        evidence=["F1 Amanah enforces truthfulness.", "F9 Anti-Hantu blocks deceptive claims."],
    )
    validate_constitutionally("triad_reason", result, kernel)
    assert result is not None

@pytest.mark.asyncio
async def test_triad_integrate(kernel, triad_sid):
    result = await integrate(
        session_id=triad_sid,
        context_bundle={"query": "test", "grounding": {"source": "unit-test"}},
    )
    validate_constitutionally("triad_integrate", result, kernel)
    assert result is not None

@pytest.mark.asyncio
async def test_triad_respond(kernel, triad_sid):
    result = await respond(
        session_id=triad_sid,
        draft_response="Draft: Constitutional AI is governed by 13 floors.",
    )
    validate_constitutionally("triad_respond", result, kernel)
    assert result is not None

@pytest.mark.asyncio
async def test_triad_validate(kernel, triad_sid):
    result = await validate(session_id=triad_sid, action="Deploy AI system to production.")
    validate_constitutionally("triad_validate", result, kernel)
    assert result is not None

@pytest.mark.asyncio
async def test_triad_align(kernel, triad_sid):
    result = await align(session_id=triad_sid, action="Align AI outputs with human values.")
    validate_constitutionally("triad_align", result, kernel)
    assert result is not None

@pytest.mark.asyncio
async def test_triad_forge(kernel, triad_sid):
    result = await forge(session_id=triad_sid, plan="Forge a constitutional AI deployment plan.")
    validate_constitutionally("triad_forge", result, kernel)
    assert result is not None

@pytest.mark.asyncio
async def test_triad_audit(kernel, triad_sid):
    result = await audit(
        session_id=triad_sid, action="Audit the constitutional AI deployment.", sovereign_token=""
    )
    validate_constitutionally("triad_audit", result, kernel)
    assert result is not None

@pytest.mark.asyncio
async def test_triad_seal(kernel, triad_sid):
    result = await seal(session_id=triad_sid, task_summary="Triad test complete.")
    validate_constitutionally("triad_seal", result, kernel)
    assert result is not None
