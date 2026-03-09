"""
core/schema/output.py — Canonical ArifOSOutput Envelope

This is the SINGLE unified output schema for ALL arifOS MCP tools.

Every tool must return this envelope.  Tool-specific data goes inside
the `payload` field.  Nothing else is allowed at the top level.

Top-level contract:
  ok          — transport success flag
  tool        — tool name that produced this response
  session_id  — active session identifier (nullable)
  stage       — owning metabolic stage
  verdict     — canonical governance verdict (6 values only)
  status      — transport/runtime state (4 values only)
  metrics     — all numeric telemetry (unified)
  trace       — stage execution path (stage → verdict)
  authority   — actor / approval state (production-safe)
  payload     — tool-specific structured output
  errors      — normalized runtime errors
  meta        — schema version, timestamp, debug/dry-run flags
  debug       — optional debug appendix (only when meta.debug == True)

Fields removed from old RuntimeEnvelope:
  ❌ final_verdict        (duplicate of verdict)
  ❌ telemetry            (merged into metrics)
  ❌ score_delta          (merged into metrics)
  ❌ witness              (archived to debug block)
  ❌ philosophy           (archived — debug/vault only)
  ❌ opex                 (archived — debug block)
  ❌ apex                 (archived — debug block)
  ❌ auth_context         (merged into authority)
  ❌ token_fingerprint    (security layer — not in production output)
  ❌ data                 (renamed to payload)
  ❌ counterfactual       (archived — debug block)
  ❌ phase2_hooks         (internal — not public API)

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from core.schema.authority import Authority
from core.schema.errors import SchemaError
from core.schema.meta import DebugBlock, Meta
from core.schema.metrics import Metrics
from core.schema.trace import Trace
from core.schema.verdict import Status, Verdict


class ArifOSOutput(BaseModel):
    """
    Canonical output envelope for ALL arifOS MCP tools.

    This is the ONLY schema that tools should return.
    Tool-specific data lives inside `payload`.
    """

    # ── Transport ──────────────────────────────────────────────────────────────
    ok: bool = Field(default=True, description="Transport success flag")
    tool: str = Field(description="Name of the tool that produced this response")

    # ── Identity ───────────────────────────────────────────────────────────────
    session_id: str | None = Field(default=None, description="Active session identifier")
    stage: str = Field(description="Owning metabolic stage (e.g. 333_MIND)")

    # ── Governance ─────────────────────────────────────────────────────────────
    verdict: Verdict = Field(description="Canonical constitutional verdict")
    status: Status = Field(default=Status.SUCCESS, description="Transport / runtime state")

    # ── Telemetry ──────────────────────────────────────────────────────────────
    metrics: Metrics = Field(default_factory=Metrics, description="Unified numeric telemetry")

    # ── Execution path ─────────────────────────────────────────────────────────
    trace: Trace = Field(default_factory=Trace, description="Stage execution history")

    # ── Authority ──────────────────────────────────────────────────────────────
    authority: Authority = Field(default_factory=Authority, description="Actor / approval context")

    # ── Payload ────────────────────────────────────────────────────────────────
    payload: dict[str, Any] = Field(
        default_factory=dict, description="Tool-specific structured output"
    )

    # ── Errors ─────────────────────────────────────────────────────────────────
    errors: list[SchemaError] = Field(default_factory=list, description="Normalized runtime errors")

    # ── Metadata ───────────────────────────────────────────────────────────────
    meta: Meta = Field(default_factory=Meta, description="Schema version, timestamp, flags")

    # ── Debug (optional — only when meta.debug == True) ───────────────────────
    debug: DebugBlock | None = Field(
        default=None,
        description="Debug appendix — present only when meta.debug is True",
    )

    model_config = {"use_enum_values": True}

    def to_production(self) -> dict[str, Any]:
        """
        Serialize for production output — debug block stripped unless meta.debug.

        This is the canonical serialization method for MCP tool responses.

        The `trace` field is serialized as canonical stage-key → verdict-value
        (e.g. ``{"000_INIT": "SEAL"}``), not as raw Pydantic field names.
        """
        result = self.model_dump(mode="json", exclude_none=False)
        # Replace trace with canonical { "000_INIT": "SEAL", ... } format
        result["trace"] = self.trace.to_dict()
        if not self.meta.debug:
            result.pop("debug", None)
        return result

    def to_legacy_compat(self) -> dict[str, Any]:
        """
        Produce a backward-compatible dict that adds the old fields back alongside
        the new ones.  Useful during migration while old consumers still exist.

        Fields added:
          final_verdict, status (already present), auth_context (from authority),
          telemetry (from metrics), score_delta (from metrics)
        """
        base = self.to_production()
        # Add legacy aliases
        base["final_verdict"] = base["verdict"]
        base["auth_context"] = {
            "actor_id": self.authority.actor_id,
            "authority_level": self.authority.level,
            "auth_state": self.authority.auth_state,
            "approval_scope": self.authority.approval_scope,
        }
        base["telemetry"] = {
            "dS": self.metrics.entropy_delta,
            "peace2": self.metrics.peace,
            "confidence": self.metrics.confidence,
            "verdict": base["verdict"],
        }
        base["score_delta"] = {
            "truth": self.metrics.truth,
            "clarity": self.metrics.clarity_delta,
        }
        base["data"] = base["payload"]
        return base
