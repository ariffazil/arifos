"""
aclip_cai/core/thermo_budget.py — Thermodynamic Session Budget Manager

Tracks ΔS (entropy delta), Peace² (safety margins), and Ω₀ (uncertainty
band) per session, enforcing the Genius Equation G = A × P × X × E² ≥ 0.80.

Constitutional Physics:
  G = A × P × X × E²
    A = Akal (Logical Accuracy)
    P = Peace (Safety/Stability)
    X = Exploration (Novelty/Creativity)
    E = Energy (Efficiency, squared)
  G < 0.80 → output is VOID

EUREKA Layer 3 — Real Thermodynamic Budgets:
  Landauer's Principle: E_min = k_B × T × ln(2) per bit erased (~2.85e-21 J at 300 K)
  Every token consumed and memory operation is grounded in real physics.
  Note: this is a thermodynamic approximation — real hardware costs exceed
  the Landauer minimum by several orders of magnitude.

Authority: ARIF FAZIL (Sovereign)
Version: 2026.02.22-FORGE-KERNEL-SEAL
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Landauer's Principle constants (EUREKA Layer 3)
# ---------------------------------------------------------------------------

_K_BOLTZMANN = 1.380649e-23  # J/K
_T_ROOM = 300.0  # Kelvin (standard operating temperature)
# Minimum energy per bit erased: E_min = k_B × T × ln(2)
LANDAUER_LIMIT_JOULES: float = _K_BOLTZMANN * _T_ROOM * math.log(2)  # ~2.87e-21 J

# Bit-cost assumptions for Landauer accounting
BITS_PER_TOKEN = 32  # Estimated bits of state erased per processed token
BITS_PER_BYTE = 8  # Bits per byte of additional memory allocated

# ---------------------------------------------------------------------------
# ThermoSnapshot — Immutable thermodynamic state at a point in time
# ---------------------------------------------------------------------------


@dataclass
class ThermoSnapshot:
    session_id: str
    timestamp: str
    delta_s: float  # Entropy delta (target ΔS ≤ 0)
    peace2: float  # Safety margin (target P² ≥ 1.0)
    omega0: float  # Uncertainty estimate (target 0.03–0.15)
    akal: float  # Logical accuracy A ∈ [0, 1]
    exploration: float  # Novelty X ∈ [0, 1]
    energy: float  # Efficiency E ∈ [0, 1]
    genius: float  # G = A × peace2 × exploration × energy²
    genius_pass: bool  # G ≥ 0.80
    # EUREKA Layer 3 — Landauer-grounded energy accounting
    tokens_consumed: int = 0  # cumulative tokens processed this session
    bits_erased: int = 0  # estimated bits erased (tokens×32 + memory×8)
    min_energy_joules: float = 0.0  # Landauer minimum: bits_erased × k_B×T×ln(2)

    @classmethod
    def compute(
        cls,
        session_id: str,
        delta_s: float = 0.0,
        peace2: float = 1.0,
        omega0: float = 0.04,
        akal: float = 0.95,
        exploration: float = 0.90,
        energy: float = 0.92,
        tokens_consumed: int = 0,
        bits_erased: int = 0,
        min_energy_joules: float = 0.0,
    ) -> ThermoSnapshot:
        genius = akal * peace2 * exploration * (energy**2)
        return cls(
            session_id=session_id,
            timestamp=datetime.now(tz=timezone.utc).isoformat(),
            delta_s=delta_s,
            peace2=peace2,
            omega0=omega0,
            akal=akal,
            exploration=exploration,
            energy=energy,
            genius=genius,
            genius_pass=genius >= 0.80,
            tokens_consumed=tokens_consumed,
            bits_erased=bits_erased,
            min_energy_joules=min_energy_joules,
        )


# ---------------------------------------------------------------------------
# ThermoBudget — Tracks and enforces thermodynamic constraints per session
# ---------------------------------------------------------------------------


class ThermoBudget:
    """
    Per-session thermodynamic budget manager.

    Usage:
        budget = ThermoBudget()
        budget.open_session("sess-001")
        budget.record_step("sess-001", delta_s=-0.15, peace2=1.05)
        snap = budget.snapshot("sess-001")
        print(snap.genius, snap.genius_pass)
    """

    # Constitutional thresholds
    GENIUS_THRESHOLD = 0.80  # G ≥ 0.80 required
    PEACE2_MINIMUM = 1.00  # Peace² ≥ 1.0
    OMEGA0_LOW = 0.03  # Humility lower bound
    OMEGA0_HIGH = 0.15  # Humility upper bound (v64.1 relaxed)
    DELTA_S_TARGET = 0.00  # ΔS must be ≤ 0 (clarity gain)

    def __init__(self) -> None:
        self._sessions: dict[str, dict] = {}

    def open_session(
        self,
        session_id: str,
        initial_akal: float = 0.98,
        initial_energy: float = 0.95,
        initial_exploration: float = 0.95,
    ) -> None:
        """Register a new session with default thermodynamic state."""
        self._sessions[session_id] = {
            "delta_s": 0.0,
            "peace2": 1.0,
            "omega0": 0.04,
            "akal": initial_akal,
            "exploration": initial_exploration,
            "energy": initial_energy,
            "step_count": 0,
            "history": [],
            # EUREKA Layer 3 — Landauer accounting
            "tokens_consumed": 0,
            "bits_erased": 0,
            "min_energy_joules": 0.0,
        }

    def record_step(
        self,
        session_id: str,
        delta_s: float = 0.0,
        peace2: float | None = None,
        omega0: float | None = None,
        akal: float | None = None,
        exploration: float | None = None,
        energy: float | None = None,
    ) -> ThermoSnapshot:
        """
        Record a metabolic step for the session and return a snapshot.

        ΔS accumulates (entropy is additive per step).
        Energy decays with each step (E² law — exhaustion is exponential).
        """
        if session_id not in self._sessions:
            self.open_session(session_id)

        state = self._sessions[session_id]
        state["delta_s"] += delta_s
        state["peace2"] = peace2 if peace2 is not None else state["peace2"]
        state["omega0"] = omega0 if omega0 is not None else state["omega0"]
        state["akal"] = akal if akal is not None else state["akal"]
        state["exploration"] = exploration if exploration is not None else state["exploration"]

        # Energy decay: each step costs a small fraction (E² law)
        e = energy if energy is not None else state["energy"]
        state["energy"] = max(0.01, e * 0.995)  # 0.5% decay per step
        state["step_count"] += 1

        snap = ThermoSnapshot.compute(
            session_id=session_id,
            delta_s=state["delta_s"],
            peace2=state["peace2"],
            omega0=state["omega0"],
            akal=state["akal"],
            exploration=state["exploration"],
            energy=state["energy"],
            tokens_consumed=state.get("tokens_consumed", 0),
            bits_erased=state.get("bits_erased", 0),
            min_energy_joules=state.get("min_energy_joules", 0.0),
        )

        state["history"].append(
            {
                "step": state["step_count"],
                "genius": snap.genius,
                "delta_s": snap.delta_s,
            }
        )
        return snap

    def update_budget(
        self,
        session_id: str,
        *,
        delta_s: float = 0.0,
        peace2: float | None = None,
        omega0: float | None = None,
        akal: float | None = None,
        exploration: float | None = None,
        energy: float | None = None,
    ) -> ThermoSnapshot:
        """
        Backwards-compatible alias for legacy triad modules.

        Prefer :meth:`record_step` for new code.
        """
        return self.record_step(
            session_id=session_id,
            delta_s=delta_s,
            peace2=peace2,
            omega0=omega0,
            akal=akal,
            exploration=exploration,
            energy=energy,
        )

    def snapshot(self, session_id: str) -> ThermoSnapshot | None:
        """Return the current thermodynamic snapshot for a session."""
        state = self._sessions.get(session_id)
        if not state:
            return None
        return ThermoSnapshot.compute(
            session_id=session_id,
            delta_s=state["delta_s"],
            peace2=state["peace2"],
            omega0=state["omega0"],
            akal=state["akal"],
            exploration=state["exploration"],
            energy=state["energy"],
            tokens_consumed=state.get("tokens_consumed", 0),
            bits_erased=state.get("bits_erased", 0),
            min_energy_joules=state.get("min_energy_joules", 0.0),
        )

    def omega_in_band(self, session_id: str) -> bool:
        """Return True if session's Ω₀ is within [OMEGA0_LOW, OMEGA0_HIGH]."""
        state = self._sessions.get(session_id)
        if not state:
            return False
        return self.OMEGA0_LOW <= state["omega0"] <= self.OMEGA0_HIGH

    def is_genius_pass(self, session_id: str) -> bool:
        """Return True if current G ≥ 0.80."""
        snap = self.snapshot(session_id)
        return snap.genius_pass if snap else False

    # ------------------------------------------------------------------
    # EUREKA Layer 3 — Real Landauer energy accounting
    # ------------------------------------------------------------------

    # Landauer's Principle constant (class-level alias for easy access via instance)
    _LANDAUER_LIMIT = LANDAUER_LIMIT_JOULES

    def record_operation(
        self,
        session_id: str,
        operation_type: str,
        token_count: int = 0,
        memory_delta_bytes: int = 0,
    ) -> ThermoSnapshot:
        """
        Record a computational operation and update Landauer-grounded energy accounting.

        Energy cost per Landauer's Principle:
            E_min = bits_erased × k_B × T × ln(2)

        Bit estimation:
            - Each token ≈ 32 bits of state erased during processing
            - Each byte of memory allocated ≈ 8 bits erased

        Note: This is a thermodynamic approximation — real hardware costs
        exceed the Landauer minimum by several orders of magnitude.

        Args:
            session_id:          Target session.
            operation_type:      Label for the operation (e.g. "reasoning", "tool_call").
            token_count:         Number of tokens processed.
            memory_delta_bytes:  Additional memory allocated (bytes).

        Returns:
            Updated ThermoSnapshot with current Landauer accounting.
        """
        if session_id not in self._sessions:
            self.open_session(session_id)

        state = self._sessions[session_id]
        state["tokens_consumed"] = state.get("tokens_consumed", 0) + token_count

        # Estimate bits erased using named physical constants
        bits = (token_count * BITS_PER_TOKEN) + (memory_delta_bytes * BITS_PER_BYTE)
        state["bits_erased"] = state.get("bits_erased", 0) + bits
        state["min_energy_joules"] = state["bits_erased"] * LANDAUER_LIMIT_JOULES

        return self.record_step(session_id)

    def is_within_budget(self, session_id: str, max_joules: float = 1e-15) -> bool:
        """
        Check whether the session's accumulated Landauer energy cost is within budget.

        Args:
            session_id: Target session.
            max_joules: Maximum allowed thermodynamic cost (default 1e-15 J).
                        Note: This is a normalised approximation, not literal hardware power.

        Returns:
            True if min_energy_joules ≤ max_joules.
        """
        state = self._sessions.get(session_id, {})
        return state.get("min_energy_joules", 0.0) <= max_joules

    def landauer_summary(self, session_id: str) -> dict:
        """
        Return Landauer energy accounting summary for a session.

        Useful for audit trails and thermodynamic feasibility checks.
        """
        state = self._sessions.get(session_id, {})
        bits = state.get("bits_erased", 0)
        return {
            "session_id": session_id,
            "operation_note": "thermodynamic approximation — real hardware costs exceed Landauer minimum",
            "landauer_limit_joules": LANDAUER_LIMIT_JOULES,
            "tokens_consumed": state.get("tokens_consumed", 0),
            "bits_erased": bits,
            "min_energy_joules": state.get("min_energy_joules", 0.0),
            "entropy_cost_nat": round(bits * 0.6931, 6),  # bits × ln(2) in nats
        }

    def budget_summary(self, session_id: str) -> dict:
        """Return a telemetry-friendly summary dict."""
        snap = self.snapshot(session_id)
        if not snap:
            return {"error": f"Session {session_id!r} not found"}
        return {
            "session_id": snap.session_id,
            "genius": round(snap.genius, 4),
            "genius_pass": snap.genius_pass,
            "delta_s": round(snap.delta_s, 4),
            "peace2": round(snap.peace2, 4),
            "omega0": round(snap.omega0, 4),
            "omega_in_band": self.omega_in_band(session_id),
            "step_count": self._sessions[session_id]["step_count"],
            "landauer": self.landauer_summary(session_id),
        }

    def all_sessions_summary(self) -> list[dict]:
        """Telemetry snapshot across all open sessions."""
        return [self.budget_summary(sid) for sid in self._sessions]
