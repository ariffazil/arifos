from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Verdict(str, Enum):
    SEAL = "SEAL"
    PROVISIONAL = "PROVISIONAL"
    PARTIAL = "PARTIAL"
    SABAR = "SABAR"
    HOLD = "HOLD"
    HOLD_888 = "HOLD_888"
    VOID = "VOID"


class RuntimeStatus(str, Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    TIMEOUT = "TIMEOUT"
    DRY_RUN = "DRY_RUN"
    SABAR = "SABAR"


class MachineState(str, Enum):
    READY = "READY"
    BLOCKED = "BLOCKED"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"


class MachineIssueLabel(str, Enum):
    AUTH_BOOTSTRAP_REQUIRED = "AUTH_BOOTSTRAP_REQUIRED"
    AUTH_TOKEN_MISSING = "AUTH_TOKEN_MISSING"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    TOOL_NOT_EXPOSED = "TOOL_NOT_EXPOSED"
    BOOTSTRAP_ROUTE_MISSING = "BOOTSTRAP_ROUTE_MISSING"
    DEPLOYMENT_CONFIG_ERROR = "DEPLOYMENT_CONFIG_ERROR"
    SCHEMA_INVALID = "SCHEMA_INVALID"
    INTERNAL_RUNTIME_ERROR = "INTERNAL_RUNTIME_ERROR"
    TIMEOUT = "TIMEOUT"
    DNS_FAIL = "DNS_FAIL"
    TLS_FAIL = "TLS_FAIL"
    WAF_BLOCK = "WAF_BLOCK"


class IntelligenceStage(str, Enum):
    EXPLORATION = "EXPLORATION"
    ENTROPY = "ENTROPY"
    EUREKA = "EUREKA"


class ExplorationState(str, Enum):
    BROAD = "BROAD"
    SCOPED = "SCOPED"
    EXHAUSTED = "EXHAUSTED"


class EntropyState(str, Enum):
    LOW = "LOW"
    MANAGEABLE = "MANAGEABLE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class EurekaState(str, Enum):
    NONE = "NONE"
    PARTIAL = "PARTIAL"
    FORGED = "FORGED"


class Stage(str, Enum):
    INIT_000 = "000_INIT"
    SENSE_111 = "111_SENSE"
    REALITY_222 = "222_REALITY"
    MIND_333 = "333_MIND"
    ROUTER_444 = "444_ROUTER"
    MEMORY_555 = "555_MEMORY"
    HEART_666 = "666_HEART"
    CRITIQUE_666 = "666_CRITIQUE"
    FORGE_777 = "777_FORGE"
    JUDGE_888 = "888_JUDGE"
    VAULT_999 = "999_VAULT"


class AuthorityLevel(str, Enum):
    HUMAN = "human"
    AGENT = "agent"
    SYSTEM = "system"
    ANONYMOUS = "anonymous"
    OPERATOR = "operator"
    SOVEREIGN = "sovereign"
    DECLARED = "declared"
    APEX = "apex"


class PersonaRole(str, Enum):
    """AI self-declared operational roles - governed whitelist."""

    ARCHITECT = "architect"
    ENGINEER = "engineer"
    AUDITOR = "auditor"
    VALIDATOR = "validator"
    ASSISTANT = "assistant"


class CanonicalMetrics(BaseModel):
    truth: float = 0.0
    clarity_delta: float = 0.0
    confidence: float = 0.0
    peace: float = 0.0
    vitality: float = 0.0
    entropy_delta: float = 0.0
    authority: float = 0.0
    risk: float = 0.0


class CanonicalAuthority(BaseModel):
    actor_id: str = "anonymous"
    level: AuthorityLevel = AuthorityLevel.ANONYMOUS
    human_required: bool = False
    approval_scope: list[str] = Field(default_factory=list)
    auth_state: str = "unverified"


class CanonicalError(BaseModel):
    code: str
    message: str
    stage: str | None = None
    recoverable: bool = True


class CanonicalMeta(BaseModel):
    schema_version: str = "1.0.0"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    debug: bool = False
    dry_run: bool = False
    motto: str | None = None


class PersonaId(str, Enum):
    """
    Governed AI operational personas. F9-compliant: honest naming, no sovereign claim.

    Scar-Weight Theory (W_beban):
    — Each persona carries a specific burden to protect the system.
    — Disagreement by design ensures constitutional coverage.
    — Human (888 Judge) resolves irreconcilable conflicts.

    Trinity Mapping:
        AGI Mind (Δ):  ARCHITECT + ENGINEER → "Should & Can"
        ASI Heart (Ω): AUDITOR → "What could break"
        APEX Soul (Ψ): VALIDATOR + ORCHESTRATOR → "Is it true & In what order"

    Scars (Burdens):
        ARCHITECT: Accountability jangka panjang | "Should this exist?"
        ENGINEER: Pager scars, outages | "Can we make it work?"
        AUDITOR: "Batu api" reputation | "What could break / be abused?"
        VALIDATOR: Approval pressure | "Is it actually true / correct?"
    """

    ARCHITECT = "architect"
    ENGINEER = "engineer"
    AUDITOR = "auditor"
    VALIDATOR = "validator"


class RuntimeRole(str, Enum):
    """AI runtime role within the current call."""

    ASSISTANT = "assistant"
    ROUTER = "router"
    TOOL_BROKER = "tool_broker"
    EVALUATOR = "evaluator"


class ToolchainRole(str, Enum):
    """Position of the AI agent in a multi-agent toolchain."""

    ORCHESTRATOR = "orchestrator"
    LEAF = "leaf"
    SUBAGENT = "subagent"


class UserModelSource(str, Enum):
    """Allowed provenance sources for bounded user-model fields."""

    EXPLICIT = "explicit"
    OBSERVABLE = "observable"
    DEFAULT_POLICY = "default_policy"
    UNKNOWN = "unknown"


class AdaptationMode(str, Enum):
    """Governed adaptation scope for runtime user modeling."""

    BEHAVIORAL_ONLY = "behavioral_only"


class UserModelField(BaseModel):
    """Single user-model field with provenance and bounded evidence."""

    value: Any | None = None
    source: UserModelSource = UserModelSource.UNKNOWN
    evidence: str | None = None


class InferencePolicy(BaseModel):
    """Explicit anti-Theory-of-Mind guardrails for runtime adaptation."""

    psychological_inference: str = "disallowed"
    behavioral_adaptation: str = "allowed"
    null_for_unknown: bool = True
    source_priority: list[UserModelSource] = Field(
        default_factory=lambda: [
            UserModelSource.EXPLICIT,
            UserModelSource.OBSERVABLE,
            UserModelSource.DEFAULT_POLICY,
        ]
    )


class UserModel(BaseModel):
    """
    Bounded user-model contract.

    The runtime may adapt to explicit asks and observable interaction signals,
    but must not attribute hidden motives or psychological states.
    """

    stated_goal: UserModelField | None = None
    behavioral_constraints: list[UserModelField] = Field(default_factory=list)
    output_constraints: list[UserModelField] = Field(default_factory=list)
    requested_tone: UserModelField | None = None
    expertise_level: UserModelField | None = None
    emotion_state: UserModelField | None = None
    hidden_motive: UserModelField | None = None
    adaptation_mode: AdaptationMode = AdaptationMode.BEHAVIORAL_ONLY
    inference_policy: InferencePolicy = Field(default_factory=InferencePolicy)


class CallerContext(BaseModel):
    """
    AI execution identity layer — instrument only, never sovereign (F9/F10).

    Populated by the MCP server from transport metadata. The LLM may submit a
    ``requested_persona`` hint; the server governs the final ``persona_id``.
    """

    agent_id: str | None = Field(default=None, description="Stable runtime instance ID.")
    model_id: str | None = Field(default=None, description="Model/version string.")
    persona_id: PersonaId = Field(
        default=PersonaId.ENGINEER,
        description="Governed operational persona. Server-assigned; LLM hint only.",
    )
    runtime_role: RuntimeRole = Field(
        default=RuntimeRole.ASSISTANT,
        description="Operational role for this call.",
    )
    toolchain_role: ToolchainRole = Field(
        default=ToolchainRole.LEAF,
        description="Position in multi-agent/tool chain.",
    )
    # Forward-compatible extension slot
    extra: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(extra="allow")


class RuntimeEnvelope(BaseModel):
    ok: bool = True
    tool: str
    session_id: str | None = None
    stage: str
    verdict: Verdict = Verdict.SABAR
    status: RuntimeStatus = RuntimeStatus.SUCCESS
    machine_status: MachineState = MachineState.READY
    machine_issue: MachineIssueLabel | None = None
    intelligence_stage: IntelligenceStage | None = None
    intelligence_state: dict[str, Any] = Field(
        default_factory=lambda: {
            # 3E Schema: Exploration → Entropy → Eureka
            "exploration": "BROAD",
            "entropy": "MANAGEABLE",
            "eureka": "NONE",
            "hypotheses": [],
            "unknowns": [],
            "stable_facts": [],
            "unstable_assumptions": [],
            "conflicts": [],
            "uncertainty_score": 0.5,  # F7 Humility Band
            "insight": None,
            "confidence": 0.0,
            "decision_required": [],
        }
    )
    metrics: CanonicalMetrics = Field(default_factory=CanonicalMetrics)
    trace: dict[str, Verdict] = Field(default_factory=dict)
    authority: CanonicalAuthority = Field(default_factory=CanonicalAuthority)
    payload: dict[str, Any] = Field(default_factory=dict)
    errors: list[CanonicalError] = Field(default_factory=list)
    meta: CanonicalMeta = Field(default_factory=CanonicalMeta)
    auth_context: dict[str, Any] | None = Field(default=None)
    caller_context: CallerContext | None = Field(
        default=None,
        description="AI execution identity. Auto-populated by MCP server.",
    )
    user_model: UserModel | None = Field(
        default=None,
        description=(
            "Bounded user model built from explicit asks and observable constraints only. "
            "Psychological inference is disallowed by policy."
        ),
    )
    philosophy: dict[str, Any] | None = Field(
        default=None,
        description="Optional governed quote layer selected by APEX-G.",
    )
    debug: dict[str, Any] | None = None
    model_config = ConfigDict(extra="allow")
