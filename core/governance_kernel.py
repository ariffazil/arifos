# aaa_mcp/core/governance_kernel.py
# v64.2 — Unified GovernanceState (Ψ) Object with Thermodynamic Constraints
# T000: 2026.02.15-FORGE-TRINITY-SEAL
# Q2 Verdict: SYNCHRONOUS but CONDITIONAL

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

# F4 + F11: Thermodynamic constraints (moved from aaa_mcp/ to core/)
try:
    from core.physics.thermodynamics import EntropyManager, ThermodynamicState

    THERMODYNAMICS_AVAILABLE = True
except ImportError:
    THERMODYNAMICS_AVAILABLE = False


class AuthorityLevel(Enum):
    """L5 Identity Control — Authority tagging."""

    ANALYSIS = "analysis"  # Informational only
    SUGGESTION = "suggestion"  # Optional recommendation
    REQUIRES_HUMAN = "requires_human"  # Decision boundary
    UNSAFE_TO_AUTOMATE = "unsafe"  # Hard stop


class GovernanceState(Enum):
    """L6-L8 Governance states."""

    ACTIVE = "active"  # Normal operation
    AWAITING_888 = "awaiting_888"  # Q2: Synchronous hold
    CONDITIONAL = "conditional"  # Proceed with constraints
    VOID = "void"  # Blocked


