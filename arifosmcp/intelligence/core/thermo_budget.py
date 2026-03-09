"""
arifosmcp.intelligence/core/thermo_budget.py -- Thermodynamic Session Budget Manager

Tracks delta_S, Peace2, and Omega0 per session, enforcing G = A x P x X x E2 >= 0.80.

APEX Extension: G_dagger = A * P * X * E2 * (delta_S / C)

Authority: ARIF FAZIL (Sovereign)
Version: 2026.02.22-FORGE-KERNEL-SEAL
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timezone


def _band(value: float, low: float, high: float) -> str:
    if value < low:
        return "low"
    if value < high:
        return "moderate"
    return "high"


def _capacity_context(capacity_product: float) -> tuple[str, str]:
    status = _band(capacity_product, 0.25, 0.60)
    meanings = {
        "low": "Structural headroom is thin; the system is under-capacitated before effort begins.",
        "moderate": "Structural headroom is usable; effort can still move outcomes materially.",
        "high": "Structural headroom is strong; the system has meaningful latent capability.",
    }
    return status, meanings[status]


def _effort_context(effort: float) -> tuple[str, str]:
    status = "idle" if effort < 1.5 else "engaged" if effort < 4.0 else "intensive"
    meanings = {
        "idle": "Very little inference effort has been applied so far.",
        "engaged": "Reasoning effort is active but not yet saturated.",
        "intensive": "The system is spending substantial inference effort to solve the task.",
    }
    return status, meanings[status]


def _entropy_context(delta_s: float, h_before: float, h_after: float) -> tuple[str, str]:
    if delta_s < 0:
        return (
            "clarifying",
            f"Entropy fell from {h_before:.3f} to {h_after:.3f}; the session produced clarity.",
        )
    if delta_s > 0:
        return (
            "diffusing",
            f"Entropy rose from {h_before:.3f} to {h_after:.3f}; the session added disorder.",
        )
    return "flat", "Entropy did not materially move; the session is informationally flat."


def _efficiency_context(eta: float, token_cost: int, entropy_removed: float) -> tuple[str, str]:
    if entropy_removed <= 0:
        return "stalled", "No entropy was removed, so efficiency is effectively stalled."
    if token_cost <= 0:
        return (
            "unmetered",
            "Clarity changed, but compute cost is missing so efficiency is provisional.",
        )
    if eta >= 0.01:
        return "dense", "The runtime is removing a lot of entropy per unit of compute."
    if eta >= 0.001:
        return (
            "workable",
            "The runtime is producing some clarity per compute, but not efficiently yet.",
        )
    return "thin", "The runtime is spending compute faster than it is removing entropy."


def _governance_context(
    amanah_score: float,
    truth_floor: str,
    authority_status: str,
    sovereignty_status: str,
    tri_witness_status: str,
) -> tuple[str, str]:
    states = {
        truth_floor.lower(),
        authority_status.lower(),
        sovereignty_status.lower(),
        tri_witness_status.lower(),
    }
    if "fail" in states:
        return (
            "failed",
            "A governance floor is failing, so the runtime should not be treated "
            "as safely governed.",
        )
    if {"estimate only", "cannot compute"} & states:
        return (
            "provisional",
            "Governance is only partially observed; treat this runtime as not fully attested.",
        )
    if amanah_score >= 0.8 and states <= {"pass"}:
        return "attested", "Governance floors are aligned and amanah is strong."
    return (
        "mixed",
        "Governance signals are present but not strong enough to claim full attestation.",
    )


def _primary_constraint(
    capacity_product: float,
    effort: float,
    entropy_removed: float,
    eta: float,
    governance_status: str,
) -> str:
    if governance_status in {"failed", "provisional", "mixed"}:
        return "governance"
    if entropy_removed <= 0:
        return "entropy"
    if eta <= 0:
        return "efficiency"
    if capacity_product < 0.25:
        return "capacity"
    if effort < 1.5:
        return "effort"
    return "none"


def _runtime_story(
    capacity_status: str,
    effort_status: str,
    entropy_status: str,
    efficiency_status: str,
    governance_status: str,
    g_dagger: float,
) -> str:
    return (
        f"Capacity is {capacity_status}, effort is {effort_status}, entropy is {entropy_status}, "
        f"efficiency is {efficiency_status}, governance is {governance_status}; "
        f"realized governed intelligence is {g_dagger:.6f}."
    )


@dataclass
class ThermoSnapshot:
    session_id: str
    timestamp: str
    delta_s: float
    peace2: float
    omega0: float
    akal: float
    exploration: float
    energy: float
    genius: float
    genius_pass: bool
    # APEX Metrics
    effort: float = 0.0
    reasoning_steps: int = 0
    tool_calls: int = 0
    token_cost: int = 0
    architecture: float = 1.0
    parameters: float = 1.0
    data_quality: float = 0.95
    entropy_baseline: float = 1.0
    H_before: float = 1.0
    H_after: float = 1.0
    entropy_removed: float = 0.0
    eta: float = 0.0
    G_star: float = 0.0
    G_dagger: float = 0.0
    G_dagger_pass: bool = False
    amanah_score: float = 0.0
    truth_floor: str = "Estimate Only"
    authority_status: str = "Estimate Only"
    sovereignty_status: str = "Estimate Only"
    tri_witness_status: str = "Cannot Compute"

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
        effort: float = 0.0,
        reasoning_steps: int = 0,
        tool_calls: int = 0,
        token_cost: int = 0,
        architecture: float = 1.0,
        parameters: float = 1.0,
        data_quality: float = 0.95,
        entropy_baseline: float = 1.0,
        amanah_score: float | None = None,
        truth_floor: str = "Estimate Only",
        authority_status: str = "Estimate Only",
        sovereignty_status: str = "Estimate Only",
        tri_witness_status: str = "Cannot Compute",
    ) -> ThermoSnapshot:
        genius = akal * peace2 * exploration * (energy ** 2)
        h_before = max(0.0, entropy_baseline)
        h_after = max(0.0, h_before + delta_s)
        delta_s_reduction = max(0.0, h_before - h_after)
        eta = delta_s_reduction / token_cost if token_cost > 0 else 0.0
        g_star = architecture * parameters * data_quality * (effort ** 2)
        g_dagger = g_star * eta

        if amanah_score is None:
            amanah_components = [
                1.0 if delta_s <= 0 else 0.0,
                min(1.0, max(peace2, 0.0)),
                1.0 if 0.03 <= omega0 <= 0.15 else 0.0,
                0.5 if token_cost <= 0 else (1.0 if eta > 0 else 0.0),
            ]
            amanah_score = sum(amanah_components) / len(amanah_components)

        if truth_floor == "Estimate Only":
            truth_floor = "pass" if delta_s <= 0 else "warn"

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
            reasoning_steps=reasoning_steps,
            tool_calls=tool_calls,
            token_cost=token_cost,
            architecture=architecture,
            parameters=parameters,
            data_quality=data_quality,
            entropy_baseline=entropy_baseline,
            H_before=round(h_before, 6),
            H_after=round(h_after, 6),
            entropy_removed=round(delta_s_reduction, 6),
            eta=round(eta, 6),
            G_star=round(g_star, 6),
            G_dagger=round(g_dagger, 6),
            G_dagger_pass=g_dagger >= 0.80,
            amanah_score=round(amanah_score, 6),
            truth_floor=truth_floor,
            authority_status=authority_status,
            sovereignty_status=sovereignty_status,
            tri_witness_status=tri_witness_status,
        )

    def as_apex_output(self) -> dict:
        """Return APEX-aligned runtime output with explicit theorem layers."""
        capacity_product = round(self.architecture * self.parameters * self.data_quality, 6)
        capacity_status, capacity_meaning = _capacity_context(capacity_product)
        effort_status, effort_meaning = _effort_context(self.effort)
        entropy_status, entropy_meaning = _entropy_context(
            self.delta_s, self.H_before, self.H_after
        )
        efficiency_status, efficiency_meaning = _efficiency_context(
            self.eta, self.token_cost, self.entropy_removed
        )
        governance_status, governance_meaning = _governance_context(
            self.amanah_score,
            self.truth_floor,
            self.authority_status,
            self.sovereignty_status,
            self.tri_witness_status,
        )
        constraint = _primary_constraint(
            capacity_product,
            self.effort,
            self.entropy_removed,
            self.eta,
            governance_status,
        )

        return {
            "capacity_layer": {
                "A": self.architecture,
                "P": self.parameters,
                "X": self.data_quality,
                "capacity_product": capacity_product,
                "status": capacity_status,
                "meaning": capacity_meaning,
            },
            "effort_layer": {
                "E": round(self.effort, 4),
                "effort_amplifier": round(self.effort ** 2, 6),
                "reasoning_steps": self.reasoning_steps,
                "tool_calls": self.tool_calls,
                "status": effort_status,
                "meaning": effort_meaning,
            },
            "entropy_layer": {
                "H_before": self.H_before,
                "H_after": self.H_after,
                "delta_S": self.entropy_removed,
                "status": entropy_status,
                "meaning": entropy_meaning,
            },
            "efficiency_layer": {
                "C": self.token_cost,
                "entropy_removed": self.entropy_removed,
                "eta": self.eta,
                "status": efficiency_status,
                "meaning": efficiency_meaning,
            },
            "governed_intelligence": {
                "G_star": self.G_star,
                "G_dagger": self.G_dagger,
                "status": "passing" if self.G_dagger_pass else "subcritical",
                "meaning": (
                    "Governed intelligence is above threshold."
                    if self.G_dagger_pass
                    else "Governed intelligence is still below the current threshold."
                ),
            },
            "governance_layer": {
                "amanah_score": self.amanah_score,
                "truth_floor": self.truth_floor,
                "authority_status": self.authority_status,
                "sovereignty_status": self.sovereignty_status,
                "tri_witness_status": self.tri_witness_status,
                "status": governance_status,
                "meaning": governance_meaning,
            },
            "diagnostics": {
                "log_decomposition": {
                    "logA": round(math.log(self.architecture), 4) if self.architecture > 0 else 0.0,
                    "logP": round(math.log(self.parameters), 4) if self.parameters > 0 else 0.0,
                    "logX": round(math.log(self.data_quality), 4) if self.data_quality > 0 else 0.0,
                    "2logE": round(2 * math.log(self.effort), 4) if self.effort > 0 else 0.0,
                    "logDeltaS": round(math.log(self.entropy_removed), 4)
                    if self.entropy_removed > 0
                    else 0.0,
                    "logC": round(math.log(self.token_cost), 4) if self.token_cost > 0 else 0.0,
                },
                "primary_constraint": constraint,
                "equation": "log G† = logA + logP + logX + 2logE + logDeltaS - logC",
                "runtime_story": _runtime_story(
                    capacity_status,
                    effort_status,
                    entropy_status,
                    efficiency_status,
                    governance_status,
                    self.G_dagger,
                ),
            },
        }


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

    GENIUS_THRESHOLD = 0.80
    PEACE2_MINIMUM = 1.00
    OMEGA0_LOW = 0.03
    OMEGA0_HIGH = 0.15
    DELTA_S_TARGET = 0.00
    G_DAGGER_THRESHOLD = 0.80

    def __init__(self) -> None:
        self._sessions: dict = {}

    def open_session(
        self,
        session_id: str,
        initial_akal: float = 0.98,
        initial_energy: float = 0.95,
        initial_exploration: float = 0.95,
        architecture: float = 1.0,
        parameters: float = 1.0,
        data_quality: float = 0.95,
        entropy_baseline: float = 1.0,
        amanah_score: float | None = None,
        truth_floor: str = "Estimate Only",
        authority_status: str = "Estimate Only",
        sovereignty_status: str = "Estimate Only",
        tri_witness_status: str = "Cannot Compute",
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
            "tool_calls": 0,
            "history": [],
            "effort": 0.0,
            "token_cost": 0,
            "architecture": architecture,
            "parameters": parameters,
            "data_quality": data_quality,
            "entropy_baseline": entropy_baseline,
            "amanah_score": amanah_score,
            "truth_floor": truth_floor,
            "authority_status": authority_status,
            "sovereignty_status": sovereignty_status,
            "tri_witness_status": tri_witness_status,
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
        tool_calls: int = 0,
        tokens: int = 0,
        data_quality: float | None = None,
        amanah_score: float | None = None,
        truth_floor: str | None = None,
        authority_status: str | None = None,
        sovereignty_status: str | None = None,
        tri_witness_status: str | None = None,
    ) -> ThermoSnapshot:
        """
        Record a metabolic step for the session and return a snapshot.

        delta_S accumulates (entropy is additive per step).
        Energy decays with each step (E2 law -- exhaustion is exponential).
        """
        if session_id not in self._sessions:
            self.open_session(session_id)

        state = self._sessions[session_id]
        state["delta_s"] += delta_s
        state["peace2"] = peace2 if peace2 is not None else state["peace2"]
        state["omega0"] = omega0 if omega0 is not None else state["omega0"]
        state["akal"] = akal if akal is not None else state["akal"]
        state["exploration"] = exploration if exploration is not None else state["exploration"]

        e = energy if energy is not None else state["energy"]
        state["energy"] = max(0.01, e * 0.995)
        state["step_count"] += 1
        state["tool_calls"] += tool_calls

        state["effort"] += 1.0 + 0.5 * tool_calls
        state["token_cost"] += tokens
        if data_quality is not None:
            state["data_quality"] = data_quality
        if amanah_score is not None:
            state["amanah_score"] = amanah_score
        if truth_floor is not None:
            state["truth_floor"] = truth_floor
        if authority_status is not None:
            state["authority_status"] = authority_status
        if sovereignty_status is not None:
            state["sovereignty_status"] = sovereignty_status
        if tri_witness_status is not None:
            state["tri_witness_status"] = tri_witness_status

        snap = ThermoSnapshot.compute(
            session_id=session_id,
            delta_s=state["delta_s"],
            peace2=state["peace2"],
            omega0=state["omega0"],
            akal=state["akal"],
            exploration=state["exploration"],
            energy=state["energy"],
            effort=state["effort"],
            reasoning_steps=state["step_count"],
            tool_calls=state["tool_calls"],
            token_cost=state["token_cost"],
            architecture=state["architecture"],
            parameters=state["parameters"],
            data_quality=state["data_quality"],
            entropy_baseline=state.get("entropy_baseline", 1.0),
            amanah_score=state.get("amanah_score"),
            truth_floor=state.get("truth_floor", "Estimate Only"),
            authority_status=state.get("authority_status", "Estimate Only"),
            sovereignty_status=state.get("sovereignty_status", "Estimate Only"),
            tri_witness_status=state.get("tri_witness_status", "Cannot Compute"),
        )

        state["history"].append(
            {
                "step": state["step_count"],
                "genius": snap.genius,
                "delta_s": snap.delta_s,
                "G_dagger": snap.G_dagger,
                "effort": snap.effort,
                "tool_calls": snap.tool_calls,
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
        amanah_score: float | None = None,
        truth_floor: str | None = None,
        authority_status: str | None = None,
        sovereignty_status: str | None = None,
        tri_witness_status: str | None = None,
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
            amanah_score=amanah_score,
            truth_floor=truth_floor,
            authority_status=authority_status,
            sovereignty_status=sovereignty_status,
            tri_witness_status=tri_witness_status,
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
            effort=state.get("effort", 0.0),
            reasoning_steps=state.get("step_count", 0),
            tool_calls=state.get("tool_calls", 0),
            token_cost=state.get("token_cost", 0),
            architecture=state.get("architecture", 1.0),
            parameters=state.get("parameters", 1.0),
            data_quality=state.get("data_quality", 0.95),
            entropy_baseline=state.get("entropy_baseline", 1.0),
            amanah_score=state.get("amanah_score"),
            truth_floor=state.get("truth_floor", "Estimate Only"),
            authority_status=state.get("authority_status", "Estimate Only"),
            sovereignty_status=state.get("sovereignty_status", "Estimate Only"),
            tri_witness_status=state.get("tri_witness_status", "Cannot Compute"),
        )

    def omega_in_band(self, session_id: str) -> bool:
        """Return True if session Omega0 is within [OMEGA0_LOW, OMEGA0_HIGH]."""
        state = self._sessions.get(session_id)
        if not state:
            return False
        return self.OMEGA0_LOW <= state["omega0"] <= self.OMEGA0_HIGH

    def is_genius_pass(self, session_id: str) -> bool:
        """Return True if current G >= 0.80."""
        snap = self.snapshot(session_id)
        return snap.genius_pass if snap else False

    def is_g_dagger_pass(self, session_id: str) -> bool:
        """Return True if current G_dagger >= 0.80."""
        snap = self.snapshot(session_id)
        return snap.G_dagger_pass if snap else False

    is_G_dagger_pass = is_g_dagger_pass  # noqa: N815

    def budget_summary(self, session_id: str) -> dict:
        """Return the current session summary in the latest APEX layer schema."""
        snap = self.snapshot(session_id)
        if not snap:
            return {"error": f"Session {session_id!r} not found"}
        return {
            "session_id": snap.session_id,
            "step_count": self._sessions[session_id]["step_count"],
            "apex_output": snap.as_apex_output(),
        }

    def all_sessions_summary(self) -> list:
        """Telemetry snapshot across all open sessions."""
        return [self.budget_summary(sid) for sid in self._sessions]
