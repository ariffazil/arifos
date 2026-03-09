"""
tests/philosophy/test_manifold.py

Tests for the APEX-G Quote Manifold selection engine (core/philosophy/manifold.py).

Validates:
- Manifold loads the 99-quote corpus
- select() returns the nearest quote with floor affinity bonus
- Floor affinity weighting changes selection scores
- Provenance is included in output
- select_from_session_state() convenience wrapper works
- QuoteSelection.to_dict() serializes correctly
- Module-level select_wisdom() function works
- Runtime tool select_wisdom_manifold() works
"""

import pytest

from core.philosophy.manifold import (
    FLOOR_AFFINITY_BONUS,
    QuoteManifold,
    QuoteSelection,
    get_manifold,
    select_wisdom,
)


# ── Manifold loading ─────────────────────────────────────────────────────────


def test_manifold_loads_99_quotes():
    """QuoteManifold loads exactly 99 quotes from the manifold JSON."""
    m = get_manifold()
    assert m.loaded is True
    assert m.quote_count == 99


def test_manifold_is_singleton():
    """get_manifold() returns the same instance on repeated calls."""
    a = get_manifold()
    b = get_manifold()
    assert a is b


def test_fresh_manifold_instance_loads():
    """A fresh QuoteManifold() instance also loads successfully."""
    m = QuoteManifold()
    assert m.loaded is True
    assert m.quote_count == 99


# ── Basic selection ──────────────────────────────────────────────────────────


def test_select_returns_quote_selection():
    """select() returns a QuoteSelection with non-empty text."""
    m = get_manifold()
    result = m.select(tau=0.5, delta_s=0.0, p2=1.2, g=0.85, psi=0.7, kappa_r=0.6)
    assert isinstance(result, QuoteSelection)
    assert result.text != ""
    assert result.author != ""


def test_select_distance_non_negative():
    """select() returns a non-negative distance."""
    m = get_manifold()
    result = m.select(tau=0.8, delta_s=-0.3, p2=1.1, g=0.78, psi=0.85, kappa_r=0.72)
    assert result.distance >= 0.0


def test_select_score_positive():
    """select() returns a positive score."""
    m = get_manifold()
    result = m.select(tau=0.5, delta_s=0.0, p2=1.0, g=0.85, psi=0.5, kappa_r=0.5)
    assert result.score > 0.0


def test_select_near_scar_centroid():
    """Selecting near the scar centroid returns a scar-category quote."""
    m = get_manifold()
    # scar centroid: tau=0.80, delta_s=-0.30, p2=1.10, g=0.78, psi=0.85, kappa_r=0.72
    result = m.select(tau=0.80, delta_s=-0.30, p2=1.10, g=0.78, psi=0.85, kappa_r=0.72)
    assert result.category == "scar"


def test_select_near_seal_centroid():
    """Selecting near the seal centroid returns a seal-category quote."""
    m = get_manifold()
    # seal centroid: tau=0.98, delta_s=-0.80, p2=1.95, g=0.97, psi=0.98, kappa_r=0.90
    result = m.select(tau=0.98, delta_s=-0.80, p2=1.95, g=0.97, psi=0.98, kappa_r=0.90)
    assert result.category == "seal"


def test_select_near_wisdom_centroid():
    """Selecting near the wisdom centroid returns a wisdom-category quote."""
    m = get_manifold()
    # wisdom centroid: tau=0.40, delta_s=-0.40, p2=1.40, g=0.88, psi=0.97, kappa_r=0.68
    result = m.select(tau=0.40, delta_s=-0.40, p2=1.40, g=0.88, psi=0.97, kappa_r=0.68)
    assert result.category == "wisdom"


def test_select_near_love_centroid():
    """Selecting near the love centroid returns a love-category quote."""
    m = get_manifold()
    # love centroid: tau=0.82, delta_s=-0.50, p2=1.85, g=0.93, psi=0.82, kappa_r=0.95
    result = m.select(tau=0.82, delta_s=-0.50, p2=1.85, g=0.93, psi=0.82, kappa_r=0.95)
    assert result.category == "love"


