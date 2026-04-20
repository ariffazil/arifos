import pytest
import numpy as np
from arifos.geox.physics.petrophysics import archie_sw, simandoux_sw, indonesia_sw, monte_carlo_sw

def test_archie_sw():
    # Rw=0.1, Rt=10, phi=0.2, a=1, m=2, n=2
    # Sw = sqrt( (1*0.1) / (0.2^2 * 10) ) = sqrt( 0.1 / (0.04 * 10) ) = sqrt(0.1 / 0.4) = sqrt(0.25) = 0.5
    sw = archie_sw(rw=0.1, rt=10, phi=0.2, a=1, m=2, n=2)
    assert pytest.approx(sw, 0.001) == 0.5

def test_simandoux_sw_clean():
    # Clean sand case should match Archie
    sw_archie = archie_sw(rw=0.1, rt=10, phi=0.2)
    sw_sim = simandoux_sw(rw=0.1, rt=10, phi=0.2, vcl=0.0, rsh=1.0)
    assert pytest.approx(sw_sim, 0.001) == sw_archie

def test_indonesia_sw():
    # Basic check for Indonesia model
    sw = indonesia_sw(rw=0.05, rt=5.0, phi=0.25, vcl=0.1, rsh=2.0)
    assert 0 < sw < 1.0

def test_monte_carlo_sw():
    params = {
        "rw": (0.05, 0.005),
        "rt": (10.0, 1.0),
        "phi": (0.2, 0.02),
        "a": 1.0,
        "m": 2.0,
        "n": 2.0
    }
    result = monte_carlo_sw("archie", params, n_samples=100)
    assert "stats" in result
    assert "mean" in result["stats"]
    assert 0 < result["nominal_sw"] < 1.0

def test_governance_trigger():
    # Extreme porosity should trigger 888_HOLD
    params = {
        "rw": 0.1,
        "rt": 1.0,
        "phi": 0.5, # > 0.45
        "a": 1.0,
        "m": 2.0,
        "n": 2.0
    }
    result = monte_carlo_sw("archie", params)
    assert result["verdict"] == "888_HOLD"
    assert any("Porosity" in t for t in result["hold_triggers"])
