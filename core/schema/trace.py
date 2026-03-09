"""
core/schema/trace.py — Stage Execution Trace Schema

One unified trace per response.  No nested data.trace, no phase2_hooks.

Format: { "000_INIT": "SEAL", "111_SENSE": "PARTIAL", ... }

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, model_validator

from core.schema.verdict import Verdict

# Canonical stage keys in pipeline order
TRACE_STAGE_KEYS: tuple[str, ...] = (
    "000_INIT",
    "111_SENSE",
    "222_REALITY",
    "333_MIND",
    "444_ROUTER",
    "555_HEART",
    "666_CRITIQUE",
    "777_FORGE",
    "888_JUDGE",
    "999_VAULT",
)


class Trace(BaseModel):
    """
    Stage execution trace — one verdict per stage.

    Only stages that actually executed are included.
    Values must be canonical Verdict strings.
    """

    stage_000_init: Verdict | None = None
    stage_111_sense: Verdict | None = None
    stage_222_reality: Verdict | None = None
    stage_333_mind: Verdict | None = None
    stage_444_router: Verdict | None = None
    stage_555_heart: Verdict | None = None
    stage_666_critique: Verdict | None = None
    stage_777_forge: Verdict | None = None
    stage_888_judge: Verdict | None = None
    stage_999_vault: Verdict | None = None

    def to_dict(self) -> dict[str, str | None]:
        """Convert to canonical { stage_key: verdict_value } mapping."""
        mapping = {
            "000_INIT": self.stage_000_init,
            "111_SENSE": self.stage_111_sense,
            "222_REALITY": self.stage_222_reality,
            "333_MIND": self.stage_333_mind,
            "444_ROUTER": self.stage_444_router,
            "555_HEART": self.stage_555_heart,
            "666_CRITIQUE": self.stage_666_critique,
            "777_FORGE": self.stage_777_forge,
            "888_JUDGE": self.stage_888_judge,
            "999_VAULT": self.stage_999_vault,
        }
        # Return only executed stages (non-None values), converting Verdict to str
        return {
            k: (v.value if isinstance(v, Verdict) else v)
            for k, v in mapping.items()
            if v is not None
        }

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Trace:
        """
        Build a Trace from a raw { stage_key: verdict_string } dict.

        Unknown stage keys are silently ignored (F9: Anti-Hantu — no ghost fields).
        """
        key_to_field = {
            "000_INIT": "stage_000_init",
            "111_SENSE": "stage_111_sense",
            "222_REALITY": "stage_222_reality",
            "333_MIND": "stage_333_mind",
            "444_ROUTER": "stage_444_router",
            "555_HEART": "stage_555_heart",
            "666_CRITIQUE": "stage_666_critique",
            "777_FORGE": "stage_777_forge",
            "888_JUDGE": "stage_888_judge",
            "999_VAULT": "stage_999_vault",
        }
        kwargs: dict[str, Verdict | None] = {}
        for stage_key, verdict_raw in raw.items():
            field = key_to_field.get(stage_key)
            if field is None:
                continue
            try:
                kwargs[field] = Verdict(verdict_raw)
            except (ValueError, TypeError):
                kwargs[field] = Verdict.SABAR  # Safe fallback

        return cls(**kwargs)

    @model_validator(mode="before")
    @classmethod
    def _accept_dict_shorthand(cls, data: Any) -> Any:
        """Allow constructing Trace directly from a stage→verdict dict."""
        if isinstance(data, dict):
            # If it looks like a stage-key dict (keys start with digits), convert it
            if any(len(k) >= 3 and k[:3].isdigit() for k in data if isinstance(k, str)):
                return cls.from_dict(data).model_dump()
        return data
