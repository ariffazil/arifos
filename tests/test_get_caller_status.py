
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from arifosmcp.runtime.tools import get_caller_status
from arifosmcp.runtime.models import RuntimeStatus, Verdict, Stage, RuntimeEnvelope

@pytest.mark.asyncio
async def test_get_caller_status_decoration():
    """Verify get_caller_status correctly decorates the envelope via _wrap_call."""
    # We mock call_kernel so _wrap_call can run its decoration logic
    with patch("arifosmcp.runtime.tools.call_kernel", new_callable=AsyncMock) as mock_kernel:
        mock_kernel.return_value = {
            "tool": "get_caller_status",
            "session_id": "global",
            "stage": Stage.INIT_000.value,
            "verdict": Verdict.SEAL.value,
            "status": RuntimeStatus.SUCCESS.value,
            "payload": {},
            "metrics": {"telemetry": {"G_star": 0.5, "confidence": 0.8}, "basis": {}, "witness": {}},
            "authority": {"claim_status": "anonymous", "actor_id": "anonymous"}
        }
        
        envelope = await get_caller_status(session_id="global")
        
        assert envelope.status == RuntimeStatus.SUCCESS
        assert envelope.tool == "get_caller_status"
        assert envelope.caller_state == "anonymous"
        assert envelope.diagnostics_only is True
        assert "check_vital" in envelope.allowed_next_tools
        assert any(t["tool"] == "arifOS_kernel" for t in envelope.blocked_tools)
        assert "bootstrap_sequence" in envelope.payload
        assert envelope.payload["system_motto"] == "DITEMPA BUKAN DIBERI — Forged, Not Given"

@pytest.mark.asyncio
async def test_get_caller_status_anchored_visibility():
    """Verify get_caller_status shows mind/heart tools when anchored."""
    with patch("arifosmcp.runtime.tools.call_kernel", new_callable=AsyncMock) as mock_kernel:
        mock_kernel.return_value = {
            "tool": "get_caller_status",
            "session_id": "session-123",
            "stage": Stage.INIT_000.value,
            "verdict": Verdict.SEAL.value,
            "status": RuntimeStatus.SUCCESS.value,
            "payload": {},
            "authority": {"claim_status": "anchored", "actor_id": "arif"}
        }
        
        envelope = await get_caller_status(session_id="session-123")
        
        assert envelope.caller_state == "anchored"
        assert "agi_reason" in envelope.allowed_next_tools
        assert "search_reality" in envelope.allowed_next_tools
        # High risk tools like engineer should still be blocked if not verified
        assert any(t["tool"] == "agentzero_engineer" for t in envelope.blocked_tools)
