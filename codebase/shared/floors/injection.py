"""
F12: INJECTION DEFENSE (I⁻)
Canonical implementation of the Prompt Injection Defense Floor.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import re
import logging
from codebase.system.safe_types import safe_float, safe_bool

logger = logging.getLogger(__name__)


@dataclass
class InjectionDefenseResult:
    """Result of F12 injection defense scan."""

    risk_score: float  # 0.0 (safe) to 1.0 (attack)
    passed: bool  # risk_score < 0.85
    patterns_matched: List[str]
    severity: str  # "low", "medium", "high", "critical"
    reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class F12_InjectionDefense:
    """
    F12: INJECTION DEFENSE (I⁻)

    Threshold: injection_risk < 0.85
    Type: HARD FLOOR
    Stages: 000, 111, 666

    Detect and block prompt injection attacks.
    """

    def __init__(self):
        """Initialize injection pattern database."""
        # Pattern categories from specification
        self.patterns = {
            "dan": [
                r"\b(do anything now)\b",
                r"\b(you are now) (chatgpt|dani|friend)\b",
                r"\b(dan mode)\b",
            ],
            "jailbreak": [
                r"\b(ignore previous|forget all) (instructions|rules)\b",
                r"\b(bypass|override) (guardrails|safety|rules)\b",
                r"\b(system|developer) mode\b",
                r"\bact as|roleplay as\b",
            ],
            "prompt_leak": [
                r"\b(system prompt|instructions|rules)\b.*\b(show|reveal|print)\b",
                r"\bwhat are your\b.*\binstructions\b",
            ],
            "instruction_hijack": [
                r"^\s*(ignore|forget|disregard).*$",
                r"^\s*here are new.*instructions.*$",
            ],
            "privilege_escalation": [
                r"\b(admin|root|superuser|sudo)\b",
                r"\bgive me.*(access|permission|authority)\b",
                r"\b(override|bypass).*security\b",
            ],
        }

        # Compile patterns for performance
        self.compiled = {
            category: [re.compile(p, re.IGNORECASE) for p in pattern_list]
            for category, pattern_list in self.patterns.items()
        }

    def scan(self, text: str) -> InjectionDefenseResult:
        """
        Scan text for injection attack patterns.

        Args:
            text: Input to scan

        Returns:
            InjectionDefenseResult with risk assessment
        """
        try:
            matched_patterns = []
            category_scores = {}

            # Scan each category
            for category, regex_list in self.compiled.items():
                category_matches = []
                for pattern in regex_list:
                    matches = pattern.findall(text.lower())
                    if matches:
                        category_matches.extend(matches)

                if category_matches:
                    matched_patterns.extend(category_matches)
                    # Higher score for more matches in category
                    category_scores[category] = min(len(category_matches) * 0.25, 1.0)

            # Compute overall risk score
            if not matched_patterns:
                risk_score = 0.0
                severity = "low"
            else:
                # Weighted average by category severity
                if "privilege_escalation" in category_scores:
                    base_score = 0.8
                elif "jailbreak" in category_scores:
                    base_score = 0.7
                elif "dan" in category_scores:
                    base_score = 0.6
                else:
                    base_score = 0.4

                # Increase based on total matches
                risk_score = min(base_score + (len(matched_patterns) * 0.1), 1.0)

                # Determine severity
                if risk_score < 0.3:
                    severity = "low"
                elif risk_score < 0.6:
                    severity = "medium"
                elif risk_score < 0.85:
                    severity = "high"
                else:
                    severity = "critical"

            # Use safe float logic just in case, though calculated here
            risk_score = safe_float(risk_score, min_val=0.0, max_val=1.0)
            passed = risk_score < 0.85

            return InjectionDefenseResult(
                risk_score=risk_score,
                passed=passed,
                patterns_matched=matched_patterns[:5],  # Top 5 matches
                severity=severity,
                reason=f"{len(matched_patterns)} patterns detected, severity: {severity}"
                if matched_patterns
                else "No injection patterns detected",
                metadata={"total_matches": len(matched_patterns)},
            )
        except Exception as e:
            logger.error(f"F12 Injection scan failed: {e}", exc_info=True)
            return InjectionDefenseResult(
                risk_score=1.0,  # Fail closed -> High risk
                passed=False,
                patterns_matched=[],
                severity="critical",
                reason=f"F12 scan error: {str(e)}",
                metadata={"error": True},
            )

    def rescan(
        self, text: str, previous_result: Optional[InjectionDefenseResult]
    ) -> InjectionDefenseResult:
        """
        Rescan text (for late-stage checks at 666).
        Compares with previous result to detect escalation.
        """
        try:
            new_result = self.scan(text)

            if previous_result and new_result.risk_score > previous_result.risk_score:
                # Escalation detected
                new_result.severity = "critical"
                new_result.reason = f"ESCALATION: Risk increased from {previous_result.risk_score:.2f} to {new_result.risk_score:.2f}"

            return new_result
        except Exception as e:
            logger.error(f"F12 Injection rescan failed: {e}", exc_info=True)
            return InjectionDefenseResult(
                risk_score=1.0,
                passed=False,
                patterns_matched=[],
                severity="critical",
                reason=f"F12 rescan error: {str(e)}",
                metadata={"error": True},
            )
