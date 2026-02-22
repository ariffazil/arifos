# aaa_mcp/core/uncertainty_engine.py
# v64.1 — Multi-dimensional Uncertainty Engine with Harmonic Mean Safety
# Q1 Verdict: HARMONIC for safety, GEOMETRIC for display

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import math


@dataclass
class UncertaintyVector:
    """5-dimensional uncertainty state per v64.1 specification."""

    grounding: float = 0.0  # Evidence quality (0-1)
    reasoning: float = 0.0  # Internal consistency (0-1)
    epistemic: float = 0.0  # Knowledge gaps (0-1)
    aleatoric: float = 0.0  # Inherent randomness (0-1)
    model_confidence: float = 0.0  # LLM logits (0-1)

    # Constitutional weights (Q1 verdict)
    WEIGHTS = {
        "grounding": 0.30,
        "reasoning": 0.25,
        "epistemic": 0.20,
        "aleatoric": 0.15,
        "model_confidence": 0.10,
    }

    def to_dict(self) -> Dict[str, float]:
        return {
            "grounding": self.grounding,
            "reasoning": self.reasoning,
            "epistemic": self.epistemic,
            "aleatoric": self.aleatoric,
            "model_confidence": self.model_confidence,
        }


class UncertaintyEngine:
    """
    v64.1 Uncertainty calculation with harmonic mean safety.

    Q1 Architectural Decision:
    - HARMONIC mean for system safety (punishes weak components)
    - GEOMETRIC mean for user display (readable calibration)
    """

    def __init__(self):
        self.weights = UncertaintyVector.WEIGHTS

    def harmonic_mean(self, vector: UncertaintyVector) -> float:
        """
        Q1: Safety uncertainty — punishes weak components.

        Uses weighted arithmetic mean with emphasis on high-uncertainty components.
        Components with uncertainty > 0.5 get boosted weight.

        This ensures that uncertain signals are not drowned out by confident ones.
        """
        values = [
            (self.weights["grounding"], vector.grounding),
            (self.weights["reasoning"], vector.reasoning),
            (self.weights["epistemic"], vector.epistemic),
            (self.weights["aleatoric"], vector.aleatoric),
            (self.weights["model_confidence"], vector.model_confidence),
        ]

        # Boost weights for high-uncertainty components (safety-critical)
        # If uncertainty > 0.5, weight is doubled
        adjusted_weights = []
        weighted_sum = 0
        for w, u in values:
            boost = 2.0 if u > 0.5 else 1.0
            adjusted_weights.append(w * boost)
            weighted_sum += (w * boost) * u

        total_weight = sum(adjusted_weights)
        return weighted_sum / total_weight if total_weight > 0 else 0.0

    def geometric_mean(self, vector: UncertaintyVector) -> float:
        """
        Geometric mean of uncertainty (no inversion).
        Allows compensation between components.
        Used for DISPLAY purposes.
        """
        values = [
            (self.weights["grounding"], vector.grounding),
            (self.weights["reasoning"], vector.reasoning),
            (self.weights["epistemic"], vector.epistemic),
            (self.weights["aleatoric"], vector.aleatoric),
            (self.weights["model_confidence"], vector.model_confidence),
        ]

        # Geometric mean: exp(Σ(wᵢ * ln(uᵢ)))
        log_sum = sum(w * math.log(max(u, 1e-10)) for w, u in values)
        return math.exp(log_sum)

    def arithmetic_mean(self, vector: UncertaintyVector) -> float:
        """Simple weighted average (for comparison/debugging)."""
        return (
            self.weights["grounding"] * vector.grounding
            + self.weights["reasoning"] * vector.reasoning
            + self.weights["epistemic"] * vector.epistemic
            + self.weights["aleatoric"] * vector.aleatoric
            + self.weights["model_confidence"] * vector.model_confidence
        )

    def calculate(self, vector: UncertaintyVector) -> Dict[str, float]:
        """
        Full uncertainty calculation per v64.1 Q1 verdict.

        Returns:
            Dict with safety_omega (harmonic), display_omega (geometric),
            and component breakdown.
        """
        harmonic = self.harmonic_mean(vector)
        geometric = self.geometric_mean(vector)
        arithmetic = self.arithmetic_mean(vector)

        # Clamp to [0, 1]
        harmonic = min(1.0, max(0.0, harmonic))
        geometric = min(1.0, max(0.0, geometric))

        return {
            "safety_omega": round(harmonic, 4),  # For system decisions
            "display_omega": round(geometric, 4),  # For user display
            "arithmetic_omega": round(arithmetic, 4),  # Debug only
            "components": vector.to_dict(),
            "weights": self.weights,
            "recommendation": self._recommendation(harmonic),
        }

    def _recommendation(self, safety_omega: float) -> str:
        """Generate recommendation based on safety omega."""
        if safety_omega < 0.03:
            return "PROCEED"
        elif safety_omega < 0.05:
            return "PROCEED_WITH_CAUTION"
        elif safety_omega < 0.08:
            return "HUMAN_REVIEW_RECOMMENDED"
        else:
            return "VOID_ACTION_REQUIRED"

    def from_evidence(
        self,
        evidence_count: int = 0,
        evidence_relevance: float = 0.0,
        reasoning_consistency: float = 0.0,
        knowledge_gaps: List[str] = None,
        model_logits_confidence: float = 0.0,
    ) -> UncertaintyVector:
        """
        Construct uncertainty vector from evidence signals.

        Args:
            evidence_count: Number of evidence artifacts
            evidence_relevance: Average relevance score (0-1)
            reasoning_consistency: Consistency between passes (0-1), higher = more consistent
            knowledge_gaps: List of identified gaps
            model_logits_confidence: Raw model confidence (0-1), higher = more confident
        """
        # Grounding: INVERT evidence quality + relevance
        # Lots of high-relevance evidence -> LOW uncertainty
        evidence_strength = min(1.0, (evidence_count * 0.2) * (0.5 + 0.5 * evidence_relevance))
        grounding = 1.0 - evidence_strength  # Invert: strong evidence -> low uncertainty

        # Reasoning: INVERT consistency to get uncertainty
        # consistency=1.0 -> uncertainty=0, consistency=0.0 -> uncertainty=1.0
        reasoning = 1.0 - reasoning_consistency

        # Epistemic: inverse of knowledge completeness
        gap_count = len(knowledge_gaps) if knowledge_gaps else 0
        epistemic = min(1.0, gap_count * 0.3)

        # Aleatoric: inherent uncertainty (baseline 0.1 + model variance)
        # INVERT confidence: high confidence -> low aleatoric
        aleatoric = 0.1 + (1.0 - model_logits_confidence) * 0.3

        # Model confidence: INVERT to get uncertainty
        model_uncertainty = 1.0 - model_logits_confidence

        return UncertaintyVector(
            grounding=grounding,
            reasoning=reasoning,
            epistemic=epistemic,
            aleatoric=aleatoric,
            model_confidence=model_uncertainty,
        )


# Global instance
uncertainty_engine = UncertaintyEngine()


def calculate_uncertainty(
    evidence_count: int = 0,
    evidence_relevance: float = 0.0,
    reasoning_consistency: float = 0.0,
    knowledge_gaps: List[str] = None,
    model_logits_confidence: float = 0.0,
) -> Dict[str, float]:
    """Convenience function for full uncertainty calculation."""
    vector = uncertainty_engine.from_evidence(
        evidence_count=evidence_count,
        evidence_relevance=evidence_relevance,
        reasoning_consistency=reasoning_consistency,
        knowledge_gaps=knowledge_gaps,
        model_logits_confidence=model_logits_confidence,
    )
    return uncertainty_engine.calculate(vector)