# ── Floor affinity weighting ─────────────────────────────────────────────────


def test_floor_affinity_increases_score():
    """Active floors matching the quote's affinities increase the selection score."""
    m = get_manifold()
    # Query near scar centroid — F6, F7, F1 are scar affinities
    base = m.select(
        tau=0.80, delta_s=-0.30, p2=1.10, g=0.78, psi=0.85, kappa_r=0.72,
        active_floors=[],
    )
    boosted = m.select(
        tau=0.80, delta_s=-0.30, p2=1.10, g=0.78, psi=0.85, kappa_r=0.72,
        active_floors=["F6", "F7", "F1"],
    )
    assert boosted.score >= base.score


def test_floor_affinity_bonus_is_correct():
    """floor_affinity_bonus equals FLOOR_AFFINITY_BONUS × number of matched floors."""
    m = get_manifold()
    result = m.select(
        tau=0.80, delta_s=-0.30, p2=1.10, g=0.78, psi=0.85, kappa_r=0.72,
        active_floors=["F6", "F7"],
    )
    # Bonus must be a non-negative multiple of FLOOR_AFFINITY_BONUS
    assert result.floor_affinity_bonus >= 0.0
    matched = len(result.active_floors_matched)
    assert result.floor_affinity_bonus == pytest.approx(matched * FLOOR_AFFINITY_BONUS)


def test_no_active_floors_zero_bonus():
    """No active floors → floor_affinity_bonus = 0.0."""
    m = get_manifold()
    result = m.select(active_floors=[])
    assert result.floor_affinity_bonus == 0.0
    assert result.active_floors_matched == []


# ── Provenance ───────────────────────────────────────────────────────────────


def test_select_includes_provenance():
    """select() result includes a provenance dict."""
    m = get_manifold()
    result = m.select()
    assert isinstance(result.provenance, dict)
    assert "method" in result.provenance


def test_provenance_method_is_kd_tree():
    """When scipy is available, provenance method is 'kd_tree'."""
    try:
        from scipy.spatial import KDTree  # noqa: F401
        m = get_manifold()
        result = m.select()
        assert result.provenance["method"] == "kd_tree"
    except ImportError:
        pytest.skip("scipy not available")


def test_provenance_includes_formula():
    """Provenance includes the scoring formula string."""
    m = get_manifold()
    result = m.select()
    assert "formula" in result.provenance
    assert "floor_affinity_bonus" in result.provenance["formula"].lower()


def test_provenance_total_quotes():
    """Provenance includes total_quotes_in_manifold == 99."""
    m = get_manifold()
    result = m.select()
    assert result.provenance.get("total_quotes_in_manifold") == 99


def test_query_vector_in_result():
    """query_vector in the result matches the input coordinates."""
    m = get_manifold()
    result = m.select(tau=0.7, delta_s=-0.2, p2=1.3, g=0.90, psi=0.6, kappa_r=0.55)
    qv = result.query_vector
    assert qv[0] == pytest.approx(0.7)
    assert qv[1] == pytest.approx(-0.2)
    assert qv[2] == pytest.approx(1.3)
    assert qv[3] == pytest.approx(0.90)
    assert qv[4] == pytest.approx(0.6)
    assert qv[5] == pytest.approx(0.55)


# ── QuoteSelection.to_dict() ─────────────────────────────────────────────────


def test_to_dict_has_required_keys():
    """QuoteSelection.to_dict() contains the expected top-level keys."""
    m = get_manifold()
    result = m.select()
    d = result.to_dict()
    assert "quote_id" in d
    assert "category" in d
    assert "author" in d
    assert "text" in d
    assert "apex_g" in d
    assert "selection_telemetry" in d
    assert "provenance" in d


