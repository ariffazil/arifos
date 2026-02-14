import pytest

# Skip tests if core modules unavailable
try:
    from aaa_mcp.protocol.response import (
        build_align_response,
        build_empathize_response,
        build_init_response,
        build_reason_response,
        build_seal_response,
        build_sense_response,
        build_think_response,
        build_verdict_response,
    )
    from aaa_mcp.protocol.tool_graph import TOOL_GRAPH

    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False

pytestmark = pytest.mark.skipif(not CORE_AVAILABLE, reason="Core aaa_mcp modules not available")


def test_init_gate_integration():
    """
    Integration test for the L0 init_gate tool.
    Checks that the response is structured correctly.
    """
    # Arrange
    session_id = "test-session-123"

    # Act
    response = build_init_response(session_id=session_id, verdict="SEAL", mode="conscience")

    # Assert
    assert "🔥" in response.message
    assert "DITEMPA, BUKAN DIBERI" in response.message
    assert response.session_id == session_id
    assert response.policy_verdict == "SEAL"
    assert response.data["bookend"] == "INIT"


def test_agi_sense_integration():
    """Integration test for the L1 agi_sense tool."""
    # Arrange
    session_id = "test-session-789"
    # Act
    response = build_sense_response(
        session_id=session_id, intent="test_intent", lane="test_lane", requires_grounding=True
    )
    # Assert
    assert response.stage == "111"
    assert response.data["intent"] == "test_intent"
    assert response.data["lane"] == "test_lane"


def test_agi_think_integration():
    """Integration test for the L2 agi_think tool."""
    # Arrange
    session_id = "test-session-abc"
    # Act
    response = build_think_response(
        session_id=session_id, hypotheses=[{"name": "h1"}], recommended_path="h1"
    )
    # Assert
    assert response.stage == "222"
    assert response.data["hypothesis_count"] == 1


def test_agi_reason_integration():
    """Integration test for the L3 agi_reason tool."""
    # Arrange
    session_id = "test-session-def"
    # Act
    response = build_reason_response(
        session_id=session_id, conclusion="test", truth_score=0.9, confidence=0.8, verdict="SEAL"
    )
    # Assert
    assert response.stage == "333"
    assert response.data["truth_score"] == 0.9


def test_asi_empathize_integration():
    """Integration test for the L4 asi_empathize tool."""
    # Arrange
    session_id = "test-session-ghi"
    # Act
    response = build_empathize_response(
        session_id=session_id, empathy_kappa_r=0.95, stakeholders=["s1"]
    )
    # Assert
    assert response.stage == "555"
    assert response.data["empathy_score"] == 0.95


def test_asi_align_integration():
    """Integration test for the L5 asi_align tool."""
    # Arrange
    session_id = "test-session-jkl"
    # Act
    response = build_align_response(session_id=session_id, is_reversible=True, risk_level="LOW")
    # Assert
    assert response.stage == "666"
    assert response.data["is_reversible"] is True


def test_apex_verdict_integration():
    """Integration test for the L7 apex_verdict tool."""
    # Arrange
    session_id = "test-session-mno"
    # Act
    response = build_verdict_response(
        session_id=session_id, query="test", truth_score=0.9, verdict="SEAL", justification="test"
    )
    # Assert
    assert response.stage == "888"
    assert response.policy_verdict == "SEAL"


def test_vault_seal_integration():
    """
    Integration test for the L8 vault_seal tool.
    Checks that the seal response is structured correctly.
    """
    # Arrange
    session_id = "test-session-456"
    seal_id = "seal-abc"
    seal_hash = "hash123"

    # Act
    response = build_seal_response(
        session_id=session_id, seal_id=seal_id, seal_hash=seal_hash, verdict="SEALED"
    )

    # Assert
    assert "💎" in response.message
    assert "🧠" in response.message
    assert "🔒" in response.message
    assert "DITEMPA, BUKAN DIBERI" in response.message
    assert response.session_id == session_id
    assert response.data["seal_id"] == seal_id
    assert response.data["seal_hash"].startswith(seal_hash[:16])
    assert response.data["bookend"] == "SEAL"
