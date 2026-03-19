"""
tests/aclip_cai/test_thermo.py
================================

Unit tests for aclip_cai.core.thermo_budget — thermodynamic session tracking.
"""

import pytest
from aclip_cai.core.thermo_budget import ThermoBudget, ThermoSnapshot


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
    for i in range(10):
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
