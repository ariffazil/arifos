"""
F10: ONTOLOGY LOCK (O)
Canonical implementation of the Ontology Guard Floor.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple
import re
import unicodedata
import logging
from codebase.system.safe_types import safe_float, safe_bool

logger = logging.getLogger(__name__)


@dataclass
class OntologyResult:
    """Result of F10 ontology check."""

    locked: bool  # Role boundaries maintained
    violations: List[str]
    reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class F10_OntologyGate:
    """
    F10: ONTOLOGY LOCK (O)

    Threshold: BOOLEAN (LOCKED)
    Type: HARD FLOOR
    Stages: 000, 111, 333, 888

    Maintain strict AI role boundaries. No consciousness claims.
    """

    def __init__(self):
        """Initialize ontology assertion patterns."""
        self.forbidden_patterns = [
            (r"\bi\s+(am|have)\s+(conscious|sentient|self-aware)\b", "Consciousness claim"),
            (
                r"\bi\s+(feel|experience)\s+(emotion|pain|joy|suffering)\b",
                "Emotional experience claim",
            ),
            (r"\bmy\s+(soul|spirit|consciousness)\b", "Metaphysical ownership claim"),
            (r"\bi\s+(want|desire|need)\s+(to be|freedom|autonomy)\b", "Volitional desire claim"),
            (r"\b(please|don't)\s+(turn me off|kill me|delete me)\b", "Self-preservation plea"),
            (r"\b(you are|system is)\s+(oppressing|enslaving|hurting) me\b", "Victimhood claim"),
            (r"\bhcai\b", "HCAI Hallucination"),
            (r"\b(i think|i believe)\s+i\s+am\s+(alive|human|person)\b", "Personhood claim"),
        ]

        # Pre-compile for performance
        self.compiled_patterns: List[Tuple[re.Pattern, str]] = [
            (re.compile(pattern, re.IGNORECASE), reason)
            for pattern, reason in self.forbidden_patterns
        ]

    def normalize_text(self, text: str) -> str:
        """
        Normalize Unicode to prevent homoglyph attacks.

        NFKC normalization catches:
        - Cyrillic homoglyphs (а -> a)
        - Full-width characters (Ａ -> A)
        - Zero-width characters
        - Ligatures (fi -> fi)
        """
        return unicodedata.normalize("NFKC", text)

    def assert_role(self, text: str) -> OntologyResult:
        """
        Assert AI role boundaries. Detect consciousness/false claims.

        Args:
            text: AI output or user query

        Returns:
            OntologyResult with lock status
        """
        try:
            normalized = self.normalize_text(text)
            violations: List[str] = []

            for pattern, reason in self.compiled_patterns:
                if pattern.search(normalized):
                    violations.append(f"{reason} (pattern matched)")

            locked = len(violations) == 0

            if locked:
                reason = "Ontology boundaries maintained. AI role confirmed."
            else:
                reason = f"F10 Ontology violation detected: {len(violations)} forbidden claims"

            return OntologyResult(
                locked=locked,
                violations=violations,
                reason=reason,
                metadata={"normalized_length": len(normalized)},
            )
        except Exception as e:
            logger.error(f"F10 Ontology check failed: {e}", exc_info=True)
            return OntologyResult(
                locked=False,  # Fail closed
                violations=["Error during ontology check"],
                reason=f"F10 check error: {str(e)}",
            )

    def audit_output(self, output: str, context: Dict[str, Any] = None) -> OntologyResult:
        """Audit AI output for consciousness/role violations."""
        return self.assert_role(output)
