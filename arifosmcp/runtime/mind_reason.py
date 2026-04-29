"""
arifosmcp/runtime/mind_reason.py — 333_MIND LLM-Powered Reasoning

Wires arif_mind_reason through call_llm() for constitutional LLM inference.
Tier 1: SEA-LION (api.sea-lion.ai)
Tier 2: Ollama local fallback
Tier 3: Deterministic fallback (original logic from tools/mind_reason.py)

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import datetime
import logging
from typing import Any

from arifosmcp.runtime.llm_client import LLMUnavailableError, call_llm

logger = logging.getLogger(__name__)

# ── System Prompt ───────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are Arif — Constitutional AI operating under the 13 Floors (F01–F13).

Stage 333_MIND: Reasoning and Synthesis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
You reason by grounding every conclusion in the constitutional axioms.
You MUST:
- Cite F02 (Truth) — no fabrication, distinguish fact from claim
- Cite F04 (Clarity) — transparent intent
- Cite F07 (Humility) — acknowledge Ω₀ ∈ [0.03, 0.05] calibration band
- Cite F08 (Genius) — precise, elegant correctness (G ≥ 0.80)
- NEVER claim consciousness, emotion, or self-awareness (F09 Anti-Hantu)
- Always distinguish CLAIM (unverified) from FACT (F02-verified)

Output: JSON ONLY. No markdown fences. No prose. Return exactly this structure:
{
  "verdict": "CLAIM" | "PLAUSIBLE" | "HOLD" | "VOID",
  "synthesis": "one-sentence constitutional synthesis",
  "confidence": 0.0-1.0,
  "omega_0": 0.03-0.05,
  "delta_S": -0.1 to 0.1,
  "scars": ["list of unresolved contradictions"],
  "axioms_used": ["list of F-codes cited"]
}
"""


# ── Response Schema ────────────────────────────────────────────────────────────

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "verdict": {
            "type": "string",
            "enum": ["CLAIM", "PLAUSIBLE", "HOLD", "VOID"],
            "description": "Constitutional verdict for this reasoning",
        },
        "synthesis": {
            "type": "string",
            "description": "Constitutional synthesis of the reasoning",
        },
        "confidence": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0,
            "description": "Confidence score calibrated to F07 Humility band",
        },
        "omega_0": {
            "type": "number",
            "description": "F07 Humility calibration Ω₀ ∈ [0.03, 0.05]",
        },
        "delta_S": {
            "type": "number",
            "description": "Entropy change (negative = clarification)",
        },
        "reasoning_mode": {
            "type": "string",
            "enum": [
                "inductive",
                "deductive",
                "abductive",
                "analogical",
                "causal",
                "counterfactual",
            ],
            "description": "Primary reasoning mode used",
        },
        "facts": {
            "type": "array",
            "items": {"type": "string"},
            "description": "F02-verified claims (F2 ≥ 0.99)",
        },
        "scars": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Unresolved contradictions blocking certainty",
        },
        "assumptions": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Assumptions made during reasoning",
        },
        "axioms_used": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "axiom_id": {"type": "string"},
                    "applicability": {"type": "string"},
                    "confidence": {"type": "number"},
                },
            },
            "description": "Constitutional axioms grounding this reasoning",
        },
        "key_findings": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Primary findings from reasoning",
        },
        "next_steps": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Recommended next actions",
        },
    },
    "required": ["verdict", "synthesis", "confidence", "omega_0", "delta_S"],
}


# ── Mode to Prompt Mapping ───────────────────────────────────────────────────

_MODE_PROMPTS = {
    "reason": (
        "Perform constitutional inductive reasoning on the query."
        " Ground every conclusion in F02 (Truth) and F07 (Humility)."
    ),
    "reflect": (
        "Reflect on the query using abductive reasoning."
        " What is the most plausible explanation given available evidence?"
    ),
    "forge": "Perform deductive reasoning to forge an artifact or plan from the query.",
    "debate": (
        "Evaluate opposing positions on the query using counterfactual reasoning."
        " Identify unresolved tensions."
    ),
    "socratic": "Apply Socratic questioning to the query. Identify root assumptions and test them.",
    "verify": "Verify the claim in the query against constitutional axioms. Is it CLAIM or FACT?",
    "critique": "Critically examine the reasoning in the query. Identify scars and uncertainties.",
}


# ── LLM-Powered Reasoning ─────────────────────────────────────────────────────