@dataclass
class GovernanceKernel:
    """
    v64.2 Unified Governance Kernel (Ψ) — T000 Rebirth

    Architectural Fix: Thermodynamic constraints (F4, F11, F7)
    now live in core/ (kernel), not aaa_mcp/ (adapter).

    Q2 Architectural Decision:
    - Single runtime object for all governance state
    - Synchronous AWAITING_888 when thresholds exceeded
    - Conditional flow for low-risk operations
    - Thermodynamic state integrated (ZRAM, CPU, memory)

    All layers read/write this object — no more scattered checks.
    """

    # L0: Thermodynamic Foundation (NEW — v64.2)
    entropy_manager: Any | None = field(default=None, repr=False)
    thermodynamic_state: Any | None = field(default=None)

    # L5: Authority & Identity
    authority_level: AuthorityLevel = AuthorityLevel.ANALYSIS
    decision_owner: str = "ai"  # "ai" | "human" | "system"

    # L4: Uncertainty State (from UncertaintyEngine)
    safety_omega: float = 0.0  # Harmonic mean (system safety)
    display_omega: float = 0.0  # Geometric mean (user display)
    uncertainty_components: dict[str, float] = field(default_factory=dict)

    # L7: Action Gate — Irreversibility
    irreversibility_index: float = 0.0  # impact × recovery_cost × time
    reversibility_score: float = 1.0  # 1.0 = fully reversible

    # L6: Constitutional State
    governance_state: GovernanceState = GovernanceState.ACTIVE
    escalation_required: bool = False

    # L8: Human Sovereign
    human_approval_status: str = (
        "not_required"  # "not_required" | "pending" | "approved" | "denied"
    )
    human_override_timestamp: float | None = None

    # Thresholds (Q2: CONDITIONAL)
    IRREVERSIBILITY_THRESHOLD: float = 0.6  # index > 0.6 → AWAITING_888
    UNCERTAINTY_THRESHOLD: float = 0.06  # safety_omega > 0.06 → AWAITING_888

    # Metadata
    timestamp: float = field(default_factory=time.time)
    session_id: str = ""

    def __post_init__(self):
        """
        F4 + F11: Initialize thermodynamic constraints (v64.2 fix).

        This ensures EntropyManager lives in kernel (core/), not adapter (aaa_mcp/).
        Constitutional Boundary: Thermodynamic state is kernel-level concern.
        """
        if THERMODYNAMICS_AVAILABLE and self.entropy_manager is None:
            self.entropy_manager = EntropyManager()
            # Initial thermodynamic assessment
            self.thermodynamic_state = self.entropy_manager.check_thermodynamic_budget()

    def check_thermodynamic_constraints(self) -> Any | None:
        """
        F4 + F11 + F7: Check hardware-level thermodynamic constraints.

        Returns ThermodynamicState with verdict (SEAL, SABAR, VOID).
        Called by orchestrator before expensive operations.
        """
        if self.entropy_manager is None:
            return None

        self.thermodynamic_state = self.entropy_manager.check_thermodynamic_budget()

        # Update governance state based on thermodynamics
        if self.thermodynamic_state.verdict == "VOID":
            self.governance_state = GovernanceState.VOID
            self.authority_level = AuthorityLevel.UNSAFE_TO_AUTOMATE
        elif self.thermodynamic_state.verdict == "SABAR":
            self.governance_state = GovernanceState.AWAITING_888
            self.authority_level = AuthorityLevel.REQUIRES_HUMAN

        return self.thermodynamic_state

    def update_uncertainty(
        self, safety_omega: float, display_omega: float, components: dict[str, float]
    ):
        """Update uncertainty state and re-evaluate governance."""
        self.safety_omega = safety_omega
        self.display_omega = display_omega
        self.uncertainty_components = components
        self._evaluate_governance()

    def update_irreversibility(
        self, impact_scope: float, recovery_cost: float, time_to_reverse: float
    ):
        """
        Calculate irreversibility index.

        Formula: impact_scope × recovery_cost × time_to_reverse
        All factors normalized to [0, 1]
        """
        self.irreversibility_index = impact_scope * recovery_cost * time_to_reverse
        self.reversibility_score = 1.0 - self.irreversibility_index
        self._evaluate_governance()

    def _evaluate_governance(self):
        """
        Q2: CONDITIONAL synchronous hold.

        AWAITING_888 triggers only when:
        - irreversibility_index > 0.6 OR
        - safety_omega > 0.06

        Low-risk flows remain continuous.
        """
        high_irreversibility = self.irreversibility_index > self.IRREVERSIBILITY_THRESHOLD
        high_uncertainty = self.safety_omega > self.UNCERTAINTY_THRESHOLD

        if high_irreversibility or high_uncertainty:
            self.governance_state = GovernanceState.AWAITING_888
            self.escalation_required = True
            self.human_approval_status = "pending"
            self.authority_level = AuthorityLevel.REQUIRES_HUMAN
        elif self.safety_omega > 0.03:
            self.governance_state = GovernanceState.CONDITIONAL
            self.authority_level = AuthorityLevel.SUGGESTION
        else:
            self.governance_state = GovernanceState.ACTIVE
            self.authority_level = AuthorityLevel.ANALYSIS

    def approve_human(self, approved: bool, actor: str = "888"):
        """
        L8 Human sovereign approval.

        Args:
            approved: True = approve, False = deny
            actor: Identity of human approver (default "888")
        """
        self.human_approval_status = "approved" if approved else "denied"
        self.human_override_timestamp = time.time()
        self.decision_owner = actor if approved else "system"

        if approved:
            self.governance_state = GovernanceState.CONDITIONAL
            self.escalation_required = False
        else:
            self.governance_state = GovernanceState.VOID

    def can_proceed(self) -> bool:
        """Check if system can proceed with output."""
        if self.governance_state == GovernanceState.VOID:
            return False
        if self.governance_state == GovernanceState.AWAITING_888:
            return False
        return True

    def get_output_tags(self) -> list[str]:
        """Generate output tags based on authority level."""
        tags = []

        if self.authority_level == AuthorityLevel.ANALYSIS:
            tags.append("[ANALYSIS]")
        elif self.authority_level == AuthorityLevel.SUGGESTION:
            tags.append("[SUGGESTION]")
        elif self.authority_level == AuthorityLevel.REQUIRES_HUMAN:
            tags.append("[REQUIRES_HUMAN_JUDGMENT]")
        elif self.authority_level == AuthorityLevel.UNSAFE_TO_AUTOMATE:
            tags.append("[UNSAFE_TO_AUTOMATE]")

        if self.governance_state == GovernanceState.AWAITING_888:
            tags.append("[PENDING_888_APPROVAL]")

        return tags

    def to_dict(self) -> dict[str, Any]:
        """Serialize governance state."""
        return {
            "authority_level": self.authority_level.value,
            "decision_owner": self.decision_owner,
            "safety_omega": round(self.safety_omega, 4),
            "display_omega": round(self.display_omega, 4),
            "uncertainty_components": self.uncertainty_components,
            "irreversibility_index": round(self.irreversibility_index, 4),
            "reversibility_score": round(self.reversibility_score, 4),
            "governance_state": self.governance_state.value,
            "escalation_required": self.escalation_required,
            "human_approval_status": self.human_approval_status,
            "thresholds": {
                "irreversibility": self.IRREVERSIBILITY_THRESHOLD,
                "uncertainty": self.UNCERTAINTY_THRESHOLD,
            },
            "can_proceed": self.can_proceed(),
            "output_tags": self.get_output_tags(),
            "timestamp": self.timestamp,
            "session_id": self.session_id,
        }


# Global governance kernel registry (per-session)
_governance_kernels: dict[str, GovernanceKernel] = {}


def get_governance_kernel(session_id: str) -> GovernanceKernel:
    """Get or create governance kernel for session."""
    if session_id not in _governance_kernels:
        kernel = GovernanceKernel(session_id=session_id)
        _governance_kernels[session_id] = kernel
    return _governance_kernels[session_id]


def clear_governance_kernel(session_id: str):
    """Clear governance kernel (cleanup)."""
    if session_id in _governance_kernels:
        del _governance_kernels[session_id]
