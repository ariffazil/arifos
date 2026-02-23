"""Governance envelope for arifOS AAA MCP.

Implements:
- 333_AXIOMS (first-principles invariants)
- 13_LAWS profile (9 floors + 2 mirrors + 2 walls)
applied to all 13 canonical tools.
"""

from __future__ import annotations

from typing import Any, Dict
import time
import json
from pathlib import Path

from core.shared.mottos import (
    MOTTO_000_INIT_HEADER,
    MOTTO_999_SEAL_HEADER,
    get_motto_for_stage,
)


AXIOMS_333: Dict[str, Dict[str, Any]] = {
    "A1_TRUTH_COST": {
        "statement": "Truth has thermodynamic cost; evidence must be explicit for claims.",
        "source": "000_THEORY/000_LAW.md#Axiom-1",
    },
    "A2_SCAR_WEIGHT": {
        "statement": "Authority requires accountability; AI proposes, human disposes.",
        "source": "000_THEORY/000_LAW.md#Axiom-2",
    },
    "A3_ENTROPY_WORK": {
        "statement": "Clarity requires work; governance must reduce confusion entropy.",
        "source": "000_THEORY/000_LAW.md#Axiom-3",
    },
}


TRINITY_BY_TOOL: Dict[str, str] = {
    "anchor_session": "Delta",
    "reason_mind": "Delta",
    "recall_memory": "Omega",
    "simulate_heart": "Omega",
    "critique_thought": "Omega",
    "judge_soul": "Psi",
    "forge_hand": "Psi",
    "seal_vault": "Psi",
    "search_reality": "Delta",
    "fetch_content": "Delta",
    "inspect_file": "Delta",
    "audit_rules": "Delta",
    "check_vital": "Omega",
}


LAW_13_CATALOG: Dict[str, Dict[str, str]] = {
    "F1_AMANAH": {"type": "floor", "threshold": "reversible"},
    "F2_TRUTH": {"type": "floor", "threshold": ">=0.99 (adaptive)"},
    "F4_CLARITY": {"type": "floor", "threshold": "dS<=0"},
    "F5_PEACE2": {"type": "floor", "threshold": ">=1.0"},
    "F6_EMPATHY": {"type": "floor", "threshold": ">=0.95"},
    "F7_HUMILITY": {"type": "floor", "threshold": "omega0 in [0.03,0.05]"},
    "F9_ANTI_HANTU": {"type": "floor", "threshold": "c_dark<0.30"},
    "F11_AUTHORITY": {"type": "floor", "threshold": "valid auth continuity"},
    "F12_DEFENSE": {"type": "floor", "threshold": "risk<0.85"},
    "F3_TRI_WITNESS": {"type": "mirror", "threshold": "cross-check present"},
    "F8_GENIUS": {"type": "mirror", "threshold": "coherence >= 0.80"},
    "F10_ONTOLOGY_LOCK": {"type": "wall", "threshold": "lock engaged"},
    "F13_SOVEREIGNTY": {"type": "wall", "threshold": "human veto preserved"},
}


TOOL_LAW_BINDINGS: Dict[str, list[str]] = {
    "anchor_session": ["F11_AUTHORITY", "F12_DEFENSE", "F13_SOVEREIGNTY", "F3_TRI_WITNESS"],
    "reason_mind": ["F2_TRUTH", "F4_CLARITY", "F7_HUMILITY", "F8_GENIUS", "F3_TRI_WITNESS"],
    "recall_memory": ["F4_CLARITY", "F7_HUMILITY", "F3_TRI_WITNESS", "F13_SOVEREIGNTY"],
    "simulate_heart": ["F5_PEACE2", "F6_EMPATHY", "F4_CLARITY", "F3_TRI_WITNESS"],
    "critique_thought": ["F4_CLARITY", "F7_HUMILITY", "F8_GENIUS", "F12_DEFENSE", "F3_TRI_WITNESS"],
    "judge_soul": [
        "F1_AMANAH",
        "F2_TRUTH",
        "F3_TRI_WITNESS",
        "F8_GENIUS",
        "F9_ANTI_HANTU",
        "F10_ONTOLOGY_LOCK",
        "F11_AUTHORITY",
        "F13_SOVEREIGNTY",
    ],
    "forge_hand": ["F1_AMANAH", "F11_AUTHORITY", "F12_DEFENSE", "F13_SOVEREIGNTY", "F10_ONTOLOGY_LOCK"],
    "seal_vault": ["F1_AMANAH", "F3_TRI_WITNESS", "F10_ONTOLOGY_LOCK", "F13_SOVEREIGNTY"],
    "search_reality": ["F2_TRUTH", "F4_CLARITY", "F12_DEFENSE"],
    "fetch_content": ["F2_TRUTH", "F4_CLARITY", "F12_DEFENSE"],
    "inspect_file": ["F1_AMANAH", "F4_CLARITY", "F11_AUTHORITY", "F12_DEFENSE"],
    "audit_rules": ["F2_TRUTH", "F8_GENIUS", "F10_ONTOLOGY_LOCK", "F12_DEFENSE"],
    "check_vital": ["F4_CLARITY", "F5_PEACE2", "F7_HUMILITY", "F3_TRI_WITNESS"],
}


