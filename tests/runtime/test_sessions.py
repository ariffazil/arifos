"""
tests/runtime/test_sessions.py — Session Management Tests

Tests for runtime/sessions.py — identity binding and session continuity
"""

import pytest
from unittest.mock import Mock, patch


class TestSessionNormalization:
    """Test _normalize_session_id function."""

    def test_normalize_with_valid_session(self):
        """Test normalizing a valid session ID."""
        from arifosmcp.runtime.sessions import _normalize_session_id

        result = _normalize_session_id("test-session-123")
        assert result == "test-session-123"

    def test_normalize_with_none_creates_new(self):
        """Test that None creates a new session ID."""
        from arifosmcp.runtime.sessions import _normalize_session_id

        result = _normalize_session_id(None)
        assert result.startswith("session-")
        assert len(result) == 16  # "session-" + 8 hex chars

    def test_normalize_with_empty_string_creates_new(self):
        """Test that empty string creates a new session ID."""
        from arifosmcp.runtime.sessions import _normalize_session_id

        result = _normalize_session_id("")
        assert result.startswith("session-")


class TestSessionIdentityBinding:
    """Test session identity binding functions."""

    def test_bind_and_get_identity(self):
        """Test binding and retrieving session identity."""
        from arifosmcp.runtime.sessions import bind_session_identity, get_session_identity

        # Bind identity
        bind_session_identity(
            session_id="test-bind-001",
            actor_id="arif",
            authority_level="sovereign",
            auth_context={"verified": True},
            human_approval=True,
        )

        # Retrieve identity
        identity = get_session_identity("test-bind-001")
        assert identity is not None
        assert identity["actor_id"] == "ariffazil"  # Normalized
        assert identity["authority_level"] == "sovereign"
        assert identity["human_approval"] is True

    def test_get_identity_nonexistent(self):
        """Test getting identity for non-existent session."""
        from arifosmcp.runtime.sessions import get_session_identity

        identity = get_session_identity("nonexistent-session-xyz")
        assert identity is None

    def test_clear_session_identity(self):
        """Test clearing session identity."""
        from arifosmcp.runtime.sessions import (
            bind_session_identity,
            get_session_identity,
            clear_session_identity,
        )

        # Bind and verify
        bind_session_identity(
            session_id="test-clear-001",
            actor_id="test-user",
            authority_level="user",
            auth_context={},
        )
        assert get_session_identity("test-clear-001") is not None

        # Clear and verify
        clear_session_identity("test-clear-001")
        assert get_session_identity("test-clear-001") is None


class TestActiveSession:
    """Test active session management."""

    def test_set_and_resolve_active_session(self):
        """Test setting and resolving active session."""
        from arifosmcp.runtime.sessions import set_active_session, _resolve_session_id

        # Set active session
        set_active_session("active-session-001")

        # Resolve with None should return active session
        result = _resolve_session_id(None)
        assert result == "active-session-001"

    def test_resolve_session_with_provided_id(self):
        """Test resolving with provided ID takes precedence."""
        from arifosmcp.runtime.sessions import set_active_session, _resolve_session_id

        set_active_session("active-session")
        result = _resolve_session_id("provided-session")

        # Provided ID takes precedence
        assert result == "provided-session"


class TestRuntimeContext:
    """Test runtime context resolution."""

    def test_resolve_runtime_context_anonymous(self):
        """Test context resolution for anonymous user."""
        from arifosmcp.runtime.sessions import resolve_runtime_context

        context = resolve_runtime_context(
            incoming_session_id=None, auth_context=None, actor_id=None, declared_name=None
        )

        assert context["canonical_actor_id"] == "anonymous"
        assert context["transport_session_id"] == "global"

    def test_resolve_runtime_context_with_actor(self):
        """Test context resolution with actor ID."""
        from arifosmcp.runtime.sessions import resolve_runtime_context

        context = resolve_runtime_context(
            incoming_session_id="session-123",
            auth_context=None,
            actor_id="arif",
            declared_name="Arif Fazil",
        )

        # Actor ID should be normalized
        assert context["canonical_actor_id"] == "ariffazil"
        assert context["display_name"] == "Arif Fazil"


class TestSessionCounting:
    """Test session counting functionality."""

    def test_list_active_sessions_count(self):
        """Test counting active sessions."""
        from arifosmcp.runtime.sessions import (
            bind_session_identity,
            list_active_sessions_count,
            clear_session_identity,
        )

        # Get initial count
        initial_count = list_active_sessions_count()

        # Bind a new session
        bind_session_identity(
            session_id="count-test-001", actor_id="test", authority_level="user", auth_context={}
        )

        # Count should increase
        new_count = list_active_sessions_count()
        assert new_count == initial_count + 1

        # Cleanup
        clear_session_identity("count-test-001")
