"""
core/schema/verdict.py — Canonical Verdict Enumeration

Only six canonical verdicts exist in arifOS.

Physics interpretation:
  SEAL        — entropy minimized (stable state)
  PROVISIONAL — unstable equilibrium (hypothesis under evaluation)
  PARTIAL     — low-energy intermediate (incomplete but usable)
  SABAR       — metastable state (pause / waiting for context)
  HOLD        — constrained boundary condition (waiting for authority)
  VOID        — entropy collapse (terminal / hard rejection — rare)

Critical Rule:
  if stage < 888_JUDGE and verdict == VOID → normalize to SABAR
  Only 000_INIT (auth failures) and 888_JUDGE may emit VOID.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from enum import Enum

# ──────────────────────────────────────────────────────────────────────────────
# Verdict enum
# ──────────────────────────────────────────────────────────────────────────────


class Verdict(str, Enum):
    """
    Canonical constitutional verdict set (6 values only).

    These are the ONLY legal verdict values across all arifOS tools.
    """

    SEAL = "SEAL"
    PROVISIONAL = "PROVISIONAL"
    PARTIAL = "PARTIAL"
    SABAR = "SABAR"
    HOLD = "HOLD"
    VOID = "VOID"


# ──────────────────────────────────────────────────────────────────────────────
# Status enum (transport / runtime — separate from verdict)
# ──────────────────────────────────────────────────────────────────────────────


class Status(str, Enum):
    """
    Transport/runtime state.

    verdict = governance meaning
    status  = runtime/transport meaning

    These must never be mixed.
    """

    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    TIMEOUT = "TIMEOUT"
    DRY_RUN = "DRY_RUN"


# ──────────────────────────────────────────────────────────────────────────────
# Tool classification (for verdict-contract enforcement)
# ──────────────────────────────────────────────────────────────────────────────

EXPLORATORY_TOOLS: frozenset[str] = frozenset(
    {
        "reason_mind",
        "vector_memory",
        "search_reality",
        "ingest_evidence",
        "anchor_session",
    }
)

SAFETY_TOOLS: frozenset[str] = frozenset(
    {
        "simulate_heart",
        "critique_thought",
        "audit_rules",
    }
)

COMMITMENT_TOOLS: frozenset[str] = frozenset(
    {
        "apex_judge",
        "eureka_forge",
        "seal_vault",
    }
)

# Allowed verdicts per tool class
EXPLORATORY_ALLOWED: frozenset[Verdict] = frozenset(
    {Verdict.SEAL, Verdict.PROVISIONAL, Verdict.PARTIAL, Verdict.SABAR}
)
SAFETY_ALLOWED: frozenset[Verdict] = frozenset(
    {Verdict.SEAL, Verdict.PARTIAL, Verdict.SABAR, Verdict.HOLD}
)
COMMITMENT_ALLOWED: frozenset[Verdict] = frozenset(
    {Verdict.SEAL, Verdict.HOLD, Verdict.VOID, Verdict.SABAR}
)
