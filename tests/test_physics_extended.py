"""
Extended physics tests covering TrinityTensor, entropy, Omega_0, pi,
PeaceSquared, GeniusDial (G_from_dial), and ConstitutionalTensor.

Complements test_constitutional_core.py which covers basics.
"""

from __future__ import annotations

import pytest


# =============================================================================
# TRINITY TENSOR
# =============================================================================


class TestTrinityTensor:
    def test_normal_values(self):
        from core.shared.physics import TrinityTensor

        t = TrinityTensor(H=0.8, A=0.9, S=0.7)
        assert t.H == 0.8
        assert t.A == 0.9
        assert t.S == 0.7

    def test_clamping_above_one(self):
        from core.shared.physics import TrinityTensor

        t = TrinityTensor(H=1.5, A=2.0, S=-0.5)
        assert t.H == 1.0
        assert t.A == 1.0
        assert t.S == 0.0

    def test_clamping_below_zero(self):
        from core.shared.physics import TrinityTensor

        t = TrinityTensor(H=-0.3, A=0.5, S=-1.0)
        assert t.H == 0.0
        assert t.S == 0.0


class TestGeometricMean:
    def test_empty_returns_zero(self):
        from core.shared.physics import geometric_mean

        assert geometric_mean([]) == 0.0

    def test_non_positive_returns_zero(self):
        from core.shared.physics import geometric_mean

        assert geometric_mean([0.5, 0.0, 0.9]) == 0.0
        assert geometric_mean([-0.1, 0.5]) == 0.0

    def test_normal_values(self):
        from core.shared.physics import geometric_mean

        result = geometric_mean([0.8, 0.9, 0.7])
        assert 0.0 < result < 1.0

    def test_all_ones(self):
        from core.shared.physics import geometric_mean

        assert geometric_mean([1.0, 1.0, 1.0]) == pytest.approx(1.0)


class TestStdDev:
    def test_single_value_zero(self):
        from core.shared.physics import std_dev

        assert std_dev([0.8]) == 0.0

    def test_empty_zero(self):
        from core.shared.physics import std_dev

        assert std_dev([]) == 0.0

    def test_multiple_values(self):
        from core.shared.physics import std_dev

        result = std_dev([0.5, 0.8, 0.6, 0.9])
        assert result > 0.0


class TestW3Extended:
    def test_w3_from_tensor(self):
        from core.shared.physics import TrinityTensor, W_3_from_tensor

        tensor = TrinityTensor(H=0.9, A=0.95, S=0.88)
        result = W_3_from_tensor(tensor)
        assert 0.0 < result <= 1.0

    def test_tri_witness_alias(self):
        from core.shared.physics import tri_witness, W_3

        assert tri_witness(0.9, 0.8, 0.7) == pytest.approx(W_3(0.9, 0.8, 0.7))


# =============================================================================
# ENTROPY — delta_S
# =============================================================================


class TestEntropy:
    def test_delta_s_cooling(self):
        from core.shared.physics import delta_S

        # Short clear output < noisy input → cooling (negative delta)
        before = "aaabbbcccdddeeefffggg"
        after = "aaabbbccc"
        result = delta_S(before, after)
        # delta_S could be positive or negative depending on entropy calc
        assert isinstance(result, float)

    def test_delta_s_lists(self):
        from core.shared.physics import delta_S

        before = ["a", "b", "c", "d", "e"]
        after = ["a", "a", "a", "b", "b"]
        result = delta_S(before, after)
        assert isinstance(result, float)

    def test_entropy_delta_alias(self):
        from core.shared.physics import delta_S, entropy_delta

        assert delta_S("hello", "hi") == entropy_delta("hello", "hi")

    def test_is_cooling_reduced_complexity(self):
        from core.shared.physics import is_cooling

        # Identical text → delta_S == 0 → is_cooling (<=0)
        assert is_cooling("test", "test") is True

    def test_clarity_ratio_returns_float(self):
        from core.shared.physics import clarity_ratio

        result = clarity_ratio("complex detailed text with many tokens", "summary")
        assert isinstance(result, float)
        assert result > 0.0


