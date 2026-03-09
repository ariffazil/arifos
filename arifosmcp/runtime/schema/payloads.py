"""
arifosmcp/runtime/schema/payloads.py — Tool-Specific Payload Schemas

Each tool returns its structured data inside the `payload` field of ArifOSOutput.
These schemas define what goes inside payload for each tool.

Tool → Payload class mapping:
  anchor_session      → AnchorSessionPayload
  reason_mind         → ReasonMindPayload
  vector_memory       → VectorMemoryPayload
  simulate_heart      → SimulateHeartPayload
  critique_thought    → CritiqueThoughtPayload
  apex_judge          → ApexJudgePayload
  eureka_forge        → EurekaForgePayload
  seal_vault          → SealVaultPayload
  search_reality      → SearchRealityPayload
  ingest_evidence     → IngestEvidencePayload
  audit_rules         → AuditRulesPayload
  check_vital         → CheckVitalPayload
  metabolic_loop      → MetabolicLoopPayload

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

# ──────────────────────────────────────────────────────────────────────────────
# A. anchor_session
# ──────────────────────────────────────────────────────────────────────────────


class AnchorSessionPayload(BaseModel):
    """Payload for anchor_session tool (000_INIT stage)."""

    state: Literal["active", "resumed", "error"] = "active"
    grounding_required: bool = False


# ──────────────────────────────────────────────────────────────────────────────
# B. reason_mind
# ──────────────────────────────────────────────────────────────────────────────


class Hypothesis(BaseModel):
    """A single reasoning hypothesis from reason_mind."""

    path: Literal["conservative", "exploratory", "adversarial"]
    band: Literal["CLAIM", "HYPOTHESIS", "PLAUSIBLE"]
    confidence: float = Field(ge=0.0, le=1.0)
    hypothesis: str


class ReasonMindPayload(BaseModel):
    """Payload for reason_mind tool (333_MIND stage)."""

    reasoning_status: Literal["exploratory", "converged", "blocked"] = "exploratory"
    confidence_band: Literal["CLAIM", "HYPOTHESIS", "PLAUSIBLE"] = "PLAUSIBLE"
    needs_grounding: bool = True
    next_stage: str | None = None
    hypotheses: list[Hypothesis] = Field(default_factory=list)


# ──────────────────────────────────────────────────────────────────────────────
# C. vector_memory
# ──────────────────────────────────────────────────────────────────────────────


class MemoryMatch(BaseModel):
    """A single memory match result."""

    id: str
    score: float = Field(ge=0.0, le=1.0)
    source: str
    summary: str


class VectorMemoryPayload(BaseModel):
    """Payload for vector_memory tool (555_HEART / memory stage)."""

    matches: list[MemoryMatch] = Field(default_factory=list)
    count: int = 0


# ──────────────────────────────────────────────────────────────────────────────
# D. simulate_heart
# ──────────────────────────────────────────────────────────────────────────────


class StakeholderImpact(BaseModel):
    """Impact assessment for a single stakeholder."""

    name: str
    impact: Literal["low", "medium", "high", "critical"]
    risk: float = Field(ge=0.0, le=1.0)


class SimulateHeartPayload(BaseModel):
    """Payload for simulate_heart tool (555_HEART stage)."""

    stakeholder_status: Literal["safe", "caution", "risky", "critical"] = "safe"
    stakeholders: list[StakeholderImpact] = Field(default_factory=list)
    needs_human_review: bool = False


# ──────────────────────────────────────────────────────────────────────────────
# E. critique_thought
# ──────────────────────────────────────────────────────────────────────────────


class CritiqueThoughtPayload(BaseModel):
    """Payload for critique_thought tool (666_CRITIQUE stage)."""

    critique_status: Literal["passed", "challenged", "blocked"] = "challenged"
    weaknesses: list[str] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)
    recommendation: Literal["approve", "refine", "reject", "pause"] = "refine"


# ──────────────────────────────────────────────────────────────────────────────
# F. apex_judge
# ──────────────────────────────────────────────────────────────────────────────


class ApexJudgePayload(BaseModel):
    """Payload for apex_judge tool (888_JUDGE stage)."""

    judgment: Literal["SEAL", "HOLD", "VOID", "SABAR"] = "HOLD"
    human_decision_required: bool = True
    governance_token: str | None = None
    lawful: bool = False


# ──────────────────────────────────────────────────────────────────────────────
# G. eureka_forge
# ──────────────────────────────────────────────────────────────────────────────


class EurekaForgePayload(BaseModel):
    """Payload for eureka_forge tool (777_FORGE stage)."""

    execution_status: Literal["executed", "blocked", "dry_run", "error"] = "blocked"
    command: str | None = None
    working_dir: str | None = None
    approval_required: bool = True
    output: str | None = None


# ──────────────────────────────────────────────────────────────────────────────
# H. seal_vault
# ──────────────────────────────────────────────────────────────────────────────


class SealVaultPayload(BaseModel):
    """Payload for seal_vault tool (999_VAULT stage)."""

    sealed: bool = False
    vault_ref: str | None = None
    summary_hash: str | None = None


# ──────────────────────────────────────────────────────────────────────────────
# I. search_reality
# ──────────────────────────────────────────────────────────────────────────────


class SearchResult(BaseModel):
    """A single search result from search_reality."""

    title: str
    url: str
    source: str
    score: float = Field(ge=0.0, le=1.0, default=0.0)
    snippet: str | None = None


class SearchRealityPayload(BaseModel):
    """Payload for search_reality tool (222_REALITY stage)."""

    grounding_status: Literal["strong", "partial", "none"] = "none"
    results: list[SearchResult] = Field(default_factory=list)
    results_count: int = 0


# ──────────────────────────────────────────────────────────────────────────────
# J. ingest_evidence
# ──────────────────────────────────────────────────────────────────────────────


class IngestEvidencePayload(BaseModel):
    """Payload for ingest_evidence tool (222_REALITY stage)."""

    source_type: Literal["file", "url", "text"] = "text"
    target: str | None = None
    mode: Literal["summary", "full", "structured"] = "summary"
    content: str = ""
    truncated: bool = False


# ──────────────────────────────────────────────────────────────────────────────
# K. audit_rules
# ──────────────────────────────────────────────────────────────────────────────


class AuditViolation(BaseModel):
    """A single floor violation found during audit."""

    floor: str
    severity: Literal["critical", "warning", "info"]
    description: str


class AuditRulesPayload(BaseModel):
    """Payload for audit_rules tool (666_CRITIQUE stage)."""

    audit_scope: Literal["quick", "full", "targeted"] = "quick"
    floors_checked: list[str] = Field(default_factory=list)
    violations: list[AuditViolation] = Field(default_factory=list)
    passed: bool = True


# ──────────────────────────────────────────────────────────────────────────────
# L. check_vital
# ──────────────────────────────────────────────────────────────────────────────


class CheckVitalPayload(BaseModel):
    """Payload for check_vital tool (555_HEALTH stage)."""

    cpu: float | None = Field(default=None, ge=0.0, le=1.0)
    memory: float | None = Field(default=None, ge=0.0, le=1.0)
    swap: float | None = Field(default=None, ge=0.0, le=1.0)
    io: float | None = None
    temp: float | None = None


# ──────────────────────────────────────────────────────────────────────────────
# M. metabolic_loop
# ──────────────────────────────────────────────────────────────────────────────


class MetabolicLoopPayload(BaseModel):
    """Payload for metabolic_loop / arifOS.kernel tool."""

    loop_status: Literal["active", "complete", "blocked", "error"] = "active"
    current_stage: str | None = None
    next_stage: str | None = None
    completed_stages: list[str] = Field(default_factory=list)
    output: Any | None = None


# ──────────────────────────────────────────────────────────────────────────────
# Session memory (session_memory tool)
# ──────────────────────────────────────────────────────────────────────────────


class MemoryEntry(BaseModel):
    """A single stored memory entry."""

    timestamp: str
    content: str
    importance: float = Field(ge=0.0, le=1.0, default=0.5)


class SessionMemoryPayload(BaseModel):
    """Payload for session_memory tool."""

    operation: Literal["store", "retrieve", "clear"] = "retrieve"
    success: bool = True
    memories: list[MemoryEntry] | None = None


# ──────────────────────────────────────────────────────────────────────────────
# open_apex_dashboard
# ──────────────────────────────────────────────────────────────────────────────


class ApexDashboardPayload(BaseModel):
    """Payload for open_apex_dashboard tool."""

    dashboard_url: str = ""
    access_token: str | None = None
    expires_at: str | None = None


# ──────────────────────────────────────────────────────────────────────────────
# Registry: tool name → payload class
# ──────────────────────────────────────────────────────────────────────────────

TOOL_PAYLOAD_REGISTRY: dict[str, type[BaseModel]] = {
    "anchor_session": AnchorSessionPayload,
    "reason_mind": ReasonMindPayload,
    "vector_memory": VectorMemoryPayload,
    "simulate_heart": SimulateHeartPayload,
    "critique_thought": CritiqueThoughtPayload,
    "apex_judge": ApexJudgePayload,
    "eureka_forge": EurekaForgePayload,
    "seal_vault": SealVaultPayload,
    "search_reality": SearchRealityPayload,
    "ingest_evidence": IngestEvidencePayload,
    "audit_rules": AuditRulesPayload,
    "check_vital": CheckVitalPayload,
    "metabolic_loop": MetabolicLoopPayload,
    "arifOS.kernel": MetabolicLoopPayload,
    "session_memory": SessionMemoryPayload,
    "open_apex_dashboard": ApexDashboardPayload,
}
