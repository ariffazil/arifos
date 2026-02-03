"""
arifOS MCP Session Context
Implicit session binding for constitutional tools.
"""

from contextvars import ContextVar
from typing import Optional

# Universal session ID context (works across async tasks)
_SESSION_ID: ContextVar[Optional[str]] = ContextVar("session_id", default=None)


def set_current_session_id(session_id: str) -> None:
    """Set the session ID for the current context."""
    _SESSION_ID.set(session_id)


def get_current_session_id() -> Optional[str]:
    """Retrieve the session ID from the current context."""
    return _SESSION_ID.get()
