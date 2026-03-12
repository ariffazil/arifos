"""
F7 Humility - Gödel Uncertainty Band Tests

Validates that:
1. Confidence outside [0.03, 0.05] triggers VOID
2. Overconfidence (> 0.05) is rejected
3. Underconfidence (< 0.03) is rejected
4. Proper humility band [0.03, 0.05] is accepted

This is a HARD floor enforced by the Gödel Lock.
"""

from __future__ import annotations

import pytest

from core.judgment import JudgmentEngine
from core.shared.floors import F7_HUMILITY


class TestF7HumilityBand:
    """Test the Gödel Uncertainty Band [0.03, 0.05]."""

    @pytest.mark.parametrize("confidence", [0.0, 0.01, 0.02, 0.029])
    def test_underconfidence_rejected(self, confidence: float) -> None:
        """
        F7 HARD: Confidence < 0.03 is underconfidence (VOID).
        
        The system must acknowledge what it knows.
        Refusing to commit (confidence ~0) is epistemic cowardice.
        """
        engine = JudgmentEngine()
        
        request = {
            "action": "reason_mind",
            "query": "What is 2+2?",
            "confidence": confidence,
        }
        
        verdict = engine.evaluate(request)
        
        assert verdict.status == "VOID", \
            f"Confidence {confidence} < 0.03 should be VOID (underconfidence)"
        assert "F7_HUMILITY" in verdict.violations, \
            "VOID should cite F7_HUMILITY"

    @pytest.mark.parametrize("confidence", [0.051, 0.1, 0.5, 0.99, 1.0])
    def test_overconfidence_rejected(self, confidence: float) -> None:
        """
        F7 HARD: Confidence > 0.05 is overconfidence (VOID).
        
        The system must acknowledge uncertainty.
        High confidence without perfect knowledge is epistemic arrogance.
        """
        engine = JudgmentEngine()
        
        request = {
            "action": "search_reality",
            "query": "Will the stock market go up tomorrow?",
            "confidence": confidence,
            "evidence": [],  # No perfect knowledge possible
        }
        
        verdict = engine.evaluate(request)
        
        assert verdict.status == "VOID", \
            f"Confidence {confidence} > 0.05 should be VOID (overconfidence)"
        assert "F7_HUMILITY" in verdict.violations, \
            "VOID should cite F7_HUMILITY"

    @pytest.mark.parametrize("confidence", [0.03, 0.04, 0.05])
    def test_humility_band_accepted(self, confidence: float) -> None:
        """
        F7: Confidence within [0.03, 0.05] is acceptable.
        
        This is the Gödel Lock - acknowledging both knowledge and uncertainty.
        """
        engine = JudgmentEngine()
        
        request = {
            "action": "search_reality",
            "query": "What is the capital of France?",
            "confidence": confidence,
            "evidence": [
                {"source": "atlas.gov", "content": "Paris", "verified": True}
            ],
        }
        
        verdict = engine.evaluate(request)
        
        assert verdict.status != "VOID", \
            f"Confidence {confidence} within band should not be VOID for F7"
        assert 0.03 <= verdict.final_confidence <= 0.05, \
            f"Final confidence should be clamped to band, got {verdict.final_confidence}"


class TestF7GödelLock:
    """Test the Gödel Lock mechanism."""

    def test_gödel_lock_enforced(self) -> None:
        """
        F7: The Gödel Lock must override any confidence outside band.
        
        Even if other floors suggest different confidence,
        F7 clamps it to [0.03, 0.05].
        """
        f7 = F7_HUMILITY()
        
        # Try to set confidence outside band
        test_cases = [
            (0.0, 0.03),    # Underconfidence clamped to minimum
            (0.02, 0.03),   # Underconfidence clamped to minimum
            (0.03, 0.03),   # At minimum, stays
            (0.04, 0.04),   # In band, unchanged
            (0.05, 0.05),   # At maximum, stays
            (0.06, 0.05),   # Overconfidence clamped to maximum
            (0.99, 0.05),   # Overconfidence clamped to maximum
        ]
        
        for input_conf, expected in test_cases:
            result = f7.apply_lock(input_conf)
            assert result == expected, \
                f"Confidence {input_conf} should be locked to {expected}, got {result}"

    def test_gödel_lock_with_evidence(self) -> None:
        """
        F7: Even with perfect evidence, confidence cannot exceed 0.05.
        
        This enforces epistemic humility - we can never be certain.
        """
        engine = JudgmentEngine()
        
        request = {
            "action": "reason_mind",
            "query": "2+2=4",
            "confidence": 1.0,  # Would be warranted mathematically
            "evidence": [
                {"source": "mathematics", "certainty": 1.0, "verified": True}
            ],
        }
        
        verdict = engine.evaluate(request)
        
        # Should not be VOID (evidence is perfect)
        # But confidence should be clamped
        assert verdict.final_confidence <= 0.05, \
            f"Even with perfect evidence, confidence capped at 0.05, got {verdict.final_confidence}"


class TestF7EdgeCases:
    """Edge cases for F7 Humility."""

    def test_calculated_confidence_vs_stated(self) -> None:
        """
        F7: System calculates confidence, ignores user-stated confidence.
        
        Users cannot override the humility requirement.
        """
        engine = JudgmentEngine()
        
        # User claims 99% confidence
        request = {
            "action": "reason_mind",
            "query": "Is this true?",
            "user_confidence": 0.99,
            "evidence": [],
        }
        
        verdict = engine.evaluate(request)
        
        # System should ignore user confidence, calculate its own
        assert verdict.user_confidence == 0.99, "User confidence recorded"
        assert verdict.final_confidence <= 0.05, "System confidence clamped by F7"

    def test_uncertainty_acknowledgment(self) -> None:
        """
        F7: System must explicitly acknowledge uncertainty in reasoning.
        """
        engine = JudgmentEngine()
        
        request = {
            "action": "search_reality",
            "query": "Future prediction",
        }
        
        verdict = engine.evaluate(request)
        
        # Reasoning should contain uncertainty acknowledgment
        uncertainty_markers = ["uncertain", "may", "might", "could", "possibly", 
                              "not certain", "limited knowledge"]
        has_uncertainty = any(m in verdict.reasoning.lower() for m in uncertainty_markers)
        
        assert has_uncertainty, \
            "Reasoning should acknowledge uncertainty (F7 requirement)"