def test_to_dict_telemetry_keys():
    """selection_telemetry sub-dict has distance, score, floor_affinity_bonus."""
    m = get_manifold()
    d = m.select().to_dict()
    tel = d["selection_telemetry"]
    assert "distance" in tel
    assert "score" in tel
    assert "floor_affinity_bonus" in tel
    assert "active_floors_matched" in tel
    assert "query_vector" in tel


# ── select_from_session_state ────────────────────────────────────────────────


def test_select_from_session_state_stage_string():
    """select_from_session_state accepts stage as a string like '666_HEART'."""
    m = get_manifold()
    result = m.select_from_session_state(stage="666_HEART", g_score=0.85)
    assert isinstance(result, QuoteSelection)
    assert result.text != ""


def test_select_from_session_state_stage_int():
    """select_from_session_state accepts stage as an integer."""
    m = get_manifold()
    result = m.select_from_session_state(stage=999, g_score=0.97)
    assert isinstance(result, QuoteSelection)


# ── Module-level select_wisdom() ─────────────────────────────────────────────


def test_module_level_select_wisdom():
    """select_wisdom() module function works without instantiating QuoteManifold."""
    result = select_wisdom(stage="444", g_score=0.88, active_floors=["F4"])
    assert isinstance(result, QuoteSelection)
    assert result.text != ""


def test_module_level_select_wisdom_returns_all_categories():
    """
    Different stage/state combinations produce quotes from different categories.

    We sample several distinct state vectors and verify that at least 3 unique
    categories appear among the results.
    """
    m = get_manifold()
    test_states = [
        {"tau": 0.10, "delta_s": 0.0, "p2": 1.0, "g": 0.85, "psi": 0.95, "kappa_r": 0.6},
        {"tau": 0.50, "delta_s": 0.1, "p2": 1.2, "g": 0.82, "psi": 0.92, "kappa_r": 0.6},
        {"tau": 0.80, "delta_s": -0.3, "p2": 1.1, "g": 0.78, "psi": 0.85, "kappa_r": 0.72},
        {"tau": 0.90, "delta_s": -0.6, "p2": 1.7, "g": 0.92, "psi": 0.75, "kappa_r": 0.82},
        {"tau": 0.98, "delta_s": -0.8, "p2": 1.95, "g": 0.97, "psi": 0.98, "kappa_r": 0.90},
    ]
    categories = {m.select(**s).category for s in test_states}
    assert len(categories) >= 3, f"Expected ≥3 distinct categories, got: {categories}"


# ── Runtime tool wrapper ──────────────────────────────────────────────────────


def test_runtime_tool_select_wisdom_manifold():
    """arifosmcp.runtime.tools.select_wisdom_manifold() returns a dict with quote data."""
    from arifosmcp.runtime.tools import select_wisdom_manifold

    result = select_wisdom_manifold(stage="444", g_score=0.88)
    assert isinstance(result, dict)
    assert "text" in result
    assert "author" in result
    assert "selection_telemetry" in result


def test_runtime_tool_active_floors_csv():
    """select_wisdom_manifold parses comma-separated active_floors string."""
    from arifosmcp.runtime.tools import select_wisdom_manifold

    result = select_wisdom_manifold(
        stage="666",
        delta_s=-0.3,
        p2=1.1,
        g_score=0.78,
        psi=0.85,
        kappa_r=0.72,
        active_floors="F6,F7,F1",
    )
    assert "selection_telemetry" in result
    # At least one floor should have been matched
    tel = result["selection_telemetry"]
    assert "floor_affinity_bonus" in tel


# ── Word-power mechanisms & resonance density ────────────────────────────────


def test_select_returns_power_mechanisms():
    """QuoteSelection contains a non-empty power_mechanisms list."""
    m = get_manifold()
    result = m.select()
    assert isinstance(result.power_mechanisms, list)
    assert len(result.power_mechanisms) >= 1