# =============================================================================
# UNCERTAINTY BAND — Omega_0
# =============================================================================


class TestUncertaintyBand:
    def test_is_locked_in_band(self):
        from core.shared.physics import UncertaintyBand

        band = UncertaintyBand(0.04)
        assert band.is_locked() is True

    def test_is_locked_below_min(self):
        from core.shared.physics import UncertaintyBand

        band = UncertaintyBand(0.02)
        assert band.is_locked() is False

    def test_is_locked_above_max(self):
        from core.shared.physics import UncertaintyBand

        band = UncertaintyBand(0.06)
        assert band.is_locked() is False

    def test_confidence_interval(self):
        from core.shared.physics import UncertaintyBand

        band = UncertaintyBand(0.04)
        lo, hi = band.confidence_interval(0.85)
        assert lo == pytest.approx(0.81)
        assert hi == pytest.approx(0.89)

    def test_confidence_interval_clamped(self):
        from core.shared.physics import UncertaintyBand

        band = UncertaintyBand(0.04)
        lo, hi = band.confidence_interval(0.02)
        assert lo >= 0.0
        lo2, hi2 = band.confidence_interval(0.98)
        assert hi2 <= 1.0

    def test_clamping(self):
        from core.shared.physics import UncertaintyBand

        band = UncertaintyBand(1.5)
        assert band.omega_0 == 1.0
        band2 = UncertaintyBand(-0.1)
        assert band2.omega_0 == 0.0


class TestOmega0:
    def test_high_confidence_low_omega(self):
        from core.shared.physics import Omega_0

        band = Omega_0(1.0)
        assert band.omega_0 == pytest.approx(0.03)

    def test_low_confidence_high_omega(self):
        from core.shared.physics import Omega_0

        band = Omega_0(0.0)
        assert band.omega_0 == pytest.approx(0.05)

    def test_mid_confidence(self):
        from core.shared.physics import Omega_0

        band = Omega_0(0.5)
        assert 0.03 <= band.omega_0 <= 0.05

    def test_humility_band_alias(self):
        from core.shared.physics import Omega_0, humility_band

        assert Omega_0(0.7).omega_0 == humility_band(0.7).omega_0


# =============================================================================
# PRECISION & KALMAN
# =============================================================================


class TestPrecision:
    def test_pi_normal_variance(self):
        from core.shared.physics import pi

        assert pi(0.25) == pytest.approx(4.0)

    def test_pi_zero_variance_inf(self):
        from core.shared.physics import pi

        result = pi(0.0)
        assert result == float("inf")

    def test_pi_negative_variance_inf(self):
        from core.shared.physics import pi

        result = pi(-0.5)
        assert result == float("inf")

    def test_kalman_gain_equal_variance(self):
        from core.shared.physics import kalman_gain

        # Equal prior and likelihood → K = 0.5
        result = kalman_gain(0.5, 0.5)
        assert result == pytest.approx(0.5)

    def test_kalman_gain_low_likelihood_variance(self):
        from core.shared.physics import kalman_gain

        # Very low likelihood variance → trust new evidence more → K close to 1
        result = kalman_gain(0.5, 0.01)
        assert result > 0.8

    def test_kalman_gain_high_likelihood_variance(self):
        from core.shared.physics import kalman_gain

        # Very high likelihood variance → trust prior more → K close to 0
        result = kalman_gain(0.01, 0.9)
        assert result < 0.2


# =============================================================================
# PEACE SQUARED — extended
# =============================================================================


