"""
arifosmcp/runtime/contracts_v2.py — Hardened Constitutional Contracts (v4)

UPGRADE: Recursive Integrity Hashing and Stability Thresholds.
HARDENING (2026-03-25 — Paris Weather Incident):
  - OutputPolicy enum: forces model surface behaviour when domain payload is absent
  - DRY_RUN poison pill: any dry_run=True envelope forces SIMULATION_ONLY policy
  - Domain payload gate: DOMAIN_PAYLOAD_GATES defines required keys per domain class
  - Verdict namespace split: ROUTER_SEAL vs DOMAIN_SEAL vs SESSION_SEAL
  See: 000/FLOORS/F02_TRUTH.md §Enforcement Addendum (v2026.03.25)
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


class OutputPolicy(str, Enum):
    """
    F2/F7 enforcement: controls what the model surface is ALLOWED to assert.

    REAL_DOMAIN   — domain payload verified; factual claims permitted.
    SIMULATION_ONLY — result is DRY_RUN; model MUST label any answer as
                      'Estimate Only / Simulated'. Never present domain values as real.
    CANNOT_COMPUTE  — required domain payload keys absent; model MUST answer
                      'Cannot Compute — required domain payload absent.'
                      Never substitute training data or memory.
    ROUTER_META     — this is a routing/meta decision only; no domain facts released.
    """
    REAL_DOMAIN = "REAL_DOMAIN"
    SIMULATION_ONLY = "SIMULATION_ONLY"
    CANNOT_COMPUTE = "CANNOT_COMPUTE"
    ROUTER_META = "ROUTER_META"


class VerdictScope(str, Enum):
    """
    Fix 3 — Verdict namespace split.
    Prevents ROUTER_SEAL from blessing domain factual claims.

    ROUTER_SEAL  — internal routing decision is consistent. Does NOT authorise
                   domain claims about the real world.
    DOMAIN_SEAL  — domain payload has Earth evidence + required keys. Factual
                   claims are permitted for this result.
    SESSION_SEAL — anchor session is valid and active.
    DRY_RUN_SEAL — simulation completed. No real execution or domain data.
    DOMAIN_VOID  — required domain payload keys are missing. Cannot Compute.
    """
    ROUTER_SEAL = "ROUTER_SEAL"
    DOMAIN_SEAL = "DOMAIN_SEAL"
    SESSION_SEAL = "SESSION_SEAL"
    DRY_RUN_SEAL = "DRY_RUN_SEAL"
    DOMAIN_VOID = "DOMAIN_VOID"


# F2 — Required payload keys per domain class.
# If a tool returns a domain result missing ANY of these keys,
# the envelope must be CANNOT_COMPUTE / DOMAIN_VOID.
DOMAIN_PAYLOAD_GATES: dict[str, list[str]] = {
    "weather":   ["temp_c", "provider", "timestamp", "location"],
    "finance":   ["price", "ticker", "source", "timestamp"],
    "health":    ["metric", "value", "unit", "source"],
    "code_exec": ["stdout", "exit_code", "execution_id"],
    "search":    ["results", "source_urls", "query_echo"],
    "geography": ["lat", "lon", "place_name", "source"],
}


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
        if self.ambiguity_score > 0.9:
            return False
        return self.delta_s <= 0 and self.confidence >= 0.80

    def to_dict(self) -> dict[str, Any]:
        return {
            "ambiguity_score": round(self.ambiguity_score, 4),
            "contradiction_count": self.contradiction_count,
            "delta_s": round(self.delta_s, 4),
            "confidence": round(self.confidence, 4),
            "is_stable": self.is_stable(),
        }


def check_domain_gate(
    domain_class: str, payload: dict[str, Any]
) -> tuple[bool, list[str]]:
    """
    F2 domain payload gate.
    Returns (passed: bool, missing_keys: list[str]).
    If passed is False, caller must set OutputPolicy.CANNOT_COMPUTE.
    """
    required = DOMAIN_PAYLOAD_GATES.get(domain_class, [])
    missing = [k for k in required if k not in payload]
    return (len(missing) == 0), missing


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
    warnings: list[str] = field(default_factory=list)
    # F2/F7 — output policy: controls what model surface is ALLOWED to assert.
    output_policy: OutputPolicy = OutputPolicy.REAL_DOMAIN
    # Fix 3 — scoped verdict namespace.
    verdict_scope: VerdictScope = VerdictScope.ROUTER_SEAL
    # Fix 1 — DRY_RUN flag: if True, forces SIMULATION_ONLY policy.
    dry_run: bool = False

    def seal_envelope(self) -> None:
        # Fix 1: DRY_RUN poison pill — applied before hash, so it's part of integrity.
        if self.dry_run or self.payload.get("dry_run") is True:
            self.dry_run = True
            self.output_policy = OutputPolicy.SIMULATION_ONLY
            self.verdict_scope = VerdictScope.DRY_RUN_SEAL
            self.status = ToolStatus.OK  # routing may be ok, but domain is not real
            self.warnings.append(
                "DRY_RUN=True: this result is a simulation. "
                "No domain values (weather, finance, health, code output) are real. "
                "Model MUST label any answer referencing this as 'Estimate Only / Simulated'."
            )
        data_to_hash = {
            "payload": self.payload,
            "trace": self.trace.to_dict() if self.trace else {},
            "tool": self.tool,
            "session_id": self.session_id,
            "output_policy": self.output_policy.value,
            "verdict_scope": self.verdict_scope.value,
        }
        self.integrity_hash = hashlib.sha256(
            json.dumps(data_to_hash, sort_keys=True, default=str).encode()
        ).hexdigest()

    def apply_domain_gate(self, domain_class: str) -> None:
        """
        Fix 2 — F2 domain payload gate.
        Call this after populating payload for any domain-class tool result.
        Sets CANNOT_COMPUTE + DOMAIN_VOID if required keys are missing.
        """
        passed, missing = check_domain_gate(domain_class, self.payload)
        if not passed:
            self.output_policy = OutputPolicy.CANNOT_COMPUTE
            self.verdict_scope = VerdictScope.DOMAIN_VOID
            self.status = ToolStatus.VOID
            self.warnings.append(
                f"DOMAIN_GATE_FAIL [{domain_class}]: missing keys {missing}. "
                "Model MUST answer: 'Cannot Compute — required domain payload absent.' "
                "Do NOT substitute training data or memory."
            )
        else:
            self.output_policy = OutputPolicy.REAL_DOMAIN
            self.verdict_scope = VerdictScope.DOMAIN_SEAL

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
            # Fix 1/2/3 — always surface these so models and hosts can enforce policy
            "output_policy": self.output_policy.value,
            "verdict_scope": self.verdict_scope.value,
            "dry_run": self.dry_run,
            "warnings": self.warnings,
        }

    @classmethod
    def hold(
        cls,
        tool: str,
        session_id: str,
        reason: str,
        trace: TraceContext | None = None,
        **kwargs: Any,
    ) -> ToolEnvelope:
        payload = {"reason": reason}
        payload.update(kwargs)
        return cls(
            status=ToolStatus.HOLD,
            tool=tool,
            session_id=session_id,
            risk_tier=RiskTier.HIGH,
            requires_human=True,
            trace=trace,
            payload=payload,
            human_decision=HumanDecisionMarker.HUMAN_CONFIRMATION_REQUIRED,
        )

    @classmethod
    def void(
        cls,
        tool: str,
        session_id: str,
        reason: str,
        trace: TraceContext | None = None,
        **kwargs: Any,
    ) -> ToolEnvelope:
        payload = {"reason": reason}
        payload.update(kwargs)
        return cls(
            status=ToolStatus.VOID,
            tool=tool,
            session_id=session_id,
            risk_tier=RiskTier.LOW,
            trace=trace,
            payload=payload,
            human_decision=HumanDecisionMarker.MACHINE_RECOMMENDATION_ONLY,
        )


def validate_fail_closed(
    auth_context: dict | None,
    risk_tier: str | None,
    session_id: str | None,
    tool: str,
    trace: TraceContext | None = None,
) -> bool:
    return bool(auth_context and risk_tier and session_id)


def calculate_entropy_budget(
    ambiguity_score: float, confidence: float, input_len: int = 0, output_len: int = 0
) -> EntropyBudget:
    return EntropyBudget(
        ambiguity_score=ambiguity_score, delta_s=output_len - input_len, confidence=confidence
    )


def generate_trace_context(
    stage_id: str,
    session_id: str,
    policy_version: str = "v2026.03.24-hardened",
    parent_trace_id: str | None = None,
) -> TraceContext:
    return TraceContext(
        trace_id=f"trace-{secrets.token_hex(16)}",
        parent_trace_id=parent_trace_id,
        stage_id=stage_id,
        policy_version=policy_version,
        session_id=session_id,
    )


def determine_human_marker(
    risk_tier: RiskTier, confidence: float, blast_radius: str = "minimal"
) -> HumanDecisionMarker:
    if risk_tier == RiskTier.SOVEREIGN or blast_radius in ("significant", "catastrophic"):
        return HumanDecisionMarker.HUMAN_APPROVAL_BOUND
    if risk_tier == RiskTier.HIGH or confidence < 0.80:
        return HumanDecisionMarker.HUMAN_CONFIRMATION_REQUIRED
    return HumanDecisionMarker.MACHINE_RECOMMENDATION_ONLY


__all__ = [
    "ToolStatus",
    "RiskTier",
    "HumanDecisionMarker",
    "SessionClass",
    "TraceContext",
    "EntropyBudget",
    "ToolEnvelope",
    "validate_fail_closed",
    "calculate_entropy_budget",
    "generate_trace_context",
    "determine_human_marker",
    # Hardening additions (2026-03-25)
    "OutputPolicy",
    "VerdictScope",
    "DOMAIN_PAYLOAD_GATES",
    "check_domain_gate",
]