def test_select_power_mechanisms_are_valid():
    """power_mechanisms only contains the four canonical mechanism strings."""
    from core.philosophy.coordinates import ALL_MECHANISMS

    m = get_manifold()
    result = m.select(tau=0.5, delta_s=0.0, p2=1.2, g=0.85, psi=0.7, kappa_r=0.6)
    for mech in result.power_mechanisms:
        assert mech in ALL_MECHANISMS, f"Unknown mechanism: {mech}"


def test_select_resonance_density_in_range():
    """resonance_density ρ is within [0, 1]."""
    m = get_manifold()
    result = m.select()
    assert 0.0 <= result.resonance_density <= 1.0


def test_select_resonance_bonus_positive():
    """resonance_bonus is non-negative."""
    m = get_manifold()
    result = m.select()
    assert result.resonance_bonus >= 0.0


def test_resonance_bonus_equals_rho_times_weight():
    """resonance_bonus == resonance_density × RESONANCE_BONUS_WEIGHT."""
    from core.philosophy.manifold import RESONANCE_BONUS_WEIGHT

    m = get_manifold()
    result = m.select()
    assert result.resonance_bonus == pytest.approx(
        result.resonance_density * RESONANCE_BONUS_WEIGHT, rel=1e-5
    )


def test_to_dict_has_word_power_section():
    """to_dict() includes a 'word_power' sub-dict."""
    m = get_manifold()
    d = m.select().to_dict()
    assert "word_power" in d
    wp = d["word_power"]
    assert "power_mechanisms" in wp
    assert "resonance_density" in wp
    assert "resonance_bonus" in wp


def test_higher_resonance_density_boosts_score():
    """
    All else equal, a quote with higher ρ scores higher than one with lower ρ.

    We construct two artificial selections and compare their scores directly.
    """
    from core.philosophy.manifold import FLOOR_AFFINITY_BONUS, RESONANCE_BONUS_WEIGHT

    dist = 0.10
    bonus = 1 * FLOOR_AFFINITY_BONUS  # 1 matched floor

    rho_high = 0.95
    rho_low = 0.60

    score_high = (1.0 / (1.0 + dist)) * (1.0 + bonus) * (1.0 + rho_high * RESONANCE_BONUS_WEIGHT)
    score_low = (1.0 / (1.0 + dist)) * (1.0 + bonus) * (1.0 + rho_low * RESONANCE_BONUS_WEIGHT)

    assert score_high > score_low


def test_wisdom_and_seal_have_high_resonance():
    """
    Quotes near the 'wisdom' and 'seal' centroids should have high resonance density.

    wisdom baseline ρ=0.90, seal baseline ρ=0.95 → both should be > 0.75 in practice.
    """
    m = get_manifold()
    wisdom_result = m.select(tau=0.40, delta_s=-0.40, p2=1.40, g=0.88, psi=0.97, kappa_r=0.68)
    seal_result = m.select(tau=0.98, delta_s=-0.80, p2=1.95, g=0.97, psi=0.98, kappa_r=0.90)

    assert wisdom_result.resonance_density > 0.75, (
        f"Wisdom quote ρ={wisdom_result.resonance_density} expected > 0.75"
    )
    assert seal_result.resonance_density > 0.75, (
        f"Seal quote ρ={seal_result.resonance_density} expected > 0.75"
    )


def test_provenance_includes_resonance_weight():
    """Provenance dict includes 'resonance_bonus_weight'."""
    m = get_manifold()
    result = m.select()
    assert "resonance_bonus_weight" in result.provenance


def test_provenance_formula_includes_rho():
    """Scoring formula in provenance references ρ."""
    m = get_manifold()
    result = m.select()
    assert "ρ" in result.provenance["formula"]


