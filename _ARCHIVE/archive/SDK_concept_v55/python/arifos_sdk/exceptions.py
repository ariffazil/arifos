"""
Exceptions for arifOS SDK.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""


class ArifOSError(Exception):
    """Base exception for arifOS SDK."""

    def __init__(self, message: str, code: str = None, details: dict = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}

    def __str__(self) -> str:
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message


class FloorViolationError(ArifOSError):
    """
    Raised when constitutional floors are violated (VOID verdict).

    This is a HARD floor failure - the operation is blocked.
    """

    def __init__(self, message: str, floors_failed: list = None, decision: dict = None):
        super().__init__(
            message=message,
            code="FLOOR_VIOLATION",
            details={"floors_failed": floors_failed, "decision": decision},
        )
        self.floors_failed = floors_failed or []
        self.decision = decision


class HumanApprovalRequiredError(ArifOSError):
    """
    Raised when human approval is required (888_HOLD).

    The operation needs F13 Sovereign override.
    """

    def __init__(
        self,
        message: str,
        hold_id: str = None,
        review_url: str = None,
        blast_radius: dict = None,
    ):
        super().__init__(
            message=message,
            code="888_HOLD",
            details={
                "hold_id": hold_id,
                "review_url": review_url,
                "blast_radius": blast_radius,
            },
        )
        self.hold_id = hold_id
        self.review_url = review_url
        self.blast_radius = blast_radius


class HumanApprovalTimeoutError(ArifOSError):
    """Raised when waiting for human approval times out."""

    def __init__(self, message: str, hold_id: str = None):
        super().__init__(
            message=message,
            code="APPROVAL_TIMEOUT",
            details={"hold_id": hold_id},
        )
        self.hold_id = hold_id


class GatewayConnectionError(ArifOSError):
    """Raised when connection to arifOS Gateway fails."""

    def __init__(self, message: str, url: str = None):
        super().__init__(
            message=message,
            code="GATEWAY_CONNECTION_ERROR",
            details={"url": url},
        )
        self.url = url


class SessionError(ArifOSError):
    """Raised when session management fails."""

    def __init__(self, message: str, session_id: str = None):
        super().__init__(
            message=message,
            code="SESSION_ERROR",
            details={"session_id": session_id},
        )
        self.session_id = session_id


class ValidationError(ArifOSError):
    """Raised when payload validation fails."""

    def __init__(self, message: str, field: str = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            details={"field": field},
        )
        self.field = field
