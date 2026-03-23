"""
arifosmcp/runtime/contracts_v2.py — Hardened Constitutional Contracts (v3)

UPGRADE: Recursive Integrity Hashing and Stability Thresholds.
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

class ToolStatus(str, Enum):
    OK = "ok"
    HOLD = "hold"
    VOID = "void"
    ERROR = "error"
    SABAR = "sabar"

class RiskTier(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    SOVEREIGN = "sovereign"

class HumanDecisionMarker(str, Enum):
    MACHINE_RECOMMENDATION_ONLY = "machine_recommendation_only"
    HUMAN_CONFIRMATION_REQUIRED = "human_confirmation_required"
    HUMAN_APPROVAL_BOUND = "human_approval_bound"
    SEALED = "sealed"

class SessionClass(str, Enum):
    OBSERVE = "observe"
    ADVISE = "advise"
    EXECUTE = "execute"
    SOVEREIGN = "sovereign"

@dataclass(frozen=True)
class TraceContext:
    trace_id: str
    parent_trace_id: str | None
    stage_id: str
    policy_version: str
    session_id: str
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
    ambiguity_score: float = 0.0
    contradiction_count: int = 0
    delta_s: float = 0.0
    confidence: float = 0.0

    def is_stable(self) -> bool:
        if self.ambiguity_score > 0.9: return False
        return self.delta_s <= 0 and self.confidence >= 0.80

    def to_dict(self) -> dict[str, Any]:
        return {
            "ambiguity_score": round(self.ambiguity_score, 4),
            "contradiction_count": self.contradiction_count,
            "delta_s": round(self.delta_s, 4),
            "confidence": round(self.confidence, 4),
            "is_stable": self.is_stable(),
        }

@dataclass
class ToolEnvelope:
    status: ToolStatus
    tool: str
    session_id: str
    risk_tier: RiskTier
    confidence: float = 0.0
    human_decision: HumanDecisionMarker = HumanDecisionMarker.MACHINE_RECOMMENDATION_ONLY
    requires_human: bool = False
    integrity_hash: str = ""
    trace: TraceContext | None = None
    entropy: EntropyBudget = field(default_factory=EntropyBudget)
    payload: dict[str, Any] = field(default_factory=dict)

    def seal_envelope(self) -> None:
        data_to_hash = {
            "payload": self.payload,
            "trace": self.trace.to_dict() if self.trace else {},
            "tool": self.tool,
            "session_id": self.session_id
        }
        self.integrity_hash = hashlib.sha256(
            json.dumps(data_to_hash, sort_keys=True, default=str).encode()
        ).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        self.seal_envelope()
        return {
            "status": self.status.value,
            "tool": self.tool,
            "session_id": self.session_id,
            "risk_tier": self.risk_tier.value,
            "confidence": round(self.confidence, 4),
            "human_decision": self.human_decision.value,
            "integrity_hash": self.integrity_hash,
            "trace": self.trace.to_dict() if self.trace else None,
            "entropy": self.entropy.to_dict(),
            "payload": self.payload,
        }

    @classmethod
    def hold(cls, tool: str, session_id: str, reason: str, trace: TraceContext | None = None) -> ToolEnvelope:
        return cls(
            status=ToolStatus.HOLD, tool=tool, session_id=session_id, risk_tier=RiskTier.SOVEREIGN,
            requires_human=True, trace=trace, payload={"reason": reason},
            human_decision=HumanDecisionMarker.HUMAN_CONFIRMATION_REQUIRED
        )

def validate_fail_closed(auth_context: dict | None, risk_tier: str | None, session_id: str | None, tool: str, trace: TraceContext | None = None) -> bool:
    return bool(auth_context and risk_tier and session_id)

def calculate_entropy_budget(ambiguity_score: float, confidence: float, input_len: int = 0, output_len: int = 0) -> EntropyBudget:
    return EntropyBudget(ambiguity_score=ambiguity_score, delta_s=output_len - input_len, confidence=confidence)

def generate_trace_context(stage_id: str, session_id: str, policy_version: str = "v2026.03.24-hardened", parent_trace_id: str | None = None) -> TraceContext:
    return TraceContext(trace_id=f"trace-{secrets.token_hex(16)}", parent_trace_id=parent_trace_id, stage_id=stage_id, policy_version=policy_version, session_id=session_id)

def determine_human_marker(risk_tier: RiskTier, confidence: float, blast_radius: str = "minimal") -> HumanDecisionMarker:
    if risk_tier == RiskTier.SOVEREIGN or blast_radius in ("significant", "catastrophic"):
        return HumanDecisionMarker.HUMAN_APPROVAL_BOUND
    if risk_tier == RiskTier.HIGH or confidence < 0.80:
        return HumanDecisionMarker.HUMAN_CONFIRMATION_REQUIRED
    return HumanDecisionMarker.MACHINE_RECOMMENDATION_ONLY

__all__ = [
    "ToolStatus", "RiskTier", "HumanDecisionMarker", "SessionClass", "TraceContext", 
    "EntropyBudget", "ToolEnvelope", "validate_fail_closed", "calculate_entropy_budget",
    "generate_trace_context", "determine_human_marker"
]
