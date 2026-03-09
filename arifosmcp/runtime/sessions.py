"""
arifosmcp/runtime/sessions.py — Session Continuity State

Centralized session registry for arifOS runtime. 
Extracted from legacy transport layer to enable clean architecture.
"""

from typing import Any
from core.shared.types import ActorIdentity

# Global Session Registry (In-memory fallback for stateless bridge)
_ACTOR_IDENTITIES: dict[str, ActorIdentity] = {}
_ACTOR_SESSION_MAP: dict[str, str] = {}  # session_id -> actor_id
_ACTIVE_SESSION_ID: str | None = None
_SESSION_CONTINUITY_STATE: dict[str, dict[str, Any]] = {}

def _resolve_session_id(provided_id: str | None) -> str | None:
    """Resolve session_id from provided input or last active session."""
    if provided_id and str(provided_id).strip():
        return provided_id
    return _ACTIVE_SESSION_ID

def set_active_session(session_id: str) -> None:
    """Update the global pointer for the last active session."""
    global _ACTIVE_SESSION_ID
    _ACTIVE_SESSION_ID = session_id
