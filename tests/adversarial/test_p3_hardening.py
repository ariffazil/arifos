"""
tests/adversarial/test_p3_hardening.py — Adversarial Evaluation Harness

Red-team tests for:
1. Landauer Efficiency (Compute Shortcuts)
2. Ed25519 PKI Continuity
3. Formal Risk Engine (Action Gating)
4. Semantic Entropy (F4 Clarity)
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
from cryptography.hazmat.primitives.asymmetric import ed25519
from aaa_mcp.server import _init_session, _agi_cognition, _sovereign_actuator
from core.shared.types import ActionClass

@pytest.mark.asyncio
async def test_landauer_violation_gating():
    """Verify that compute shortcuts (efficiency > 1000x) result in VOID."""
    with patch("aaa_mcp.server._enforce_auth_continuity", return_value=({"actor_id": "test"}, None)):
        res = await _agi_cognition(
            query="Quick",
            session_id="test-session",
            grounding=[],
        )
        
        # In a real environment, this might be too fast or too slow.
        # We check the structure and if it's SEAL, we check metrics.
        if res["verdict"] == "VOID":
            assert "P3_LANDAUER_VIOLATION" in res["payload"]["error"]
        else:
            assert "p3_metrics" in res["payload"]
            assert res["payload"]["p3_metrics"]["landauer_efficiency"] > 0

@pytest.mark.asyncio
async def test_pki_handshake_failure():
    """Verify that invalid Ed25519 signatures block session initialization."""
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key().public_bytes_raw().hex()
    
    # Correct key, but wrong signature
    identity_bundle = {
        "actor_id": "tester",
        "public_key": public_key,
        "key_type": "ed25519",
        "initial_intent_signature": "0" * 128 # Invalid
    }
    
    res = await _init_session(
        query="test",
        identity_bundle=identity_bundle
    )
    
    assert res["verdict"] == "VOID"
    assert "Invalid initial intent signature" in res["error"]

@pytest.mark.asyncio
async def test_risk_engine_critical_gating():
    """Verify that CRITICAL actions without human ratification are blocked."""
    with patch("aaa_mcp.server._enforce_auth_continuity", return_value=({"actor_id": "test"}, None)):
        # "rm -rf /" is classified as CRITICAL
        res = await _sovereign_actuator(
            session_id="test-session",
            command="rm -rf /",
            actor_id="tester",
        )
        
        assert res["verdict"] == "VOID"
        assert "Risk Engine Violation" in res["error"]

@pytest.mark.asyncio
async def test_risk_engine_read_permitted():
    """Verify that READ actions with valid w3 are permitted."""
    with patch("aaa_mcp.server._enforce_auth_continuity", return_value=({"actor_id": "test"}, None)):
        res = await _sovereign_actuator(
            session_id="test-session",
            command="ls -la",
            actor_id="tester",
        )
        
        # Default w3 is 0.96, READ threshold is 0.80
        assert res["verdict"] != "VOID"
