"""
arifOS Gateway Identity Model

Identity and RBAC for the MCP Gateway.
Maps session_id → human actor for accountability (F11 Authority).

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class IdentitySource(str, Enum):
    """Sources of identity authentication."""

    IDP_OIDC = "idp_oidc"
    K8S_SERVICE_ACCOUNT = "k8s_service_account"
    MCP_AUTH_TOKEN = "mcp_auth_token"
    API_KEY = "api_key"


class ActorType(str, Enum):
    """Types of actors."""

    HUMAN = "human"
    SERVICE_ACCOUNT = "service_account"
    AGENT = "agent"


@dataclass
class Actor:
    """An actor (human or service) initiating operations."""

    id: str
    type: ActorType
    source: IdentitySource
    email: str | None = None
    name: str | None = None
    groups: list[str] = field(default_factory=list)
    team: str | None = None

    # For agents: who authorized this agent?
    authorized_by: str | None = None

    # Attestation (for prod operations)
    attestation: str | None = None
    attestation_timestamp: str | None = None

    def to_vault_record(self) -> dict[str, Any]:
        """Convert to VAULT999-compatible record."""
        return {
            "actor_id": self.id,
            "actor_type": self.type.value,
            "source": self.source.value,
            "email": self.email,
            "name": self.name,
            "groups": self.groups,
            "team": self.team,
            "authorized_by": self.authorized_by,
            "attestation": bool(self.attestation),
        }


@dataclass
class SessionIdentity:
    """
    Links a constitutional session to a human actor.

    This answers: "Which human is accountable for this operation?"
    """

    session_id: str
    actor: Actor

    # Operation context
    tool_name: str
    tool_class: str

    # Timestamps
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    # Risk indicators
    blast_radius_score: float = 0.0

    def get_accountable_human(self) -> str | None:
        """
        Get the ultimately accountable human.

        For human actors: returns self
        For service accounts: returns authorized_by
        For agents: traces back to authorizing human
        """
        if self.actor.type == ActorType.HUMAN:
            return self.actor.id
        elif self.actor.authorized_by:
            return self.actor.authorized_by
        else:
            return None  # Orphaned operation — should trigger F11 VOID

    def generate_chain_of_custody(self) -> str:
        """Generate cryptographic chain of custody hash."""
        record = {
            "session_id": self.session_id,
            "actor_id": self.actor.id,
            "actor_type": self.actor.type.value,
            "tool": self.tool_name,
            "timestamp": self.created_at,
        }
        return hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()[:16]


class IdentityRegistry:
    """
    Registry for session-to-identity mappings.

    Stored in Redis (session cache) + VAULT999 (permanent audit).
    """

    def __init__(self):
        self._sessions: dict[str, SessionIdentity] = {}

    def register(
        self,
        session_id: str,
        actor: Actor,
        tool_name: str,
        tool_class: str,
    ) -> SessionIdentity:
        """Register a new session with identity."""
        session = SessionIdentity(
            session_id=session_id,
            actor=actor,
            tool_name=tool_name,
            tool_class=tool_class,
        )
        self._sessions[session_id] = session
        return session

    def get(self, session_id: str) -> SessionIdentity | None:
        """Get session identity by ID."""
        return self._sessions.get(session_id)

    def check_authorization(
        self,
        session_id: str,
        required_class: str,
    ) -> tuple[bool, str]:
        """
        Check if actor is authorized for operation class.

        Returns: (authorized, reason)
        """
        session = self.get(session_id)
        if not session:
            return False, "Session not found (F11)"

        # Check actor type vs operation class
        if required_class == "destructive" and session.actor.type == ActorType.AGENT:
            return (
                False,
                "Agents cannot perform destructive operations without human attestation (F11, F13)",
            )

        if required_class == "prod_write" and not session.actor.attestation:
            return False, "Production operations require human attestation (F13)"

        return True, "Authorized"


# Singleton instance
identity_registry = IdentityRegistry()


def create_human_actor(
    user_id: str,
    email: str,
    name: str,
    groups: list[str] = None,
    source: IdentitySource = IdentitySource.IDP_OIDC,
) -> Actor:
    """Create a human actor."""
    return Actor(
        id=user_id,
        type=ActorType.HUMAN,
        source=source,
        email=email,
        name=name,
        groups=groups or [],
    )


def create_service_account(
    sa_id: str,
    authorized_by: str,
    groups: list[str] = None,
) -> Actor:
    """Create a service account actor."""
    return Actor(
        id=sa_id,
        type=ActorType.SERVICE_ACCOUNT,
        source=IdentitySource.K8S_SERVICE_ACCOUNT,
        groups=groups or [],
        authorized_by=authorized_by,
    )


def create_agent(
    agent_id: str,
    authorized_by: str,
    groups: list[str] = None,
) -> Actor:
    """Create an AI agent actor."""
    return Actor(
        id=agent_id,
        type=ActorType.AGENT,
        source=IdentitySource.MCP_AUTH_TOKEN,
        groups=groups or [],
        authorized_by=authorized_by,
    )
