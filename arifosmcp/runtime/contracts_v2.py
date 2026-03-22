"""
arifosmcp/runtime/contracts_v2.py — Hardened Constitutional Contracts (v2)

Global upgrades for all 11 tools per architectural review:
1. Typed contracts with standardized envelope
2. Fail-closed defaults
3. Cross-tool trace IDs
4. Human decision markers
5. Entropy budget tracking

This is the foundation that makes arifOS a governed constitution,
not just an AI framework.
"""

from __future__ import annotations

import hashlib
import json
import secrets
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal


# ═══════════════════════════════════════════════════════════════════════════════
# 1. TYPED CONTRACTS — Standardized Envelope for ALL Tools
# ═══════════════════════════════════════════════════════════════════════════════

class ToolStatus(str, Enum):
    """Canonical status for ALL tool returns."""
    OK = "ok"
    HOLD = "hold"      # Paused, needs human
    VOID = "void"      # Rejected, do not proceed
    ERROR = "error"    # System failure
    SABAR = "sabar"    # Cooling/retry required


class RiskTier(str, Enum):
    """Risk classification for ALL operations."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    SOVEREIGN = "sovereign"  # Requires human fiat


class HumanDecisionMarker(str, Enum):
    """Explicit human involvement markers."""
    MACHINE_RECOMMENDATION_ONLY = "machine_recommendation_only"
    HUMAN_CONFIRMATION_REQUIRED = "human_confirmation_required"
    HUMAN_APPROVAL_BOUND = "human_approval_bound"
    SEALED = "sealed"


class SessionClass(str, Enum):
    """Authority scope classes for init_anchor."""
    OBSERVE = "observe"      # Read-only, monitoring
    ADVISE = "advise"        # Recommendations, no execution
    EXECUTE = "execute"      # Standard operations
    SOVEREIGN = "sovereign"  # High-stakes, irreversible


@dataclass(frozen=True)
class TraceContext:
    """
    Cross-tool trace IDs for complete auditability.
    
    Without this, audit becomes cerita kabur (ghost story).
    """
    trace_id: str                    # Root trace for entire operation
    parent_trace_id: str | None      # Who called this tool
    stage_id: str                    # 000-999 stage identifier
    policy_version: str              # Which policy governed this
    session_id: str                  # Session binding
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "parent_trace_id": self.parent_trace_id,
            "stage_id": self.stage_id,
            "policy_version": self.policy_version,
            "session_id": self.session_id,
            "timestamp": self.timestamp,
        }


@dataclass
class EntropyBudget:
    """
    Entropy tracking for stability measurement.
    
    arifOS is about stability, not just output.
    """
    ambiguity_score: float = 0.0       # 0.0-1.0, higher = more ambiguous
    contradiction_count: int = 0       # Number of contradictions detected
    unresolved_assumptions: list[str] = field(default_factory=list)
    blast_radius_estimate: str = "minimal"  # minimal | limited | significant | catastrophic
    
    # Thermodynamic metrics
    delta_s: float = 0.0               # Entropy change
    confidence: float = 0.0            # 0.0-1.0
    
    def is_stable(self) -> bool:
        """Check if operation meets stability thresholds."""
        return (
            self.ambiguity_score < 0.5 and
            self.contradiction_count == 0 and
            self.delta_s <= 0 and
            self.confidence >= 0.80
        )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "ambiguity_score": round(self.ambiguity_score, 4),
            "contradiction_count": self.contradiction_count,
            "unresolved_assumptions": self.unresolved_assumptions,
            "blast_radius_estimate": self.blast_radius_estimate,
            "delta_s": round(self.delta_s, 4),
            "confidence": round(self.confidence, 4),
            "is_stable": self.is_stable(),
        }


@dataclass
class ToolEnvelope:
    """
    STANDARDIZED ENVELOPE — ALL tools return this.
    
    This alone reduces entropy a lot by making every tool
    speak the same language.
    """
    # Core identity
    status: ToolStatus
    tool: str
    session_id: str
    
    # Risk and authority
    risk_tier: RiskTier
    confidence: float = 0.0
    human_decision: HumanDecisionMarker = HumanDecisionMarker.MACHINE_RECOMMENDATION_ONLY
    requires_human: bool = False
    
    # Integrity (cryptographic binding)
    inputs_hash: str = ""            # SHA256 of canonical inputs
    outputs_hash: str = ""           # SHA256 of canonical outputs
    
    # Audit trail
    trace: TraceContext | None = None
    evidence_refs: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    
    # Entropy/stability
    entropy: EntropyBudget = field(default_factory=EntropyBudget)
    
    # Routing (what can happen next)
    next_allowed_tools: list[str] = field(default_factory=list)
    
    # Tool-specific payload
    payload: dict[str, Any] = field(default_factory=dict)
    
    def compute_hashes(self, inputs: dict, outputs: dict) -> None:
        """Compute integrity hashes for inputs and outputs."""
        self.inputs_hash = hashlib.sha256(
            json.dumps(inputs, sort_keys=True, default=str).encode()
        ).hexdigest()[:32]
        
        self.outputs_hash = hashlib.sha256(
            json.dumps(outputs, sort_keys=True, default=str).encode()
        ).hexdigest()[:32]
    
    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict for JSON transport."""
        return {
            "status": self.status.value,
            "tool": self.tool,
            "session_id": self.session_id,
            "risk_tier": self.risk_tier.value,
            "confidence": round(self.confidence, 4),
            "human_decision": self.human_decision.value,
            "requires_human": self.requires_human,
            "inputs_hash": self.inputs_hash,
            "outputs_hash": self.outputs_hash,
            "trace": self.trace.to_dict() if self.trace else None,
            "evidence_refs": self.evidence_refs,
            "warnings": self.warnings,
            "entropy": self.entropy.to_dict(),
            "next_allowed_tools": self.next_allowed_tools,
            "payload": self.payload,
        }
    
    @classmethod
    def hold(
        cls,
        tool: str,
        session_id: str,
        reason: str,
        trace: TraceContext | None = None,
        missing_requirements: list[str] | None = None,
        next_allowed_tools: list[str] | None = None,
        suggested_canonical_call: dict | None = None,
        claimed_actor_id: str | None = None,
    ) -> "ToolEnvelope":
        """Factory for HOLD state — fail-closed default with structured continuation."""
        payload: dict = {
            "hold_reason": reason,
            "identity": {
                "claimed_actor_id": claimed_actor_id or "anonymous",
                "verified_actor_id": None,
                "auth_state": "unverified",
                "note": "Claimed identity is not treated as authority until auth_context is provided.",
            },
        }
        if missing_requirements:
            payload["missing_requirements"] = missing_requirements
            payload["next_required_inputs"] = missing_requirements
        if suggested_canonical_call:
            payload["suggested_canonical_call"] = suggested_canonical_call
        if next_allowed_tools:
            payload["guidance"] = (
                f"To continue: provide {', '.join(missing_requirements or ['required fields'])} "
                f"and call {next_allowed_tools[0]}."
            )
        return cls(
            status=ToolStatus.HOLD,
            tool=tool,
            session_id=session_id,
            risk_tier=RiskTier.SOVEREIGN,
            confidence=0.0,
            human_decision=HumanDecisionMarker.HUMAN_CONFIRMATION_REQUIRED,
            requires_human=True,
            trace=trace,
            warnings=[f"HOLD: {reason}"],
            next_allowed_tools=next_allowed_tools or [],
            payload=payload,
        )
    
    @classmethod
    def void(
        cls,
        tool: str,
        session_id: str,
        reason: str,
        trace: TraceContext | None = None,
    ) -> "ToolEnvelope":
        """Factory for VOID state — hard rejection."""
        return cls(
            status=ToolStatus.VOID,
            tool=tool,
            session_id=session_id,
            risk_tier=RiskTier.SOVEREIGN,
            confidence=0.0,
            human_decision=HumanDecisionMarker.MACHINE_RECOMMENDATION_ONLY,
            requires_human=False,
            trace=trace,
            warnings=[f"VOID: {reason}"],
            payload={"void_reason": reason},
        )


