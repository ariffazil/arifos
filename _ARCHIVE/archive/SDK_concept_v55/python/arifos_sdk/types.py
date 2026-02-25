"""
Type definitions for arifOS SDK.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class Verdict(str, Enum):
    """Constitutional verdicts."""

    SEAL = "SEAL"
    VOID = "VOID"
    PARTIAL = "PARTIAL"
    SABAR = "SABAR"
    HOLD_888 = "888_HOLD"


class ActorType(str, Enum):
    """Types of actors."""

    HUMAN = "human"
    SERVICE_ACCOUNT = "service_account"
    AGENT = "agent"


class ToolClass(str, Enum):
    """Risk classification for tools."""

    READ_ONLY = "read_only"
    INFRA_WRITE = "infra_write"
    DESTRUCTIVE = "destructive"
    PROD_WRITE = "prod_write"


@dataclass
class FloorResult:
    """Result of a single floor check."""

    floor: str  # F1, F2, etc.
    name: str
    passed: bool
    score: float
    detail: str | None = None


@dataclass
class BlastRadius:
    """Infrastructure blast radius calculation."""

    score: float  # 0.0-1.0
    affected_pods: int
    affected_deployments: int
    critical_namespaces: list[str]
    mitigation_suggestions: list[str]


@dataclass
class GatewayDecision:
    """Result of gateway constitutional evaluation."""

    session_id: str
    tool_name: str
    tool_class: ToolClass
    verdict: Verdict
    floors: list[FloorResult]
    hard_failures: list[str]
    blast_radius: BlastRadius | None = None
    reasoning: str = ""
    manifest_hash: str | None = None
    downstream_endpoint: str | None = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    @property
    def is_blocked(self) -> bool:
        """Check if operation is blocked."""
        return self.verdict == Verdict.VOID

    @property
    def requires_human_approval(self) -> bool:
        """Check if 888_HOLD."""
        return self.verdict == Verdict.HOLD_888

    @property
    def can_proceed(self) -> bool:
        """Check if operation can proceed (SEAL or PARTIAL)."""
        return self.verdict in (Verdict.SEAL, Verdict.PARTIAL)


@dataclass
class HumanApprovalRequest:
    """Request for human approval (888_HOLD)."""

    hold_id: str
    session_id: str
    tool_name: str
    payload: dict[str, Any]
    blast_radius: BlastRadius | None
    floors_failed: list[str]
    reasoning: str
    requested_by: str
    requested_at: str
    review_url: str

    def to_slack_message(self) -> str:
        """Format as Slack message."""
        return f"""
🛑 *888_HOLD: Human Approval Required*

*Operation:* `{self.tool_name}`
*Session:* `{self.session_id}`
*Requested by:* {self.requested_by}

*Blast Radius:* {self.blast_radius.score if self.blast_radius else 'N/A'}
*Floors Failed:* {', '.join(self.floors_failed) if self.floors_failed else 'None'}

*Reason:* {self.reasoning}

*Review:* {self.review_url}
        """.strip()

    def to_email_subject(self) -> str:
        """Format as email subject."""
        return f"[arifOS] 888_HOLD: {self.tool_name} requires approval"


@dataclass
class HumanApprovalResponse:
    """Response to human approval request."""

    hold_id: str
    approved: bool
    verdict: Verdict
    approved_by: str | None = None
    approved_at: str | None = None
    rejection_reason: str | None = None

    @property
    def is_approved(self) -> bool:
        """Check if approved (SEAL)."""
        return self.approved and self.verdict == Verdict.SEAL


@dataclass
class SessionContext:
    """Context for a constitutional session."""

    session_id: str
    actor_id: str
    actor_type: ActorType
    groups: list[str]
    team: str | None = None
    attestation: str | None = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def get_accountable_human(self) -> str:
        """Get ultimately accountable human."""
        if self.actor_type == ActorType.HUMAN:
            return self.actor_id
        return f"{self.actor_id} (authorized by: unknown)"
