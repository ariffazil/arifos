"""
tests/arifosmcp.intelligence/test_thermo.py
================================

Unit tests for arifosmcp.intelligence.core.thermo_budget — thermodynamic session tracking.
"""

import importlib.util
import sys
from pathlib import Path

import pytest


def _load_thermo_budget_module():
    module_name = "tests_thermo_budget_mod"
    if module_name in sys.modules:
        return sys.modules[module_name]

    module_path = (
        Path(__file__).resolve().parents[2]
        / "arifosmcp"
        / "intelligence"
        / "core"
        / "thermo_budget.py"
    )
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


thermo_budget = _load_thermo_budget_module()
ThermoBudget = thermo_budget.ThermoBudget
ThermoSnapshot = thermo_budget.ThermoSnapshot


@pytest.fixture
def budget():
    return ThermoBudget()


def test_snapshot_defaults(budget):
    """First step returns a valid snapshot with Genius computed."""
    snap = budget.record_step(session_id="s1", delta_s=-0.3)
    assert isinstance(snap, ThermoSnapshot)
    assert isinstance(snap.genius, float)
    assert 0.0 <= snap.genius <= 1.0


def test_genius_passes_on_good_metrics(budget):
    """G ≥ 0.80 with explicit high-quality parameters.

    G = A × P × X × E²
      = 0.95 × 1.0 × 0.90 × 1.0² = 0.855 (provably ≥ 0.80)
    Passing energy=1.0 explicitly avoids decay affecting the assertion.
    """
    snap = budget.record_step(
        session_id="s2",
        delta_s=-0.5,
        peace2=1.0,
        exploration=0.90,
        energy=1.0,  # Explicit: bypasses open_session default decay
    )
    assert snap.genius >= 0.80, f"G={snap.genius:.4f} < 0.80"

    assert snap.genius_pass is True


def test_energy_decays_over_steps(budget):
    """Energy should monotonically decrease (or stay stable) over multiple steps."""
    energies = []
    for _i in range(10):
        snap = budget.record_step(session_id="s3", delta_s=0.0)
        energies.append(snap.energy)
    assert energies[-1] < energies[0], "Energy should decay over steps"


def test_delta_s_accumulates(budget):
    """Cumulative ΔS should reflect summed deltas across steps."""
    budget.record_step("s4", delta_s=-0.2)
    snap = budget.record_step("s4", delta_s=-0.3)
    # .delta_s holds the running total
    assert snap.delta_s == pytest.approx(-0.5, abs=1e-6)


def test_genius_fails_with_bad_exploration(budget):
    """G < 0.80 when exploration is near zero."""
    snap = budget.record_step(
        session_id="s5",
        exploration=0.01,
    )
    # With exploration=0.01, G = A * P * 0.01 * E² is very small
    assert snap.genius < 0.80
    assert snap.genius_pass is False


def test_separate_sessions_independent(budget):
    """Two sessions should not share state."""
    budget.record_step("sA", delta_s=-1.0)
    # Open sB fresh; delta_s should start from 0
    budget.open_session("sB")
    snap_b = budget.record_step("sB", delta_s=0.0)
    assert snap_b.delta_s == pytest.approx(0.0, abs=1e-9)


def test_apex_output_math_and_meaning_are_aligned(budget):
    """APEX runtime schema should keep math and narrative aligned."""
    budget.open_session(
        "s-apex",
        architecture=1.05,
        parameters=1.2,
        data_quality=0.9,
    )
    budget.record_step("s-apex", delta_s=-0.3, tool_calls=2, tokens=500)
    budget.record_step("s-apex", delta_s=-0.2, tool_calls=1, tokens=300)
    budget.record_step("s-apex", delta_s=-0.1, tool_calls=0, tokens=200)

    apex_output = budget.budget_summary("s-apex")["apex_output"]
    capacity = apex_output["capacity_layer"]
    effort = apex_output["effort_layer"]
    entropy = apex_output["entropy_layer"]
    efficiency = apex_output["efficiency_layer"]
    governed = apex_output["governed_intelligence"]
    governance = apex_output["governance_layer"]
    diagnostics = apex_output["diagnostics"]

    assert capacity["capacity_product"] == pytest.approx(1.05 * 1.2 * 0.9, abs=1e-6)
    assert effort["effort_amplifier"] == pytest.approx(effort["E"] ** 2, abs=1e-6)
    assert entropy["delta_S"] == pytest.approx(entropy["H_before"] - entropy["H_after"], abs=1e-6)
    assert efficiency["eta"] == pytest.approx(
        efficiency["entropy_removed"] / efficiency["C"], abs=1e-6
    )
    assert governed["G_dagger"] == pytest.approx(
        governed["G_star"] * efficiency["eta"], abs=1e-6
    )

    assert capacity["status"] == "high"
    assert effort["status"] == "intensive"
    assert entropy["status"] == "clarifying"
    assert efficiency["status"] == "thin"
    assert governance["status"] == "provisional"
    assert diagnostics["primary_constraint"] == "governance"
    assert "Structural headroom is strong" in capacity["meaning"]
    assert "substantial inference effort" in effort["meaning"]
    assert "produced clarity" in entropy["meaning"]
    assert "spending compute faster" in efficiency["meaning"]
    assert "partially observed" in governance["meaning"]
    assert "realized governed intelligence is" in diagnostics["runtime_story"]


def test_entropy_removed_is_capped_to_entropy_baseline(budget):
    """Entropy removal should not exceed the available baseline entropy."""
    budget.open_session("s-cap", entropy_baseline=1.0)

    snap = budget.record_step("s-cap", delta_s=-2.0, tokens=100)
    apex_output = snap.as_apex_output()

    assert snap.H_before == pytest.approx(1.0, abs=1e-6)
    assert snap.H_after == pytest.approx(0.0, abs=1e-6)
    assert snap.entropy_removed == pytest.approx(1.0, abs=1e-6)
    assert snap.eta == pytest.approx(0.01, abs=1e-6)
    assert apex_output["entropy_layer"]["delta_S"] == pytest.approx(1.0, abs=1e-6)
    assert apex_output["efficiency_layer"]["eta"] == pytest.approx(0.01, abs=1e-6)
