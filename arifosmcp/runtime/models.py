from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class Verdict(str, Enum):
    SEAL = "SEAL"
    PARTIAL = "PARTIAL"
    SABAR = "SABAR"
    VOID = "VOID"
    HOLD_888 = "HOLD-888"
    UNSET = "UNSET"


class Stage(str, Enum):
    INIT = "000_INIT"
    MIND_111 = "111_MIND"
    MIND_333 = "333_MIND"
    ROUTER = "444_ROUTER"
    MEMORY = "555_MEMORY"
    HEART = "666_HEART"
    APEX = "777_APEX"
    JUDGE = "888_JUDGE"
    VAULT = "999_VAULT"


class AuthorityLevel(str, Enum):
    HUMAN = "human"
    AGENT = "agent"
    SYSTEM = "system"
    ANONYMOUS = "anonymous"


class StakesClass(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    UNKNOWN = "UNKNOWN"


class AuthContext(BaseModel):
    actor_id: str = "anonymous"
    authority_level: AuthorityLevel = AuthorityLevel.ANONYMOUS
    stakes_class: StakesClass = StakesClass.UNKNOWN
    session_id: str | None = None
    token_fingerprint: str | None = None
    nonce: str | None = None
    iat: int | None = None
    exp: int | None = None
    approval_scope: List[str] = Field(default_factory=list)
    parent_signature: str | None = None
    signature: str | None = None
    math: Dict[str, float] | None = None

    model_config = ConfigDict(extra="allow")


class Telemetry(BaseModel):
    dS: float = Field(default=-0.7, description="Entropy delta")
    peace2: float = Field(default=1.1, description="Stability/Safety margin squared")
    confidence: float = Field(default=0.9, description="Confidence score")
    verdict: str = "Alive"


class Witness(BaseModel):
    human: float = 0.0
    ai: float = 0.0
    earth: float = 0.0


class Philosophy(BaseModel):
    quote_id: str
    quote: str
    author: str
    category: str


class RuntimeEnvelope(BaseModel):
    verdict: Verdict = Verdict.UNSET
    stage: Stage
    session_id: str
    telemetry: Telemetry = Field(default_factory=Telemetry)
    witness: Witness = Field(default_factory=Witness)
    auth_context: AuthContext = Field(default_factory=AuthContext)
    philosophy: Optional[Philosophy] = None
    data: Dict[str, Any] = Field(default_factory=dict)
