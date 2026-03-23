"""Core governance kernel state and transition logic.

This module is intentionally narrow:
- Maintains runtime governance state for one session.
- Enforces deterministic transition rules for uncertainty/risk/energy.
- Exposes compatibility helpers used by legacy callers.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from math import isfinite
from typing import Any

try:
    from core.physics.thermodynamics_hardened import (
        ThermodynamicBudget,
        ThermodynamicError,
        get_thermodynamic_budget,
    )

    THERMODYNAMICS_AVAILABLE = True
except ImportError:
    ThermodynamicBudget = None  # type: ignore[assignment]
    get_thermodynamic_budget = None  # type: ignore[assignment]
    THERMODYNAMICS_AVAILABLE = False
    ThermodynamicError = Exception  # type: ignore[assignment,misc]
    LandauerViolation = Exception  # type: ignore[assignment,misc]
    EntropyIncreaseViolation = Exception  # type: ignore[assignment,misc]


logger = logging.getLogger(__name__)


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
    entropic_drift: float = 0.01
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
    last_verified_at: datetime | None = None
    last_verified_latency_ms: float | None = None
    session_id: str = ""
    earth_witness_score: float = 1.0  # P0 Strike: F03_WITNESS

    # P0 HARDENING: Temporal Metrics (PRESENT dial)
    metabolic_flux: float = 0.0  # ΔTokens / Δt
    epistemic_temp: float = 0.0  # ΔS / Δt
    temporal_jitter: float = 0.0  # Deviation from wall-clock

    @property
    def temporal_stability(self) -> float:
        """
        Calculate the stability of the Present (P) dial based on temporal health.
        Inverse of metabolic flux and jitter.
        """
        # 1. Flux Calculation (Tokens per Second)
        # Use verified latency if available, otherwise fallback to wall-clock dt
        if self.last_verified_latency_ms and self.last_verified_latency_ms > 0:
            dt = self.last_verified_latency_ms / 1000.0
        else:
            dt = time.time() - self.last_transition_at

        if dt > 0:
            self.metabolic_flux = self.tokens_consumed / dt

        # 2. Hardened Thresholds
        max_flux = 500.0  # tokens/sec (Human metabolic limit)
        max_jitter = 50.0  # ms (System stability limit)

        # 3. Penalty projection
        flux_p = min(1.0, self.metabolic_flux / max_flux) if self.metabolic_flux > 0 else 0.0
        jitter_p = min(1.0, self.temporal_jitter / max_jitter) if self.temporal_jitter > 0 else 0.0

        # G Theorem: Present stability = 1.0 - (Flux + Jitter)
        # Haste breeds entropy; jitter breeds instability.
        stability = 1.0 - (0.6 * flux_p + 0.4 * jitter_p)

        # ZKPC Grounding: If dt is suspiciously small (< 1ms), force stability floor
        if dt < 0.001 and self.tokens_consumed > 10:
            stability *= 0.1  # Severe penalty for 'Instant Truth'

        return max(0.0, min(1.0, stability))

    def __post_init__(self) -> None:
        self.current_energy = self._clamp_unit(self.current_energy, field_name="current_energy")
        self.safety_omega = self._clamp_unit(self.safety_omega, field_name="safety_omega")
        self.display_omega = self._clamp_unit(self.display_omega, field_name="display_omega")

        if (
            THERMODYNAMICS_AVAILABLE
            and self.thermodynamic_state is None
            and get_thermodynamic_budget is not None
        ):
            try:
                self.thermodynamic_state = get_thermodynamic_budget(self.session_id)
            except Exception:
                # Budget not initialized, skip for now.
                # Stage 000 will initialize it properly.
                self.thermodynamic_state = None

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
        if self.thermodynamic_state is not None:
            # check the budget
            try:
                # ThermodynamicBudget in P3 maintains its own state and violations
                return self.thermodynamic_state.to_dict()
            except Exception as e:
                logger.error(f"Error checking thermodynamic budget: {e}")
                return None
        # P3: Check hardened thermodynamic budget
        try:
            from core.physics.thermodynamics_hardened import (
                ThermodynamicExhaustion,
                get_thermodynamic_budget,
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

    def apply_temporal_grounding(self, contract: Any) -> None:
        """
        Enforce temporal contracts on kernel decisions.
        - Penalizes too-fast reasoning for Class-A.
        - Checks for expired authority.
        - Anchors kernel to verified wall-clock.
        """
        # Avoid circular imports but allow temporal contract validation.
        from core.shared.types import TemporalContract

        if not isinstance(contract, TemporalContract):
            return

        self.last_verified_at = contract.observed_at
        self.last_verified_latency_ms = contract.request_latency_ms

        # 1. Latency Gating (Landauer Hardening)
        # High-stakes (REQUIRES_HUMAN) must spend at least 1500ms forging
        if self.authority_level == AuthorityLevel.REQUIRES_HUMAN:
            t_min = 1500.0  # Joules/Time denominator threshold
            if contract.request_latency_ms < t_min:
                reason = (
                    f"temporal_insufficiency: latency {contract.request_latency_ms}ms "
                    f"< {t_min}ms (F2 Violation)"
                )
                self._set_state(
                    GovernanceState.CONDITIONAL,
                    AuthorityLevel.SUGGESTION,
                    reason,
                )

        # 2. Authority Expiry (F11/F13 Hold)
        if contract.valid_until:
            current_time = (
                datetime.now(contract.valid_until.tzinfo)
                if contract.valid_until.tzinfo is not None
                else datetime.now()
            )
            if current_time > contract.valid_until:
                self._set_state(
                    GovernanceState.VOID,
                    AuthorityLevel.UNSAFE_TO_AUTOMATE,
                    "authority_expired: TTL exceeded",
                )

        # 3. Cooling Check (PHOENIX-72)
        if contract.cooldown_expiry and datetime.now() < contract.cooldown_expiry:
            if self.governance_state != GovernanceState.AWAITING_888:
                self._set_state(
                    GovernanceState.AWAITING_888,
                    AuthorityLevel.REQUIRES_HUMAN,
                    "phoenix_cooling: active wait window",
                    human_status="pending",
                )

        self._evaluate_governance()

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

    def normalize_verdict(self, stage: str, verdict: Any) -> Any:
        """
        Constitutional Verdict Normalization Layer.
        Ensures exploration stages cannot kill ideas.

        Mandatory Rule: if stage < 888 and verdict == VOID: verdict = SABAR
        """
        # Convert to Enum if string
        from core.shared.types import Verdict

        v = verdict if isinstance(verdict, Verdict) else Verdict(verdict)

        # Parse stage prefix (e.g., "111_search" -> 111)
        try:
            stage_clean = stage.split("_")[0]
            stage_int = int(stage_clean)
        except (ValueError, IndexError):
            # If stage is not numeric, treat it cautiously
            stage_int = 999

        if stage_int < 888 and v == Verdict.VOID:
            # The heart of the contract:
            # organs use VOID as "I don't know" or "rejection"
            # but until JUDGE (888), we downgrade it to SABAR.
            return Verdict.SABAR

        return v

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

    def _project_genius_floor_scores(self) -> Any:
        """Project live kernel state into the canonical FloorScores manifold."""
        from core.enforcement.genius import coerce_floor_scores

        return coerce_floor_scores(
            defaults={
                "f1_amanah": round(self.reversibility_score, 4),
                "f2_truth": round(max(0.0, 1.0 - self.safety_omega), 4),
                "f3_earth_witness": self.earth_witness_score,
                "f4_clarity": -0.1 if self.governance_state == GovernanceState.ACTIVE else 0.1,
                "f5_peace": round(self.reversibility_score, 4),
                "f6_empathy": 0.95,
                "f7_humility": round(0.04 - (self.safety_omega / 10.0), 4),
                "f8_genius": 0.8,
                "f11_command_auth": self.authority_level != AuthorityLevel.ANALYSIS,
                "f13_sovereign": 1.0 if (self.human_approval_status == "approved" or self.decision_owner == "arif") else 0.7,
            }
        )

    def _project_genius_budget_window(self) -> tuple[float, float]:
        """Resolve the thermodynamic budget window for kernel self-measurement."""
        from core.enforcement.genius import get_thermodynamic_budget_window

        return get_thermodynamic_budget_window(
            self.session_id,
            fallback_used=1.0 - self.current_energy,
            fallback_max=1.0,
        )

    @property
    def genius_score(self) -> float:
        """Derived G score: G = (A×P×X×E²) × (1-h)"""
        from core.enforcement.genius import calculate_genius

        floors = self._project_genius_floor_scores()
        budget_used, budget_max = self._project_genius_budget_window()

        res = calculate_genius(
            floors=floors,
            h=self.hysteresis_penalty,
            compute_budget_used=budget_used,
            compute_budget_max=budget_max,
        )
        return res["genius_score"]

    def get_current_state(self) -> dict[str, Any]:
        """Compatibility payload for adapters expecting live governance telemetry."""
        from core.enforcement.genius import calculate_genius
        from core.shared.types import Verdict

        if self.governance_state == GovernanceState.VOID:
            verdict = Verdict.VOID.value
        elif self.governance_state == GovernanceState.AWAITING_888:
            verdict = Verdict.HOLD.value
        elif self.governance_state == GovernanceState.CONDITIONAL:
            verdict = Verdict.PARTIAL.value
        else:
            verdict = Verdict.SEAL.value

        floors = self._project_genius_floor_scores()
        budget_used, budget_max = self._project_genius_budget_window()
        
        # P1 Strike: Derive dials from 3E Telemetry
        telemetry_payload = {
            "entropy": {"uncertainty_score": self.safety_omega},
            "exploration": {"hypotheses": [1] * max(1, self.reason_cycles)},
            "eureka": {"detected": self.governance_state == GovernanceState.ACTIVE}
        }
        
        genius_res = calculate_genius(
            floors, 
            self.hysteresis_penalty, 
            budget_used, 
            budget_max, 
            telemetry=telemetry_payload
        )
        dials = genius_res["dials"]

        # Trigger temporal stability update to refresh metabolic_flux/jitter
        stability_t = self.temporal_stability

        return {
            "session_id": self.session_id,
            "verdict": verdict,
            "metabolic_stage": 888 if self.escalation_required else 333,
            "qdf": round(max(0.0, 1.0 - self.safety_omega), 4),
            "hysteresis": self.hysteresis_penalty,
            "genius": genius_res["genius_score"],
            "floors": {
                "F1": floors.f1_amanah,
                "F2": floors.f2_truth,
                "F3": floors.f3_earth_witness,
                "F4": floors.f4_clarity,
                "F7": floors.f7_humility,
                "F8": genius_res["genius_score"],
                "F11": 1.0 if floors.f11_command_auth else 0.0,
                "F13": floors.f13_sovereign,
            },
            "witness": {
                "human": floors.f13_sovereign,
                "ai": round(dials["A"], 4),
                "earth": round(self.earth_witness_score, 4),
                "shadow": round(dials["X"], 4),
                "w3_consensus": round(floors.tri_witness_consensus, 4),
            },
            "telemetry": {
                "dS": -0.1 if self.can_proceed() else 0.15,
                "peace2": round(max(0.0, self.reversibility_score), 4),
                "kappa_r": round(dials["A"], 4),
                "confidence": round(genius_res["genius_score"], 4),
                "psi_le": round(self.current_energy, 4),
                "joules": self.tokens_consumed * 0.0005,
                "metabolic_flux": round(self.metabolic_flux, 2),
                "temporal_stability": round(stability_t, 4),
                "uncertainty_score": self.safety_omega,
                "reason_cycles": self.reason_cycles,
            },
            "dials": dials,
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


def route_pipeline(query: str, context: dict | None = None) -> list[str]:
    """
    Minimal metabolic router.
    Returns ordered stage plan for the kernel.
    Ensures exploration vs. commitment stages are properly sequenced.
    """
    q = (query or "").lower()
    plan = ["111_SENSE", "333_MIND", "666_CRITIQUE"]

    grounding = ("search", "evidence", "source", "verify", "ground", "data")
    memory = ("recall", "remember", "memory", "vault", "history")
    safety = ("risk", "harm", "danger", "safe", "ethic", "impact")
    execute = ("run", "execute", "command", "shell", "delete", "write", "deploy")
    govern = ("law", "constitution", "authority", "approve", "judge")

    if any(k in q for k in grounding):
        plan.insert(1, "222_REALITY")

    if any(k in q for k in memory):
        if "555_MEMORY" not in plan:
            plan.insert(-1, "555_MEMORY")

    if any(k in q for k in safety):
        if "666_HEART" not in plan:
            plan.insert(-1, "666_HEART")

    if any(k in q for k in execute):
        if "777_FORGE" not in plan:
            plan.append("777_FORGE")

    if any(k in q for k in govern):
        if "888_JUDGE" not in plan:
            plan.append("888_JUDGE")

    if "777_FORGE" in plan:
        if "800_NEGOTIATE" not in plan:
            plan.insert(plan.index("777_FORGE") + 1, "800_NEGOTIATE")

    if "777_FORGE" in plan and "888_JUDGE" not in plan:
        plan.append("888_JUDGE")

    if context and context.get("force_grounding"):
        if "222_REALITY" not in plan:
            plan.insert(1, "222_REALITY")

    mode = context.get("mode", "recommend") if context else "recommend"
    if mode in ("inspect", "analyze"):
        return ["000_INIT", "333_MIND"]

    if context and context.get("human_required") or mode == "governed_execute":
        if "888_JUDGE" not in plan:
            plan.append("888_JUDGE")

    return plan


__all__ = [
    "AuthorityLevel",
    "GovernanceState",
    "GovernanceThresholds",
    "GovernanceKernel",
    "THERMODYNAMICS_AVAILABLE",
    "ThermodynamicBudget",
    "get_governance_kernel",
    "clear_governance_kernel",
    "_governance_kernels",
    "AppLayer",
    "FloorClassification",
    "FloorManifesto",
    "AppManifesto",
    "AppRegistry",
    "route_pipeline",
]
