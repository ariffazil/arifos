"""Request/session dependency helpers for AAA MCP tools."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class SessionContext:
    actor_id: str
    session_id: str
    token_present: bool


def build_session_context(actor_id: str, session_id: str, auth_token: str | None) -> SessionContext:
    """Normalize runtime session context for FastMCP handlers."""
    return SessionContext(
        actor_id=(actor_id or "anonymous").strip(),
        session_id=(session_id or "").strip(),
        token_present=bool(auth_token),
    )


def context_to_dict(ctx: SessionContext) -> Dict[str, Any]:
    return {
        "actor_id": ctx.actor_id,
        "session_id": ctx.session_id,
        "token_present": ctx.token_present,
    }
