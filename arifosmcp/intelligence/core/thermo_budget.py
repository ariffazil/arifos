"""
arifosmcp.intelligence/core/thermo_budget.py — Thermodynamic Session Budget Manager

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

    # --- APEX Metrics (G† = G* · η) ---
    effort: float = 0.0  # E: accumulated tool calls + reasoning steps
    token_cost: int = 0  # C: cumulative tokens this session
    architecture: float = 1.0  # A: static model quality index
    parameters: float = 1.0  # P: normalized param count
    data_quality: float = 0.95  # X: context/data quality ∈ [0,1]
    eta: float = 0.0  # η = |ΔS| / C  (insight per token)
    G_star: float = 0.0  # A·P·X·E²
    G_dagger: float = 0.0  # G* · η  (governed intelligence score)
    G_dagger_pass: bool = False  # G† ≥ 0.80

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
        # APEX parameters
        effort: float = 0.0,
        token_cost: int = 0,
        architecture: float = 1.0,
        parameters: float = 1.0,
        data_quality: float = 0.95,
    ) -> ThermoSnapshot:
        genius = akal * peace2 * exploration * (energy**2)
        # ΔS is reduction: magnitude of negative delta_s (clarity gain)
        delta_s_reduction = abs(min(0.0, delta_s))
        eta = delta_s_reduction / token_cost if token_cost > 0 else 0.0
        G_star = architecture * parameters * data_quality * (effort**2)
        G_dagger = G_star * eta
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
            effort=effort,
            token_cost=token_cost,
            architecture=architecture,
            parameters=parameters,
            data_quality=data_quality,
            eta=round(eta, 6),
            G_star=round(G_star, 6),
            G_dagger=round(G_dagger, 6),
            G_dagger_pass=G_dagger >= 0.80,
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
    G_DAGGER_THRESHOLD = 0.80  # G† ≥ 0.80 required
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
        # APEX static factors
        architecture: float = 1.0,
        parameters: float = 1.0,
        data_quality: float = 0.95,
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
            # APEX
            "effort": 0.0,
            "token_cost": 0,
            "architecture": architecture,
            "parameters": parameters,
            "data_quality": data_quality,
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
        # APEX additions
        tool_calls: int = 0,
        tokens: int = 0,
        data_quality: float | None = None,
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

        # APEX: accumulate effort and token cost
        state["effort"] += 1.0 + 0.5 * tool_calls
        state["token_cost"] += tokens
        if data_quality is not None:
            state["data_quality"] = data_quality

        snap = ThermoSnapshot.compute(
            session_id=session_id,
            delta_s=state["delta_s"],
            peace2=state["peace2"],
            omega0=state["omega0"],
            akal=state["akal"],
            exploration=state["exploration"],
            energy=state["energy"],
            # APEX fields
            effort=state["effort"],
            token_cost=state["token_cost"],
            architecture=state["architecture"],
            parameters=state["parameters"],
            data_quality=state["data_quality"],
        )

        state["history"].append(
            {
                "step": state["step_count"],
                "genius": snap.genius,
                "delta_s": snap.delta_s,
                "G_dagger": snap.G_dagger,
                "effort": snap.effort,
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
        tool_calls: int = 0,
        tokens: int = 0,
        data_quality: float | None = None,
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
            tool_calls=tool_calls,
            tokens=tokens,
            data_quality=data_quality,
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
            # APEX fields
            effort=state.get("effort", 0.0),
            token_cost=state.get("token_cost", 0),
            architecture=state.get("architecture", 1.0),
            parameters=state.get("parameters", 1.0),
            data_quality=state.get("data_quality", 0.95),
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

    def is_G_dagger_pass(self, session_id: str) -> bool:
        """Return True if current G† ≥ 0.80."""
        snap = self.snapshot(session_id)
        return snap.G_dagger_pass if snap else False

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
            # APEX metrics
            "effort": round(snap.effort, 3),
            "token_cost": snap.token_cost,
            "architecture": snap.architecture,
            "parameters": snap.parameters,
            "data_quality": round(snap.data_quality, 4),
            "eta": round(snap.eta, 6),
            "G_star": round(snap.G_star, 4),
            "G_dagger": round(snap.G_dagger, 4),
            "G_dagger_pass": snap.G_dagger_pass,
        }

    def all_sessions_summary(self) -> list[dict]:
        """Telemetry snapshot across all open sessions."""
        return [self.budget_summary(sid) for sid in self._sessions]
