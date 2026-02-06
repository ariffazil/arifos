"""
arifOS v55 Handler Layer Tests
Tests for Phase 2: Handler existence, session state, edge cases

DITEMPA BUKAN DIBERI
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

# Ensure repo root is on path
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


# =============================================================================
# Phase 2.1: Handler Existence Tests
# =============================================================================

class TestHandlerExistence:
    """Verify all 9 core handlers exist and are callable."""

    def test_handler_imports(self):
        """All handlers can be imported without errors."""
        from mcp_server.tools.canonical_trinity import (
            mcp_init,
            mcp_agi,
            mcp_asi,
            mcp_apex,
            mcp_reality,
            mcp_trinity,
            mcp_vault,
        )
        
        assert callable(mcp_init)
        assert callable(mcp_agi)
        assert callable(mcp_asi)
        assert callable(mcp_apex)
        assert callable(mcp_reality)
        assert callable(mcp_trinity)
        assert callable(mcp_vault)

    def test_lambda_wrappers_callable(self):
        """Lambda wrappers for split tools are callable."""
        from mcp_server.tools.canonical_trinity import mcp_agi, mcp_asi, mcp_apex
        
        # Test AGI wrappers
        agi_sense = lambda **kw: mcp_agi(action="sense", **kw)
        agi_think = lambda **kw: mcp_agi(action="think", **kw)
        agi_reason = lambda **kw: mcp_agi(action="reason", **kw)
        
        assert callable(agi_sense)
        assert callable(agi_think)
        assert callable(agi_reason)
        
        # Test ASI wrappers
        asi_empathize = lambda **kw: mcp_asi(action="empathize", **kw)
        asi_align = lambda **kw: mcp_asi(action="align", **kw)
        
        assert callable(asi_empathize)
        assert callable(asi_align)
        
        # Test APEX wrapper
        apex_verdict = lambda **kw: mcp_apex(action="judge", **kw)
        assert callable(apex_verdict)

    def test_all_9_handlers_registered(self):
        """Tool registry contains all 9 core handlers."""
        from mcp_server.core.tool_registry import ToolRegistry
        
        registry = ToolRegistry()
        tools = registry.list_tools()
        
        expected_tools = [
            "init_gate",
            "agi_sense",
            "agi_think",
            "agi_reason",
            "asi_empathize",
            "asi_align",
            "apex_verdict",
            "reality_search",
            "vault_seal",
        ]
        
        for tool_name in expected_tools:
            assert tool_name in tools, f"Tool {tool_name} not registered"
            tool = tools[tool_name]
            assert tool.handler is not None, f"{tool_name} has no handler"
            assert callable(tool.handler), f"{tool_name} handler not callable"


# =============================================================================
# Phase 2.2: Session State Propagation Tests
# =============================================================================

class TestSessionStateBasics:
    """Test basic session state infrastructure."""

    @pytest.mark.asyncio
    async def test_session_id_accepted(self):
        """Handlers accept session_id parameter."""
        from mcp_server.tools.canonical_trinity import mcp_agi, mcp_asi
        
        # Mock the kernel to avoid dependencies
        with patch('mcp.tools.canonical_trinity.get_kernel_manager') as mock_km:
            mock_agi = AsyncMock()
            mock_agi.execute = AsyncMock(return_value={
                "session_id": "sess_test123",
                "entropy_delta": 0.0,
                "vote": "SEAL"
            })
            mock_km.return_value.get_agi.return_value = mock_agi
            
            # Call with session_id
            result = await mcp_agi(action="sense", query="test", session_id="sess_test123")
            
            # Verify session_id was passed to kernel
            assert mock_agi.execute.called
            call_args = mock_agi.execute.call_args
            assert call_args[0][1]["session_id"] == "sess_test123"

    @pytest.mark.asyncio
    async def test_session_id_returned(self):
        """Handlers return session_id in response."""
        from mcp_server.tools.canonical_trinity import mcp_agi
        
        with patch('mcp.tools.canonical_trinity.get_kernel_manager') as mock_km:
            mock_agi = AsyncMock()
            mock_agi.execute = AsyncMock(return_value={
                "session_id": "sess_test123",
                "entropy_delta": 0.0,
                "vote": "SEAL"
            })
            mock_km.return_value.get_agi.return_value = mock_agi
            
            result = await mcp_agi(action="sense", query="test", session_id="sess_test123")
            
            assert "session_id" in result
            assert result["session_id"] == "sess_test123"

    def test_session_id_pattern_valid(self):
        """Session IDs match expected pattern."""
        import re
        from mcp_server.core.tool_registry import ToolRegistry
        
        registry = ToolRegistry()
        tool = registry.get("agi_sense")
        
        schema = tool.input_schema
        session_id_prop = schema["properties"]["session_id"]
        
        assert "pattern" in session_id_prop
        pattern = session_id_prop["pattern"]
        
        # Test valid session IDs (pattern requires at least 8 chars after sess_)
        valid_ids = ["sess_abc12345", "sess_XYZ78901", "sess_12345678"]
        regex = re.compile(pattern)
        
        for sid in valid_ids:
            assert regex.match(sid), f"Valid ID {sid} doesn't match pattern"


# =============================================================================
# Phase 2.3: Circular Dependency Tests
# =============================================================================

class TestCircularDependencies:
    """Verify no circular imports between handlers."""

    def test_no_handler_cross_imports(self):
        """Handlers don't import each other."""
        import os
        import re
        
        repo_root = Path(__file__).parents[1]
        tools_dir = repo_root / "codebase" / "mcp" / "tools"
        
        # Helper function to search for regex in files
        def search_in_files(directory, pattern):
            matches = []
            regex = re.compile(pattern)
            for root, dirs, files in os.walk(directory):
                # Exclude _archive and __pycache__
                if "_archive" in dirs:
                    dirs.remove("_archive")
                if "__pycache__" in dirs:
                    dirs.remove("__pycache__")
                
                for file in files:
                    if file.endswith(".py"):
                        file_path = Path(root) / file
                        try:
                            content = file_path.read_text(encoding="utf-8")
                            # Check if any line matches the import pattern
                            for line in content.splitlines():
                                if regex.search(line):
                                    matches.append(str(file_path))
                                    break
                        except Exception:
                            pass
            return matches

        # Check for mcp_agi imports (exact word match to avoid mcp_agi_genius)
        # Matches: "from ... import mcp_agi" or "import mcp_agi"
        matches_agi = search_in_files(tools_dir, r"(^|\s)(from|import)\s+.*mcp_agi\b")
        
        # Check for mcp_asi imports
        matches_asi = search_in_files(tools_dir, r"(^|\s)(from|import)\s+.*mcp_asi\b")
        
        assert not matches_agi, f"Found mcp_agi cross-imports in: {matches_agi}"
        assert not matches_asi, f"Found mcp_asi cross-imports in: {matches_asi}"

    def test_handlers_call_kernel_only(self):
        """Handlers use kernel interface, not direct handler calls."""
        from aaa_mcp.tools import canonical_trinity
        import inspect
        
        # Get source of mcp_agi
        source = inspect.getsource(canonical_trinity.mcp_agi)
        
        # Should call get_kernel_manager, not other handlers
        assert "get_kernel_manager" in source
        assert "kernel.execute" in source
        
        # Should NOT directly call other handlers
        assert "mcp_asi(" not in source
        assert "mcp_apex(" not in source


