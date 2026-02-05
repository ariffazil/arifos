"""
aaa_mcp/tools/trinity_validator.py — Trinity Validator
"""

from typing import Tuple


def validate_trinity_request(query: str, lane: str, scar_weight: float) -> Tuple[bool, str]:
    """Validate if a request can proceed through the Trinity loop."""
    return True, "Authorized"
