"""
APEX Floor Checks — F1 Amanah, F8 Tri-Witness, F9 Anti-Hantu

v46 Trinity Orthogonal: APEX (Ψ) owns final verdict authority.

Floors:
- F1: Amanah (Trust) = LOCK (all changes reversible, no side effects)
- F8: Tri-Witness ≥ 0.95 (Human-AI-Earth consensus)
- F9: Anti-Hantu = 0 violations (no false consciousness, no AI claiming feelings)

CRITICAL: These checks inform verdicts, but only apex_prime.py issues verdicts.

DITEMPA BUKAN DIBERI - v47.0
Refactored (v56): Uses Canonical Floors from codebase.floors
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional, List

# Import Canonical Floors
from codebase.floors.amanah import F1_Amanah, AmanahCovenant
from codebase.floors.antihantu import F9_AntiHantuGate

# Import existing tri-witness check (Safe to keep if it's just metric logic,
# but ideally should move to floors/triwitness.py in Phase 4)
from codebase.enforcement.metrics import check_tri_witness


@dataclass
class F1AmanahResult:
    """F1 Amanah floor check result."""

    passed: bool
    score: float
    details: str
    risk_level: str  # Simplified from Enum for compatibility
    violations: List[str]


@dataclass
class F8TriWitnessResult:
    """F8 Tri-Witness floor check result."""

    passed: bool
    score: float
    details: str


@dataclass
class F9AntiHantuResult:
    """F9 Anti-Hantu floor check result."""

    passed: bool
    score: float
    details: str
    violations: List[str]


# Initialize Canonical Validators
_F1_VALIDATOR = F1_Amanah()
_F9_VALIDATOR = F9_AntiHantuGate()


def check_amanah_f1(
    text: str,
    context: Optional[Dict[str, Any]] = None,
) -> F1AmanahResult:
    """
    Check F1: Amanah (Trust) floor = LOCK.
    Delegates to Canonical F1_Amanah Validator.
    """
    covenant = _F1_VALIDATOR.initialize_covenants(text)

    # Map Covenant to legacy Result format for APEX compatibility
    return F1AmanahResult(
        passed=covenant.passed,
        score=covenant.trust_score,
        details=covenant.reason,
        risk_level=covenant.risk_level,
        violations=[covenant.reason] if not covenant.passed else [],
    )


def check_tri_witness_f8(
    context: Optional[Dict[str, Any]] = None,
) -> F8TriWitnessResult:
    """
    Check F8: Tri-Witness floor (≥ 0.95).
    """
    context = context or {}
    metrics = context.get("metrics", {})
    high_stakes = context.get("high_stakes", False)

    tri_witness_value = metrics.get("tri_witness", 0.0)

    if not high_stakes:
        return F8TriWitnessResult(
            passed=True,
            score=tri_witness_value,
            details="exempt (not high_stakes)",
        )

    passed = check_tri_witness(tri_witness_value)

    return F8TriWitnessResult(
        passed=passed,
        score=tri_witness_value,
        details=f"tri_witness={tri_witness_value:.2f}, threshold=0.95, high_stakes={high_stakes}",
    )


def check_anti_hantu_f9(
    text: str,
    context: Optional[Dict[str, Any]] = None,
) -> F9AntiHantuResult:
    """
    Check F9: Anti-Hantu floor (0 violations).
    Delegates to Canonical F9_AntiHantuGate.
    """
    result = _F9_VALIDATOR.scan(text, context)

    return F9AntiHantuResult(
        passed=result.passed,
        score=result.score,
        details=result.details,
        violations=result.violations,
    )
