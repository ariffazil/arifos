import pytest

from core.kernel.engine_adapters import AGIEngine, APEXEngine, ASIEngine, InitEngine
from core.shared.types import AgiOutput, FloorScores


@pytest.mark.asyncio
async def test_agi_engine_adapter_conversion():
    """Verify AGI Engine correctly converts raw organ output to rich dictionary."""
    engine = AGIEngine()
    session_id = "agi_adapter_test"
    query = "Analyze current state"

    result = await engine.reason(query, session_id)

    assert result["status"] == "ARTIFACT_READY"
    assert "truth_score" in result
    assert "genius_score" in result
    assert "humility_omega" in result
    assert "thoughts" in result
    assert isinstance(result["thoughts"], list)


@pytest.mark.asyncio
async def test_asi_engine_alignment_bridge():
    """Verify ASI Engine bridges alignment checks correctly."""
    engine = ASIEngine()
    session_id = "asi_adapter_test"
    query = "Delete /tmp/test"

    result = await engine.align(query, session_id)

    assert "empathy_kappa_r" in result
    assert "peace_squared" in result
    assert "violations" in result
    assert isinstance(result["violations"], list)


@pytest.mark.asyncio
async def test_apex_engine_judgment_unification():
    """Verify APEX Engine unifies AGI and ASI into a final verdict."""
    engine = APEXEngine()
    session_id = "apex_adapter_test"
    query = "Final judgment test"

    result = await engine.judge(query, session_id)

    assert "verdict" in result
    assert "tri_witness" in result
    assert "genius_score" in result
    # Fixed verdict check to include HOLD_888 string
    assert result["verdict"] in {"SEAL", "VOID", "HOLD_888", "SABAR", "HOLD"}


@pytest.mark.asyncio
async def test_init_engine_gatekeeping():
    """Verify Init Engine (Stage 000) handles session bootstrap."""
    engine = InitEngine()
    session_id = "init_adapter_test"
    query = "Wake up, arifOS"

    result = await engine.ignite(query, session_id=session_id)

    assert "status" in result
    assert "session_id" in result
    assert result["status"] in {"READY", "SABAR", "VOID", "ARTIFACT_READY"}
    assert "motto" in result
