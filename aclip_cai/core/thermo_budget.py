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

Authority: ARIF FAZIL (Sovereign)
Version: 2026.02.22-FORGE-KERNEL-SEAL
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

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
        initial_akal: float = 0.95,
        initial_energy: float = 0.92,
        initial_exploration: float = 0.90,
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
        }

    def all_sessions_summary(self) -> list[dict]:
        """Telemetry snapshot across all open sessions."""
        return [self.budget_summary(sid) for sid in self._sessions]
