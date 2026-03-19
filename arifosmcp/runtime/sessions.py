"""
arifosmcp/runtime/sessions.py — Session Continuity State

Centralized session registry for arifOS runtime.
Single source of truth for session → identity binding.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from typing import Any

from core.shared.types import ActorIdentity

# Global Session Registry (In-memory fallback for stateless bridge)
_ACTOR_IDENTITIES: dict[str, ActorIdentity] = {}
_ACTOR_SESSION_MAP: dict[str, str] = {}  # session_id -> actor_id
_ACTIVE_SESSION_ID: str | None = None
_SESSION_CONTINUITY_STATE: dict[str, dict[str, Any]] = {}

# ── Session Identity Storage ──────────────────────────────────────────────
# Stores the resolved identity for each anchored session.
# This is the canonical binding: session_id → {actor_id, authority_level, auth_context, ...}
_SESSION_IDENTITY: dict[str, dict[str, Any]] = {}


def _resolve_session_id(provided_id: str | None) -> str | None:
    """Resolve session_id from provided input or last active session."""
    if provided_id and str(provided_id).strip():
        return provided_id
    return _ACTIVE_SESSION_ID


def set_active_session(session_id: str) -> None:
    """Update the global pointer for the last active session."""
    global _ACTIVE_SESSION_ID
    _ACTIVE_SESSION_ID = session_id


def bind_session_identity(
    session_id: str,
    actor_id: str,
    authority_level: str,
    auth_context: dict[str, Any],
    approval_scope: list[str] | None = None,
) -> None:
    """
    Bind a verified identity to a session. Called after successful init_anchor.

    This is the canonical write: after this call, get_session_identity(session_id)
    will return the stored identity instead of anonymous defaults.
    """
    _SESSION_IDENTITY[session_id] = {
        "actor_id": actor_id,
        "authority_level": authority_level,
        "auth_context": auth_context,
        "approval_scope": approval_scope or [],
        "caller_state": "anchored",
    }
    _ACTOR_SESSION_MAP[session_id] = actor_id


def get_session_identity(session_id: str) -> dict[str, Any] | None:
    """
    Retrieve the stored identity for a session.

    Returns None if the session has not been anchored via init_anchor.
    """
    return _SESSION_IDENTITY.get(session_id)


def clear_session_identity(session_id: str) -> None:
    """Remove stored identity for a session (e.g., on revocation)."""
    _SESSION_IDENTITY.pop(session_id, None)
    _ACTOR_SESSION_MAP.pop(session_id, None)
