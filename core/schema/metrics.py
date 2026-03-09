"""
core/schema/metrics.py — Unified Metrics Schema

All numeric telemetry from all tools normalized into a single block.
Nothing lives in score_delta, telemetry.truth, etc. — it all goes here.

Canonical metric keys:
  truth          — epistemic fidelity (τ)         [0.0, 1.0]
  clarity_delta  — confusion reduction (Δclarity) [-1.0, +1.0]
  confidence     — current confidence (G)          [0.0, 1.0]
  peace          — stability score (P²)            [0.0, 2.0]
  vitality       — overall metabolic health (Ψ)   [0.0, 10.0]
  entropy_delta  — thermodynamic delta (ΔS)        [-1.0, +1.0]
  authority      — authority continuity            [0.0, 1.0]
  risk           — action / consequence risk       [0.0, 1.0]

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class Metrics(BaseModel):
    """
    Unified APEX-G metrics block.

    All fields are optional to allow tools to emit only what they compute.
    Missing fields default to None (not fabricated).
    """

    truth: float | None = Field(default=None, ge=0.0, le=1.0, description="τ epistemic fidelity")
    clarity_delta: float | None = Field(
        default=None, ge=-1.0, le=1.0, description="Δclarity confusion reduction"
    )
    confidence: float | None = Field(
        default=None, ge=0.0, le=1.0, description="G current confidence"
    )
    peace: float | None = Field(default=None, ge=0.0, le=2.0, description="P² stability score")
    vitality: float | None = Field(
        default=None, ge=0.0, le=10.0, description="Ψ overall metabolic health"
    )
    entropy_delta: float | None = Field(
        default=None, ge=-1.0, le=1.0, description="ΔS thermodynamic delta"
    )
    authority: float | None = Field(
        default=None, ge=0.0, le=1.0, description="authority continuity score"
    )
    risk: float | None = Field(
        default=None, ge=0.0, le=1.0, description="action / consequence risk"
    )

    def to_dict_compact(self) -> dict[str, float]:
        """Return only non-None metrics as a compact dict."""
        return {k: v for k, v in self.model_dump().items() if v is not None}
