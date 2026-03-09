"""
core/schema/authority.py — Authority Context Schema

Governance authority block — who is acting, at what level, and whether
human approval is required.

Production-safe: token fingerprints, nonces, and signatures are NOT
exposed here.  Those belong in the security/audit layer only.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class AuthorityLevel(str, Enum):
    """Canonical authority levels."""

    HUMAN = "human"
    SOVEREIGN = "sovereign"
    OPERATOR = "operator"
    AGENT = "agent"
    SYSTEM = "system"
    ANONYMOUS = "anonymous"


class AuthState(str, Enum):
    """Authentication / authorization state."""

    VERIFIED = "verified"
    PENDING = "pending"
    ANONYMOUS = "anonymous"
    REVOKED = "revoked"
    EXPIRED = "expired"


class Authority(BaseModel):
    """
    Production authority context.

    Only actor_id, level, human_required, approval_scope, and auth_state
    are included in production output.  Security fields (token fingerprint,
    nonce, signature blob, iat/exp) must NOT appear here unless the caller
    has explicitly requested debug/security mode.
    """

    actor_id: str = Field(default="anonymous", description="Canonical actor identifier")
    level: AuthorityLevel = Field(
        default=AuthorityLevel.ANONYMOUS, description="Authority level of the actor"
    )
    human_required: bool = Field(
        default=False, description="Whether human approval is required to proceed"
    )
    approval_scope: list[str] = Field(
        default_factory=list,
        description="Operations this actor is approved to perform",
    )
    auth_state: AuthState = Field(
        default=AuthState.ANONYMOUS, description="Authentication/authorization state"
    )
