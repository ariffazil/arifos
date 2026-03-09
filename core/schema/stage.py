"""
core/schema/stage.py — Canonical Stage Enumeration

Metabolic stages of the arifOS pipeline: 000 → 999.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from enum import Enum


class Stage(str, Enum):
    """
    Canonical metabolic stages for the arifOS pipeline.

    Maps to the AClip stage spine: 000 → 444 → 666 → 888 → 999.
    """

    INIT = "000_INIT"
    SENSE = "111_SENSE"
    REALITY = "222_REALITY"
    MIND = "333_MIND"
    ROUTER = "444_ROUTER"
    HEART = "555_HEART"
    CRITIQUE = "666_CRITIQUE"
    FORGE = "777_FORGE"
    JUDGE = "888_JUDGE"
    VAULT = "999_VAULT"
    # Health sub-stage (used by check_vital)
    HEALTH = "555_HEALTH"


# Ordered stage weights for comparisons (lower = earlier in pipeline)
STAGE_ORDER: dict[Stage, int] = {
    Stage.INIT: 0,
    Stage.SENSE: 111,
    Stage.REALITY: 222,
    Stage.MIND: 333,
    Stage.ROUTER: 444,
    Stage.HEART: 555,
    Stage.HEALTH: 555,
    Stage.CRITIQUE: 666,
    Stage.FORGE: 777,
    Stage.JUDGE: 888,
    Stage.VAULT: 999,
}


def stage_weight(stage: Stage) -> int:
    """Return numeric weight for a stage (used in verdict-contract comparisons)."""
    return STAGE_ORDER.get(stage, 0)
