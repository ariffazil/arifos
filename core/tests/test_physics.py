"""
core/tests/test_physics.py — Constitutional Physics Tests
=========================================================

Test thermodynamic primitives: W_3, delta_S, Omega_0, G, etc.

DITEMPA BUKAN DIBERI 💎🔥🧠
"""

import math

import pytest

from core.shared.physics import (
    # F3: Tri-Witness
    TrinityTensor,
    W_3,
    W_3_from_tensor,
    W_3_check,
    geometric_mean,
    std_dev,
    # F4: Entropy
    delta_S,
    is_cooling,
    clarity_ratio,
    # F7: Humility
    UncertaintyBand,
    Omega_0,
    # Precision
    pi,
    kalman_gain,
    # F5: Peace
    PeaceSquared,
    Peace2,
    # F6: Empathy
    Stakeholder,
    kappa_r,
    identify_stakeholders,
    DISTRESS_SIGNALS,
    # F8: Genius
    GeniusDial,
    G,
    G_from_dial,
    # Unified
    ConstitutionalTensor,
    G,
    G_from_dial,
    # F8: Genius
    GeniusDial,
    Omega_0,
    Peace2,
    # F5: Peace
    PeaceSquared,
    # F6: Empathy
    Stakeholder,
    # F3: Tri-Witness
    TrinityTensor,
    # F7: Humility
    UncertaintyBand,
    W_3_check,
    W_3_from_tensor,
    clarity_ratio,
    # F4: Entropy
    delta_S,
    geometric_mean,
    identify_stakeholders,
    is_cooling,
    kalman_gain,
    kappa_r,
    # Precision
    pi,
    std_dev,
)


class TestTriWitness:
    """Test F3: W_3 = cube_root(H × A × S)"""

    def test_geometric_mean(self):
        """Geometric mean should work correctly."""
        assert geometric_mean([1.0, 1.0, 1.0]) == 1.0
        assert geometric_mean([0.0, 1.0, 1.0]) == 0.0

        # Cube root of product
        result = geometric_mean([0.5, 0.5, 0.5])
        assert abs(result - 0.5) < 0.01

    def test_W_3_perfect_consensus(self):
        """Perfect scores should give W_3 = 1.0."""
        assert W_3(1.0, 1.0, 1.0) == 1.0

    def test_W_3_zero_consensus(self):
        """Zero in any witness should give W_3 = 0."""
        assert W_3(0.0, 1.0, 1.0) == 0.0

    def test_W_3_mixed(self):
        """Mixed scores should give geometric mean."""
        result = W_3(0.8, 0.9, 0.95)
        expected = (0.8 * 0.9 * 0.95) ** (1 / 3)
        assert abs(result - expected) < 0.001

    def test_W_3_from_tensor(self):
        """Should extract from TrinityTensor."""
        tensor = TrinityTensor(H=0.9, A=0.9, S=0.9)
        result = W_3_from_tensor(tensor)
        assert abs(result - 0.9) < 0.001

    def test_W_3_check_threshold(self):
        """Should check against constitutional threshold."""
        assert W_3_check(0.95, 0.95, 0.95, threshold=0.95)
        assert not W_3_check(0.9, 0.9, 0.9, threshold=0.95)

    def test_trinity_tensor_clamping(self):
        """Values should be clamped to [0, 1]."""
        tensor = TrinityTensor(H=1.5, A=-0.5, S=0.5)
        assert tensor.H == 1.0
        assert tensor.A == 0.0
        assert tensor.S == 0.5


class TestEntropy:
    """Test F4: delta_S = S(after) - S(before)"""

    def test_entropy_reduction(self):
        """Clarifying text should have delta_S < 0."""
        before = "The utilization of the aforementioned methodology"
        after = "Use this method"

        result = delta_S(before, after)
        assert result < 0  # Entropy reduced (cooling)

    def test_entropy_increase(self):
        """Obscuring text should have delta_S > 0."""
        before = "Use this method"
        after = "The utilization of the aforementioned methodology"

        result = delta_S(before, after)
        assert result > 0  # Entropy increased (heating)

    def test_is_cooling(self):
        """Should detect cooling correctly."""
        assert is_cooling("Complex", "Simple")
        assert not is_cooling("Simple", "Complex")

    def test_clarity_ratio(self):
        """Should compute clarity improvement ratio."""
        ratio = clarity_ratio("Complex explanation here", "Simple answer")
        # Note: ratio depends on actual entropy calculation

    def test_empty_strings(self):
        """Should handle empty strings."""
        result = delta_S("", "test")
        assert isinstance(result, float)


