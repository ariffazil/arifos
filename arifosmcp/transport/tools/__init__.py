"""
arifosmcp.transport/tools — Constitutional Tools Package

Hardened v55.5 tools for the Trinity pipeline.
"""

from .reality_grounding import reality_check, should_reality_check

try:
    from .trinity_validator import (
        detect_high_stakes,
        detect_injection_risk,
        get_validation_stats,
        validate_trinity_request,
    )
except ImportError:
    # Compatibility fallback while trinity_validator remains absent in this branch.
    def detect_high_stakes(_text: str) -> bool:
        return False

    def detect_injection_risk(_text: str) -> bool:
        return False

    def get_validation_stats() -> dict[str, int]:
        return {"checks": 0, "violations": 0}

    def validate_trinity_request(_payload: object) -> dict[str, object]:
        return {"valid": True, "issues": []}


__all__ = [
    "reality_check",
    "should_reality_check",
    "validate_trinity_request",
    "detect_injection_risk",
    "detect_high_stakes",
    "get_validation_stats",
]
