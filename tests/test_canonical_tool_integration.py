import pytest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys
import types


def _load_module(module_name: str, rel_path: str):
    root = Path(__file__).resolve().parents[1]
    aaa_mcp_path = root / "aaa_mcp"
    protocol_path = aaa_mcp_path / "protocol"

    if "aaa_mcp" not in sys.modules:
        pkg = types.ModuleType("aaa_mcp")
        pkg.__path__ = [str(aaa_mcp_path)]
        sys.modules["aaa_mcp"] = pkg
    if "aaa_mcp.protocol" not in sys.modules:
        protocol_pkg = types.ModuleType("aaa_mcp.protocol")
        protocol_pkg.__path__ = [str(protocol_path)]
        sys.modules["aaa_mcp.protocol"] = protocol_pkg

    module_path = root / rel_path
    spec = spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module spec for {module_path}")
    module = module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


LOAD_ERROR = None
try:
    response_module = _load_module("aaa_mcp.protocol.response", "aaa_mcp/protocol/response.py")
    tool_graph_module = _load_module("aaa_mcp.protocol.tool_graph", "aaa_mcp/protocol/tool_graph.py")
except Exception as exc:
    LOAD_ERROR = exc

if LOAD_ERROR is None:
    build_align_response = response_module.build_align_response
    build_empathize_response = response_module.build_empathize_response
    build_init_response = response_module.build_init_response
    build_reason_response = response_module.build_reason_response
    build_seal_response = response_module.build_seal_response
    build_sense_response = response_module.build_sense_response
    build_think_response = response_module.build_think_response
    build_verdict_response = response_module.build_verdict_response
    TOOL_GRAPH = tool_graph_module.TOOL_GRAPH

pytestmark = pytest.mark.skipif(
    LOAD_ERROR is not None, reason=f"Core aaa_mcp modules not available: {LOAD_ERROR}"
)


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
