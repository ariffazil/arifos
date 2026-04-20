from __future__ import annotations
"""
arifOS v2.0 — Kernel Core Schemas
══════════════════════════════════
Defines the wire-types for the constitutional microkernel.
Rule 2: One state name = one meaning.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, List, Optional, Dict
from pydantic import BaseModel, Field, ConfigDict


class RiskTier(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class KernelTaskMode(str, Enum):
    """Explicit task modes for the kernel router."""
    QUERY = "query"            # Pure informational
    METABOLIC = "metabolic"    # Full init->sense->mind->heart->judge
    FORGE = "forge"            # Execution dispatch
    RECONCILE = "reconcile"    # State alignment
    AUDIT = "audit"            # Integrity check


class Session(BaseModel):
    """Kernel session context."""
    session_id: str
    actor_id: str
    authority_level: str
    risk_tier: RiskTier = RiskTier.MEDIUM
    is_polluted: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Verdict(BaseModel):
    """Canonical constitutional verdict."""
    verdict: str  # SEAL, HOLD, SABAR, VOID
    confidence: float = Field(ge=0.0, le=1.0)
    dS: float = Field(..., description="Entropy delta")
    peace2: float = Field(..., description="Stability score")
    omega_ortho: float = Field(..., description="Orthogonality score")
    floors_passed: List[str]
    floors_violated: List[str]
    reason: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DecisionPacket(BaseModel):
    """The output of the MIND stage, input to HEART/JUDGE."""
    summary: str
    facts: List[str]
    assumptions: List[str]
    uncertainties: List[str]
    proposed_action: Optional[Dict[str, Any]] = None
    confidence_score: float
    logic_chain: List[str]


class ExecutionManifest(BaseModel):
    """Signed directive for Tier 05 FORGE."""
    manifest_id: str
    session_id: str
    tool_name: str
    arguments: Dict[str, Any]
    verdict_hash: str  # Hash of the SEAL verdict
    consensus_token: str
    risk_tier: RiskTier
    expires_at: datetime


class VaultRecord(BaseModel):
    """Immutable Merkle-hashed ledger entry."""
    record_id: str
    parent_hash: str
    self_hash: str
    session_id: str
    actor_id: str
    stage: str
    verdict: str
    payload: Dict[str, Any]
    metrics: Dict[str, float]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TrustLevel(str, Enum):
    LOW = "low"      # External perception, unverified
    HIGH = "high"    # Internal metabolic, verified actor
    SOVEREIGN = "sovereign" # Architect override


class HighTrustExecutionManifest(ExecutionManifest):
    """Execution manifest requiring high-trust signer."""
    signer_id: str
    signature: str
    trust_level: TrustLevel = TrustLevel.HIGH


class LowTrustQueryPacket(BaseModel):
    """Packet for informational, low-risk queries."""
    query: str
    session_id: str
    trust_level: TrustLevel = TrustLevel.LOW


class KernelRouterInput(BaseModel):
    """Hardened input for arifOS_kernel."""
    query: str
    mode: KernelTaskMode = KernelTaskMode.METABOLIC
    session: Session
    context: Dict[str, Any] = Field(default_factory=dict)
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