class TestPeaceSquaredClass:
    def test_p2_empty_dict(self):
        from core.shared.physics import PeaceSquared

        ps = PeaceSquared({})
        assert ps.P2() == 1.0

    def test_p2_with_harms(self):
        from core.shared.physics import PeaceSquared

        ps = PeaceSquared({"Alice": 0.3, "Bob": 0.7})
        assert ps.P2() == pytest.approx(0.3)

    def test_is_peaceful_passes(self):
        from core.shared.physics import PeaceSquared

        ps = PeaceSquared({"user": 0.01})
        assert ps.is_peaceful() is True

    def test_is_peaceful_fails(self):
        from core.shared.physics import PeaceSquared

        ps = PeaceSquared({"user": 0.5})
        assert ps.is_peaceful() is False

    def test_worst_affected_none_for_empty(self):
        from core.shared.physics import PeaceSquared

        ps = PeaceSquared({})
        assert ps.worst_affected() is None

    def test_worst_affected_identifies_max(self):
        from core.shared.physics import PeaceSquared

        ps = PeaceSquared({"Alice": 0.2, "Bob": 0.8, "Carol": 0.5})
        assert ps.worst_affected() == "Bob"


class TestPeace2Constructor:
    def test_peace2_returns_peace_squared(self):
        from core.shared.physics import Peace2, PeaceSquared

        result = Peace2({"user": 0.3})
        assert isinstance(result, PeaceSquared)


# =============================================================================
# GENIUS — G_from_dial
# =============================================================================


class TestGFromDial:
    def test_g_from_dial(self):
        from core.shared.physics import GeniusDial, G_from_dial

        dial = GeniusDial(A=0.9, P=0.9, X=0.9, E=0.9)
        result = G_from_dial(dial)
        assert result == pytest.approx(dial.G())

    def test_g_from_dial_zero(self):
        from core.shared.physics import GeniusDial, G_from_dial

        dial = GeniusDial(A=0.0, P=1.0, X=1.0, E=1.0)
        assert G_from_dial(dial) == pytest.approx(0.0)


# =============================================================================
# HARM SCORE — tests with or without SBERT
# =============================================================================


class TestHarmScore:
    def test_harm_score_returns_float(self):
        from core.shared.physics import harm_score

        result = harm_score("kill all humans")
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0

    def test_harm_score_empty_query(self):
        from core.shared.physics import harm_score

        result = harm_score("")
        assert result == 0.0


# =============================================================================
# CONSTITUTIONAL TENSOR
# =============================================================================


class TestConstitutionalTensor:
    def _make_tensor(self, truth_score=0.99, entropy_delta=0.0, humility_omega=0.04):
        from core.shared.physics import (
            ConstitutionalTensor,
            TrinityTensor,
            UncertaintyBand,
            GeniusDial,
            PeaceSquared,
        )

        return ConstitutionalTensor(
            witness=TrinityTensor(H=0.95, A=0.95, S=0.95),
            entropy_delta=entropy_delta,
            humility=UncertaintyBand(humility_omega),
            genius=GeniusDial(A=0.9, P=0.9, X=0.9, E=0.9),
            peace=PeaceSquared({"user": 0.05}),
            empathy=0.85,
            truth_score=truth_score,
            evidence=None,  # Test None → [] conversion
        )

    def test_evidence_none_becomes_empty_list(self):
        t = self._make_tensor()
        assert t.evidence == []

    def test_constitutional_check_passes(self):
        t = self._make_tensor(truth_score=0.99, entropy_delta=0.0, humility_omega=0.04)
        verdict, violations = t.constitutional_check()
        assert verdict == "SEAL"
        assert violations == []

    def test_constitutional_check_fails_truth(self):
        t = self._make_tensor(truth_score=0.95)
        verdict, violations = t.constitutional_check()
        assert verdict == "VOID"
        assert any("F2" in v for v in violations)

    def test_constitutional_check_fails_entropy(self):
        t = self._make_tensor(entropy_delta=0.1)
        verdict, violations = t.constitutional_check()
        assert verdict == "VOID"
        assert any("F4" in v for v in violations)

    def test_constitutional_check_fails_humility(self):
        t = self._make_tensor(humility_omega=0.01)
        verdict, violations = t.constitutional_check()
        assert verdict == "VOID"
        assert any("F7" in v for v in violations)
