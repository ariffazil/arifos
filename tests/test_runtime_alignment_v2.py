
import pytest
import asyncio
import json
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from fastmcp import FastMCP
from arifosmcp.runtime.resources import register_resources, read_resource_content
from arifosmcp.runtime.tools import init_anchor, check_vital, Stage
from arifosmcp.runtime.models import Verdict, RuntimeEnvelope, CanonicalAuthority

@pytest.fixture
def mcp():
    return FastMCP("test-server")

@pytest.fixture
def registered_mcp(mcp):
    register_resources(mcp)
    return mcp

class TestResourceAlignment:
    @pytest.mark.asyncio
    async def test_canon_states_content(self, registered_mcp):
        """P1: Verify canon://states resource content exists and is correct."""
        content = await read_resource_content("canon://states")
        assert content is not None
        assert "# arifOS Session Ladder" in content
        assert "anonymous" in content
        assert "anchored" in content
        assert "OPERATOR" in content

    @pytest.mark.asyncio
    async def test_canon_index_includes_states(self, registered_mcp):
        """P5: Verify canon://index includes all 5 resources (once prompts are cleared)."""
        content = await read_resource_content("canon://index")
        data = json.loads(content)
        assert "canon://states" in data["resources"]
        assert len(data["resources"]) >= 5

class TestToolPayloadAlignment:
    @pytest.mark.asyncio
    async def test_init_anchor_enriched_payload(self):
        """P1: Verify init_anchor enriched payload with authority and next_action."""
        # We need to mock _wrap_call because init_anchor calls it
        # and _wrap_call calls call_kernel which requires a running server/engine
        with patch("arifosmcp.runtime.tools._wrap_call", new_callable=AsyncMock) as mock_wrap:
            mock_envelope = MagicMock(spec=RuntimeEnvelope)
            mock_envelope.payload = {
                "session_id": "test-sid",
                "caller_state": "anchored",
                "authority": "OPERATOR",
                "auth_context": {"actor_id": "test-actor"},
                "next_action": "Use arifOS_kernel"
            }
            mock_wrap.return_value = mock_envelope
            
            result = await init_anchor(actor_id="test-actor")
            
            assert result.payload["authority"] == "OPERATOR"
            assert "next_action" in result.payload
            assert result.payload["caller_state"] == "anchored"

    @pytest.mark.asyncio
    async def test_check_vital_bootstrap_guidance(self):
        """P1: Verify check_vital bootstrap guidance fields."""
        with patch("arifosmcp.runtime.tools._wrap_call", new_callable=AsyncMock) as mock_wrap:
            mock_envelope = MagicMock(spec=RuntimeEnvelope)
            # check_vital enriches the envelope from _wrap_call
            mock_envelope.payload = {} 
            mock_wrap.return_value = mock_envelope
            
            # We need to mock _normalize_session_id to return "global" or something stable
            with patch("arifosmcp.runtime.tools._normalize_session_id", return_value="global"):
                # We also need to mock GovernanceKernel since check_vital creates one
                with patch("arifosmcp.runtime.tools.GovernanceKernel") as mock_kernel_cls:
                    mock_kernel = mock_kernel_cls.return_value
                    mock_kernel.get_current_state.return_value = {"auth_state": "anonymous"}
                    
                    result = await check_vital()
                    
                    assert "bootstrap" in result.payload
                    bootstrap = result.payload["bootstrap"]
                    assert "current_state" in bootstrap
                    assert "accessible_tools" in bootstrap
                    assert "blocked_tools" in bootstrap
                    assert "operator_guidance" in bootstrap
                    assert "canon://states" in bootstrap["ladder_resource"]

class TestErrorRemediationAlignment:
    @pytest.mark.asyncio
    async def test_remediation_first_error_response(self):
        """P1: Verify remediation-first error responses in unified_tool_output."""
        from core.enforcement.governance_engine import wrap_tool_output
        
        # Simulate a failing case (VOID verdict)
        payload = {
            "verdict": "VOID",
            "failed_laws": ["F11_AUTHORITY"],
            "auth_state": "unverified",
            "error": "Authentication required"
        }
        
        # wrap_tool_output is synchronous in governance_engine.py
        result = wrap_tool_output(
            tool="test_tool",
            stage="444_ROUTER",
            session_id="test-session",
            payload=payload,
            verdict="VOID"
        )
        
        assert "errors" in result
        error = result["errors"][0]
        assert "remediation" in error
        remediation = error["remediation"]
        assert remediation["next_tool"] == "init_anchor"
        assert "required_args" in remediation
        assert "example_payload" in remediation
        assert remediation["retry_safe"] is True

