from __future__ import annotations

from enum import Enum
from typing import Any

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
    approval_scope: list[str] = Field(default_factory=list)
    parent_signature: str | None = None
    signature: str | None = None
    math: dict[str, float] | None = None

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


# ── OPEX: Operational Epistemics ─────────────────────────────────────────────


class OPEXBundle(BaseModel):
    """Epistemic intake schema: what the tool thinks, with what confidence, why, and what it doesn't know."""

    output_candidate: str = ""
    probability: float = Field(default=0.0, ge=0.0, le=1.0)
    evidence: list[str] = Field(default_factory=list)
    uncertainty: list[str] = Field(default_factory=list)


# ── APEX: Applied Prudential EXecution ───────────────────────────────────────


class APEXAkal(BaseModel):
    coherence: str = "unknown"  # "passes" | "fails" | "unknown"
    contradiction: str = "none detected"


class APEXPresent(BaseModel):
    context_fit: str = "unknown"  # "high" | "medium" | "low" | "unknown"
    user_intent_match: str = "unknown"


class APEXEnergy(BaseModel):
    effort_to_verify: str = "medium"  # "low" | "medium" | "high"
    entropy_if_wrong: str = "medium"  # "low" | "medium" | "high"


class APEXExplorationAmanah(BaseModel):
    explored_alternatives: int = 0
    trust_boundary: str = "do not overclaim"


class APEXJudgment(BaseModel):
    recommendation: str = "Pause"  # "Approved" | "Partial" | "Pause" | "Hold" | "Void"
    human_decision_required: bool = True


class APEXBundle(BaseModel):
    """Governance output schema: is the result fit to present, act on, or escalate?"""

    akal: APEXAkal = Field(default_factory=APEXAkal)
    present: APEXPresent = Field(default_factory=APEXPresent)
    energy: APEXEnergy = Field(default_factory=APEXEnergy)
    exploration_amanah: APEXExplorationAmanah = Field(default_factory=APEXExplorationAmanah)
    judgment: APEXJudgment = Field(default_factory=APEXJudgment)


def derive_apex(envelope: RuntimeEnvelope, opex: OPEXBundle) -> APEXBundle:
    """Derive APEX governance bundle from envelope telemetry + OPEX fields."""
    # akal.coherence: passes if verdict is not VOID or SABAR
    coherence = "passes" if envelope.verdict not in (Verdict.VOID, Verdict.SABAR) else "fails"
    contradiction = "none detected" if coherence == "passes" else "constitutional floor violation"

    # present.context_fit: high if peace2 >= 1.0, medium if >= 0.7, low otherwise
    p2 = envelope.telemetry.peace2
    context_fit = "high" if p2 >= 1.0 else ("medium" if p2 >= 0.7 else "low")

    # energy.entropy_if_wrong: inversely correlated with peace2 stability
    entropy_if_wrong = "low" if p2 >= 1.2 else ("medium" if p2 >= 1.0 else "high")

    # effort_to_verify: based on evidence density from OPEX
    n_evidence = len(opex.evidence)
    effort_to_verify = "low" if n_evidence >= 3 else ("medium" if n_evidence >= 1 else "high")

    # exploration_amanah.trust_boundary: cleared only when high confidence + strong tri-witness
    w = envelope.witness
    tri = (w.human * w.ai * w.earth) ** (1 / 3) if (w.human and w.ai and w.earth) else 0.0
    trust_boundary = "cleared" if (opex.probability >= 0.85 and tri >= 0.95) else "do not overclaim"

    # judgment: map Verdict → recommendation + human gate
    _verdict_map: dict[Verdict, tuple[str, bool]] = {
        Verdict.SEAL: ("Approved", False),
        Verdict.PARTIAL: ("Partial", False),
        Verdict.SABAR: ("Pause", True),
        Verdict.VOID: ("Void", True),
        Verdict.HOLD_888: ("Hold", True),
        Verdict.UNSET: ("Pause", True),
    }
    rec, human_required = _verdict_map.get(envelope.verdict, ("Pause", True))

    return APEXBundle(
        akal=APEXAkal(coherence=coherence, contradiction=contradiction),
        present=APEXPresent(context_fit=context_fit, user_intent_match=context_fit),
        energy=APEXEnergy(effort_to_verify=effort_to_verify, entropy_if_wrong=entropy_if_wrong),
        exploration_amanah=APEXExplorationAmanah(
            explored_alternatives=n_evidence,
            trust_boundary=trust_boundary,
        ),
        judgment=APEXJudgment(recommendation=rec, human_decision_required=human_required),
    )


class RuntimeEnvelope(BaseModel):
    verdict: Verdict = Verdict.UNSET
    stage: Stage
    session_id: str
    failure_origin: str | None = None
    remediation_notes: list[str] = Field(default_factory=list)
    telemetry: Telemetry = Field(default_factory=Telemetry)
    witness: Witness = Field(default_factory=Witness)
    auth_context: AuthContext = Field(default_factory=AuthContext)
    philosophy: Philosophy | None = None
    data: dict[str, Any] = Field(default_factory=dict)
    opex: OPEXBundle | None = None  # Epistemic layer: what/why/confidence/unknowns
    apex: APEXBundle | None = None  # Governance layer: fit-to-release judgment
