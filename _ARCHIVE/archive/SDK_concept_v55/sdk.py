"""
arifOS SDK — Gateway to Governed Intelligence
==============================================
The SDK is not a convenience wrapper. It's the user-facing expression
of L5 multi-agent intelligence.

Usage:
    from arifos_sdk import ArifOS

    client = ArifOS()

    # Simple ask — runs full 4-agent federation
    result = await client.ask("Analyze the quarterly data")

    # With session persistence
    async with client.session() as session:
        r1 = await session.ask("What's the revenue trend?")
        r2 = await session.ask("Compare to last quarter")  # Maintains context

    # Reflection — meta-AGI loop
    reflection = await client.reflect(result)

    # Audit trail
    history = await client.audit(session_id="abc123")

Architecture:
    client.ask()
        ↓
    L5 Federation (Architect → Engineer → Auditor → Validator)
        ↓
    APEX PRIME verdict (SEAL/VOID/PARTIAL)
        ↓
    VAULT-999 (audit trail)
        ↓
    Governed response to user

Version: v55.3-L5-alpha
Author: Muhammad Arif bin Fazil
License: AGPL-3.0-only

DITEMPA BUKAN DIBERI.
"""

import hashlib
import json
import uuid

# Import L5 agents (local SDK package)
try:
    from .architect import Architect
    from .base_agent import Verdict, FloorScores

    L5_AVAILABLE = True
except Exception:
    L5_AVAILABLE = False

    # Fallback types for when L5 isn't installed
    class Verdict(Enum):
        SEAL = "SEAL"
        PARTIAL = "PARTIAL"
        VOID = "VOID"
        SABAR = "SABAR"
        HOLD_888 = "888_HOLD"


class ResponseStatus(Enum):
    """SDK response status."""

    SUCCESS = "success"  # SEAL or PARTIAL
    BLOCKED = "blocked"  # VOID
    PENDING = "pending"  # 888_HOLD (needs human)
    ERROR = "error"  # System error


@dataclass
class AskResponse:
    """
    Response from client.ask()

    Contains:
    - answer: The governed response (or None if blocked)
    - status: SUCCESS, BLOCKED, PENDING, ERROR
    - verdict: APEX PRIME verdict
    - floor_scores: All 13 floor scores
    - violations: Any floor violations
    - plan: Architect's execution plan (if available)
    - session_id: For continuing conversation
    - timestamp: When response was generated
    """

    answer: Optional[str]
    status: ResponseStatus
    verdict: Verdict
    floor_scores: dict
    violations: list[str]
    plan: Optional[dict] = None
    session_id: Optional[str] = None
    query: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    processing_time_ms: float = 0.0

    def is_success(self) -> bool:
        """Check if response was successful."""
        return self.status == ResponseStatus.SUCCESS

    def is_blocked(self) -> bool:
        """Check if response was blocked (VOID)."""
        return self.status == ResponseStatus.BLOCKED

    def needs_human(self) -> bool:
        """Check if response needs human review."""
        return self.status == ResponseStatus.PENDING

    def to_dict(self) -> dict:
        """Serialize for storage/transmission."""
        return {
            "answer": self.answer,
            "status": self.status.value,
            "verdict": self.verdict.value,
            "floor_scores": self.floor_scores,
            "violations": self.violations,
            "plan": self.plan,
            "session_id": self.session_id,
            "query": self.query,
            "timestamp": self.timestamp.isoformat(),
            "processing_time_ms": self.processing_time_ms,
        }


@dataclass
class ReflectResponse:
    """
    Response from client.reflect()

    Meta-AGI reflection on a previous response.
    """

    original_query: str
    original_answer: str
    reflection: str
    improvements: list[str]
    confidence_delta: float  # How much confidence changed
    should_revise: bool
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class AuditEntry:
    """Single entry in audit trail."""

    session_id: str
    query: str
    verdict: str
    floor_scores: dict
    timestamp: str
    hash: str


