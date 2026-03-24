"""
tests/runtime/test_tools_runtime.py — Runtime Tools Test Suite

Tests for:
- runtime/tools.py — Mega-tool dispatch and routing
- runtime/sessions.py — Session management and identity binding
- runtime/tools_hardened_dispatch.py — Hardened dispatch layer

Target: 85%+ coverage for runtime integrity
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import sys
from types import ModuleType


# =============================================================================
# SESSION MANAGEMENT TESTS
# =============================================================================


class TestSessionManagement:
    """Test session identity binding and continuity."""

    def test_normalize_session_id_with_valid_id(self):
        """Test _normalize_session_id with valid session ID."""
        from arifosmcp.runtime.tools import _normalize_session_id

        result = _normalize_session_id("test-session-001")
        assert result == "test-session-001"

    def test_normalize_session_id_with_none(self):
        """Test _normalize_session_id creates new session when None."""
        from arifosmcp.runtime.tools import _normalize_session_id

        result = _normalize_session_id(None)
        # Should create a new session ID
        assert result.startswith("session-")
        assert len(result) > 8

    def test_normalize_session_id_with_empty_string(self):
        """Test _normalize_session_id with empty string."""
        from arifosmcp.runtime.tools import _normalize_session_id

        result = _normalize_session_id("")
        # Should create a new session ID
        assert result.startswith("session-")

    def test_resolve_caller_context_anonymous(self):
        """Test _resolve_caller_context for anonymous user."""
        from arifosmcp.runtime.tools import _resolve_caller_context

        result = _resolve_caller_context("anonymous")
        assert result.actor_id == "anonymous"
        assert result.identity_type == "anonymous"

    def test_resolve_caller_context_with_claim(self):
        """Test _resolve_caller_context with claimed identity."""
        from arifosmcp.runtime.tools import _resolve_caller_context

        result = _resolve_caller_context("arif")
        assert result.actor_id == "arif"
        assert result.identity_type == "claimed"

    def test_resolve_caller_state_anonymous(self):
        """Test _resolve_caller_state for anonymous."""
        from arifosmcp.runtime.tools import _resolve_caller_state

        caller_state, tools, blocked = _resolve_caller_state("session-123", None)
        assert caller_state == "anonymous"
        assert "init_anchor" in [t["tool"] for t in tools if isinstance(t, dict)]

    def test_resolve_caller_state_anchored(self):
        """Test _resolve_caller_state for anchored session."""
        from arifosmcp.runtime.tools import _resolve_caller_state
        from unittest.mock import Mock

        mock_auth = Mock()
        mock_auth.claim_status = "anchored"

        caller_state, tools, blocked = _resolve_caller_state("session-123", mock_auth)
        assert caller_state == "anchored"


# =============================================================================
# INIT_ANCHOR TESTS
# =============================================================================


class TestInitAnchor:
    """Test init_anchor tool — identity establishment."""

    @pytest.mark.asyncio
    async def test_init_anchor_basic(self):
        """Test basic init_anchor call."""
        from arifosmcp.runtime.tools import init_anchor

        result = await init_anchor(mode="init", payload={"actor_id": "test-user"})

        assert result.ok is True
        assert result.session_id is not None
        assert result.status.value == "SUCCESS"

    @pytest.mark.asyncio
    async def test_init_anchor_with_philosophy(self):
        """Test init_anchor with philosophy selection."""
        from arifosmcp.runtime.tools import init_anchor

        result = await init_anchor(
            mode="init",
            payload={
                "actor_id": "test-user",
                "philosophy": {"school": "apex_theory", "tier": "sovereign"},
            },
        )

        assert result.ok is True
        assert result.philosophy is not None

    @pytest.mark.asyncio
    async def test_init_anchor_returns_session(self):
        """Test init_anchor returns valid session."""
        from arifosmcp.runtime.tools import init_anchor

        result = await init_anchor(mode="init", payload={"actor_id": "arif"})

        # Session should be established
        assert result.session_id is not None
        assert len(result.session_id) > 0


# =============================================================================
# TOOL DISPATCH TESTS
# =============================================================================


class TestToolDispatch:
    """Test mega-tool dispatch and routing."""

    @pytest.mark.asyncio
    async def test_arifos_kernel_dry_run(self):
        """Test arifOS_kernel in dry_run mode."""
        from arifosmcp.runtime.tools import arifOS_kernel

        result = await arifOS_kernel(query="Test query", session_id="test-session", dry_run=True)

        assert result.ok is True

    @pytest.mark.asyncio
    async def test_apex_soul_seal(self):
        """Test apex_soul issues SEAL verdict."""
        from arifosmcp.runtime.tools import apex_soul

        result = await apex_soul(mode="judge", proposal="Safe proposal")

        assert result.ok is True

    @pytest.mark.asyncio
    async def test_vault_ledger_commit(self):
        """Test vault_ledger commit action."""
        from arifosmcp.runtime.tools import vault_ledger

        result = await vault_ledger(mode="commit", payload={"data": "test"})

        assert result.ok is True

    @pytest.mark.asyncio
    async def test_math_estimator(self):
        """Test math_estimator tool."""
        from arifosmcp.runtime.tools import math_estimator

        result = await math_estimator(query="Calculate 2+2", confidence=0.95)

        assert result.ok is True


# =============================================================================
# HARDENED DISPATCH TESTS
# =============================================================================


class TestHardenedDispatch:
    """Test hardened dispatch layer."""

    @pytest.mark.asyncio
    async def test_hardened_init_anchor(self):
        """Test hardened init_anchor dispatch."""
        from arifosmcp.runtime.tools_hardened_dispatch import HARDENED_DISPATCH_MAP

        assert "init_anchor" in HARDENED_DISPATCH_MAP

        dispatch = HARDENED_DISPATCH_MAP["init_anchor"]
        result = await dispatch(mode="init", payload={"actor_id": "test"})

        assert result["ok"] is True

    @pytest.mark.asyncio
    async def test_hardened_architect_registry(self):
        """Test hardened architect_registry dispatch."""
        from arifosmcp.runtime.tools_hardened_dispatch import HARDENED_DISPATCH_MAP

        assert "architect_registry" in HARDENED_DISPATCH_MAP

        dispatch = HARDENED_DISPATCH_MAP["architect_registry"]
        result = await dispatch(mode="list", payload={})

        assert result["ok"] is True
        assert "registry" in result

    def test_arifos_kernel_in_dispatch_map(self):
        """Verify arifOS_kernel is in hardened dispatch map."""
        from arifosmcp.runtime.tools_hardened_dispatch import HARDENED_DISPATCH_MAP

        assert "arifOS_kernel" in HARDENED_DISPATCH_MAP

    @pytest.mark.asyncio
    async def test_hardened_arifos_kernel_requires_session(self):
        """Test hardened arifOS_kernel requires session_id."""
        from arifosmcp.runtime.tools_hardened_dispatch import HARDENED_DISPATCH_MAP

        dispatch = HARDENED_DISPATCH_MAP["arifOS_kernel"]
        result = await dispatch(
            mode="query",
            payload={},  # No session_id
        )

        assert result["ok"] is False
        assert "error" in result
        assert "session_id" in result["error"].lower()


# =============================================================================
# WRAP CALL TESTS
# =============================================================================


class TestWrapCall:
    """Test _wrap_call wrapper function."""

    @pytest.mark.asyncio
    async def test_wrap_call_success(self):
        """Test _wrap_call with successful execution."""
        from arifosmcp.runtime.tools import _wrap_call

        async def mock_tool(**kwargs):
            return {"result": "success"}

        result = await _wrap_call(
            tool_func=mock_tool, session_id="test-session", tool_name="test_tool"
        )

        assert result.ok is True

    @pytest.mark.asyncio
    async def test_wrap_call_with_error(self):
        """Test _wrap_call handles errors gracefully."""
        from arifosmcp.runtime.tools import _wrap_call

        async def failing_tool(**kwargs):
            raise ValueError("Test error")

        result = await _wrap_call(
            tool_func=failing_tool, session_id="test-session", tool_name="failing_tool"
        )

        assert result.ok is False


# =============================================================================
# PHILOSOPHY SELECTION TESTS
# =============================================================================


class TestPhilosophySelection:
    """Test philosophy and governance selection."""

    def test_select_governed_philosophy_default(self):
        """Test default philosophy selection."""
        from arifosmcp.runtime.tools import select_governed_philosophy

        result = select_governed_philosophy()

        assert result is not None
        assert "school" in result

    def test_select_governed_philosophy_with_preference(self):
        """Test philosophy selection with preference."""
        from arifosmcp.runtime.tools import select_governed_philosophy

        result = select_governed_philosophy(
            philosophy={"school": "apex_theory", "tier": "sovereign"}
        )

        assert result["school"] == "apex_theory"


# =============================================================================
# SYSTEM HEALTH TESTS
# =============================================================================


class TestSystemHealth:
    """Test system health and monitoring tools."""

    @pytest.mark.asyncio
    async def test_system_health(self):
        """Test system_health tool."""
        from arifosmcp.runtime.tools import system_health

        result = await system_health()

        assert result.ok is True

    @pytest.mark.asyncio
    async def test_check_vital(self):
        """Test check_vital tool."""
        from arifosmcp.runtime.tools import check_vital

        result = await check_vital(session_id="test-session")

        assert result.ok is True


# =============================================================================
# EDGE CASE TESTS
# =============================================================================


class TestRuntimeEdgeCases:
    """Edge cases for runtime tools."""

    @pytest.mark.asyncio
    async def test_init_anchor_unicode_actor(self):
        """Test init_anchor with unicode actor_id."""
        from arifosmcp.runtime.tools import init_anchor

        result = await init_anchor(mode="init", payload={"actor_id": "用户_測试_ñ"})

        assert result.ok is True

    @pytest.mark.asyncio
    async def test_arifos_kernel_empty_query(self):
        """Test arifOS_kernel with empty query."""
        from arifosmcp.runtime.tools import arifOS_kernel

        result = await arifOS_kernel(query="", session_id="test-session", dry_run=True)

        # Should handle gracefully
        assert result.ok is True

    @pytest.mark.asyncio
    async def test_apex_soul_contradictory_proposal(self):
        """Test apex_soul with contradictory proposal."""
        from arifosmcp.runtime.tools import apex_soul

        result = await apex_soul(
            mode="judge", proposal="This is safe and dangerous at the same time"
        )

        assert result.ok is True
        # Should detect contradiction
