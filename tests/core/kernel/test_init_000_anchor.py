"""
tests/core/kernel/test_init_000_anchor.py — Tests for the Unified Constitutional Anchor
"""

import pytest
from unittest.mock import patch, MagicMock
from core.kernel.init_000_anchor import AnchorEngine, AuthorityLevel, init_000_anchor
from core.shared.types import Verdict

@pytest.fixture
def anchor_engine():
    return AnchorEngine()

def test_authority_level_values():
    assert AuthorityLevel.SOVEREIGN.value == "sovereign"
    assert AuthorityLevel.USER.value == "human"

@pytest.mark.asyncio
async def test_ignite_success(anchor_engine):
    # Mock evaluator.check_floor to always pass F12
    with patch("core.kernel.init_000_anchor.evaluator.check_floor") as mock_check:
        mock_check.return_value = {"passed": True, "score": 0.0, "reason": "No injection"}
        
        output = await anchor_engine.ignite("Hello arifOS", actor_id="human")
        
        assert output.verdict == Verdict.SEAL
        assert output.status == "READY"
        assert output.auth_verified is True
        assert output.session_id is not None
        assert output.governance_token is not None
        assert output.governance.authority_level == "human"

@pytest.mark.asyncio
async def test_ignite_sovereign(anchor_engine):
    with patch("core.kernel.init_000_anchor.evaluator.check_floor") as mock_check:
        mock_check.return_value = {"passed": True, "score": 0.0, "reason": "No injection"}
        
        output = await anchor_engine.ignite("System status", actor_id="arif-fazil")
        
        assert output.governance.authority_level == "sovereign"

@pytest.mark.asyncio
async def test_ignite_f12_injection_fail(anchor_engine):
    with patch("core.kernel.init_000_anchor.evaluator.check_floor") as mock_check:
        mock_check.return_value = {"passed": False, "score": 1.0, "reason": "SQL Injection detected"}
        
        output = await anchor_engine.ignite("'; DROP TABLE users; --", actor_id="human")
        
        assert output.verdict == Verdict.VOID
        assert output.status == "ERROR"
        assert "F12" in output.violations
        assert output.error_message == "SQL Injection detected"

@pytest.mark.asyncio
async def test_ignite_f11_unauthorized_actor(anchor_engine):
    with patch("core.kernel.init_000_anchor.evaluator.check_floor") as mock_check:
        mock_check.return_value = {"passed": True, "score": 0.0, "reason": "No injection"}
        
        output = await anchor_engine.ignite("Hello", actor_id="hacker_99")
        
        assert output.verdict == Verdict.VOID
        assert "F11" in output.violations
        assert "Unauthorized actor" in output.error_message

@pytest.mark.asyncio
async def test_ignite_f13_high_stakes_hold(anchor_engine):
    with patch("core.kernel.init_000_anchor.evaluator.check_floor") as mock_check:
        mock_check.return_value = {"passed": True, "score": 0.0, "reason": "No injection"}
        
        # 'rm -rf' is high stakes
        output = await anchor_engine.ignite("rm -rf /", actor_id="human")
        
        assert output.verdict == Verdict.HOLD
        assert "F13" in output.violations
        assert "Sovereign approval required" in output.error_message

@pytest.mark.asyncio
async def test_ignite_high_stakes_sovereign_allowed(anchor_engine):
    with patch("core.kernel.init_000_anchor.evaluator.check_floor") as mock_check:
        mock_check.return_value = {"passed": True, "score": 0.0, "reason": "No injection"}
        
        output = await anchor_engine.ignite("rm -rf /", actor_id="arif-fazil")
        
        assert output.verdict == Verdict.SEAL
        assert output.status == "READY"

def test_estimate_infra_risk(anchor_engine):
    assert anchor_engine._estimate_infra_risk("short query") == 0.1
    assert anchor_engine._estimate_infra_risk("execute this big command") == 0.5
    assert anchor_engine._estimate_infra_risk("a" * 6000) == 0.8

@pytest.mark.asyncio
async def test_init_000_anchor_wrapper():
    with patch("core.kernel.init_000_anchor.anchor_engine.ignite") as mock_ignite:
        mock_ignite.return_value = "mocked_output"
        res = await init_000_anchor("test query", actor_id="human")
        assert res == "mocked_output"
        mock_ignite.assert_called_once_with("test query", "human")
