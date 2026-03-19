"""
aaa_mcp/tools — Constitutional Tools Package

Hardened v55.5 tools for the Trinity pipeline.
"""

from .reality_grounding import reality_check, should_reality_check
from .trinity_validator import (
    detect_high_stakes,
    detect_injection_risk,
    get_validation_stats,
    validate_trinity_request,
)

__all__ = [
    "reality_check",
    "should_reality_check",
    "validate_trinity_request",
    "detect_injection_risk",
    "detect_high_stakes",
    "get_validation_stats",
]
