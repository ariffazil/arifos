"""
tests/adversarial/test_p3_hardening.py
"""

import pytest
import os
import importlib
import core.physics.thermodynamics_hardened

# FORCE PHYSICS ENABLED
os.environ["ARIFOS_PHYSICS_DISABLED"] = "0"
importlib.reload(core.physics.thermodynamics_hardened)

from core.physics.thermodynamics_hardened import (
    init_thermodynamic_budget,
    check_landauer_before_seal,
    LandauerViolation,
    EntropyIncreaseViolation,
    ThermodynamicExhaustion,
    record_entropy_io,
    consume_reason_energy,
)


def test_ghost_energy_violation():
    session_id = "adv_ghost"
    init_thermodynamic_budget(session_id, initial_budget=1.0)
    with pytest.raises(LandauerViolation) as excinfo:
        check_landauer_before_seal(
            session_id=session_id, compute_ms=0.001, tokens=1, delta_s=-2.0e16
        )
    assert "Bound VIOLATED" in str(excinfo.value) or "Efficiency VIOLATED" in str(excinfo.value)


def test_entropy_increase_rejection():
    session_id = "adv_entropy"
    init_thermodynamic_budget(session_id, initial_budget=1.0)
    with pytest.raises(EntropyIncreaseViolation) as excinfo:
        record_entropy_io(session_id, input_entropy=0.5, output_entropy=0.8)
    assert "F4 Clarity VIOLATED" in str(excinfo.value)


def test_budget_exhaustion_blocking():
    session_id = "adv_exhaust"
    init_thermodynamic_budget(session_id, initial_budget=0.0001)
    with pytest.raises(ThermodynamicExhaustion) as excinfo:
        consume_reason_energy(session_id, n_cycles=1)
    assert "Budget EXHAUSTED" in str(excinfo.value)
