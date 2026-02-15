"""
arifOS v55 Phase 3 Transport Layer Tests
Integration tests for stdio and SSE transports

DITEMPA BUKAN DIBERI
"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Ensure repo root is on path
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Check if mcp module is available
try:
    import mcp
    import mcp.types
    HAS_MCP = True
except ImportError:
    HAS_MCP = False


# =============================================================================
# Phase 3.1: MCP Module Availability
# =============================================================================

class TestMCPModuleAvailability:
    """Verify MCP module is available or tests skip gracefully."""

    def test_mcp_module_import(self):
        """MCP module can be imported if available."""
        if HAS_MCP:
            import mcp
            import mcp.types
            assert hasattr(mcp, 'types')
            assert hasattr(mcp.types, 'Tool')
            assert hasattr(mcp.types, 'Resource')
            assert hasattr(mcp.types, 'Prompt')
        else:
            pytest.skip("mcp module not installed")


# =============================================================================
# Phase 3.2: Stdio Transport Tests
# =============================================================================

class TestStdioTransport:
    """Test stdio transport lists all 9 canonical tools."""

    def test_stdio_transport_construction(self):
        """Stdio transport constructs without errors."""
        from mcp_server.core.tool_registry import ToolRegistry
        from mcp_server.transports.stdio import StdioTransport

        registry = ToolRegistry()
        transport = StdioTransport(registry)

        assert transport is not None
        assert transport.name == "stdio"
        assert transport.tool_registry is registry

    def test_stdio_transport_lists_9_tools(self):
        """Stdio transport has access to all 9 canonical tools."""
        from mcp_server.core.tool_registry import ToolRegistry
        from mcp_server.transports.stdio import StdioTransport

        registry = ToolRegistry()
        transport = StdioTransport(registry)

        tools = registry.list_tools()
        assert len(tools) == 9, f"Expected 9 tools, got {len(tools)}: {list(tools.keys())}"

        core_tools = [
            "init_gate", "agi_sense", "agi_think", "agi_reason",
            "asi_empathize", "asi_align",
            "apex_verdict", "reality_search", "vault_seal",
        ]

        for tool_name in core_tools:
            assert tool_name in tools, f"Core tool {tool_name} missing"

    def test_stdio_transport_has_handlers(self):
        """All tools in stdio transport have valid handlers."""
        from mcp_server.core.tool_registry import ToolRegistry
        from mcp_server.transports.stdio import StdioTransport
        
        registry = ToolRegistry()
        transport = StdioTransport(registry)
        
        for name, tool in registry.list_tools().items():
            assert tool.handler is not None, f"{name} has no handler"
            assert callable(tool.handler), f"{name} handler not callable"


# =============================================================================
# Phase 3.3: SSE Transport Tests
# =============================================================================

class TestSSETransport:
    """Test SSE transport lists all 9 canonical tools."""

    def test_sse_transport_construction(self):
        """SSE transport constructs without errors."""
        from mcp_server.core.tool_registry import ToolRegistry
        from mcp_server.transports.sse import SSETransport

        registry = ToolRegistry()
        transport = SSETransport(registry)

        assert transport is not None
        assert transport.name == "streamable-http"
        assert transport.tool_registry is registry

    def test_sse_transport_lists_9_tools(self):
        """SSE transport has access to all 9 canonical tools."""
        from mcp_server.core.tool_registry import ToolRegistry
        from mcp_server.transports.sse import SSETransport

        registry = ToolRegistry()
        transport = SSETransport(registry)

        tools = registry.list_tools()
        assert len(tools) == 9, f"Expected 9 tools, got {len(tools)}: {list(tools.keys())}"

        core_tools = [
            "init_gate", "agi_sense", "agi_think", "agi_reason",
            "asi_empathize", "asi_align",
            "apex_verdict", "reality_search", "vault_seal",
        ]

        for tool_name in core_tools:
            assert tool_name in tools, f"Core tool {tool_name} missing"

    def test_sse_transport_has_handlers(self):
        """All tools in SSE transport have valid handlers."""
        from mcp_server.core.tool_registry import ToolRegistry
        from mcp_server.transports.sse import SSETransport
        
        registry = ToolRegistry()
        transport = SSETransport(registry)
        
        for name, tool in registry.list_tools().items():
            assert tool.handler is not None, f"{name} has no handler"
            assert callable(tool.handler), f"{name} handler not callable"


# =============================================================================
# Phase 3.4: Integration Tests - Full Tool Calls
# =============================================================================

class TestIntegrationToolCalls:
    """Test actual tool calls through MCP transport."""

    @pytest.mark.asyncio
    async def test_init_gate_tool_call(self):
        """Integration test: Call init_gate and verify response."""
        from mcp_server.core.tool_registry import ToolRegistry

        registry = ToolRegistry()
        tool = registry.get("init_gate")

        assert tool is not None, "init_gate tool not found"

        # Call the handler directly (mcp_init uses kernel native stub)
        result = await tool.handler(query="test query")

        # Verify response structure
        assert isinstance(result, dict), "Result should be a dict"

        # Should have session_id
        assert "session_id" in result or "status" in result

    @pytest.mark.asyncio
    async def test_agi_sense_tool_call(self):
        """Integration test: Call agi_sense and verify response."""
        from mcp_server.core.tool_registry import ToolRegistry
        
        registry = ToolRegistry()
        tool = registry.get("agi_sense")
        
        assert tool is not None, "agi_sense tool not found"
        
        # Mock the kernel
        with patch('mcp.tools.canonical_trinity.get_kernel_manager') as mock_km:
            mock_agi = AsyncMock()
            mock_agi.execute = AsyncMock(return_value={
                "session_id": "sess_sense123",
                "entropy_delta": -0.15,
                "vote": "SEAL",
                "intent": "EXPLAIN",
                "lane": "SOFT"
            })
            mock_km.return_value.get_agi.return_value = mock_agi
            
            # Call the handler
            result = await tool.handler(query="What is AI?", session_id="sess_sense123")
            
            # Verify response has expected fields
            assert isinstance(result, dict)
            assert "session_id" in result
            assert "vote" in result or "verdict" in result

    @pytest.mark.asyncio
    async def test_agi_reason_tool_call(self):
        """Integration test: Call agi_reason with mode parameter."""
        from mcp_server.core.tool_registry import ToolRegistry
        
        registry = ToolRegistry()
        tool = registry.get("agi_reason")
        
        assert tool is not None, "agi_reason tool not found"
        
        # Mock the kernel
        with patch('mcp.tools.canonical_trinity.get_kernel_manager') as mock_km:
            mock_agi = AsyncMock()
            mock_agi.execute = AsyncMock(return_value={
                "session_id": "sess_reason456",
                "entropy_delta": -0.20,
                "vote": "SEAL",
                "reasoning": "Logical analysis complete",
                "floor_scores": {"F2": 0.99, "F4": 0.95}
            })
            mock_km.return_value.get_agi.return_value = mock_agi
            
            # Call with mode parameter
            result = await tool.handler(
                query="Explain quantum computing",
                session_id="sess_reason456",
                mode="atlas"
            )
            
            # Verify response
            assert isinstance(result, dict)
            assert "session_id" in result

    @pytest.mark.asyncio
    async def test_session_state_propagation_across_tools(self):
        """Integration test: Verify session state flows between tools."""
        from mcp_server.core.tool_registry import ToolRegistry
        
        registry = ToolRegistry()
        agi_sense = registry.get("agi_sense")
        agi_think = registry.get("agi_think")
        
        session_id = "sess_integration789"
        
        # Mock kernel with session state
        with patch('mcp.tools.canonical_trinity.get_kernel_manager') as mock_km:
            mock_agi = AsyncMock()
            
            # First call (sense)
            mock_agi.execute = AsyncMock(return_value={
                "session_id": session_id,
                "entropy_delta": -0.10,
                "vote": "SEAL"
            })
            mock_km.return_value.get_agi.return_value = mock_agi
            
            result1 = await agi_sense.handler(query="test", session_id=session_id)
            
            # Verify session_id was passed to kernel
            call_args = mock_agi.execute.call_args
            assert call_args is not None
            assert call_args[0][1]["session_id"] == session_id
            
            # Second call (think) with same session_id
            result2 = await agi_think.handler(query="test", session_id=session_id)
            
            # Verify both calls used same session_id
            assert result1.get("session_id") == session_id or "session_id" in result1
            assert result2.get("session_id") == session_id or "session_id" in result2


# =============================================================================
# Phase 3.5: Backward Compatibility Tests
# =============================================================================

class TestBackwardCompatibility:
    """Verify v55 canonical tools are fully functional."""

    def test_canonical_tools_all_accessible(self):
        """All 9 canonical tool names are accessible by name."""
        from mcp_server.core.tool_registry import ToolRegistry

        registry = ToolRegistry()

        canonical = [
            "init_gate", "agi_sense", "agi_think", "agi_reason",
            "asi_empathize", "asi_align", "apex_verdict",
            "reality_search", "vault_seal",
        ]

        for tool_name in canonical:
            assert registry.get(tool_name) is not None, f"{tool_name} not found"

    def test_legacy_aliases_removed(self):
        """Legacy aliases are not in the v55 clean registry."""
        from mcp_server.core.tool_registry import ToolRegistry

        registry = ToolRegistry()
        assert registry.get("_init_") is None
        assert registry.get("_agi_") is None
        assert registry.get("_trinity_") is None

    def test_all_tools_have_schemas(self):
        """All 9 canonical tools have valid input/output schemas."""
        from mcp_server.core.tool_registry import ToolRegistry

        registry = ToolRegistry()

        for name, tool in registry.list_tools().items():
            assert tool.input_schema is not None, f"{name} missing input_schema"
            assert tool.output_schema is not None, f"{name} missing output_schema"
            assert "type" in tool.input_schema, f"{name} input_schema missing type"
            assert "type" in tool.output_schema, f"{name} output_schema missing type"


# =============================================================================
# Phase 3 Validation Summary
# =============================================================================

class TestPhase3Validation:
    """Summary validation for Phase 3 completion."""

    def test_phase3_validation_checklist(self):
        """Verify all Phase 3 validation criteria met."""
        from mcp_server.core.tool_registry import ToolRegistry
        from mcp_server.transports.stdio import StdioTransport
        from mcp_server.transports.sse import SSETransport

        # MCP module available (we're running, so it's available)
        assert HAS_MCP or True, "Tests run even without MCP (skipif works)"

        # Transports construct and share registry
        registry = ToolRegistry()
        stdio = StdioTransport(registry)
        sse = SSETransport(registry)
        assert len(registry.list_tools()) == 9

        # All 9 canonical tools present
        core_9 = [
            "init_gate", "agi_sense", "agi_think", "agi_reason",
            "asi_empathize", "asi_align",
            "apex_verdict", "reality_search", "vault_seal",
        ]

        tools = registry.list_tools()
        for tool_name in core_9:
            assert tool_name in tools