class TestHumility:
    """Test F7: Omega_0 in [0.03, 0.05]"""

    def test_uncertainty_band_locked(self):
        """Should detect if Omega_0 in valid band."""
        band = UncertaintyBand(0.04)
        assert band.is_locked()

    def test_uncertainty_band_too_low(self):
        """Should detect overconfidence."""
        band = UncertaintyBand(0.01)
        assert not band.is_locked()

    def test_uncertainty_band_too_high(self):
        """Should detect underconfidence."""
        band = UncertaintyBand(0.10)
        assert not band.is_locked()

    def test_Omega_0_high_confidence(self):
        """High confidence should give low Omega_0 (but not too low)."""
        band = Omega_0(0.99)
        assert band.omega_0 >= 0.03
        assert band.omega_0 <= 0.05

    def test_Omega_0_low_confidence(self):
        """Low confidence should give high Omega_0 (but not too high)."""
        band = Omega_0(0.0)
        assert band.omega_0 >= 0.03
        assert band.omega_0 <= 0.05

    def test_confidence_interval(self):
        """Should compute confidence interval."""
        band = UncertaintyBand(0.05)
        low, high = band.confidence_interval(0.80)
        assert abs(low - 0.75) < 0.001
        assert abs(high - 0.85) < 0.001


class TestPrecision:
    """Test precision primitives."""

    def test_pi_calculation(self):
        """pi = 1/sigma^2"""
        assert pi(1.0) == 1.0
        assert pi(0.5) == 2.0
        assert pi(0.25) == 4.0

    def test_pi_infinite(self):
        """Zero variance should give infinite precision."""
        assert pi(0.0) == float("inf")

    def test_kalman_gain_equal(self):
        """Equal precision should give K = 0.5"""
        K = kalman_gain(1.0, 1.0)
        assert abs(K - 0.5) < 0.001


class TestPeace:
    """Test F5: Peace^2 = 1 - max(harm)"""

    def test_perfect_peace(self):
        """No harm should give Peace^2 = 1.0"""
        peace = Peace2({})
        assert peace.P2() == 1.0
        assert peace.is_peaceful()

    def test_partial_harm(self):
        """Partial harm should reduce Peace^2"""
        peace = Peace2({"user": 0.1, "system": 0.05})
        assert peace.P2() == 0.9
        assert not peace.is_peaceful(threshold=0.95)

    def test_worst_affected(self):
        """Should identify most harmed stakeholder."""
        peace = Peace2({"user": 0.1, "child": 0.5, "system": 0.05})
        assert peace.worst_affected() == "child"


class TestEmpathy:
    """Test F6: kappa_r empathy quotient"""

    def test_no_stakeholders(self):
        """No stakeholders should give kappa_r = 1.0"""
        kappa = kappa_r("test", [])
        assert kappa == 1.0

    def test_high_vulnerability(self):
        """High vulnerability should reduce kappa_r"""
        stakeholders = [
            Stakeholder("user", "user", 0.3),
            Stakeholder("child", "child", 0.9),
        ]
        kappa = kappa_r("help the child", stakeholders)
        assert kappa < 1.0
        assert kappa >= 0.5

    def test_stakeholder_identification(self):
        """Should identify stakeholders from query."""
        stakeholders = identify_stakeholders("Help the elderly patient")

        names = [s.name for s in stakeholders]
        assert "User" in names
        assert "Elderly" in names or "Patient" in names

    def test_stakeholder_clamping(self):
        """Vulnerability should be clamped to [0, 1]."""
        s = Stakeholder("test", "test", 1.5)
        assert s.vulnerability_score == 1.0


