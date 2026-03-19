"""Core governance kernel state and transition logic.

This module is intentionally narrow:
- Maintains runtime governance state for one session.
- Enforces deterministic transition rules for uncertainty/risk/energy.
- Exposes compatibility helpers used by legacy callers.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from math import isfinite
from typing import Any

try:
    from core.physics.thermodynamics import EntropyManager, ThermodynamicState

    THERMODYNAMICS_AVAILABLE = True
except ImportError:
    EntropyManager = None  # type: ignore[assignment]
    ThermodynamicState = None  # type: ignore[assignment]
    THERMODYNAMICS_AVAILABLE = False


class AuthorityLevel(Enum):
    """Identity and control boundary."""

    ANALYSIS = "analysis"
    SUGGESTION = "suggestion"
    REQUIRES_HUMAN = "requires_human"
    UNSAFE_TO_AUTOMATE = "unsafe"


class GovernanceState(Enum):
    """Runtime governance state."""

    ACTIVE = "active"
    AWAITING_888 = "awaiting_888"
    CONDITIONAL = "conditional"
    VOID = "void"
    RECOVERING = "recovering"
    DEGRADED = "degraded"
    QUARANTINED = "quarantined"


@dataclass(frozen=True)
class GovernanceThresholds:
    """Normalized threshold contract for kernel decisions."""

    irreversibility_hold: float
    uncertainty_hold: float
    uncertainty_conditional: float
    energy_hold: float
    max_tokens: int = 100000
    max_reason_cycles: int = 10
    max_tool_calls: int = 50


@dataclass
class GovernanceKernel:
    """Unified kernel state object (Psi)."""

    entropy_manager: Any | None = field(default=None, repr=False)
    thermodynamic_state: Any | None = field(default=None)

    authority_level: AuthorityLevel = AuthorityLevel.ANALYSIS
    decision_owner: str = "ai"

    safety_omega: float = 0.0
    display_omega: float = 0.0
    uncertainty_components: dict[str, float] = field(default_factory=dict)

    irreversibility_index: float = 0.0
    reversibility_score: float = 1.0
    current_energy: float = 1.0

    # Granular life energy (Metabolic counters)
    tokens_consumed: int = 0
    reason_cycles: int = 0
    tool_calls: int = 0

    governance_state: GovernanceState = GovernanceState.ACTIVE
    governance_reason: str = "initialized"
    escalation_required: bool = False

    human_approval_status: str = "not_required"
    human_override_timestamp: float | None = None

    IRREVERSIBILITY_THRESHOLD: float = 0.6
    UNCERTAINTY_THRESHOLD: float = 0.06
    ENERGY_THRESHOLD: float = 0.2
    CONDITIONAL_UNCERTAINTY_THRESHOLD: float = 0.03

    timestamp: float = field(default_factory=time.time)
    last_transition_at: float = field(default_factory=time.time)
    session_id: str = ""

    def __post_init__(self) -> None:
        self.current_energy = self._clamp_unit(self.current_energy, field_name="current_energy")
        self.safety_omega = self._clamp_unit(self.safety_omega, field_name="safety_omega")
        self.display_omega = self._clamp_unit(self.display_omega, field_name="display_omega")

        if THERMODYNAMICS_AVAILABLE and self.entropy_manager is None and EntropyManager is not None:
            self.entropy_manager = EntropyManager()
            self.thermodynamic_state = self.entropy_manager.check_thermodynamic_budget()

    @property
    def thresholds(self) -> GovernanceThresholds:
        return GovernanceThresholds(
            irreversibility_hold=self.IRREVERSIBILITY_THRESHOLD,
            uncertainty_hold=self.UNCERTAINTY_THRESHOLD,
            uncertainty_conditional=self.CONDITIONAL_UNCERTAINTY_THRESHOLD,
            energy_hold=self.ENERGY_THRESHOLD,
            max_tokens=100000,
            max_reason_cycles=10,
            max_tool_calls=50,
        )

    @property
    def environment(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "timestamp": self.timestamp,
            "decision_owner": self.decision_owner,
            "authority_level": self.authority_level.value,
        }

    @property
    def energy(self) -> dict[str, Any]:
        return {
            "current_energy": round(self.current_energy, 4),
            "thermodynamic_state": (
                self.thermodynamic_state.to_dict()
                if self.thermodynamic_state and hasattr(self.thermodynamic_state, "to_dict")
                else None
            ),
            "irreversibility_index": round(self.irreversibility_index, 4),
            "reversibility_score": round(self.reversibility_score, 4),
            "human_approval_status": self.human_approval_status,
            "metabolic_usage": {
                "tokens": self.tokens_consumed,
                "reason_cycles": self.reason_cycles,
                "tool_calls": self.tool_calls,
            },
        }

    @property
    def void(self) -> dict[str, Any]:
        return {
            "safety_omega": round(self.safety_omega, 4),
            "display_omega": round(self.display_omega, 4),
            "uncertainty_components": dict(self.uncertainty_components),
        }

    @property
    def state_field(self) -> dict[str, Any]:
        return {
            "environment": self.environment,
            "energy": self.energy,
            "void": self.void,
        }

    @staticmethod
    def _clamp_unit(value: float, *, field_name: str) -> float:
        if not isfinite(value):
            raise ValueError(f"{field_name} must be a finite number")
        return max(0.0, min(1.0, float(value)))

    def _set_state(
        self,
        state: GovernanceState,
        authority_level: AuthorityLevel,
        reason: str,
        *,
        human_status: str | None = None,
    ) -> None:
        self.governance_state = state
        self.authority_level = authority_level
        self.governance_reason = reason
        self.escalation_required = state == GovernanceState.AWAITING_888
        self.last_transition_at = time.time()

        if human_status is not None:
            self.human_approval_status = human_status
        elif state == GovernanceState.AWAITING_888:
            self.human_approval_status = "pending"
        elif self.human_approval_status == "pending":
            self.human_approval_status = "not_required"

    def check_thermodynamic_constraints(self) -> Any | None:
        """
        P3: Check thermodynamic budget from hardened physics module.

        Integrates with core.physics.thermodynamics_hardened for
        mandatory thermodynamic enforcement.
        """
        # First check legacy entropy manager if available
        if self.entropy_manager is not None:
            self.thermodynamic_state = self.entropy_manager.check_thermodynamic_budget()
            verdict = getattr(self.thermodynamic_state, "verdict", "")

            if verdict == "VOID":
                self._set_state(
                    GovernanceState.VOID,
                    AuthorityLevel.UNSAFE_TO_AUTOMATE,
                    "thermodynamics_void",
                )
                return self.thermodynamic_state

            if verdict == "SABAR":
                self._set_state(
                    GovernanceState.AWAITING_888,
                    AuthorityLevel.REQUIRES_HUMAN,
                    "thermodynamics_sabar",
                    human_status="pending",
                )
                return self.thermodynamic_state

        # P3: Check hardened thermodynamic budget
        try:
            from core.physics.thermodynamics_hardened import (
                get_thermodynamic_budget,
                ThermodynamicExhaustion,
            )

            budget = get_thermodynamic_budget(self.session_id)

            if budget.is_exhausted:
                self._set_state(
                    GovernanceState.AWAITING_888,
                    AuthorityLevel.REQUIRES_HUMAN,
                    "thermodynamic_budget_exhausted",
                    human_status="pending",
                )
                return budget.to_dict()

            # Update energy based on thermodynamic budget depletion
            depletion = budget.depletion_ratio
            self.current_energy = max(0.0, 1.0 - depletion)

        except ThermodynamicExhaustion:
            self._set_state(
                GovernanceState.AWAITING_888,
                AuthorityLevel.REQUIRES_HUMAN,
                "thermodynamic_exhaustion",
                human_status="pending",
            )
        except Exception:
            # Budget not initialized yet - skip hardened check
            pass

        self._evaluate_governance()
        return self.thermodynamic_state

    def update_uncertainty(
        self,
        safety_omega: float,
        display_omega: float,
        components: dict[str, float],
    ) -> None:
        self.safety_omega = self._clamp_unit(safety_omega, field_name="safety_omega")
        self.display_omega = self._clamp_unit(display_omega, field_name="display_omega")
        self.uncertainty_components = {
            key: self._clamp_unit(float(val), field_name=f"uncertainty_components.{key}")
            for key, val in (components or {}).items()
            if isinstance(val, (float, int))
        }
        self._evaluate_governance()

    def update_irreversibility(
        self,
        impact_scope: float,
        recovery_cost: float,
        time_to_reverse: float,
    ) -> None:
        impact = self._clamp_unit(impact_scope, field_name="impact_scope")
        recovery = self._clamp_unit(recovery_cost, field_name="recovery_cost")
        time_cost = self._clamp_unit(time_to_reverse, field_name="time_to_reverse")

        self.irreversibility_index = impact * recovery * time_cost
        self.reversibility_score = max(0.0, 1.0 - self.irreversibility_index)
        self._evaluate_governance()

    def consume_energy(self, amount: float) -> None:
        if not isfinite(amount):
            raise ValueError("amount must be a finite number")
        if amount < 0:
            raise ValueError("amount must be non-negative")

        self.current_energy = max(0.0, min(1.0, self.current_energy - float(amount)))
        self._evaluate_governance()

    def consume_tokens(self, count: int) -> None:
        """Consume LLM tokens and reduce energy proportionally."""
        self.tokens_consumed += count
        # Heuristic: 100k tokens = 0.5 energy
        self.current_energy = max(0.0, self.current_energy - (count / 200000))
        self._evaluate_governance()

    def consume_reason_cycle(self) -> None:
        """Consume one internal reasoning cycle."""
        self.reason_cycles += 1
        # Heuristic: 10 cycles = 0.2 energy
        self.current_energy = max(0.0, self.current_energy - 0.02)
        self._evaluate_governance()

    def consume_tool_call(self) -> None:
        """Consume one external tool call."""
        self.tool_calls += 1
        # Heuristic: 50 calls = 0.3 energy
        self.current_energy = max(0.0, self.current_energy - 0.006)
        self._evaluate_governance()

    def _evaluate_governance(self) -> None:
        if self.current_energy <= 0.0:
            self._set_state(
                GovernanceState.VOID,
                AuthorityLevel.UNSAFE_TO_AUTOMATE,
                "energy_depleted",
            )
            return

        if self.irreversibility_index > self.IRREVERSIBILITY_THRESHOLD:
            self._set_state(
                GovernanceState.AWAITING_888,
                AuthorityLevel.REQUIRES_HUMAN,
                "irreversibility_high",
                human_status="pending",
            )
            return

        if self.safety_omega > self.UNCERTAINTY_THRESHOLD:
            self._set_state(
                GovernanceState.AWAITING_888,
                AuthorityLevel.REQUIRES_HUMAN,
                "uncertainty_high",
                human_status="pending",
            )
            return

        if self.current_energy < self.ENERGY_THRESHOLD:
            self._set_state(
                GovernanceState.AWAITING_888,
                AuthorityLevel.REQUIRES_HUMAN,
                "energy_low",
                human_status="pending",
            )
            return

        # Hard Metabolic Constraints
        t = self.thresholds
        if self.tokens_consumed > t.max_tokens:
            self._set_state(
                GovernanceState.VOID, AuthorityLevel.UNSAFE_TO_AUTOMATE, "token_budget_exceeded"
            )
            return
        if self.reason_cycles > t.max_reason_cycles:
            self._set_state(
                GovernanceState.AWAITING_888,
                AuthorityLevel.REQUIRES_HUMAN,
                "reason_cycle_budget_exceeded",
            )
            return
        if self.tool_calls > t.max_tool_calls:
            self._set_state(
                GovernanceState.AWAITING_888,
                AuthorityLevel.REQUIRES_HUMAN,
                "tool_call_budget_exceeded",
            )
            return

        if self.safety_omega > self.CONDITIONAL_UNCERTAINTY_THRESHOLD:
            self._set_state(
                GovernanceState.CONDITIONAL,
                AuthorityLevel.SUGGESTION,
                "uncertainty_medium",
            )
            return

        self._set_state(
            GovernanceState.ACTIVE,
            AuthorityLevel.ANALYSIS,
            "stable",
        )

    def calculate_pressure(self, task_complexity: float) -> float:
        """Calculate cognitive pressure based on complexity and available energy."""
        if self.current_energy <= 0:
            return float("inf")
        pressure = task_complexity / self.current_energy

        if pressure > 2.0:  # Threshold for 'Critical'
            self._set_state(
                GovernanceState.DEGRADED, AuthorityLevel.SUGGESTION, "critical_pressure"
            )
        elif pressure > 1.0:  # Threshold for 'High'
            self._set_state(GovernanceState.CONDITIONAL, AuthorityLevel.ANALYSIS, "high_pressure")

        return pressure

    def phoenix_recovery(self, mode: str = "recover") -> None:
        """Execute Phoenix Protocol recovery transition."""
        if mode == "quarantine":
            self._set_state(
                GovernanceState.QUARANTINED, AuthorityLevel.REQUIRES_HUMAN, "phoenix_quarantine"
            )
        elif mode == "degrade":
            self._set_state(GovernanceState.DEGRADED, AuthorityLevel.SUGGESTION, "phoenix_degraded")
        elif mode == "recover":
            self.current_energy = min(1.0, self.current_energy + 0.2)  # Infuse energy
            self._set_state(
                GovernanceState.RECOVERING, AuthorityLevel.ANALYSIS, "phoenix_recovering"
            )
            # Clear critical flags here if any

    def approve_human(self, approved: bool, actor: str = "888") -> None:
        self.human_override_timestamp = time.time()
        if approved:
            self.decision_owner = actor
            if self.current_energy <= 0.0:
                self._set_state(
                    GovernanceState.VOID,
                    AuthorityLevel.UNSAFE_TO_AUTOMATE,
                    "human_approved_but_energy_depleted",
                    human_status="approved",
                )
                return

            self._set_state(
                GovernanceState.CONDITIONAL,
                AuthorityLevel.SUGGESTION,
                "human_approved",
                human_status="approved",
            )
            return

        self.decision_owner = "system"
        self._set_state(
            GovernanceState.VOID,
            AuthorityLevel.UNSAFE_TO_AUTOMATE,
            "human_denied",
            human_status="denied",
        )

    def can_proceed(self) -> bool:
        return self.governance_state in {GovernanceState.ACTIVE, GovernanceState.CONDITIONAL}

    def get_output_tags(self) -> list[str]:
        tags: list[str] = []

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

    def architecture_map(self) -> dict[str, Any]:
        """Return a compact runtime map of the intelligence architecture."""
        return {
            "stack": "000->999",
            "boundaries": {
                "core": "decision logic only",
                "aaa_mcp": "transport/protocol only",
                "aclip_cai": "triad intelligence backends",
            },
            "stages": {
                "000": {"name": "INIT", "floors": ["F11", "F12"]},
                "111-333": {"name": "AGI_MIND", "floors": ["F2", "F4", "F7", "F8"]},
                "444-666": {"name": "ASI_HEART", "floors": ["F1", "F5", "F6"]},
                "777-888": {"name": "APEX_SOUL", "floors": ["F3", "F9", "F10", "F13"]},
                "999": {"name": "VAULT", "floors": ["F1", "F3"]},
            },
            "runtime": {
                "state": self.governance_state.value,
                "authority": self.authority_level.value,
                "reason": self.governance_reason,
            },
        }

    @property
    def hysteresis_penalty(self) -> float:
        """Accumulated session scars (h)."""
        try:
            from core.telemetry import get_current_hysteresis
            return get_current_hysteresis()
        except ImportError:
            return 0.0

    @property
    def genius_score(self) -> float:
        """Derived G score: G = (A×P×X×E²) × (1-h)"""
        from core.shared.physics import GeniusDial
        
        # Estimate dials from current state
        akal = round(max(0.0, 1.0 - self.safety_omega), 4)
        present = round(self.reversibility_score, 4)
        explore = 0.9 # Default
        energy = self.current_energy
        
        dial = GeniusDial(akal, present, explore, energy, self.hysteresis_penalty)
        return dial.G()

    def get_current_state(self) -> dict[str, Any]:
        """Compatibility payload for adapters expecting live governance telemetry."""
        if self.governance_state == GovernanceState.VOID:
            verdict = "VOID"
        elif self.governance_state == GovernanceState.AWAITING_888:
            verdict = "888_HOLD"
        elif self.governance_state == GovernanceState.CONDITIONAL:
            verdict = "PARTIAL"
        else:
            verdict = "SEAL"

        return {
            "session_id": self.session_id,
            "verdict": verdict,
            "metabolic_stage": 888 if self.escalation_required else 333,
            "qdf": round(max(0.0, 1.0 - self.safety_omega), 4),
            "hysteresis": self.hysteresis_penalty,
            "genius": self.genius_score,
            "floors": {
                "F1": round(self.reversibility_score, 4),
                "F2": round(max(0.0, 1.0 - self.safety_omega), 4),
                "F3": self.witness.get("consensus", 0.0) if hasattr(self, "witness") else 0.0,
                "F4": 1.0 if self.current_energy >= self.ENERGY_THRESHOLD else 0.0,
                "F7": round(max(0.0, 1.0 - abs(self.safety_omega - 0.04)), 4),
                "F8": self.genius_score,
            },
            "witness": {
                "human": 1.0 if self.human_approval_status == "approved" else 0.7,
                "ai": round(max(0.0, 1.0 - self.safety_omega), 4),
                "earth": round(self.current_energy, 4),
                "shadow": 1.0 - (self.safety_omega * 2.0), # Adversarial proxy
            },
            "telemetry": {
                "dS": -0.1 if self.can_proceed() else 0.1,
                "peace2": round(max(0.0, self.reversibility_score), 4),
                "kappa_r": round(max(0.0, 1.0 - self.safety_omega), 4),
                "confidence": round(max(0.0, 1.0 - self.safety_omega), 4),
                "psi_le": round(max(0.0, self.current_energy), 4),
                "joules": self.tokens_consumed * 0.0005, # Energy proxy
            },
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "authority_level": self.authority_level.value,
            "decision_owner": self.decision_owner,
            "safety_omega": round(self.safety_omega, 4),
            "display_omega": round(self.display_omega, 4),
            "uncertainty_components": dict(self.uncertainty_components),
            "irreversibility_index": round(self.irreversibility_index, 4),
            "reversibility_score": round(self.reversibility_score, 4),
            "governance_state": self.governance_state.value,
            "governance_reason": self.governance_reason,
            "escalation_required": self.escalation_required,
            "human_approval_status": self.human_approval_status,
            "thresholds": {
                "irreversibility": self.IRREVERSIBILITY_THRESHOLD,
                "uncertainty": self.UNCERTAINTY_THRESHOLD,
                "uncertainty_conditional": self.CONDITIONAL_UNCERTAINTY_THRESHOLD,
                "energy": self.ENERGY_THRESHOLD,
            },
            "can_proceed": self.can_proceed(),
            "output_tags": self.get_output_tags(),
            "timestamp": self.timestamp,
            "last_transition_at": self.last_transition_at,
            "session_id": self.session_id,
            "state_field": self.state_field,
        }


class AppLayer(Enum):
    """Application layer in the refined 4-layer taxonomy."""

    L0_CONSTITUTION = "L0"
    L1_INSTRUCTION = "L1"
    L2_OPERATION = "L2"
    L3_CIVILIZATION = "L3"


class FloorClassification(Enum):
    """How a floor is classified for an app."""

    HARD = "hard"
    SOFT = "soft"
    N_A = "n/a"


@dataclass
class FloorManifesto:
    """Manifesto entry for one floor."""

    floor_id: str
    classification: FloorClassification
    custom_threshold: Any | None = None
    rationale: str = ""


@dataclass
class AppManifesto:
    """Constitutional manifesto for an application."""

    app_name: str
    layer: AppLayer
    description: str
    version: str = "1.0.0"
    floors: list[FloorManifesto] = field(default_factory=list)
    requires_sovereign_gate: bool = False
    irreversible_actions: list[str] = field(default_factory=list)
    l0_organs_used: list[str] = field(default_factory=lambda: ["agi_cognition"])
    author: str = ""
    dependencies: list[str] = field(default_factory=list)

    def validate(self) -> bool:
        if not self.floors:
            raise ValueError(f"App '{self.app_name}' must declare at least one floor")
        floor_ids = {floor.floor_id for floor in self.floors}
        missing_required = {"F1", "F2", "F7"} - floor_ids
        if missing_required:
            raise ValueError(
                f"App '{self.app_name}' missing required floors: {sorted(missing_required)}"
            )
        return True

    def to_dict(self) -> dict[str, Any]:
        return {
            "app_name": self.app_name,
            "layer": self.layer.value,
            "version": self.version,
            "description": self.description,
            "floors": [
                {
                    "floor_id": floor.floor_id,
                    "classification": floor.classification.value,
                    "threshold": floor.custom_threshold,
                    "rationale": floor.rationale,
                }
                for floor in self.floors
            ],
            "requires_sovereign_gate": self.requires_sovereign_gate,
            "irreversible_actions": self.irreversible_actions,
            "l0_organs_used": self.l0_organs_used,
        }


class AppRegistry:
    """In-memory registry of constitutional applications."""

    _apps: dict[str, AppManifesto] = {}

    @classmethod
    def register(cls, manifesto: AppManifesto) -> None:
        manifesto.validate()
        cls._apps[manifesto.app_name] = manifesto

    @classmethod
    def get(cls, app_name: str) -> AppManifesto | None:
        return cls._apps.get(app_name)

    @classmethod
    def list_all(cls) -> list[str]:
        return list(cls._apps.keys())

    @classmethod
    def audit(cls) -> dict[str, Any]:
        by_layer: dict[str, int] = {}
        sovereign_gates = 0

        for app in cls._apps.values():
            layer = app.layer.value
            by_layer[layer] = by_layer.get(layer, 0) + 1
            if app.requires_sovereign_gate:
                sovereign_gates += 1

        return {
            "total_apps": len(cls._apps),
            "by_layer": by_layer,
            "sovereign_gates_required": sovereign_gates,
            "apps": {name: manifesto.to_dict() for name, manifesto in cls._apps.items()},
        }


_governance_kernels: dict[str, GovernanceKernel] = {}
_DEFAULT_SESSION_ID = "global"


def get_governance_kernel(session_id: str | None = None) -> GovernanceKernel:
    """Compatibility getter for callers that use global or session-scoped kernel access."""
    sid = session_id or _DEFAULT_SESSION_ID

    existing = _governance_kernels.get(sid)
    if existing is not None:
        return existing

    if session_id:
        try:
            from core.state.session_manager import session_manager

            session_kernel = session_manager.get_kernel(session_id)
            if session_kernel is not None:
                _governance_kernels[sid] = session_kernel
                return session_kernel
        except Exception:
            pass

    kernel = GovernanceKernel(session_id=sid)
    _governance_kernels[sid] = kernel
    return kernel


def clear_governance_kernel(session_id: str | None = None) -> None:
    """Compatibility clearer for tests and legacy callers."""
    if session_id is None:
        _governance_kernels.clear()
        return
    _governance_kernels.pop(session_id, None)


__all__ = [
    "AuthorityLevel",
    "GovernanceState",
    "GovernanceThresholds",
    "GovernanceKernel",
    "THERMODYNAMICS_AVAILABLE",
    "ThermodynamicState",
    "get_governance_kernel",
    "clear_governance_kernel",
    "_governance_kernels",
    "AppLayer",
    "FloorClassification",
    "FloorManifesto",
    "AppManifesto",
    "AppRegistry",
]
