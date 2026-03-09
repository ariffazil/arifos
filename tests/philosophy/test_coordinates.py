"""
tests/philosophy/test_coordinates.py

Tests for the APEX-G 6D coordinate system (core/philosophy/coordinates.py).

Validates:
- APEXGCoordinate construction and bounds checking
- stage_to_tau mapping
- session_state_to_coordinate
- Category centroids remain within axis bounds
"""

import pytest

from core.philosophy.coordinates import (
    AXIS_BOUNDS,
    CATEGORY_CENTROIDS,
    CATEGORY_FLOOR_AFFINITIES,
    DIM,
    APEXGCoordinate,
    session_state_to_coordinate,
    stage_to_tau,
)


# ── APEXGCoordinate ──────────────────────────────────────────────────────────


def test_apex_g_coordinate_valid_construction():
    """APEXGCoordinate accepts values within all axis bounds."""
    coord = APEXGCoordinate(
        tau=0.5, delta_s=0.0, p2=1.0, g=0.85, psi=0.6, kappa_r=0.7
    )
    assert coord.tau == 0.5
    assert coord.delta_s == 0.0
    assert coord.p2 == 1.0
    assert coord.g == 0.85
    assert coord.psi == 0.6
    assert coord.kappa_r == 0.7


def test_apex_g_coordinate_as_vector_length():
    """as_vector() returns a tuple of length DIM (6)."""
    coord = APEXGCoordinate(tau=0.1, delta_s=-0.5, p2=0.8, g=0.9, psi=0.4, kappa_r=0.3)
    vec = coord.as_vector()
    assert len(vec) == DIM == 6


def test_apex_g_coordinate_bounds_tau_too_high():
    """tau > 1.0 raises ValueError."""
    with pytest.raises(ValueError, match="τ"):
        APEXGCoordinate(tau=1.1, delta_s=0.0, p2=1.0, g=0.85, psi=0.5, kappa_r=0.5)


def test_apex_g_coordinate_bounds_tau_too_low():
    """tau < 0.0 raises ValueError."""
    with pytest.raises(ValueError, match="τ"):
        APEXGCoordinate(tau=-0.1, delta_s=0.0, p2=1.0, g=0.85, psi=0.5, kappa_r=0.5)


def test_apex_g_coordinate_bounds_delta_s_too_high():
    """delta_s > 1.0 raises ValueError."""
    with pytest.raises(ValueError, match="ΔS"):
        APEXGCoordinate(tau=0.5, delta_s=1.5, p2=1.0, g=0.85, psi=0.5, kappa_r=0.5)


def test_apex_g_coordinate_bounds_delta_s_too_low():
    """delta_s < -1.0 raises ValueError."""
    with pytest.raises(ValueError, match="ΔS"):
        APEXGCoordinate(tau=0.5, delta_s=-1.5, p2=1.0, g=0.85, psi=0.5, kappa_r=0.5)


def test_apex_g_coordinate_bounds_p2_too_high():
    """p2 > 2.0 raises ValueError."""
    with pytest.raises(ValueError, match="P²"):
        APEXGCoordinate(tau=0.5, delta_s=0.0, p2=2.5, g=0.85, psi=0.5, kappa_r=0.5)


def test_apex_g_coordinate_bounds_g_out_of_range():
    """g > 1.0 raises ValueError."""
    with pytest.raises(ValueError, match="G"):
        APEXGCoordinate(tau=0.5, delta_s=0.0, p2=1.0, g=1.5, psi=0.5, kappa_r=0.5)


def test_apex_g_coordinate_to_dict_roundtrip():
    """to_dict() → from_dict() roundtrip preserves values."""
    coord = APEXGCoordinate(
        tau=0.7, delta_s=-0.3, p2=1.4, g=0.88, psi=0.9, kappa_r=0.65,
        floor_affinities=["F1", "F6"]
    )
    d = coord.to_dict()
    restored = APEXGCoordinate.from_dict(d)
    assert restored.tau == coord.tau
    assert restored.delta_s == coord.delta_s
    assert restored.p2 == coord.p2
    assert restored.g == coord.g
    assert restored.psi == coord.psi
    assert restored.kappa_r == coord.kappa_r
    assert restored.floor_affinities == coord.floor_affinities


# ── stage_to_tau ────────────────────────────────────────────────────────────


def test_stage_to_tau_known_checkpoints():
    """Known stage numbers return their exact τ values."""
    assert stage_to_tau(0) == 0.00
    assert stage_to_tau(999) == 0.98
    assert stage_to_tau(666) == 0.65
    assert stage_to_tau(888) == 0.85