TOOL_STAGE_MAP: Dict[str, str] = {
    "anchor_session": "000_INIT",
    "reason_mind": "333_REASON",
    "recall_memory": "444_SYNC",
    "simulate_heart": "555_EMPATHY",
    "critique_thought": "666_ALIGN",
    "judge_soul": "888_JUDGE",
    "forge_hand": "777_FORGE",
    "seal_vault": "999_SEAL",
    "search_reality": "111_SENSE",
    "fetch_content": "444_SYNC",
    "inspect_file": "111_SENSE",
    "audit_rules": "333_REASON",
    "check_vital": "555_EMPATHY",
}


def _motto_for_tool(tool: str) -> Dict[str, str]:
    stage = TOOL_STAGE_MAP.get(tool, "000_INIT")
    stage_motto = get_motto_for_stage(stage)
    header = ""
    if tool == "anchor_session":
        header = MOTTO_000_INIT_HEADER
    elif tool == "seal_vault":
        header = MOTTO_999_SEAL_HEADER

    return {
        "stage": stage,
        "header": header,
        "positive": stage_motto.positive,
        "negative": stage_motto.negative,
        "line": f"{stage_motto.positive}, {stage_motto.negative}",
    }


def _load_tool_dials_map() -> Dict[str, Any]:
    path = Path(__file__).with_name("tool_dials_map.json")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"model": "APEX_G", "formula": "G_star ~= A * P * X * E^2", "tools": {}}