# ═══════════════════════════════════════════════════════════════════════════════
# 2. FAIL-CLOSED DEFAULTS — Validation Functions
# ═══════════════════════════════════════════════════════════════════════════════

class ValidationResult:
    """Result of input validation."""
    def __init__(self, valid: bool, reason: str | None = None, missing: list[str] = None):
        self.valid = valid
        self.reason = reason
        self.missing = missing or []
    
    def to_envelope(self, tool: str, session_id: str, trace: TraceContext | None = None) -> ToolEnvelope:
        if self.valid:
            raise ValueError("Cannot create error envelope from valid result")
        return ToolEnvelope.hold(
            tool=tool,
            session_id=session_id,
            reason=self.reason or f"Missing required: {', '.join(self.missing)}",
            trace=trace,
        )


def validate_fail_closed(
    auth_context: dict | None,
    risk_tier: str | None,
    session_id: str | None,
    tool: str,
    trace: TraceContext | None = None,
    requires_evidence: bool = False,
    evidence_refs: list | None = None,
) -> ValidationResult:
    """
    Fail-closed validation: if critical fields missing, return HOLD.
    
    Missing:
    - auth_context → HOLD
    - risk_tier → HOLD
    - session_id → HOLD
    - evidence_refs when truth claims → HOLD
    """
    missing = []
    
    if not auth_context:
        missing.append("auth_context")
    
    if not risk_tier:
        missing.append("risk_tier")
    
    if not session_id:
        missing.append("session_id")
    
    if requires_evidence and not evidence_refs:
        missing.append("evidence_refs (required for truth claims)")
    
    if missing:
        return ValidationResult(
            valid=False,
            reason=f"Fail-closed: missing {', '.join(missing)}",
            missing=missing,
        )
    
    return ValidationResult(valid=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 3. TRACE ID GENERATION — Audit Trail Infrastructure
# ═══════════════════════════════════════════════════════════════════════════════

def generate_trace_context(
    stage_id: str,
    session_id: str,
    policy_version: str = "v2026.03.22-hardened",
    parent_trace_id: str | None = None,
) -> TraceContext:
    """Generate a new trace context for tool invocation."""
    trace_id = f"trace-{secrets.token_hex(16)}"
    
    return TraceContext(
        trace_id=trace_id,
        parent_trace_id=parent_trace_id,
        stage_id=stage_id,
        policy_version=policy_version,
        session_id=session_id,
    )


def child_trace(parent: TraceContext, stage_id: str) -> TraceContext:
    """Create child trace for downstream tool calls."""
    return TraceContext(
        trace_id=parent.trace_id,  # Same root trace
        parent_trace_id=parent.trace_id,
        stage_id=stage_id,
        policy_version=parent.policy_version,
        session_id=parent.session_id,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 4. HUMAN DECISION MARKERS — Authority State Machine
# ═══════════════════════════════════════════════════════════════════════════════

def determine_human_marker(
    risk_tier: RiskTier,
    confidence: float,
    blast_radius: str,
    human_approved: bool = False,
) -> HumanDecisionMarker:
    """
    Determine appropriate human involvement marker.
    
    Machine recommendation only:
    - Low risk, high confidence, minimal blast
    
    Human confirmation required:
    - Medium risk, OR medium confidence
    
    Human approval bound:
    - High risk, OR high blast radius
    
    Sealed:
    - Already approved and sealed
    """
    if human_approved:
        return HumanDecisionMarker.SEALED
    
    if risk_tier == RiskTier.SOVEREIGN or blast_radius in ("significant", "catastrophic"):
        return HumanDecisionMarker.HUMAN_APPROVAL_BOUND
    
    if risk_tier == RiskTier.HIGH or confidence < 0.80:
        return HumanDecisionMarker.HUMAN_CONFIRMATION_REQUIRED
    
    if risk_tier == RiskTier.MEDIUM or confidence < 0.95:
        return HumanDecisionMarker.HUMAN_CONFIRMATION_REQUIRED
    
    return HumanDecisionMarker.MACHINE_RECOMMENDATION_ONLY


# ═══════════════════════════════════════════════════════════════════════════════
# 5. ENTROPY BUDGET CALCULATION — Stability Metrics
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_entropy_budget(
    ambiguity_score: float = 0.0,
    contradictions: list | None = None,
    assumptions: list[str] | None = None,
    blast_radius: str = "minimal",
    input_complexity: float = 0.0,
    output_complexity: float = 0.0,
    confidence: float = 0.0,
) -> EntropyBudget:
    """
    Calculate entropy budget for stability assessment.
    
    Delta-S = output_complexity - input_complexity
    If positive, system added entropy (bad).
    If negative, system reduced entropy (good).
    """
    delta_s = output_complexity - input_complexity
    
    return EntropyBudget(
        ambiguity_score=ambiguity_score,
        contradiction_count=len(contradictions) if contradictions else 0,
        unresolved_assumptions=assumptions or [],
        blast_radius_estimate=blast_radius,
        delta_s=delta_s,
        confidence=confidence,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT — All hardened contract components
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Enums
    "ToolStatus",
    "RiskTier", 
    "HumanDecisionMarker",
    "SessionClass",
    # Core classes
    "TraceContext",
    "EntropyBudget",
    "ToolEnvelope",
    # Validation
    "ValidationResult",
    "validate_fail_closed",
    # Trace generation
    "generate_trace_context",
    "child_trace",
    # Decision markers
    "determine_human_marker",
    # Entropy
    "calculate_entropy_budget",
]