def test_stage_to_tau_string_stage():
    """String stage labels with numeric suffix are parsed correctly."""
    assert stage_to_tau("999_SEAL") == 0.98
    assert stage_to_tau("666_HEART") == 0.65
    assert stage_to_tau("000_INIT") == 0.00


def test_stage_to_tau_interpolation():
    """Intermediate stage values are interpolated between checkpoints."""
    tau_333 = stage_to_tau(333)
    tau_444 = stage_to_tau(444)
    tau_mid = stage_to_tau(388)  # between 333 and 444
    assert tau_333 <= tau_mid <= tau_444


def test_stage_to_tau_empty_string():
    """Empty string returns a sensible default (not a crash)."""
    result = stage_to_tau("")
    assert 0.0 <= result <= 1.0


def test_stage_to_tau_range():
    """All known stage checkpoints produce τ ∈ [0, 1]."""
    for stage_label in ["000", "111", "333", "444", "555", "666", "777", "888", "999"]:
        tau = stage_to_tau(stage_label)
        assert 0.0 <= tau <= 1.0, f"stage {stage_label} → τ={tau} out of range"


# ── Category centroids ───────────────────────────────────────────────────────


@pytest.mark.parametrize("category", list(CATEGORY_CENTROIDS.keys()))
def test_category_centroid_within_bounds(category):
    """Each category centroid lies within the APEX-G axis bounds."""
    centroid = CATEGORY_CENTROIDS[category]
    axis_names = ["tau", "delta_s", "p2", "g", "psi", "kappa_r"]
    axis_keys = ["τ", "ΔS", "P²", "G", "Ψ", "κᵣ"]
    for i, (name, key) in enumerate(zip(axis_names, axis_keys)):
        lo, hi = AXIS_BOUNDS[key]
        val = centroid[i]
        assert lo <= val <= hi, (
            f"Category '{category}' centroid {name}={val} outside [{lo}, {hi}]"
        )


def test_all_seven_categories_have_centroids():
    """All seven quote categories have defined centroids."""
    expected = {"scar", "triumph", "paradox", "wisdom", "power", "love", "seal"}
    assert expected == set(CATEGORY_CENTROIDS.keys())


def test_all_categories_have_floor_affinities():
    """All seven categories have at least one floor affinity."""
    for cat, floors in CATEGORY_FLOOR_AFFINITIES.items():
        assert len(floors) >= 1, f"Category '{cat}' has no floor affinities"


# ── session_state_to_coordinate ─────────────────────────────────────────────


def test_session_state_to_coordinate_stage_666():
    """session_state_to_coordinate uses stage_to_tau for τ."""
    coord = session_state_to_coordinate(stage="666", g_score=0.88)
    assert coord.tau == pytest.approx(0.65, abs=0.01)


def test_session_state_to_coordinate_clamps_values():
    """session_state_to_coordinate clamps out-of-range inputs to valid bounds."""
    coord = session_state_to_coordinate(
        stage="999",
        delta_s=-2.0,  # out of range
        p2=3.0,  # out of range
        g_score=1.5,  # out of range
        psi=-0.1,  # out of range
        kappa_r=2.0,  # out of range
    )
    assert -1.0 <= coord.delta_s <= 1.0
    assert 0.0 <= coord.p2 <= 2.0
    assert 0.0 <= coord.g <= 1.0
    assert 0.0 <= coord.psi <= 1.0
    assert 0.0 <= coord.kappa_r <= 1.0


def test_session_state_to_coordinate_propagates_floors():
    """Active floors are stored in the coordinate's floor_affinities."""
    coord = session_state_to_coordinate(active_floors=["F1", "F6", "F7"])
    assert "F1" in coord.floor_affinities
    assert "F6" in coord.floor_affinities
    assert "F7" in coord.floor_affinities


def test_session_state_to_coordinate_no_floors():
    """session_state_to_coordinate handles missing active_floors gracefully."""
    coord = session_state_to_coordinate()
    assert coord.floor_affinities == []


# ── WordPowerMechanism constants ─────────────────────────────────────────────


def test_word_power_mechanism_constants_exist():
    """WordPowerMechanism class exposes the four mechanism string constants."""
    from core.philosophy.coordinates import WordPowerMechanism

    assert WordPowerMechanism.NEURAL_SIMULATION == "neural_simulation"
    assert WordPowerMechanism.SYMBOLIC_COMPRESSION == "symbolic_compression"
    assert WordPowerMechanism.COORDINATION == "coordination"
    assert WordPowerMechanism.ATTENTION_STEERING == "attention_steering"


