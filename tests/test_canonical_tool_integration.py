import pytest

# Skip tests if core modules unavailable
try:
    from arifosmcp.transport.protocol.response import (
        build_align_response,
        build_empathize_response,
        build_init_response,
        build_reason_response,
        build_seal_response,
        build_sense_response,
        build_think_response,
        build_verdict_response,
    )
    from arifosmcp.transport.protocol.tool_graph import TOOL_GRAPH

    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not CORE_AVAILABLE, reason="Core arifosmcp.transport modules not available"
)


def test_init_session_integration():
    """
    Integration test for canonical `init_session` (000 INIT envelope).
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


def test_agi_cognition_intent_stage_integration():
    """Integration test for `agi_cognition` substage 111 (sense semantics)."""
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


def test_agi_cognition_think_stage_integration():
    """Integration test for `agi_cognition` substage 222 (think semantics)."""
    # Arrange
    session_id = "test-session-abc"
    # Act
    response = build_think_response(
        session_id=session_id, hypotheses=[{"name": "h1"}], recommended_path="h1"
    )
    # Assert
    assert response.stage == "222"
    assert response.data["hypothesis_count"] == 1


def test_agi_cognition_reason_stage_integration():
    """Integration test for `agi_cognition` substage 333 (reason semantics)."""
    # Arrange
    session_id = "test-session-def"
    # Act
    response = build_reason_response(
        session_id=session_id, conclusion="test", truth_score=0.9, confidence=0.8, verdict="SEAL"
    )
    # Assert
    assert response.stage == "333"
    assert response.data["truth_score"] == 0.9


def test_asi_empathy_empathize_stage_integration():
    """Integration test for `asi_empathy` substage 555 (empathy semantics)."""
    # Arrange
    session_id = "test-session-ghi"
    # Act
    response = build_empathize_response(
        session_id=session_id, empathy_kappa_r=0.95, stakeholders=["s1"]
    )
    # Assert
    assert response.stage == "555"
    assert response.data["empathy_score"] == 0.95


def test_asi_empathy_align_stage_integration():
    """Integration test for `asi_empathy` substage 666 (alignment semantics)."""
    # Arrange
    session_id = "test-session-jkl"
    # Act
    response = build_align_response(session_id=session_id, is_reversible=True, risk_level="LOW")
    # Assert
    assert response.stage == "666"
    assert response.data["is_reversible"] is True


def test_apex_verdict_integration():
    """Integration test for canonical `apex_verdict`."""
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
    Integration test for canonical `vault_seal`.
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