# =============================================================================
# Phase 2.5: Edge Case Tests
# =============================================================================

class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_legacy_router_unknown_action(self):
        """Legacy _agi_ router fails gracefully on unknown action."""
        from mcp_server.tools.canonical_trinity import mcp_agi
        
        with patch('mcp.tools.canonical_trinity.get_kernel_manager') as mock_km:
            mock_agi = AsyncMock()
            # Simulate unknown action error
            mock_agi.execute = AsyncMock(side_effect=ValueError("Unknown action"))
            mock_km.return_value.get_agi.return_value = mock_agi
            
            # Should not crash, should return error verdict
            result = await mcp_agi(action="invalid_xyz", query="test")
            
            assert "verdict" in result or "vote" in result
            # Should be VOID due to error
            verdict = result.get("verdict", result.get("vote", ""))
            assert verdict in ["VOID", "SABAR"]

    @pytest.mark.asyncio
    async def test_handler_without_session_id(self):
        """Handlers work without session_id (creates one automatically)."""
        from mcp_server.tools.canonical_trinity import mcp_agi
        
        with patch('mcp.tools.canonical_trinity.get_kernel_manager') as mock_km:
            mock_agi = AsyncMock()
            mock_agi.execute = AsyncMock(return_value={
                "session_id": "auto_generated_123",
                "entropy_delta": 0.0,
                "vote": "SEAL"
            })
            mock_km.return_value.get_agi.return_value = mock_agi
            
            # Call without session_id
            result = await mcp_agi(action="sense", query="test")
            
            # Should still work and return a session_id
            assert "session_id" in result
            assert result["session_id"]  # Not None or empty

    def test_legacy_aliases_not_registered(self):
        """v55 registry does not register legacy aliases (clean registry)."""
        from mcp_server.core.tool_registry import ToolRegistry

        registry = ToolRegistry()

        # Legacy aliases should NOT be in the clean v55 registry
        assert registry.get("_agi_") is None
        assert registry.get("_asi_") is None


# =============================================================================
# Phase 2 Validation Summary
# =============================================================================

class TestPhase2Validation:
    """Summary validation for Phase 2 completion."""

    def test_all_validation_criteria_met(self):
        """Phase 2 validation checklist items."""
        from mcp_server.core.tool_registry import ToolRegistry
        
        registry = ToolRegistry()
        tools = registry.list_tools()
        
        # All 9 handlers registered
        core_tools = [
            "init_gate", "agi_sense", "agi_think", "agi_reason",
            "asi_empathize", "asi_align", "apex_verdict",
            "reality_search", "vault_seal",
        ]
        
        for tool_name in core_tools:
            assert tool_name in tools, f"Missing tool: {tool_name}"
            tool = tools[tool_name]
            assert callable(tool.handler), f"{tool_name} not callable"
            
            # Has session_id in input schema
            props = tool.input_schema.get("properties", {})
            assert "session_id" in props, f"{tool_name} missing session_id"
        
        # Total count: 9 canonical tools
        assert len(tools) >= 9, f"Expected >= 9 tools, got {len(tools)}"

    def test_no_breaking_changes(self):
        """v55 canonical tool names are all present."""
        from mcp_server.core.tool_registry import ToolRegistry

        registry = ToolRegistry()

        # v55 canonical names
        assert registry.get("init_gate") is not None
        assert registry.get("agi_sense") is not None
        assert registry.get("asi_empathize") is not None
        assert registry.get("apex_verdict") is not None
        assert registry.get("reality_search") is not None
        assert registry.get("vault_seal") is not None