def test_all_mechanisms_tuple_has_four_entries():
    """ALL_MECHANISMS contains exactly four canonical mechanism strings."""
    from core.philosophy.coordinates import ALL_MECHANISMS

    assert len(ALL_MECHANISMS) == 4


def test_category_power_mechanisms_all_valid():
    """Every mechanism listed in CATEGORY_POWER_MECHANISMS is in ALL_MECHANISMS."""
    from core.philosophy.coordinates import ALL_MECHANISMS, CATEGORY_POWER_MECHANISMS

    for cat, mechanisms in CATEGORY_POWER_MECHANISMS.items():
        for mech in mechanisms:
            assert mech in ALL_MECHANISMS, (
                f"Category '{cat}' lists unknown mechanism '{mech}'"
            )


def test_category_resonance_density_all_in_range():
    """All baseline resonance densities are within [0, 1]."""
    from core.philosophy.coordinates import CATEGORY_RESONANCE_DENSITY

    for cat, rho in CATEGORY_RESONANCE_DENSITY.items():
        assert 0.0 <= rho <= 1.0, f"Category '{cat}' resonance_density={rho} out of [0,1]"


def test_seal_has_highest_resonance_density():
    """'seal' category has the highest baseline resonance density."""
    from core.philosophy.coordinates import CATEGORY_RESONANCE_DENSITY

    seal_rho = CATEGORY_RESONANCE_DENSITY["seal"]
    for cat, rho in CATEGORY_RESONANCE_DENSITY.items():
        if cat != "seal":
            assert seal_rho >= rho, (
                f"seal rho={seal_rho} should be >= {cat} rho={rho}"
            )


# ── AGI / ASI / APEX WisdomLayer constants ───────────────────────────────────


def test_wisdom_layer_constants():
    """WisdomLayer class exposes agi, asi, apex string constants."""
    from core.philosophy.coordinates import WisdomLayer

    assert WisdomLayer.AGI == "agi"
    assert WisdomLayer.ASI == "asi"
    assert WisdomLayer.APEX == "apex"


def test_layer_descriptions_have_required_keys():
    """Each LAYER_DESCRIPTIONS entry has role, question, nature, metaphor."""
    from core.philosophy.coordinates import LAYER_DESCRIPTIONS

    for layer, desc in LAYER_DESCRIPTIONS.items():
        for key in ("role", "question", "nature", "metaphor"):
            assert key in desc, f"Layer '{layer}' missing key '{key}'"


def test_category_agi_doctrine_all_categories():
    """CATEGORY_AGI_DOCTRINE covers all seven categories."""
    from core.philosophy.coordinates import CATEGORY_AGI_DOCTRINE

    expected = {"scar", "triumph", "paradox", "wisdom", "power", "love", "seal"}
    assert expected == set(CATEGORY_AGI_DOCTRINE.keys())


def test_category_agi_doctrine_non_empty():
    """All AGI doctrine strings are non-empty."""
    from core.philosophy.coordinates import CATEGORY_AGI_DOCTRINE

    for cat, doctrine in CATEGORY_AGI_DOCTRINE.items():
        assert len(doctrine.strip()) > 0, f"Category '{cat}' has empty doctrine"


def test_agi_layer_is_symbolic_skeleton():
    """AGI layer description correctly identifies symbolic nature."""
    from core.philosophy.coordinates import LAYER_DESCRIPTIONS, WisdomLayer

    agi = LAYER_DESCRIPTIONS[WisdomLayer.AGI]
    assert "symbolic" in agi["nature"].lower()
    assert "discrete" in agi["nature"].lower()


def test_asi_layer_is_continuous():
    """ASI layer description correctly identifies continuous/geometric nature."""
    from core.philosophy.coordinates import LAYER_DESCRIPTIONS, WisdomLayer

    asi = LAYER_DESCRIPTIONS[WisdomLayer.ASI]
    assert "continuous" in asi["nature"].lower()
    assert "geometry" in asi["nature"].lower() or "relational" in asi["nature"].lower()


def test_apex_layer_includes_arbitration():
    """APEX layer description references arbitration / scoring."""
    from core.philosophy.coordinates import LAYER_DESCRIPTIONS, WisdomLayer

    apex = LAYER_DESCRIPTIONS[WisdomLayer.APEX]
    assert "arbitration" in apex["role"].lower() or "scoring" in apex["nature"].lower()