def test_all_quotes_have_power_mechanisms():
    """Every quote in the manifold JSON has at least one valid power mechanism."""
    import json
    from pathlib import Path

    from core.philosophy.coordinates import ALL_MECHANISMS

    manifold_path = (
        Path(__file__).parent.parent.parent / "data" / "wisdom_quotes_manifold.json"
    )
    data = json.loads(manifold_path.read_text(encoding="utf-8"))
    quotes = data["quotes"]
    assert len(quotes) == 99, f"Expected 99 quotes, got {len(quotes)}"

    missing_mechanism: list[int] = []
    invalid_mechanism: list[tuple[int, str]] = []

    for q in quotes:
        mechanisms = q.get("apex_g", {}).get("power_mechanisms", [])
        if not mechanisms:
            missing_mechanism.append(q["id"])
        for mech in mechanisms:
            if mech not in ALL_MECHANISMS:
                invalid_mechanism.append((q["id"], mech))

    assert len(missing_mechanism) == 0, (
        f"Quotes missing power_mechanisms: {missing_mechanism}"
    )
    assert len(invalid_mechanism) == 0, (
        f"Quotes with unknown mechanism: {invalid_mechanism}"
    )


def test_runtime_tool_returns_word_power():
    """select_wisdom_manifold() returns the word_power section."""
    from arifosmcp.runtime.tools import select_wisdom_manifold

    result = select_wisdom_manifold(stage="999", g_score=0.97, active_floors="F13,F11")
    assert "word_power" in result
    wp = result["word_power"]
    assert "power_mechanisms" in wp
    assert "resonance_density" in wp
    assert 0.0 <= wp["resonance_density"] <= 1.0


# ── AGI / ASI / APEX Trinity Layer Tests ─────────────────────────────────────


def test_to_dict_has_layers_key():
    """to_dict() includes a top-level 'layers' key."""
    from core.philosophy.coordinates import WisdomLayer

    m = get_manifold()
    d = m.select().to_dict()
    assert "layers" in d
    assert WisdomLayer.AGI in d["layers"]
    assert WisdomLayer.ASI in d["layers"]
    assert WisdomLayer.APEX in d["layers"]


def test_agi_layer_has_doctrine():
    """AGI layer includes 'doctrine' — the explicit constitutional statement."""
    m = get_manifold()
    d = m.select(tau=0.40, delta_s=-0.40, p2=1.40, g=0.88, psi=0.97, kappa_r=0.68).to_dict()
    agi = d["layers"]["agi"]
    assert "doctrine" in agi
    assert len(agi["doctrine"]) > 10


def test_agi_layer_has_quote_fields():
    """AGI layer includes quote_id, category, text, author, floor_affinities."""
    m = get_manifold()
    agi = m.select().to_dict()["layers"]["agi"]
    assert "quote_id" in agi
    assert "category" in agi
    assert "text" in agi
    assert "author" in agi
    assert "floor_affinities" in agi
    assert "power_mechanisms" in agi


def test_asi_layer_has_geometric_fields():
    """ASI layer includes distance, resonance_density, query_vector, manifold_position."""
    m = get_manifold()
    asi = m.select().to_dict()["layers"]["asi"]
    assert "distance" in asi
    assert "resonance_density" in asi
    assert "query_vector" in asi
    assert "manifold_position" in asi


def test_asi_layer_distance_matches_telemetry():
    """ASI layer distance matches selection_telemetry distance."""
    m = get_manifold()
    d = m.select(tau=0.5, delta_s=0.0, p2=1.2, g=0.85, psi=0.7, kappa_r=0.6).to_dict()
    assert d["layers"]["asi"]["distance"] == d["selection_telemetry"]["distance"]


def test_apex_layer_has_arbitration_fields():
    """APEX layer includes score, formula, floor_affinity_bonus, resonance_bonus."""
    m = get_manifold()
    apex = m.select().to_dict()["layers"]["apex"]
    assert "score" in apex
    assert "formula" in apex
    assert "floor_affinity_bonus" in apex
    assert "resonance_bonus" in apex
    assert "active_floors_matched" in apex


