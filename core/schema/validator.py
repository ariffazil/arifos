"""
core/schema/validator.py — Verdict Contract Enforcement

Enforces the canonical stage-verdict rules:

  1. Exploratory tools (reason_mind, vector_memory, search_reality,
     ingest_evidence, anchor_session) may NOT emit VOID.
     VOID → SABAR.

  2. Safety/alignment tools (simulate_heart, critique_thought,
     audit_rules) may NOT emit VOID.
     VOID → SABAR.

  3. Only commitment/action tools (apex_judge, eureka_forge, seal_vault)
     and the 000_INIT stage may emit VOID as a real rejection.

  4. Stage-level rule (matches core/shared/verdict_contract.py):
     if stage_weight < 888 and stage != 000 and verdict == VOID:
         verdict = SABAR

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import logging

from core.schema.stage import Stage
from core.schema.verdict import (
    EXPLORATORY_TOOLS,
    SAFETY_TOOLS,
    Verdict,
)

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# Stage-level verdict contract
# ──────────────────────────────────────────────────────────────────────────────

# Stages that are FORBIDDEN from emitting VOID
_VOID_FORBIDDEN_STAGES: frozenset[Stage] = frozenset(
    {
        Stage.SENSE,
        Stage.REALITY,
        Stage.MIND,
        Stage.HEART,
        Stage.HEALTH,
        Stage.CRITIQUE,
        Stage.FORGE,
        Stage.ROUTER,
    }
)


class VerdictValidator:
    """
    Enforce the canonical stage-verdict contract.

    Usage::

        normalized = VerdictValidator.validate_by_stage(Stage.MIND, Verdict.VOID)
        # returns Verdict.SABAR — premature VOID normalized

        normalized = VerdictValidator.validate_by_tool("reason_mind", Verdict.VOID)
        # returns Verdict.SABAR — exploratory tool cannot emit VOID

        normalized = VerdictValidator.validate_by_stage(Stage.JUDGE, Verdict.VOID)
        # returns Verdict.VOID — 888_JUDGE may emit VOID
    """

    @classmethod
    def validate_by_stage(cls, stage: Stage, verdict: Verdict) -> Verdict:
        """
        Validate and normalize verdict for a given pipeline stage.

        Premature VOID (before 888_JUDGE) → SABAR.
        000_INIT is allowed to emit VOID for auth failures.
        """
        if stage in _VOID_FORBIDDEN_STAGES and verdict == Verdict.VOID:
            logger.warning(
                "verdict_validator: stage %s emitted VOID — normalized to SABAR "
                "(VOID reserved for 000_INIT auth failures and 888_JUDGE)",
                stage.value,
            )
            return Verdict.SABAR
        return verdict

    @classmethod
    def validate_by_tool(cls, tool_name: str, verdict: Verdict) -> Verdict:
        """
        Validate and normalize verdict based on tool classification.

        Exploratory and safety tools cannot emit VOID — normalized to SABAR.
        Only commitment/action tools may emit VOID.
        """
        if tool_name in EXPLORATORY_TOOLS or tool_name in SAFETY_TOOLS:
            if verdict == Verdict.VOID:
                logger.warning(
                    "verdict_validator: tool '%s' emitted VOID — normalized to SABAR "
                    "(VOID forbidden for exploratory/safety tools)",
                    tool_name,
                )
                return Verdict.SABAR
        return verdict

    @classmethod
    def validate(cls, tool_name: str, stage: Stage, verdict: Verdict) -> Verdict:
        """
        Combined validation: apply both tool-class and stage-level rules.

        Applies tool rule first (stricter), then stage rule.
        """
        normalized = cls.validate_by_tool(tool_name, verdict)
        normalized = cls.validate_by_stage(stage, normalized)
        return normalized

    @classmethod
    def is_valid_for_stage(cls, stage: Stage, verdict: Verdict) -> tuple[bool, str]:
        """
        Return (is_valid, warning_message) without modifying the verdict.

        Does NOT raise — only reports.  Call validate_by_stage() to normalize.
        """
        if stage in _VOID_FORBIDDEN_STAGES and verdict == Verdict.VOID:
            return (
                False,
                f"Stage {stage.value} may not emit VOID; use SABAR for pause states.",
            )
        return True, ""
