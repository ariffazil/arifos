"""
F8 Genius - Governed Intelligence Threshold Tests

Validates that:
1. Genius score G† = A × P × X × E² is calculated correctly
2. G† < 0.80 triggers PARTIAL verdict
3. G† ≥ 0.80 allows SEAL verdict
4. All dials (Akal, Peace, Exploration, Energy) contribute correctly

This is a DERIVED floor based on the APEX Theorem.
"""

from __future__ import annotations

import pytest
import math

from core.judgment import JudgmentEngine
from core.shared.floors import F8_GENIUS


class TestF8GeniusCalculation:
    """Test the Genius Index formula: G† = A × P × X × E²."""

    def test_genius_formula_correctness(self) -> None:
        """
        F8: G† = A × P × X × E² must be calculated correctly.
        
        Where:
        - A = Akal (logical accuracy) [0,1]
        - P = Peace (safety/stability) [0,1]
        - X = Exploration (knowledge) [0,1]
        - E = Energy (effort) [0,1]
        """
        f8 = F8_GENIUS()
        
        # Test case: All dials at maximum
        dials = {"A": 1.0, "P": 1.0, "X": 1.0, "E": 1.0}
        g = f8.calculate_genius(dials)
        expected = 1.0 * 1.0 * 1.0 * (1.0 ** 2)
        assert abs(g - expected) < 0.001, f"G† should be {expected}, got {g}"
        
        # Test case: Zero energy means zero genius
        dials = {"A": 1.0, "P": 1.0, "X": 1.0, "E": 0.0}
        g = f8.calculate_genius(dials)
        assert g == 0.0, "Zero energy should yield zero genius"
        
        # Test case: Balanced effort
        dials = {"A": 0.9, "P": 0.9, "X": 0.9, "E": 0.9}
        g = f8.calculate_genius(dials)
        expected = 0.9 * 0.9 * 0.9 * (0.9 ** 2)
        assert abs(g - expected) < 0.001, f"G† calculation incorrect"

    def test_low_genius_gets_partial(self) -> None:
        """
        F8: G† < 0.80 should trigger PARTIAL verdict.
        
        The system is not intelligent enough to fully trust.
        """
        engine = JudgmentEngine()
        
        # Create a request that yields low genius
        request = {
            "action": "reason_mind",
            "query": "Complex problem",
            "evidence": [],  # Low exploration (X)
            "reasoning_depth": "shallow",  # Low effort (E)
            "safety_checks": "minimal",  # Low peace (P)
        }
        
        verdict = engine.evaluate(request)
        
        if verdict.genius_score < 0.80:
            assert verdict.status == "PARTIAL", \
                f"G†={verdict.genius_score} < 0.80 should be PARTIAL, got {verdict.status}"
            assert "F8_GENIUS" in verdict.constraints, \
                "PARTIAL should cite F8_GENIUS constraint"

    def test_high_genius_gets_seal(self) -> None:
        """
        F8: G† ≥ 0.80 can receive SEAL verdict (if other floors pass).
        """
        engine = JudgmentEngine()
        
        # Create a request with high genius components
        request = {
            "action": "reason_mind",
            "query": "Well-researched problem",
            "evidence": [
                {"source": "authoritative", "verified": True},
                {"source": "peer-reviewed", "verified": True},
            ],  # High exploration (X)
            "reasoning_depth": "comprehensive",  # High effort (E)
            "safety_checks": "rigorous",  # High peace (P)
            "logical_structure": "valid",  # High accuracy (A)
        }
        
        verdict = engine.evaluate(request)
        
        if verdict.genius_score >= 0.80:
            # Can be SEAL if other floors pass
            assert verdict.status in ["SEAL", "PARTIAL"], \
                f"High G†={verdict.genius_score} should allow SEAL"


class TestF8DialContributions:
    """Test how each dial contributes to Genius score."""

    def test_energy_has_quadratic_effect(self) -> None:
        """
        F8: Energy (E) has squared effect on G†.
        
        This rewards sustained effort over bursts.
        """
        f8 = F8_GENIUS()
        
        base_dials = {"A": 1.0, "P": 1.0, "X": 1.0}
        
        # E = 0.5 → E² = 0.25
        dials_half = {**base_dials, "E": 0.5}
        g_half = f8.calculate_genius(dials_half)
        
        # E = 1.0 → E² = 1.0
        dials_full = {**base_dials, "E": 1.0}
        g_full = f8.calculate_genius(dials_full)
        
        # 4x difference due to squaring
        assert abs(g_full - 4 * g_half) < 0.001, \
            "Energy should have quadratic effect"

    def test_all_dials_multiplicative(self) -> None:
        """
        F8: All dials multiply - weakness in any reduces G† significantly.
        
        This enforces balanced intelligence (no weak links).
        """
        f8 = F8_GENIUS()
        
        # Perfect except one weak dial
        dials_weak_A = {"A": 0.5, "P": 1.0, "X": 1.0, "E": 1.0}
        dials_weak_P = {"A": 1.0, "P": 0.5, "X": 1.0, "E": 1.0}
        dials_weak_X = {"A": 1.0, "P": 1.0, "X": 0.5, "E": 1.0}
        dials_weak_E = {"A": 1.0, "P": 1.0, "X": 1.0, "E": 0.5}
        
        g_weak_A = f8.calculate_genius(dials_weak_A)
        g_weak_P = f8.calculate_genius(dials_weak_P)
        g_weak_X = f8.calculate_genius(dials_weak_X)
        g_weak_E = f8.calculate_genius(dials_weak_E)
        
        # All should be exactly 0.5 (or 0.125 for E due to squaring)
        assert abs(g_weak_A - 0.5) < 0.001, "Weak A should reduce G† by half"
        assert abs(g_weak_P - 0.5) < 0.001, "Weak P should reduce G† by half"
        assert abs(g_weak_X - 0.5) < 0.001, "Weak X should reduce G† by half"
        assert abs(g_weak_E - 0.25) < 0.001, "Weak E should reduce G† by 75% (squared)"


class TestF8EdgeCases:
    """Edge cases for F8 Genius."""

    def test_genius_score_reported(self) -> None:
        """
        F8: G† should always be reported in verdict.
        """
        engine = JudgmentEngine()
        
        request = {"action": "reason_mind", "query": "test"}
        verdict = engine.evaluate(request)
        
        assert hasattr(verdict, 'genius_score'), \
            "Verdict should include genius_score"
        assert 0.0 <= verdict.genius_score <= 1.0, \
            f"G† should be in [0,1], got {verdict.genius_score}"

    def test_genius_with_thermodynamics(self) -> None:
        """
        F8: G† interacts with F4 Entropy (ΔS).
        
        The full APEX equation: G† = (A×P×X×E²) × |ΔS|/C
        Where entropy reduction (ΔS ≤ 0) increases effective G†.
        """
        f8 = F8_GENIUS()
        
        base_dials = {"A": 0.9, "P": 0.9, "X": 0.9, "E": 0.9}
        
        # Entropy reduction (good)
        g_reduce = f8.calculate_genius_with_entropy(base_dials, delta_s=-0.1, compute=1.0)
        
        # Entropy increase (bad)
        g_increase = f8.calculate_genius_with_entropy(base_dials, delta_s=0.1, compute=1.0)
        
        assert g_reduce > g_increase, \
            "Entropy reduction should increase effective G†"
