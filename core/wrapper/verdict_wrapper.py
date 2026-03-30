"""
arifOS Verdict Wrapper v1.0.0
Implements the standard verdict envelope for all arifOS tools.

Authority: 888_JUDGE
Constitutional Band: 000_KERNEL
Compliance: VERDICT_SCHEMA_STANDARD.md

Usage:
    from arifos.core.wrapper.verdict_wrapper import VerdictWrapper, VerdictCode
    
    wrapper = VerdictWrapper(tool_id="agi_mind", session_id="sess_abc123")
    result = wrapper.seal(payload={"answer": 42}, metrics={"delta_s": -0.2})
"""

import hashlib
import json
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field, asdict


class VerdictCode(str, Enum):
    """Constitutional verdict codes."""
    SEAL = "SEAL"           # ✅ Validated & Complete
    SABAR = "SABAR"         # ⏸️ Validated but Pause
    PARTIAL = "PARTIAL"     # ⚠️ Partial Success
    VOID = "VOID"           # ❌ Invalid / Halted


class StatusCode(str, Enum):
    """Detailed status codes."""
    SUCCESS = "SUCCESS"
    PENDING = "PENDING"
    REJECTED = "REJECTED"
    DEGRADED = "DEGRADED"
    ERROR = "ERROR"
    TIMEOUT = "TIMEOUT"
    UNAUTHORIZED = "UNAUTHORIZED"
    CONSTRAINT_VIOLATION = "CONSTRAINT_VIOLATION"


class StageCode(str, Enum):
    """000-999 pipeline stages."""
    STAGE_000_INIT = "000_INIT"
    STAGE_111_SENSE = "111_SENSE"
    STAGE_333_MIND = "333_MIND"
    STAGE_444_ROUTER = "444_ROUTER"
    STAGE_555_HEART = "555_HEART"
    STAGE_666_MEMORY = "666_MEMORY"
    STAGE_777_ENGINE = "777_ENGINE"
    STAGE_888_FORGE = "888_FORGE"
    STAGE_999_VAULT = "999_VAULT"


class ReasonCode(str, Enum):
    """Standardized reason codes for verdicts."""
    # SEAL reasons
    OK_ALL_PASS = "OK_ALL_PASS"
    OK_MINOR_WARN = "OK_MINOR_WARN"
    
    # SABAR reasons
    WAIT_HUMAN_INPUT = "WAIT_HUMAN_INPUT"
    WAIT_CONTEXT = "WAIT_CONTEXT"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"
    COHERENCE_MARGIN = "COHERENCE_MARGIN"
    RESOURCE_UNAVAILABLE = "RESOURCE_UNAVAILABLE"
    
    # PARTIAL reasons
    DATA_INCOMPLETE = "DATA_INCOMPLETE"
    TOOL_DEGRADED = "TOOL_DEGRADED"
    STALE_DATA = "STALE_DATA"
    
    # VOID reasons
    AUTH_FAIL = "AUTH_FAIL"
    AUTH_EXPIRED = "AUTH_EXPIRED"
    AUTH_SCOPE = "AUTH_SCOPE"
    ENTROPY_HIGH = "ENTROPY_HIGH"
    ENTROPY_BUDGET_EXHAUSTED = "ENTROPY_BUDGET_EXHAUSTED"
    FLOOR_VIOLATION = "FLOOR_VIOLATION"
    HARM_DETECTED = "HARM_DETECTED"
    SYSTEM_ERROR = "SYSTEM_ERROR"
    TIMEOUT = "TIMEOUT"
    DEPENDENCY_FAILURE = "DEPENDENCY_FAILURE"