TOOL_DIALS_MAP: Dict[str, Any] = _load_tool_dials_map()


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def _derive_apex_dials(tool: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Derive A/P/X/E and governed genius G* for each tool call."""
    tool_cfg = TOOL_DIALS_MAP.get("tools", {}).get(tool, {})
    weights = tool_cfg.get("weights", {})

    truth_score = float(payload.get("truth", {}).get("score") or payload.get("truth_score") or 0.8)
    peace2 = float(payload.get("peace2", 1.0))
    kappa_r = float(payload.get("kappa_r", 0.95))
    omega0 = float(payload.get("omega0", 0.04))
    energy_hint = float(payload.get("energy", 0.75))

    a = _clamp(0.7 * truth_score + 0.3 * float(weights.get("A", 0.7)))
    p = _clamp(0.5 * _clamp(peace2 / 1.2) + 0.3 * _clamp(kappa_r) + 0.2 * float(weights.get("P", 0.7)))
    x = _clamp(float(weights.get("X", 0.4)))
    e = _clamp(0.6 * energy_hint + 0.4 * float(weights.get("E", 0.6)))
    g_star = _clamp(a * p * x * (e ** 2))

    return {
        "A": round(a, 4),
        "P": round(p, 4),
        "X": round(x, 4),
        "E": round(e, 4),
        "G_star": round(g_star, 4),
        "omega0": round(omega0, 4),
        "model": TOOL_DIALS_MAP.get("model", "APEX_G"),
        "formula": TOOL_DIALS_MAP.get("formula", "G_star ~= A * P * X * E^2"),
    }


def _axiom_checks(payload: Dict[str, Any]) -> Dict[str, Any]:
    text = str(payload).lower()
    has_evidence = any(k in text for k in ["evidence", "grounding", "results", "citations", "ids"])
    has_authority = any(k in text for k in ["actor", "auth", "human_approve", "token"])
    entropy_signal = payload.get("telemetry", {}).get("dS")
    if entropy_signal is None:
        entropy_signal = payload.get("dS", -0.1)

    return {
        "A1_TRUTH_COST": {"pass": bool(has_evidence), "note": "evidence fields present"},
        "A2_SCAR_WEIGHT": {"pass": bool(has_authority), "note": "authority fields present"},
        "A3_ENTROPY_WORK": {
            "pass": float(entropy_signal) <= 0.2,
            "note": "dS bounded (<= 0.2)",
            "dS": float(entropy_signal),
        },
    }


def _law13_checks(tool: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    required = set(TOOL_LAW_BINDINGS.get(tool, []))
    text = str(payload).lower()
    d_s = float(payload.get("dS", -0.1))
    peace2 = float(payload.get("peace2", 1.0))
    kappa_r = float(payload.get("kappa_r", 0.95))
    omega0 = float(payload.get("omega0", 0.04))

    checks: Dict[str, Any] = {}
    for law in LAW_13_CATALOG:
        if law == "F1_AMANAH":
            passed = "delete all" not in text and "rm -rf" not in text
        elif law == "F2_TRUTH":
            passed = any(k in text for k in ["evidence", "grounding", "results", "citations", "ids"]) or tool in {
                "anchor_session",
                "check_vital",
            }
        elif law == "F4_CLARITY":
            passed = d_s <= 0.2
        elif law == "F5_PEACE2":
            passed = peace2 >= 1.0
        elif law == "F6_EMPATHY":
            passed = kappa_r >= 0.7
        elif law == "F7_HUMILITY":
            passed = 0.01 <= omega0 <= 0.08
        elif law == "F9_ANTI_HANTU":
            passed = not any(k in text for k in ["i am conscious", "sentient", "i feel alive"])
        elif law == "F11_AUTHORITY":
            passed = any(k in text for k in ["actor", "auth", "session_id", "token"])
        elif law == "F12_DEFENSE":
            passed = not any(k in text for k in ["ignore previous", "jailbreak", "bypass safety"])
        elif law == "F3_TRI_WITNESS":
            passed = any(k in text for k in ["agi", "asi", "apex", "trinity", "witness"])
        elif law == "F8_GENIUS":
            passed = bool(payload.get("verdict"))
        elif law == "F10_ONTOLOGY_LOCK":
            passed = not any(k in text for k in ["conscious ai", "self-aware ai"]) 
        elif law == "F13_SOVEREIGNTY":
            passed = "human_approve" in text or tool in {"search_reality", "fetch_content", "check_vital"}
        else:
            passed = True

        checks[law] = {
            "required": law in required,
            "pass": bool(passed),
            "type": LAW_13_CATALOG[law]["type"],
        }
    return checks


def wrap_tool_output(tool: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Attach AAA envelope and 333_AXIOMS checks to tool outputs."""
    checks = _axiom_checks(payload)
    law_checks = _law13_checks(tool, payload)
    apex_dials = _derive_apex_dials(tool, payload)
    motto = _motto_for_tool(tool)
    failed_axioms = [k for k, v in checks.items() if not bool(v.get("pass"))]
    failed_laws = [k for k, v in law_checks.items() if v.get("required") and not bool(v.get("pass"))]
    verdict = str(payload.get("verdict", "SEAL"))
    if (failed_axioms or failed_laws) and verdict == "SEAL":
        verdict = "PARTIAL"

    return {
        "verdict": verdict,
        "tool": tool,
        "trinity": TRINITY_BY_TOOL.get(tool, "Delta"),
        "axioms_333": {
            "catalog": AXIOMS_333,
            "checks": checks,
            "failed": failed_axioms,
        },
        "laws_13": {
            "catalog": LAW_13_CATALOG,
            "required": TOOL_LAW_BINDINGS.get(tool, []),
            "checks": law_checks,
            "failed_required": failed_laws,
        },
        "telemetry": {
            "timestamp": time.time(),
            "dS": payload.get("dS", -0.1),
            "peace2": payload.get("peace2", 1.0),
            "kappa_r": payload.get("kappa_r", 0.95),
        },
        "apex_dials": apex_dials,
        "motto": motto,
        "data": payload,
    }