class Session:
    """
    Persistent conversation session.

    Maintains context across multiple asks.
    """

    def __init__(self, client: "ArifOS", session_id: Optional[str] = None):
        self.client = client
        self.session_id = session_id or str(uuid.uuid4())
        self.history: list[AskResponse] = []
        self.created_at = datetime.now(timezone.utc)
        self._context: dict = {}

    async def ask(self, query: str, **kwargs) -> AskResponse:
        """
        Ask within this session (maintains context).

        Args:
            query: User query
            **kwargs: Additional parameters

        Returns:
            AskResponse with session context
        """
        # Build context from history
        context = {
            "session_id": self.session_id,
            "history": [
                {"query": r.query, "answer": r.answer}
                for r in self.history[-5:]  # Last 5 exchanges
            ],
            **self._context,
        }

        # Run through client
        response = await self.client.ask(
            query, session_id=self.session_id, context=context, **kwargs
        )

        # Store in history
        self.history.append(response)

        return response

    def set_context(self, key: str, value: Any) -> None:
        """Set session context value."""
        self._context[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        """Get session context value."""
        return self._context.get(key, default)

    def summary(self) -> str:
        """Get session summary."""
        return (
            f"Session {self.session_id[:8]}...\n"
            f"Created: {self.created_at.isoformat()}\n"
            f"Exchanges: {len(self.history)}\n"
            f"Last verdict: {self.history[-1].verdict.value if self.history else 'N/A'}"
        )


class ArifOS:
    """
    arifOS SDK Client
    =================

    The gateway to governed AI intelligence.

    Quick Start:
        client = ArifOS()
        result = await client.ask("What is the meaning of life?")
        print(result.answer)

    With Session:
        async with client.session() as s:
            r1 = await s.ask("Tell me about entropy")
            r2 = await s.ask("How does that relate to information?")

    Configuration:
        client = ArifOS(
            endpoint="https://api.arifos.dev",  # Custom endpoint
            tri_witness_threshold=0.95,          # Consensus threshold
            enable_reflection=True,              # Enable meta-AGI
        )
    """

    def __init__(
        self,
        endpoint: Optional[str] = None,
        tri_witness_threshold: float = 0.95,
        enable_reflection: bool = True,
        vault_enabled: bool = True,
    ):
        """
        Initialize arifOS client.

        Args:
            endpoint: API endpoint (None for local mode)
            tri_witness_threshold: Minimum W₃ for consensus
            enable_reflection: Enable meta-AGI reflection
            vault_enabled: Enable VAULT-999 audit trail
        """
        self.endpoint = endpoint
        self.tri_witness_threshold = tri_witness_threshold
        self.enable_reflection = enable_reflection
        self.vault_enabled = vault_enabled

        # Initialize L5 federation if available
        if L5_AVAILABLE:
            self._federation = AgentFederation(tri_witness_threshold=tri_witness_threshold)
        else:
            self._federation = None

        # Local vault (would be PostgreSQL in production)
        self._vault: list[AuditEntry] = []

        # Active sessions
        self._sessions: dict[str, Session] = {}

    async def ask(
        self,
        query: str,
        session_id: Optional[str] = None,
        context: Optional[dict] = None,
        human_override: bool = False,
    ) -> AskResponse:
        """
        Ask a question — runs full L5 federation.

        This is the primary interface to arifOS intelligence.

        Flow:
            query → Architect (plan) → Engineer (execute) →
            Auditor (check) → Validator (seal) → response

        Args:
            query: User query
            session_id: Optional session for context
            context: Additional context
            human_override: Skip human review requirement

        Returns:
            AskResponse with governed answer
        """
        import time

        start_time = time.time()

        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())

        # Check L5 availability
        if not L5_AVAILABLE or not self._federation:
            return AskResponse(
                answer=None,
                status=ResponseStatus.ERROR,
                verdict=Verdict.VOID,
                floor_scores={},
                violations=["L5 federation not available"],
                session_id=session_id,
                query=query,
            )

        # Run through L5 federation
        try:
            # Run full federation
            result = await self._federation.execute(
                query=query,
                context=context or {},
                human_override=human_override,
            )

            # Extract answer from plan
            answer = None
            plan_dict = None

            if result.plan:
                plan_dict = result.plan.to_dict()

            # Prefer Validator output; fall back to Engineer draft or plan summary
            if result.validator_output and result.validator_output.response:
                answer = str(result.validator_output.response)
            elif result.engineer_output and result.engineer_output.response:
                answer = str(result.engineer_output.response)
            elif result.plan:
                answer = (
                    f"Plan generated with {len(result.plan.steps)} steps.\n"
                    f"Approach: {result.plan.approach}\n"
                    f"Complexity: {result.plan.estimated_total_complexity}"
                )
                if result.plan.requires_human_review:
                    answer += "\n⚠️ Human review required before execution."

            # Map verdict to status
            if result.final_verdict == Verdict.SEAL:
                status = ResponseStatus.SUCCESS
            elif result.final_verdict == Verdict.PARTIAL:
                status = ResponseStatus.SUCCESS  # Partial is still usable
            elif result.final_verdict == Verdict.HOLD_888:
                status = ResponseStatus.PENDING
            else:
                status = ResponseStatus.BLOCKED

            # Extract floor scores
            floor_scores = {}
            violations = []

            # Prefer validator scores, then auditor, then architect
            if result.validator_output:
                floor_scores = result.validator_output.floor_scores.to_dict()
                violations = result.validator_output.violations
            elif result.auditor_output:
                floor_scores = result.auditor_output.floor_scores.to_dict()
                violations = result.auditor_output.violations
            elif result.architect_output:
                floor_scores = result.architect_output.floor_scores.to_dict()
                violations = result.architect_output.violations

            processing_time = (time.time() - start_time) * 1000

            response = AskResponse(
                answer=answer,
                status=status,
                verdict=result.final_verdict,
                floor_scores=floor_scores,
                violations=violations,
                plan=plan_dict,
                session_id=session_id,
                query=query,
                processing_time_ms=processing_time,
            )

            # Write to vault
            if self.vault_enabled:
                self._write_vault(response)

            return response

        except Exception as e:
            return AskResponse(
                answer=None,
                status=ResponseStatus.ERROR,
                verdict=Verdict.VOID,
                floor_scores={},
                violations=[f"Federation error: {str(e)}"],
                session_id=session_id,
                query=query,
                processing_time_ms=(time.time() - start_time) * 1000,
            )

    async def reflect(self, response: AskResponse) -> ReflectResponse:
        """
        Meta-AGI reflection on a previous response.

        Analyzes the response for:
        - Logical consistency
        - Missing considerations
        - Potential improvements
        - Confidence calibration

        Args:
            response: Previous AskResponse to reflect on

        Returns:
            ReflectResponse with meta-analysis
        """
        if not self.enable_reflection:
            return ReflectResponse(
                original_query=response.query,
                original_answer=response.answer or "",
                reflection="Reflection disabled",
                improvements=[],
                confidence_delta=0.0,
                should_revise=False,
            )

        # Simple reflection logic (would use LLM in production)
        improvements = []
        should_revise = False
        confidence_delta = 0.0

        # Check for low scores
        if response.floor_scores:
            if response.floor_scores.get("f6_empathy", 1.0) < 0.80:
                improvements.append("Consider stakeholder impact more deeply")
                should_revise = True
                confidence_delta -= 0.05

            if response.floor_scores.get("f2_truth", 1.0) < 0.99:
                improvements.append("Verify factual claims with sources")
                should_revise = True
                confidence_delta -= 0.10

            if response.floor_scores.get("f4_clarity", 0.0) > 0:
                improvements.append("Response may increase confusion - simplify")
                should_revise = True
                confidence_delta -= 0.05

        # Check for violations
        if response.violations:
            improvements.append(f"Address violations: {', '.join(response.violations)}")
            should_revise = True
            confidence_delta -= 0.15

        reflection = (
            f"Analyzed response to: {response.query[:50]}...\n"
            f"Verdict: {response.verdict.value}\n"
            f"Improvements needed: {len(improvements)}\n"
            f"Confidence adjustment: {confidence_delta:+.2f}"
        )

        return ReflectResponse(
            original_query=response.query,
            original_answer=response.answer or "",
            reflection=reflection,
            improvements=improvements,
            confidence_delta=confidence_delta,
            should_revise=should_revise,
        )

    async def audit(
        self,
        session_id: Optional[str] = None,
        limit: int = 100,
    ) -> list[AuditEntry]:
        """
        Query VAULT-999 audit trail.

        Args:
            session_id: Filter by session (None for all)
            limit: Maximum entries to return

        Returns:
            List of AuditEntry records
        """
        entries = self._vault

        if session_id:
            entries = [e for e in entries if e.session_id == session_id]

        return entries[-limit:]

    def _write_vault(self, response: AskResponse) -> None:
        """Write response to local vault."""
        content = json.dumps(response.to_dict(), sort_keys=True)
        hash_value = hashlib.sha256(content.encode()).hexdigest()

        entry = AuditEntry(
            session_id=response.session_id or "unknown",
            query=response.query,
            verdict=response.verdict.value,
            floor_scores=response.floor_scores,
            timestamp=response.timestamp.isoformat(),
            hash=hash_value,
        )

        self._vault.append(entry)

    @asynccontextmanager
    async def session(self, session_id: Optional[str] = None) -> AsyncIterator[Session]:
        """
        Create a conversation session with persistent context.

        Usage:
            async with client.session() as s:
                r1 = await s.ask("First question")
                r2 = await s.ask("Follow-up")  # Has context from r1

        Args:
            session_id: Optional ID (generated if not provided)

        Yields:
            Session object for conversation
        """
        session = Session(self, session_id)
        self._sessions[session.session_id] = session

        try:
            yield session
        finally:
            # Session cleanup (context saved in vault)
            pass

    def get_session(self, session_id: str) -> Optional[Session]:
        """Retrieve an existing session by ID."""
        return self._sessions.get(session_id)

    @property
    def is_l5_available(self) -> bool:
        """Check if L5 federation is available."""
        return L5_AVAILABLE and self._federation is not None

    def status(self) -> dict:
        """Get client status."""
        return {
            "version": "55.3.0-L5-alpha",
            "l5_available": self.is_l5_available,
            "endpoint": self.endpoint or "local",
            "tri_witness_threshold": self.tri_witness_threshold,
            "reflection_enabled": self.enable_reflection,
            "vault_enabled": self.vault_enabled,
            "vault_entries": len(self._vault),
            "active_sessions": len(self._sessions),
        }


# Convenience function for quick usage
async def ask(query: str, **kwargs) -> AskResponse:
    """
    Quick ask without creating client.

    Usage:
        from arifos_sdk import ask
        result = await ask("What is entropy?")
    """
    client = ArifOS()
    return await client.ask(query, **kwargs)


# Export public API
__all__ = [
    "ArifOS",
    "AskResponse",
    "ReflectResponse",
    "AuditEntry",
    "Session",
    "ResponseStatus",
    "Verdict",
    "ask",
]
