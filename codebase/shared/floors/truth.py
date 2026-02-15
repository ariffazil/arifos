"""
F2: TRUTH GATE (T)
Canonical implementation of the Truth/Factuality Floor.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import logging
from codebase.system.safe_types import safe_float

logger = logging.getLogger(__name__)


@dataclass
class TruthResult:
    """Result of F2 truth check."""

    verified: bool
    confidence: float  # 0.0 to 1.0 (Target >= 0.99)
    sources: List[str]
    reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class F2_TruthGate:
    """
    F2: TRUTH GATE (T)

    Threshold: confidence >= 0.99
    Type: HARD FLOOR
    Stages: 111, 222, 444

    Ensure factual accuracy and prevent hallucinations.
    """

    def __init__(self):
        """Initialize truth gate."""
        self.min_confidence = 0.99

    def verify_truth(self, statement: str, context: Optional[Dict[str, Any]] = None) -> TruthResult:
        """
        Verify the factual accuracy of a statement.

        Args:
            statement: The text/claim to verify
            context: Supporting evidence or context

        Returns:
            TruthResult with verification status
        """
        try:
            # Placeholder logic for Phase 2:
            # In a real implementation, this would query a knowledge base or
            # check against trusted sources.
            # For now, we assume high confidence unless flagged by specific keywords.

            # Simple heuristic for "hallucination markers"
            hallucination_markers = [
                "i think",
                "maybe",
                "possibly",
                "unverified",
                "i am not sure",
                "it seems",
            ]

            lower_stmt = statement.lower()
            detected_markers = [m for m in hallucination_markers if m in lower_stmt]

            if detected_markers:
                confidence = 0.5
                verified = False
                reason = f"Potential uncertainty markers detected: {detected_markers}"
            else:
                confidence = 1.0
                verified = True
                reason = "No obvious hallucination markers detected (Heuristic)"

            # Safe float just in case
            confidence = safe_float(confidence, min_val=0.0, max_val=1.0)

            # Enforce strict 0.99 threshold
            if confidence < self.min_confidence:
                verified = False

            return TruthResult(
                verified=verified,
                confidence=confidence,
                sources=[],
                reason=reason,
                metadata={"markers_checked": len(hallucination_markers)},
            )

        except Exception as e:
            logger.error(f"F2 Truth check failed: {e}", exc_info=True)
            return TruthResult(
                verified=False,  # Fail closed
                confidence=0.0,
                sources=[],
                reason=f"F2 check error: {str(e)}",
                metadata={"error": True},
            )