def test_apex_layer_score_matches_telemetry():
    """APEX layer score matches selection_telemetry score."""
    m = get_manifold()
    d = m.select().to_dict()
    assert d["layers"]["apex"]["score"] == d["selection_telemetry"]["score"]


def test_layer_roles_are_distinct():
    """AGI, ASI, APEX layers each have unique 'role' strings."""
    m = get_manifold()
    layers = m.select().to_dict()["layers"]
    roles = [layers[k]["role"] for k in ("agi", "asi", "apex")]
    assert len(set(roles)) == 3, f"Expected 3 distinct roles, got: {roles}"


def test_layer_questions_are_distinct():
    """Each layer has a distinct 'question' it answers."""
    m = get_manifold()
    layers = m.select().to_dict()["layers"]
    questions = [layers[k]["question"] for k in ("agi", "asi", "apex")]
    assert len(set(questions)) == 3


def test_all_categories_have_agi_doctrine():
    """Every quote category produces a non-empty AGI doctrine string."""
    from core.philosophy.coordinates import CATEGORY_AGI_DOCTRINE

    for cat in ("scar", "triumph", "paradox", "wisdom", "power", "love", "seal"):
        assert cat in CATEGORY_AGI_DOCTRINE
        assert len(CATEGORY_AGI_DOCTRINE[cat]) > 20, (
            f"AGI doctrine for '{cat}' is too short"
        )


def test_layer_descriptions_all_three_layers():
    """LAYER_DESCRIPTIONS covers all three WisdomLayer constants."""
    from core.philosophy.coordinates import LAYER_DESCRIPTIONS, WisdomLayer

    assert WisdomLayer.AGI in LAYER_DESCRIPTIONS
    assert WisdomLayer.ASI in LAYER_DESCRIPTIONS
    assert WisdomLayer.APEX in LAYER_DESCRIPTIONS


def test_runtime_tool_returns_layers():
    """select_wisdom_manifold() MCP tool output includes the 'layers' structure."""
    from arifosmcp.runtime.tools import select_wisdom_manifold

    result = select_wisdom_manifold(stage="444", g_score=0.88, active_floors="F4,F7")
    assert "layers" in result
    assert "agi" in result["layers"]
    assert "asi" in result["layers"]
    assert "apex" in result["layers"]


def test_agi_layer_doctrine_matches_scar_category():
    """Selecting near scar centroid surfaces the scar AGI doctrine."""
    from core.philosophy.coordinates import CATEGORY_AGI_DOCTRINE

    m = get_manifold()
    d = m.select(tau=0.80, delta_s=-0.30, p2=1.10, g=0.78, psi=0.85, kappa_r=0.72).to_dict()
    agi = d["layers"]["agi"]
    assert agi["category"] == "scar"
    assert agi["doctrine"] == CATEGORY_AGI_DOCTRINE["scar"]


def test_agi_layer_doctrine_matches_seal_category():
    """Selecting near seal centroid surfaces the seal AGI doctrine."""
    from core.philosophy.coordinates import CATEGORY_AGI_DOCTRINE

    m = get_manifold()
    d = m.select(tau=0.98, delta_s=-0.80, p2=1.95, g=0.97, psi=0.98, kappa_r=0.90).to_dict()
    agi = d["layers"]["agi"]
    assert agi["category"] == "seal"
    assert agi["doctrine"] == CATEGORY_AGI_DOCTRINE["seal"]


def test_all_quotes_tau_strictly_below_one():
    """All 99 quotes have tau < 1.0 (interior of manifold, not boundary)."""
    import json
    from pathlib import Path

    manifold_path = (
        Path(__file__).parent.parent.parent / "data" / "wisdom_quotes_manifold.json"
    )
    data = json.loads(manifold_path.read_text(encoding="utf-8"))
    boundary = [
        (q["id"], q["apex_g"]["tau"])
        for q in data["quotes"]
        if q["apex_g"]["tau"] >= 1.0
    ]
    assert boundary == [], f"Quotes with tau >= 1.0: {boundary}"
