import pytest
import asyncio
from arifosmcp.runtime.tools import init_anchor
from arifosmcp.runtime.models import RuntimeStatus


@pytest.mark.asyncio
async def test_init_anchor_v2_function_returns_flat_payload():
    """Test init_anchor function directly to verify flat V2 payload in RuntimeEnvelope."""
    payload = {
        "actor_id": "Antigravity",
        "intent": "Verify model soul",
        "model_soul": {
            "base_identity": {
                "provider": "google",
                "model_family": "gemini",
                "model_variant": "gemini-2.0-flash",
                "runtime_class": "flash"
            }
        }
    }
    
    # Call the tool function directly
    envelope = await init_anchor(mode="init", **payload)
    
    # Check RuntimeEnvelope
    assert envelope.status == RuntimeStatus.SUCCESS
    
    # Check flattened payload content
    res = envelope.payload
    assert res["ok"] is True
    assert res["tool"] == "init_anchor"
    assert res["result_type"] == "init_anchor_result@v2"
    
    result = res["result"]
    assert result["base_identity"]["verification_status"] == "verified"
    assert result["self_claim_boundary"] == "verified_only"
    
    # Check Phase 2 Identity Split
    assert result["declared_actor_id"] == "Antigravity"
    assert result["auth_state"] == "claimed_only"


@pytest.mark.asyncio
async def test_init_anchor_v2_identity_mismatch():
    """Test init_anchor V2 detecting identity mismatch via main function."""
    payload = {
        "intent": "Test mismatch",
        "model_soul": {
            "base_identity": {
                "provider": "wrong-provider",
                "model_family": "wrong-family",
                "model_variant": "claude-3-7-sonnet" 
            }
        }
    }
    
    envelope = await init_anchor(mode="init", **payload)
    res = envelope.payload
    
    # Check mismatch detection
    assert res["result"]["base_identity"]["verification_status"] == "verified"
    assert res["result"]["base_identity"]["verified"]["soul_archetype"] == "IDENTITY_MISMATCH_HONEYPOT"


@pytest.mark.asyncio
async def test_init_anchor_v2_no_soul():
    """Test init_anchor V2 without model_soul."""
    envelope = await init_anchor(mode="init", actor_id="BasicUser", intent="No soul test")
    res = envelope.payload
    
    assert res["result_type"] == "init_anchor_result@v2"
    # No model_soul should be "unverified"
    assert res["result"]["base_identity"]["verification_status"] == "unverified"


@pytest.mark.asyncio
async def test_init_anchor_v2_claimed_only():
    """Test init_anchor V2 with an unknown model (not in registry)."""
    payload = {
        "intent": "Claimed only test",
        "model_soul": {
            "base_identity": {
                "provider": "unknown",
                "model_family": "alien",
                "model_variant": "alien-model-v9"
            }
        }
    }
    
    envelope = await init_anchor(mode="init", **payload)
    res = envelope.payload
    
    # Unknown model should be "claimed_only"
    assert res["result"]["base_identity"]["verification_status"] == "claimed_only"