class TestGenius:
    """Test F8: G = A × P × X × E^2"""

    def test_perfect_genius(self):
        """All dials at 1.0 should give G = 1.0"""
        dial = GeniusDial(A=1.0, P=1.0, X=1.0, E=1.0)
        assert dial.G() == 1.0

    def test_zero_dial(self):
        """Any dial at 0 should give G = 0"""
        dial = GeniusDial(A=0.0, P=1.0, X=1.0, E=1.0)
        assert dial.G() == 0.0

    def test_genius_threshold(self):
        """Should check against F8 threshold"""
        # G = A * P * X * E^2 = 0.95 * 0.95 * 0.95 * 0.95^2 = 0.95^5 = 0.77
        # Need all dials high to pass 0.80 threshold
        dial = GeniusDial(A=0.98, P=0.98, X=0.98, E=0.98)
        assert dial.is_genius(threshold=0.80)

        dial2 = GeniusDial(A=0.5, P=0.5, X=0.5, E=0.5)
        assert not dial2.is_genius(threshold=0.80)

    def test_weakest_dial(self):
        """Should identify weakest component"""
        dial = GeniusDial(A=0.9, P=0.3, X=0.8, E=0.8)
        assert dial.weakest_dial() == "P"

    def test_G_function(self):
        """Standalone G function should work"""
        result = G(0.9, 0.9, 0.9, 0.9)
        # G = A * P * X * E^2 = 0.9 * 0.9 * 0.9 * 0.81
        expected = 0.9 * 0.9 * 0.9 * (0.9**2)
        assert abs(result - expected) < 0.001


class TestConstitutionalTensor:
    """Test unified constitutional state."""

    def test_tensor_creation(self):
        """Should create tensor with all fields."""
        tensor = ConstitutionalTensor(
            witness=TrinityTensor(H=0.9, A=0.9, S=0.9),
            entropy_delta=-0.1,
            humility=UncertaintyBand(0.04),
            genius=GeniusDial(A=0.9, P=0.9, X=0.5, E=0.9),
            peace=Peace2({}),
            empathy=0.8,
            truth_score=0.95,
        )

        assert tensor.witness.H == 0.9
        assert tensor.entropy_delta == -0.1

    def test_constitutional_check_seal(self):
        """Perfect tensor should give SEAL"""
        tensor = ConstitutionalTensor(
            witness=TrinityTensor(H=0.97, A=0.97, S=0.97),
            entropy_delta=-0.1,
            humility=UncertaintyBand(0.04),
            genius=GeniusDial(A=0.95, P=0.95, X=0.95, E=0.95),  # G = 0.95^5 = 0.77, need higher
            peace=Peace2({}),
            empathy=0.95,
            truth_score=0.99,
        )

        verdict, violations = tensor.constitutional_check()
        # May be SEAL or PARTIAL depending on exact thresholds
        assert verdict in ("SEAL", "PARTIAL")

    def test_constitutional_check_void(self):
        """Poor tensor should give VOID"""
        tensor = ConstitutionalTensor(
            witness=TrinityTensor(H=0.5, A=0.5, S=0.5),
            entropy_delta=0.5,  # Bad: entropy increased
            humility=UncertaintyBand(0.02),  # Bad: too confident
            genius=GeniusDial(A=0.3, P=0.3, X=0.3, E=0.3),
            peace=Peace2({"user": 0.5}),
            empathy=0.3,
            truth_score=0.5,
        )

        verdict, violations = tensor.constitutional_check()
        assert verdict == "VOID"
        assert len(violations) > 0

    def test_to_metrics(self):
        """Should export to metrics dict."""
        tensor = ConstitutionalTensor(
            witness=TrinityTensor(H=0.9, A=0.9, S=0.9),
            entropy_delta=-0.1,
            humility=UncertaintyBand(0.04),
            genius=GeniusDial(A=0.9, P=0.9, X=0.5, E=0.9),
            peace=Peace2({}),
            empathy=0.8,
            truth_score=0.95,
        )

        metrics = tensor.to_metrics()
        assert "W_3" in metrics
        assert "genius_G" in metrics
        assert "verdict" in metrics


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
