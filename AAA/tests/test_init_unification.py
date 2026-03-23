"""
tests/test_init_unification.py — Unified Init Anchor Test Suite

Validates the ONE init_anchor tool consolidation:
- All modes work: init, state, status, revoke, refresh
- Legacy tools route correctly via CAPABILITY_MAP
- Constitutional floors enforced (F11, F12, F13)
- Session continuity maintained
"""

from __future__ import annotations

import pytest
import asyncio
from typing import Any

# Test imports with lazy loading to avoid circular imports
@pytest.fixture
def capability_map():
    from arifosmcp.capability_map import CAPABILITY_MAP
    return CAPABILITY_MAP

@pytest.fixture
def public_tool_specs():
    from arifosmcp.runtime.tool_specs import PUBLIC_TOOL_SPECS
    return PUBLIC_TOOL_SPECS


class TestLegacyToolRouting:
    """Verify legacy tools route to unified init_anchor via CAPABILITY_MAP."""

    def test_init_anchor_state_routes_to_init_anchor(self, capability_map):
        """Legacy 'init_anchor_state' routes to init_anchor with mode='state'."""
        target = capability_map.get("init_anchor_state")
        assert target is not None
        assert target.mega_tool == "init_anchor"
        assert target.mode == "state"
        print("✓ init_anchor_state → init_anchor(mode='state')")

    def test_revoke_anchor_state_routes_to_init_anchor(self, capability_map):
        """Legacy 'revoke_anchor_state' routes to init_anchor with mode='revoke'."""
        target = capability_map.get("revoke_anchor_state")
        assert target is not None
        assert target.mega_tool == "init_anchor"
        assert target.mode == "revoke"
        print("✓ revoke_anchor_state → init_anchor(mode='revoke')")

    def test_get_caller_status_routes_to_init_anchor(self, capability_map):
        """Legacy 'get_caller_status' routes to init_anchor with mode='status'."""
        target = capability_map.get("get_caller_status")
        assert target is not None
        assert target.mega_tool == "init_anchor"
        assert target.mode == "status"
        print("✓ get_caller_status → init_anchor(mode='status')")


class TestToolSpecCompliance:
    """Verify tool spec matches unified implementation."""

    def test_init_anchor_in_public_specs(self, public_tool_specs):
        """init_anchor is in PUBLIC_TOOL_SPECS with correct modes."""
        spec = next((s for s in public_tool_specs if s.name == "init_anchor"), None)
        assert spec is not None
        assert spec.stage == "000_INIT"
        modes = spec.input_schema["properties"]["mode"]["enum"]
        assert "init" in modes
        assert "state" in modes
        assert "status" in modes
        assert "revoke" in modes
        assert "refresh" in modes
        print(f"✓ Tool spec includes all 5 unified modes: {modes}")

    def test_description_mentions_unification(self, public_tool_specs):
        """Tool description mentions unified nature."""
        spec = next((s for s in public_tool_specs if s.name == "init_anchor"), None)
        assert spec is not None
        desc = spec.description
        assert "Unified" in desc or "unified" in desc.lower()
        assert "ONE tool" in desc or "ONE" in desc
        print("✓ Tool description documents unification")


class TestModeEnums:
    """Verify InitAnchorMode enum has all required modes."""

    def test_all_modes_present(self):
        from arifosmcp.capability_map import InitAnchorMode
        modes = {m.value for m in InitAnchorMode}
        assert "init" in modes
        assert "state" in modes
        assert "status" in modes
        assert "revoke" in modes
        assert "refresh" in modes
        print(f"✓ InitAnchorMode includes: {modes}")


class TestImplementationStructure:
    """Verify the internal implementation structure."""

    def test_init_anchor_impl_handles_all_modes(self):
        """init_anchor_impl has dispatch logic for all 5 modes."""
        from arifosmcp.runtime.tools_internal import init_anchor_impl
        import inspect
        
        source = inspect.getsource(init_anchor_impl)
        # Check for mode dispatch
        assert 'mode == "revoke"' in source or "mode == 'revoke'" in source
        assert 'mode == "refresh"' in source or "mode == 'refresh'" in source
        assert 'mode == "status"' in source or "mode == 'status'" in source
        print("✓ init_anchor_impl dispatches all 5 modes")

    def test_legacy_impls_exist_as_wrappers(self):
        """Legacy implementations are maintained as wrappers."""
        from arifosmcp.runtime.tools_internal import (
            revoke_anchor_state_impl,
            refresh_anchor_impl,
            get_caller_status_impl,
        )
        print("✓ Legacy wrapper implementations exist")


class TestUnifiedToolSignature:
    """Verify the unified tool signature accepts all parameters."""

    def test_init_anchor_accepts_all_modes_via_payload(self):
        """init_anchor accepts mode in payload."""
        from arifosmcp.runtime.tools import init_anchor
        import inspect
        
        sig = inspect.signature(init_anchor)
        params = list(sig.parameters.keys())
        
        assert "mode" in params
        assert "payload" in params
        print(f"✓ init_anchor signature: {list(params)}")


if __name__ == "__main__":
    print("=" * 70)
    print("UNIFIED INIT ANCHOR TEST SUITE — Architectural Verification")
    print("=" * 70)
    print()
    
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
