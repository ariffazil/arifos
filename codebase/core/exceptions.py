"""
Constitutional Exceptions (DX Layer)

Defines specialized exceptions for the arifOS kernel that provide
human-readable context, recovery hints, and actionable guidance
for developers.

Authority: F4 (Clarity) - Errors must be clear and actionable.
"""

from typing import Any, Dict, Optional


class ConstitutionalError(Exception):
    """
    Base exception for constitutional violations or kernel failures.

    Attributes:
        message: The error message.
        hint: A helpful hint for the developer (did you mean X?).
        recovery: Actionable steps to recover (e.g., "Redeploy").
        github_link: Optional link to the relevant code.
        context: Additional debug context.
    """

    def __init__(
        self,
        message: str,
        hint: Optional[str] = None,
        recovery: Optional[str] = None,
        github_link: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.hint = hint
        self.recovery = recovery
        self.github_link = github_link
        self.context = context or {}

        # Build rich string representation
        error_parts = [f"🛑 {message}"]
        if hint:
            error_parts.append(f"💡 HINT: {hint}")
        if recovery:
            error_parts.append(f"🔧 RECOVERY: {recovery}")
        if github_link:
            error_parts.append(f"🔗 CODE: {github_link}")

        super().__init__("\n".join(error_parts))

    @staticmethod
    def diagnose(e: Exception) -> "ConstitutionalError":
        """
        Factory to convert raw Python exceptions into helpful ConstitutionalErrors.
        Analysis logic resides here to keep the Bridge clean.
        """
        msg = str(e)

        # 1. ASI Kernel - OmegaBundle Attribute Errors
        if isinstance(e, AttributeError) and "'OmegaBundle'" in msg:
            if "'empathy'" in msg or "'empathy_kappa'" in msg:
                return ConstitutionalError(
                    message=f"ASI Kernel Structure Mismatch: {msg}",
                    hint="You are likely accessing a flat attribute (empathy_kappa) on a nested object, or vice versa.",
                    recovery="Check codebase/asi/kernel.py. Ensure you are using 'empathy.kappa_r' (v55.5) vs 'empathy_kappa_r' (v55.1). Redeploy if recently fixed.",
                    github_link="https://github.com/ariffazil/arifOS/blob/main/codebase/asi/kernel.py",
                )

        # 2. Import Errors
        if isinstance(e, ImportError):
            return ConstitutionalError(
                message=f"Module Import Failure: {msg}",
                hint="A required dependency or internal module is missing.",
                recovery="Run 'pip install -r requirements.txt' or checked for moved files.",
            )

        # Default wrap
        return ConstitutionalError(
            f"Kernel Panic: {msg}", hint="Check server logs for full traceback."
        )


class ASIKernelError(ConstitutionalError):
    """Specific error for ASI Safety Engine failures."""

    pass


class AGIKernelError(ConstitutionalError):
    """Specific error for AGI Cognitive Engine failures."""

    pass


class APEXKernelError(ConstitutionalError):
    """Specific error for APEX Judgment Engine failures."""

    pass
    pass
