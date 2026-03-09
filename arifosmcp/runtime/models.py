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


class Stage(str, Enum):
    INIT_000 = "000_INIT"
    SENSE_111 = "111_SENSE"
    REALITY_222 = "222_REALITY"
    MIND_333 = "333_MIND"
    ROUTER_444 = "444_ROUTER"
    MEMORY_555 = "555_MEMORY"
    HEART_555 = "555_HEART"
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


class RuntimeEnvelope(BaseModel):
    ok: bool = True
    tool: str
    session_id: str | None = None
    stage: str
    verdict: Verdict = Verdict.SABAR
    status: RuntimeStatus = RuntimeStatus.SUCCESS
    metrics: CanonicalMetrics = Field(default_factory=CanonicalMetrics)
    trace: dict[str, Verdict] = Field(default_factory=dict)
    authority: CanonicalAuthority = Field(default_factory=CanonicalAuthority)
    payload: dict[str, Any] = Field(default_factory=dict)
    errors: list[CanonicalError] = Field(default_factory=list)
    meta: CanonicalMeta = Field(default_factory=CanonicalMeta)
    auth_context: dict[str, Any] | None = Field(default=None, exclude=True)

    # Optional Debug layer (only if meta.debug is True)
    debug: dict[str, Any] | None = None

    model_config = ConfigDict(extra="allow")


# Deprecated legacy models preserved for internal logic until fully migrated
class Telemetry(BaseModel):
    dS: float = -0.7
    peace2: float = 1.1
    confidence: float = 0.9
    verdict: str = "Alive"


class Witness(BaseModel):
    human: float = 0.0
    ai: float = 0.0
    earth: float = 0.0


class AuthContext(BaseModel):
    actor_id: str = "anonymous"
    authority_level: AuthorityLevel = AuthorityLevel.ANONYMOUS
    session_id: str | None = None
    token_fingerprint: str | None = None
    signature: str | None = None

    model_config = ConfigDict(extra="allow")


class OPEXBundle(BaseModel):
    output_candidate: str = ""
    probability: float = 0.0
    evidence: list[str] = Field(default_factory=list)
    uncertainty: list[str] = Field(default_factory=list)


class APEXBundle(BaseModel):
    recommendation: str = "Pause"
    human_decision_required: bool = True


def derive_apex(envelope: Any, opex: Any) -> Any:
    """Mock implementation for backward compatibility during migration."""
    return APEXBundle()