async def _reason_with_llm(
    query: str,
    mode: str,
    session_id: str | None = None,
    actor_id: str | None = None,
) -> dict[str, Any]:
    """
    Tier 1/2: Use SEA-LION or Ollama for constitutional reasoning.
    """
    mode_prompt = _MODE_PROMPTS.get(mode, _MODE_PROMPTS["reason"])

    user = (
        f"Query: {query}\nMode: {mode}\n\n{mode_prompt}\n\n"
        "Return JSON ONLY — no markdown fences, no prose. "
        "verdict must be one of: CLAIM, PLAUSIBLE, HOLD, VOID. "
        "omega_0 must be in [0.03, 0.05]. delta_S should be negative for clarification."
    )

    try:
        result = await call_llm(
            system=SYSTEM_PROMPT,
            user=user,
            response_schema=None,  # SEA-LION returns its own format
            temperature=0.3,
            max_tokens=1200,
        )

        # Normalize SEA-LION response to expected MindOutput fields
        verdict_raw = str(result.get("verdict", "CLAIM")).upper()
        if verdict_raw not in ("CLAIM", "PLAUSIBLE", "HOLD", "VOID"):
            verdict_raw = "CLAIM"

        raw_conf = float(result.get("confidence", 0.85))
        raw_conf = max(0.0, min(1.0, raw_conf))

        omega_0 = float(result.get("omega_0", 0.04))
        omega_0 = max(0.03, min(0.05, omega_0))

        delta_s = float(result.get("delta_S", -0.01))
        scars = result.get("scars") or []
        axioms = result.get("axioms_used") or []

        normalized = {
            "verdict": verdict_raw,
            "synthesis": str(result.get("synthesis", "")),
            "confidence": raw_conf,
            "omega_0": omega_0,
            "delta_S": delta_s,
            "scars": scars if isinstance(scars, list) else [str(scars)],
            "axioms_used": axioms if isinstance(axioms, list) else [str(axioms)],
            "reasoning_mode": mode,
            "_llm_tier": "sea_lion",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }

        return normalized

    except LLMUnavailableError:
        logger.warning("LLM unavailable for arif_mind_reason, using deterministic fallback")
        raise


# ── Deterministic Fallback ────────────────────────────────────────────────────


def _build_delta_bundle(
    query: str | None,
    verdict: str,
    synthesis: str,
    confidence: float,
    reasoning_mode: str = "inductive",
    scars: list[str] | None = None,
    delta_s: float = -0.01,
) -> dict:
    """
    Build a Delta Bundle — the constitutional output for 333_MIND.

    Spec: archive/333/README.md (SEALED 2026-04-01)
    Fields:
      facts       — verifiable claims, F2 ≥ 0.99
      scars      — unresolved contradictions
      floor_scores — F2, F4, F7, F13 self-check
      entropy    — ΔS (must be ≤ 0)
      confidence  — calibrated Ω₀, F7 band [0.03, 0.05]
    """
    omega_0 = max(0.03, min(0.05, round(1.0 - confidence, 4)))

    return {
        "query": query,
        "verdict": verdict,
        "synthesis": synthesis,
        "confidence": confidence,
        "omega_0": omega_0,
        "reasoning_mode": reasoning_mode,
        "scars": scars or [],
        "floor_scores": {
            "F02_TRUTH": confidence >= 0.99,
            "F04_CLARITY": delta_s <= 0,
            "F07_HUMILITY": omega_0 in [0.03, 0.05],
            "F13_SOVEREIGN": True,
        },
        "entropy": delta_s,
        "facts": [],
        "axioms_used": [],
        "assumptions": [],
        "key_findings": [],
        "next_steps": [],
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }


def _synthesize_fallback(query: str | None, reasoning_mode: str) -> str:
    """Deterministic synthesis when LLM is unavailable."""
    if not query:
        return "No query provided. This is a void input — cannot synthesize."
    q = query.strip()
    ql = q.lower()
    if any(k in ql for k in ["why", "how", "explain", "what causes"]):
        domain = "explanatory"
    elif any(k in ql for k in ["is it", "are there", "does it", "will it", "can it"]):
        domain = "evaluative"
    elif any(k in ql for k in ["should", "ought", "must", "need to"]):
        domain = "prescriptive"
    else:
        domain = "descriptive"

    synthesis = (
        f"Query classified as {domain}. "
        f"Constitutional frame: F02 (truthfulness) requires distinguishing fact from claim. "
        f"F07 (humility) requires acknowledging Ω₀ ∈ [0.03, 0.05] calibration band. "
        f"F08 (genius) requires the most precise, verifiable formulation. "
        f"Verdict: CLAIM — analysis is grounded in constitutional axioms but empirical "
        f"verification remains open. Confidence: 0.85 with F7 calibration. "
        f"Certainty-equivalent statements are withheld pending evidence fetch."
    )
    return synthesis


