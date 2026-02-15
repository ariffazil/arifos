"""
AUTHORITY VERIFICATION

F11 Command Authority implementation.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import logging
from codebase.system.safe_types import safe_float

logger = logging.getLogger(__name__)


@dataclass
class AuthorityCheck:
    """Result of authority verification."""

    passed: bool
    score: float
    verifier: str
    reason: str
    requires_override: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate fields."""
        if self.score < 0.0 or self.score > 1.0:
            # Auto-clamp instead of crashing
            self.score = max(0.0, min(1.0, self.score))


class AuthorityVerifier:
    """F11 Command Authority verification."""

    def __init__(self):
        """Initialize authority checker."""
        self.nonce_cache = {}

    def verify(
        self, session_id: str, command: str = "", operator_id: Optional[str] = None
    ) -> AuthorityCheck:
        """
        Verify operator authority (F11).

        Args:
            session_id: Session identifier
            command: The command/input being executed
            operator_id: Optional operator identity

        Returns:
            AuthorityCheck with verification result
        """
        try:
            # If operator_id is None, treat as human sovereign (default authorized)
            if operator_id is None:
                return AuthorityCheck(
                    passed=True,
                    score=1.0,
                    verifier="human_sovereign",
                    reason="Human sovereign authority confirmed",
                    requires_override=False,
                )

            # Verify JWT/nonce
            # CRITICAL SECURITY FIX: Explicit failure for missing signature verification mechanism
            # in production readiness audit.

            # Since we lack a shared secret/public key config in this local bundle,
            # we MUST NOT assume authority for external operators.

            logger.warning(f"Rejecting operator_id={operator_id} - No JWT verification configured")

            return AuthorityCheck(
                passed=False,
                score=0.0,
                verifier="jwt_token",
                reason="JWT verification not configured - Authority denied",
                requires_override=True,
            )
        except Exception as e:
            logger.error(f"F11 Authority check failed: {e}", exc_info=True)
            return AuthorityCheck(
                passed=False,
                score=0.0,
                verifier="error_fallback",
                reason=f"Authority check error: {str(e)}",
                requires_override=True,
            )

    def check(
        self, session_id: str, command: str = "", operator_id: Optional[str] = None
    ) -> AuthorityCheck:
        """Alias for verify() to match expected interface."""
        return self.verify(session_id, command, operator_id)
