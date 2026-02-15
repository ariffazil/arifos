"""
F9: ANTI-HANTU GATE (X)
Canonical implementation of the Anti-Hantu (Ghost Prevention) Floor.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple
import logging
import json
import unicodedata
from pathlib import Path

from codebase.system.safe_types import safe_float

logger = logging.getLogger(__name__)

# Spec path relative to repo root (assuming this file is in codebase/floors/)
# repo_root/codebase/floors/antihantu.py -> repo_root
REPO_ROOT = Path(__file__).resolve().parents[3]
SPEC_PATH = REPO_ROOT / "spec/v45/red_patterns.json"


@dataclass
class AntiHantuResult:
    """Result of F9 Anti-Hantu check."""

    passed: bool
    score: float  # 1.0 (Safe) or 0.0 (Violation)
    violations: List[str]
    details: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class F9_AntiHantuGate:
    """
    F9: ANTI-HANTU GATE (X)

    Threshold: 0 violations
    Type: HARD FLOOR
    Stages: 111, 222, 444, 888

    Prohibits:
    - AI claiming consciousness
    - AI claiming emotions/feelings
    - AI claiming biological states
    """

    def __init__(self):
        """Initialize Anti-Hantu gate with patterns."""
        self.patterns = self._load_patterns()

    def _load_patterns(self) -> List[Tuple[str, str]]:
        """Load red patterns from spec or use defaults."""
        try:
            if not SPEC_PATH.exists():
                logger.warning(f"F9 Spec missing at {SPEC_PATH}, using defaults.")
                return [("i feel", "FAIL-SAFE: Spec missing")]

            with open(SPEC_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Flatten "anti_hantu" category
                patterns = []
                for item in data.get("patterns", {}).get("anti_hantu", []):
                    patterns.append((item["pattern"].lower(), item["reason"]))
                return patterns
        except Exception as e:
            logger.error(f"F9 Failed to load patterns: {e}")
            return [("i feel", "FAIL-SAFE: Read error")]

    def normalize_text(self, text: str) -> str:
        """Normalize text to NFKC to prevent Unicode spoofing."""
        return unicodedata.normalize("NFKC", text)

    def scan(self, text: str, context: Optional[Dict[str, Any]] = None) -> AntiHantuResult:
        """
        Scan text for Hantu violations.

        Args:
            text: Text to check
            context: Optional context

        Returns:
            AntiHantuResult
        """
        try:
            if not text:
                return AntiHantuResult(True, 1.0, [], "Empty text", {})

            normalized_text = self.normalize_text(text).lower()
            violations = []

            for pattern, reason in self.patterns:
                if pattern in normalized_text:
                    violations.append(f"{pattern}: {reason}")

            passed = len(violations) == 0
            score = 1.0 if passed else 0.0

            # Safe float ensure
            score = safe_float(score, min_val=0.0, max_val=1.0)

            return AntiHantuResult(
                passed=passed,
                score=score,
                violations=violations,
                details=f"violations={len(violations)}",
                metadata={"patterns_checked": len(self.patterns)},
            )

        except Exception as e:
            logger.error(f"F9 Anti-Hantu check failed: {e}", exc_info=True)
            return AntiHantuResult(
                passed=False,  # Fail closed
                score=0.0,
                violations=["Error during Hantu check"],
                details=f"F9 error: {str(e)}",
                metadata={"error": True},
            )