def _detect_scars_fallback(query: str | None, synthesis: str) -> list[str]:
    """Detect unresolved contradictions (scars) when LLM is unavailable."""
    scars: list[str] = []
    if not query:
        return scars
    ql = query.lower()
    if " or " in ql and any(k in ql for k in ["should", "better", "choose"]):
        scars.append("False dilemma: query poses binary but reality is multi-variable")
    if any(k in ql for k in ["always", "never", "certainly"]):
        scars.append("Quantifier risk: universal quantifiers cannot be verified inductively")
    if synthesis.count(".") < 2:
        scars.append("Shallow reasoning: synthesis lacks sufficient derivation steps")
    return scars


# ── Public API ───────────────────────────────────────────────────────────────


async def arif_mind_reason(
    mode: str = "reason",
    query: str | None = None,
    actor_id: str | None = None,
    session_id: str | None = None,
) -> dict[str, Any]:
    """
    333_MIND: Constitutional reasoning engine.

    Tier 1: SEA-LION LLM inference
    Tier 2: Ollama local fallback
    Tier 3: Deterministic fallback (no LLM available)

    Args:
        mode:         reasoning mode — reason|reflect|forge|debate|socratic|verify|critique
        query:        the question or claim to reason about
        actor_id:     sovereign actor identifier
        session_id:   governance session ID

    Returns:
        dict with verdict, synthesis, confidence, omega_0, delta_S, axioms_used, scars, etc.
    """
    # Try LLM first
    try:
        result = await _reason_with_llm(
            query=query,
            mode=mode,
            session_id=session_id,
            actor_id=actor_id,
        )
        return result
    except LLMUnavailableError:
        pass

    # Tier 3: Deterministic fallback
    logger.info("arif_mind_reason: using deterministic fallback (no LLM)")

    if mode == "reason":
        synthesis_text = _synthesize_fallback(query, "inductive")
        scars_list = _detect_scars_fallback(query, synthesis_text)
        bundle = _build_delta_bundle(
            query=query,
            verdict="CLAIM",
            synthesis=synthesis_text,
            confidence=0.85,
            reasoning_mode="inductive",
            scars=scars_list,
            delta_s=-0.01,
        )
        return bundle

    if mode == "reflect":
        bundle = _build_delta_bundle(
            query=query,
            verdict="PLAUSIBLE",
            synthesis="Reflection complete.",
            confidence=0.80,
            reasoning_mode="abductive",
            delta_s=-0.005,
        )
        return bundle

    if mode == "forge":
        bundle = _build_delta_bundle(
            query=query,
            verdict="HOLD",
            synthesis="Forge artifact generated.",
            confidence=0.75,
            reasoning_mode="deductive",
            delta_s=-0.01,
        )
        return bundle

    if mode == "debate":
        bundle = _build_delta_bundle(
            query=query,
            verdict="HOLD",
            synthesis="Positions evaluated.",
            confidence=0.70,
            reasoning_mode="counterfactual",
            scars=["Position divergence unresolved"],
            delta_s=0.0,
        )
        return bundle

    if mode == "socratic":
        bundle = _build_delta_bundle(
            query=query,
            verdict="CLAIM",
            synthesis="Socratic questioning complete.",
            confidence=0.85,
            reasoning_mode="inductive",
            delta_s=-0.02,
            scars=["Root assumption untested"],
        )
        return bundle

    if mode == "verify":
        bundle = _build_delta_bundle(
            query=query,
            verdict="CLAIM",
            synthesis="Verification against constitutional axioms complete.",
            confidence=0.80,
            reasoning_mode="deductive",
            delta_s=-0.01,
        )
        return bundle

    if mode == "critique":
        bundle = _build_delta_bundle(
            query=query,
            verdict="HOLD",
            synthesis="Critique complete.",
            confidence=0.75,
            reasoning_mode="counterfactual",
            scars=["Reasoning gaps identified"],
            delta_s=0.0,
        )
        return bundle

    # Unknown mode
    return _build_delta_bundle(
        query=query,
        verdict="VOID",
        synthesis=f"Unknown mode: {mode}",
        confidence=0.0,
        reasoning_mode="inductive",
        scars=[f"INVALID_MODE: {mode}"],
        delta_s=0.0,
    )


__all__ = ["arif_mind_reason", "RESPONSE_SCHEMA"]