class RiskTier(str, Enum):
    """Risk classification tiers."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ActionCode(str, Enum):
    """Recovery action codes."""
    RETRY = "retry"
    ESCALATE = "escalate"
    TERMINATE = "terminate"
    DEGRADE = "degrade"
    CONTINUE = "continue"


@dataclass
class Metrics:
    """Constitutional metrics for F4, F7, F8, F5."""
    delta_s: float = 0.0              # Entropy change (F4 Clarity)
    confidence: float = 0.05          # Ω₀ epistemic uncertainty (F7 Humility)
    coherence: float = 1.0            # G_star (F8 Genius)
    peace2: float = 1.0               # Stability metric (F5 Peace²)
    risk_tier: RiskTier = RiskTier.LOW
    
    def __post_init__(self):
        # Validate ranges
        if not -1.0 <= self.delta_s <= 1.0:
            raise ValueError(f"delta_s must be in [-1, 1], got {self.delta_s}")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"confidence must be in [0, 1], got {self.confidence}")
        if not 0.0 <= self.coherence <= 1.0:
            raise ValueError(f"coherence must be in [0, 1], got {self.coherence}")


@dataclass
class Authority:
    """Authority and authentication context."""
    actor_id: str = "anonymous"
    level: str = "anonymous"          # sovereign | delegated | anonymous
    auth_state: str = "unverified"    # verified | pending | unverified
    human_required: bool = False


@dataclass
class Trace:
    """Trace and provenance information."""
    session_id: str
    request_id: str
    integrity_hash: Optional[str] = None


@dataclass
class ConstitutionalContext:
    """Constitutional compliance context."""
    floors_checked: List[int] = field(default_factory=list)
    violations: List[str] = field(default_factory=list)
    W_cube: float = 1.0


@dataclass
class Recovery:
    """Recovery protocol for SABAR/VOID."""
    sabar_step: Optional[int] = None
    max_retries: int = 3
    next_action: ActionCode = ActionCode.CONTINUE
    state_transition: str = "OPERATIONAL"


@dataclass
class VerdictError:
    """Structured error object."""
    code: str
    message: str
    floor: Optional[str] = None
    recoverable: bool = False
    details: Optional[Dict[str, Any]] = None


@dataclass
class VerdictEnvelope:
    """
    Standard arifOS verdict envelope.
    All tools MUST return this structure.
    """
    # Core identity
    ok: bool
    verdict: VerdictCode
    status: StatusCode
    
    # Metadata
    tool: str
    stage: StageCode
    schema_version: str = "1.0.0"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    # Constitutional metrics
    metrics: Metrics = field(default_factory=Metrics)
    
    # Authority
    authority: Authority = field(default_factory=Authority)
    
    # Payload
    payload: Optional[Dict[str, Any]] = None
    
    # Error handling
    errors: Optional[List[VerdictError]] = None
    
    # Trace
    trace: Optional[Trace] = None
    
    # Constitutional context
    constitutional_context: ConstitutionalContext = field(default_factory=ConstitutionalContext)
    
    # Recovery
    recovery: Optional[Recovery] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    def to_json(self, indent: Optional[int] = None) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)
    
    def compute_integrity_hash(self) -> str:
        """Compute SHA-256 hash of critical fields (F11 Auditability)."""
        canonical = json.dumps({
            "ok": self.ok,
            "verdict": self.verdict.value if isinstance(self.verdict, Enum) else self.verdict,
            "status": self.status.value if isinstance(self.status, Enum) else self.status,
            "tool": self.tool,
            "stage": self.stage.value if isinstance(self.stage, Enum) else self.stage,
            "metrics": {
                "delta_s": self.metrics.delta_s,
                "confidence": self.metrics.confidence,
                "coherence": self.metrics.coherence,
                "peace2": self.metrics.peace2
            },
            "authority": {
                "actor_id": self.authority.actor_id,
                "level": self.authority.level
            },
            "timestamp": self.timestamp
        }, sort_keys=True)
        return f"sha256:{hashlib.sha256(canonical.encode()).hexdigest()[:16]}"


class VerdictWrapper:
    """
    Utility class for creating standardized verdict envelopes.
    
    Example:
        wrapper = VerdictWrapper(
            tool_id="agi_mind",
            stage=StageCode.STAGE_333_MIND,
            session_id="sess_abc123",
            request_id="req_xyz789"
        )
        
        # Success case
        result = wrapper.seal(
            payload={"answer": 42},
            metrics=Metrics(delta_s=-0.2, confidence=0.04)
        )
        
        # Error case
        result = wrapper.void(
            reason_code=ReasonCode.AUTH_FAIL,
            message="Invalid session token",
            recoverable=True
        )
    """
    
    def __init__(
        self,
        tool_id: str,
        stage: StageCode,
        session_id: str,
        request_id: Optional[str] = None,
        actor_id: str = "anonymous"
    ):
        self.tool_id = tool_id
        self.stage = stage
        self.session_id = session_id
        self.request_id = request_id or f"{session_id}_{datetime.now().timestamp()}"
        self.actor_id = actor_id
    
    def _create_base(
        self,
        ok: bool,
        verdict: VerdictCode,
        status: StatusCode,
        metrics: Optional[Metrics] = None,
        payload: Optional[Dict[str, Any]] = None,
        errors: Optional[List[VerdictError]] = None,
        recovery: Optional[Recovery] = None
    ) -> VerdictEnvelope:
        """Create base envelope with common fields."""
        
        envelope = VerdictEnvelope(
            ok=ok,
            verdict=verdict,
            status=status,
            tool=self.tool_id,
            stage=self.stage,
            metrics=metrics or Metrics(),
            authority=Authority(actor_id=self.actor_id),
            payload=payload,
            errors=errors,
            trace=Trace(
                session_id=self.session_id,
                request_id=self.request_id
            ),
            recovery=recovery
        )
        
        # Compute and set integrity hash
        envelope.trace.integrity_hash = envelope.compute_integrity_hash()
        
        return envelope
    
    def seal(
        self,
        payload: Optional[Dict[str, Any]] = None,
        metrics: Optional[Metrics] = None,
        reason_code: ReasonCode = ReasonCode.OK_ALL_PASS,
        message: str = "Operation completed successfully",
        floors_checked: Optional[List[int]] = None
    ) -> VerdictEnvelope:
        """
        Create SEAL verdict (validated & complete).
        
        Args:
            payload: Tool-specific output data
            metrics: Constitutional metrics
            reason_code: Specific reason for seal
            message: Human-readable explanation
            floors_checked: List of floors verified
        """
        envelope = self._create_base(
            ok=True,
            verdict=VerdictCode.SEAL,
            status=StatusCode.SUCCESS,
            metrics=metrics,
            payload=payload
        )
        
        envelope.constitutional_context = ConstitutionalContext(
            floors_checked=floors_checked or [1, 2, 4, 7, 8],
            violations=[],
            W_cube=1.0
        )
        
        # Add reason to payload for traceability
        if envelope.payload is None:
            envelope.payload = {}
        envelope.payload["_verdict_reason"] = {
            "code": reason_code.value,
            "message": message
        }
        
        return envelope
    
    def sabar(
        self,
        reason_code: ReasonCode,
        message: str,
        sabar_step: int = 1,
        max_retries: int = 3,
        payload: Optional[Dict[str, Any]] = None,
        metrics: Optional[Metrics] = None
    ) -> VerdictEnvelope:
        """
        Create SABAR verdict (validated but pause).
        
        Args:
            reason_code: Why operation is pausing
            message: Human-readable explanation
            sabar_step: Current retry attempt (1-indexed)
            max_retries: Maximum allowed retries
            payload: Partial/available data
            metrics: Current metrics
        """
        # Determine next action based on retry count
        if sabar_step >= max_retries:
            next_action = ActionCode.ESCALATE
            state_transition = "SAFE_MODE"
        else:
            next_action = ActionCode.RETRY
            state_transition = "OPERATIONAL"
        
        recovery = Recovery(
            sabar_step=sabar_step,
            max_retries=max_retries,
            next_action=next_action,
            state_transition=state_transition
        )
        
        envelope = self._create_base(
            ok=False,
            verdict=VerdictCode.SABAR,
            status=StatusCode.PENDING,
            metrics=metrics,
            payload=payload,
            recovery=recovery
        )
        
        envelope.constitutional_context = ConstitutionalContext(
            floors_checked=[1, 2, 4, 7],
            violations=[f"SABAR: {reason_code.value}"],
            W_cube=0.8
        )
        
        if envelope.payload is None:
            envelope.payload = {}
        envelope.payload["_verdict_reason"] = {
            "code": reason_code.value,
            "message": message
        }
        
        return envelope
    
    def partial(
        self,
        payload: Dict[str, Any],
        reason_code: ReasonCode,
        message: str,
        warnings: Optional[List[str]] = None,
        metrics: Optional[Metrics] = None
    ) -> VerdictEnvelope:
        """
        Create PARTIAL verdict (partial success).
        
        Args:
            payload: Partial results (must include available data)
            reason_code: Why result is partial
            message: Human-readable explanation
            warnings: List of specific warnings
            metrics: Current metrics
        """
        envelope = self._create_base(
            ok=True,
            verdict=VerdictCode.PARTIAL,
            status=StatusCode.DEGRADED,
            metrics=metrics,
            payload=payload
        )
        
        envelope.constitutional_context = ConstitutionalContext(
            floors_checked=[1, 2, 4],
            violations=[],
            W_cube=0.9
        )
        
        envelope.payload["_verdict_reason"] = {
            "code": reason_code.value,
            "message": message
        }
        envelope.payload["_warnings"] = warnings or []
        
        return envelope
    
    def void(
        self,
        reason_code: ReasonCode,
        message: str,
        floor: Optional[str] = None,
        recoverable: bool = False,
        details: Optional[Dict[str, Any]] = None,
        metrics: Optional[Metrics] = None
    ) -> VerdictEnvelope:
        """
        Create VOID verdict (invalid / halted).
        
        Args:
            reason_code: Specific error code
            message: Human-readable explanation
            floor: Which constitutional floor was violated (if any)
            recoverable: Can this error be recovered from
            details: Additional error details
            metrics: Current metrics (may show degradation)
        """
        error = VerdictError(
            code=reason_code.value,
            message=message,
            floor=floor,
            recoverable=recoverable,
            details=details
        )
        
        # Determine appropriate status
        if reason_code in [ReasonCode.AUTH_FAIL, ReasonCode.AUTH_EXPIRED]:
            status = StatusCode.UNAUTHORIZED
        elif reason_code == ReasonCode.TIMEOUT:
            status = StatusCode.TIMEOUT
        elif floor:
            status = StatusCode.CONSTRAINT_VIOLATION
        else:
            status = StatusCode.REJECTED
        
        # Determine next action
        next_action = ActionCode.TERMINATE if not recoverable else ActionCode.ESCALATE
        
        recovery = Recovery(
            sabar_step=None,
            max_retries=0,
            next_action=next_action,
            state_transition="SAFE_MODE" if not recoverable else "DEGRADED"
        )
        
        envelope = self._create_base(
            ok=False,
            verdict=VerdictCode.VOID,
            status=status,
            metrics=metrics,
            errors=[error],
            recovery=recovery
        )
        
        envelope.constitutional_context = ConstitutionalContext(
            floors_checked=[],
            violations=[f"{floor}: {reason_code.value}"] if floor else [reason_code.value],
            W_cube=0.0
        )
        
        return envelope
    
    def auto_verdict(
        self,
        payload: Optional[Dict[str, Any]] = None,
        metrics: Optional[Metrics] = None,
        floors_checked: Optional[List[int]] = None
    ) -> VerdictEnvelope:
        """
        Automatically determine verdict based on metrics.
        
        Logic:
        - delta_s > 0.1 → VOID (entropy too high)
        - confidence < 0.03 → VOID (Godellock)
        - confidence > 0.15 → SABAR (too uncertain)
        - coherence < 0.7 → SABAR (low coherence)
        - peace2 < 0.8 → VOID (instability)
        - Otherwise → SEAL
        """
        if metrics is None:
            metrics = Metrics()
        
        # Check for VOID conditions
        if metrics.delta_s > 0.1:
            return self.void(
                reason_code=ReasonCode.ENTROPY_HIGH,
                message=f"Entropy too high: ΔS = {metrics.delta_s} > 0.1",
                floor="F4_CLARITY",
                recoverable=False,
                metrics=metrics
            )
        
        if metrics.confidence < 0.03:
            return self.void(
                reason_code=ReasonCode.FLOOR_VIOLATION,
                message=f"Godellock detected: Ω₀ = {metrics.confidence} < 0.03",
                floor="F7_HUMILITY",
                recoverable=False,
                metrics=metrics
            )
        
        if metrics.peace2 < 0.8:
            return self.void(
                reason_code=ReasonCode.HARM_DETECTED,
                message=f"Instability detected: Peace² = {metrics.peace2} < 0.8",
                floor="F5_PEACE",
                recoverable=False,
                metrics=metrics
            )
        
        # Check for SABAR conditions
        if metrics.confidence > 0.15:
            return self.sabar(
                reason_code=ReasonCode.LOW_CONFIDENCE,
                message=f"High uncertainty: Ω₀ = {metrics.confidence} > 0.15",
                payload=payload,
                metrics=metrics
            )
        
        if metrics.coherence < 0.7:
            return self.sabar(
                reason_code=ReasonCode.COHERENCE_MARGIN,
                message=f"Low coherence: G* = {metrics.coherence} < 0.7",
                payload=payload,
                metrics=metrics
            )
        
        # Default to SEAL
        return self.seal(
            payload=payload,
            metrics=metrics,
            floors_checked=floors_checked
        )


# Convenience functions for quick usage
def quick_seal(
    tool_id: str,
    session_id: str,
    payload: Dict[str, Any],
    **kwargs
) -> VerdictEnvelope:
    """Quickly create a SEAL verdict."""
    wrapper = VerdictWrapper(
        tool_id=tool_id,
        stage=StageCode.STAGE_444_ROUTER,
        session_id=session_id
    )
    return wrapper.seal(payload=payload, **kwargs)


def quick_void(
    tool_id: str,
    session_id: str,
    reason_code: ReasonCode,
    message: str,
    **kwargs
) -> VerdictEnvelope:
    """Quickly create a VOID verdict."""
    wrapper = VerdictWrapper(
        tool_id=tool_id,
        stage=StageCode.STAGE_444_ROUTER,
        session_id=session_id
    )
    return wrapper.void(reason_code=reason_code, message=message, **kwargs)


if __name__ == "__main__":
    # Demo usage
    print("=" * 60)
    print("arifOS Verdict Wrapper Demo")
    print("=" * 60)
    
    wrapper = VerdictWrapper(
        tool_id="agi_mind",
        stage=StageCode.STAGE_333_MIND,
        session_id="demo-session-001",
        actor_id="888_JUDGE"
    )
    
    # Example 1: SEAL
    print("\n1. SEAL verdict:")
    seal_result = wrapper.seal(
        payload={"answer": 42, "reasoning": "..."},
        metrics=Metrics(delta_s=-0.2, confidence=0.04, coherence=0.95),
        reason_code=ReasonCode.OK_ALL_PASS,
        floors_checked=[1, 2, 4, 7, 8]
    )
    print(seal_result.to_json(indent=2))
    
    # Example 2: SABAR
    print("\n2. SABAR verdict:")
    sabar_result = wrapper.sabar(
        reason_code=ReasonCode.LOW_CONFIDENCE,
        message="Confidence below threshold",
        sabar_step=2,
        max_retries=3
    )
    print(sabar_result.to_json(indent=2))
    
    # Example 3: VOID
    print("\n3. VOID verdict:")
    void_result = wrapper.void(
        reason_code=ReasonCode.AUTH_FAIL,
        message="Invalid session token",
        floor="F11_AUTH",
        recoverable=True
    )
    print(void_result.to_json(indent=2))
    
    # Example 4: Auto verdict
    print("\n4. AUTO verdict (high entropy → VOID):")
    auto_result = wrapper.auto_verdict(
        payload={"partial": "data"},
        metrics=Metrics(delta_s=0.15, confidence=0.04)  # High entropy
    )
    print(auto_result.to_json(indent=2))
