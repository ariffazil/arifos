"""
ACLIP_CAI MCP Bridge Tests
===========================

Tests for MCP integration with aaa-mcp server.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch

from aclip_cai.mcp_bridge import (
    aclip_system_health,
    aclip_process_list,
    aclip_forge_guard,
    register_aclip_tools,
)


def _get_tool_fn(tool):
    """Extract the callable function from a FastMCP FunctionTool or return as-is."""
    if hasattr(tool, "fn"):
        return tool.fn  # FastMCP wraps tools in FunctionTool objects
    return tool


@pytest.mark.asyncio
async def test_mcp_bridge_system_health():
    """Test MCP bridge for system health."""
    fn = _get_tool_fn(aclip_system_health)
    result = await fn(include_swap=True)

    assert result["tool"] == "system_health"
    assert result["status"] == "ok"
    assert "data" in result
    assert "timestamp" in result
    assert "latency_ms" in result


@pytest.mark.asyncio
async def test_mcp_bridge_process_list():
    """Test MCP bridge for process list."""
    fn = _get_tool_fn(aclip_process_list)
    result = await fn(limit=5)

    assert result["tool"] == "process_list"
    assert result["status"] == "ok"
    assert "processes" in result["data"]


@pytest.mark.asyncio
async def test_mcp_bridge_forge_guard_constitutional():
    """Test forge guard includes constitutional envelope."""
    fn = _get_tool_fn(aclip_forge_guard)
    result = await fn(
        action="test", target="/tmp", session_id="test-session", risk_level="low", dry_run=True
    )

    assert result["tool"] == "forge_guard"
    assert "motto" in result
    assert "pass" in result
    assert result["data"]["verdict"] == "SEAL"


@pytest.mark.asyncio
async def test_mcp_bridge_forge_guard_blocks_dangerous():
    """Test forge guard blocks dangerous actions."""
    fn = _get_tool_fn(aclip_forge_guard)
    result = await fn(
        action="execute",
        target="rm -rf /",
        session_id="test-session",
        risk_level="low",
        dry_run=True,
    )

    assert result["data"]["verdict"] == "VOID"
    assert result["data"]["danger_detected"] is True
    assert result["pass"] == "hold"


def test_register_aclip_tools():
    """Test tool registration with mock MCP server."""
    mock_mcp = Mock()
    mock_mcp.tool = Mock(return_value=lambda f: f)

    register_aclip_tools(mock_mcp)

    # Should have registered 9 tools
    assert mock_mcp.tool.call_count == 9


@pytest.mark.asyncio
async def test_mcp_response_structure():
    """Test that MCP responses have correct structure."""
    fn = _get_tool_fn(aclip_system_health)
    result = await fn()

    # Required fields for MCP compatibility
    required_fields = ["tool", "status", "timestamp", "data", "error", "latency_ms"]
    for field in required_fields:
        assert field in result, f"Missing field: {field}"

    # Status must be valid
    assert result["status"] in ["ok", "error", "warning"]

    # Timestamp must be ISO format-like
    assert "T" in result["timestamp"]

    # Data must be dict
    assert isinstance(result["data"], dict)
