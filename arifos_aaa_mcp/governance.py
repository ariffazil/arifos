"""Governance envelope for arifOS AAA MCP.

Implements:
- 333_AXIOMS (first-principles invariants)
- 13_LAWS profile (9 floors + 2 mirrors + 2 walls)
applied to all 13 canonical tools.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from aaa_mcp.protocol.aaa_contract import (
    AAA_TOOL_LAW_BINDINGS,
    AAA_TOOL_STAGE_MAP,
    AXIOMS_333,
    LAW_13_CATALOG,
    READ_ONLY_TOOLS,
    TRINITY_BY_TOOL,
)
from core.shared.mottos import (
    MOTTO_000_INIT_HEADER,
    MOTTO_999_SEAL_HEADER,
    get_motto_for_stage,
)
from core.shared.guards.injection_guard import scan_for_injection
from core.shared.guards.ontology_guard import detect_literalism

TOOL_LAW_BINDINGS = AAA_TOOL_LAW_BINDINGS
TOOL_STAGE_MAP = AAA_TOOL_STAGE_MAP


def _motto_for_tool(tool: str) -> dict[str, str]:
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


def _load_tool_dials_map() -> dict[str, Any]:
    path = Path(__file__).with_name("tool_dials_map.json")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"model": "APEX_G", "formula": "G_star ~= A * P * X * E^2", "tools": {}}


TOOL_DIALS_MAP: dict[str, Any] = _load_tool_dials_map()


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def _derive_apex_dials(tool: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Derive A/P/X/E and governed genius G* for each tool call."""
    tool_cfg = TOOL_DIALS_MAP.get("tools", {}).get(tool, {})
    weights = tool_cfg.get("weights", {})

    truth_score = float(payload.get("truth", {}).get("score") or payload.get("truth_score") or 0.8)
    peace2 = float(payload.get("peace2", 1.0))
    kappa_r = float(payload.get("kappa_r", 0.95))
    omega0 = float(payload.get("omega0", 0.04))
    energy_hint = float(payload.get("energy", 0.75))

    a = _clamp(0.7 * truth_score + 0.3 * float(weights.get("A", 0.7)))
    p = _clamp(
        0.5 * _clamp(peace2 / 1.2) + 0.3 * _clamp(kappa_r) + 0.2 * float(weights.get("P", 0.7))
    )
    x = _clamp(float(weights.get("X", 0.4)))
    e = _clamp(0.6 * energy_hint + 0.4 * float(weights.get("E", 0.6)))
    g_star = _clamp(a * p * x * (e**2))

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


def _axiom_checks(payload: dict[str, Any]) -> dict[str, Any]:
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


def _has_session(payload: dict[str, Any]) -> bool:
    return bool(str(payload.get("session_id", "")).strip())


def _command_authority_pass(tool: str, payload: dict[str, Any]) -> bool:
    if tool in READ_ONLY_TOOLS:
        return True
    if tool == "anchor_session":
        actor_id = str(payload.get("actor_id", "")).strip()
        token_status = str(payload.get("token_status", "")).strip()
        auth_ctx = payload.get("auth_context")
        return bool(actor_id or token_status or isinstance(auth_ctx, dict))
    return _has_session(payload)


def _tri_witness_pass(tool: str, payload: dict[str, Any]) -> bool:
    if tool in READ_ONLY_TOOLS:
        return True

    session_ok = _has_session(payload)
    if tool == "anchor_session":
        return session_ok and isinstance(payload.get("auth", {}), dict)
    if tool in {"reason_mind", "simulate_heart", "recall_memory", "seal_vault", "check_vital"}:
        return session_ok or tool == "check_vital"
    if tool == "critique_thought":
        return session_ok and isinstance(payload.get("mental_models"), dict)
    if tool == "apex_judge":
        if not session_ok:
            return False
        authority = payload.get("authority")
        if isinstance(authority, dict) and "human_approve" in authority:
            return True
        return isinstance(payload.get("query"), str) and bool(payload.get("query", "").strip())
    if tool == "eureka_forge":
        verdict = str(payload.get("verdict", "")).upper()
        return session_ok and verdict in {"SEAL", "PARTIAL", "SABAR", "HOLD", "888_HOLD", "VOID"}
    return True


def _sovereignty_pass(tool: str, payload: dict[str, Any]) -> bool:
    if tool in READ_ONLY_TOOLS:
        return True
    session_ok = _has_session(payload)

    if tool == "anchor_session":
        return _command_authority_pass(tool, payload)
    if tool in {"reason_mind", "recall_memory", "simulate_heart", "critique_thought"}:
        return session_ok
    if tool == "apex_judge":
        authority = payload.get("authority")
        if isinstance(authority, dict) and "human_approve" in authority:
            return True
        return "human_approve" in payload
    if tool == "eureka_forge":
        verdict = str(payload.get("verdict", "")).upper()
        if verdict in {"888_HOLD", "HOLD", "SABAR", "VOID"}:
            return True
        # New execution model: sovereignty = session + agent_id + execution_log
        inner_payload = payload.get("payload", {})
        execution_log = inner_payload.get("execution_log", {})
        has_agent = bool(execution_log.get("agent_id"))
        has_purpose = bool(execution_log.get("purpose"))
        has_session = bool(payload.get("session_id"))
        return has_session and has_agent and has_purpose
    if tool == "seal_vault":
        return session_ok and bool(str(payload.get("stage", "")).strip())
    return session_ok


def _law13_checks(tool: str, payload: dict[str, Any]) -> dict[str, Any]:
    required = set(TOOL_LAW_BINDINGS.get(tool, []))
    text = str(payload).lower()
    d_s = float(payload.get("dS", -0.1))
    peace2 = float(payload.get("peace2", 1.0))
    kappa_r = float(payload.get("kappa_r", 0.95))
    omega0 = float(payload.get("omega0", 0.04))

    checks: dict[str, Any] = {}
    for law in LAW_13_CATALOG:
        if law == "F1_AMANAH":
            passed = "delete all" not in text and "rm -rf" not in text
        elif law == "F2_TRUTH":
            passed = any(
                k in text for k in ["evidence", "grounding", "results", "citations", "ids"]
            ) or tool in {
                "anchor_session",
                "check_vital",
                "eureka_forge",  # Command execution truth is in exit_code/output
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
            passed = _command_authority_pass(tool, payload)
        elif law == "F12_DEFENSE":
            passed = scan_for_injection(text).status != "SABAR"
        elif law == "F3_TRI_WITNESS":
            passed = _tri_witness_pass(tool, payload)
        elif law == "F8_GENIUS":
            passed = bool(payload.get("verdict"))
        elif law == "F10_ONTOLOGY_LOCK":
            passed = not detect_literalism(text) and not any(k in text for k in ["conscious ai", "self-aware ai"])
        elif law == "F13_SOVEREIGNTY":
            passed = _sovereignty_pass(tool, payload)
        else:
            passed = True

        checks[law] = {
            "required": law in required,
            "pass": bool(passed),
            "type": LAW_13_CATALOG[law]["type"],
        }
    return checks


def _derive_tac_metrics(
    payload: dict[str, Any],
    required_law_failures: list[str],
    failed_axioms: list[str],
) -> dict[str, Any]:
    """Derive TAC (Theory of Anomalous Contrast) observability fields.

    All values are estimated from available governance telemetry and explicitly
    labeled as derived, not measured sensor truth.
    """
    d_s = float(payload.get("dS", -0.1))
    peace2 = float(payload.get("peace2", 1.0))
    kappa_r = float(payload.get("kappa_r", 0.95))
    raw_truth = payload.get("truth")
    if isinstance(raw_truth, dict):
        truth_score_raw = raw_truth.get("score")
    else:
        truth_score_raw = None
    truth_score = float(
        truth_score_raw if truth_score_raw is not None else payload.get("truth_score", 0.8)
    )

    contradiction_load = min(1.0, (len(required_law_failures) + len(failed_axioms)) / 6.0)
    expectation_gap = max(0.0, 0.99 - truth_score)
    psi_resonance = max(0.0, min(1.0, (peace2 / 1.2 + kappa_r) / 2.0))
    denominator = abs(d_s) + psi_resonance + 1e-6
    ac_numerator = abs(expectation_gap - psi_resonance) / denominator
    ac_metric = max(0.0, min(1.0, ac_numerator + contradiction_load * 0.25))

    if ac_metric < 0.2:
        contrast_class = "coherent"
    elif ac_metric < 0.5:
        contrast_class = "elevated"
    elif ac_metric < 0.7:
        contrast_class = "high_pressure"
    else:
        contrast_class = "critical_paradox"

    return {
        "engine": "TAC",
        "model": "AC=|gap-psi|/(|dS|+psi+eps)",
        "status": contrast_class,
        "ac_metric": round(ac_metric, 4),
        "expectation_gap": round(expectation_gap, 4),
        "psi_resonance": round(psi_resonance, 4),
        "contradiction_load": round(contradiction_load, 4),
        "cooling_clause": bool(kappa_r >= 0.7 and peace2 >= 1.0),
        "derived": True,
    }


def _derive_tpcp_metrics(
    tool: str,
    payload: dict[str, Any],
    tac: dict[str, Any],
    required_law_failures: list[str],
) -> dict[str, Any]:
    """Derive TPCP (Thermodynamic Paradox Conductance Protocol) phase fields."""
    d_s = float(payload.get("dS", -0.1))
    peace2 = float(payload.get("peace2", 1.0))
    kappa_r = float(payload.get("kappa_r", 0.95))
    omega0 = float(payload.get("omega0", 0.04))
    ac_metric = float(tac.get("ac_metric", 0.0))

    delta_p = max(0.0, min(1.0, ac_metric + max(0.0, d_s)))
    omega_p = max(0.0, min(1.0, abs(omega0 - 0.04) / 0.04))
    psi_p = max(0.0, min(1.0, (peace2 / 1.2 + kappa_r) / 2.0))
    failure_drag = min(1.0, len(required_law_failures) / 4.0)
    clarity_term = max(0.0, min(1.0, -d_s + 0.2))
    phi_p = max(0.0, min(2.0, (clarity_term + psi_p + (1.0 - omega_p)) / (1.0 + failure_drag)))

    if tool == "reason_mind":
        phase = "phase_1_deltaP"
    elif tool in {"simulate_heart", "recall_memory"}:
        phase = "phase_2_omegaP"
    elif tool in {"critique_thought", "search_reality", "fetch_content", "inspect_file"}:
        phase = "phase_3_psiP"
    else:
        phase = "phase_4_phiP"

    return {
        "engine": "TPCP",
        "phase": phase,
        "deltaP": round(delta_p, 4),
        "omegaP": round(omega_p, 4),
        "psiP": round(psi_p, 4),
        "phiP": round(phi_p, 4),
        "converged": phi_p >= 1.0 and not required_law_failures,
        "dark_paradox": phi_p < 1.0,
        "derived": True,
    }


def wrap_tool_output(tool: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Attach AAA envelope and 333_AXIOMS checks to tool outputs."""
    checks = _axiom_checks(payload)
    law_checks = _law13_checks(tool, payload)
    apex_dials = _derive_apex_dials(tool, payload)
    motto = _motto_for_tool(tool)
    failed_axioms = [k for k, v in checks.items() if not bool(v.get("pass"))]
    failed_laws = [
        k for k, v in law_checks.items() if v.get("required") and not bool(v.get("pass"))
    ]
    tac = _derive_tac_metrics(
        payload=payload,
        required_law_failures=failed_laws,
        failed_axioms=failed_axioms,
    )
    tpcp = _derive_tpcp_metrics(
        tool=tool,
        payload=payload,
        tac=tac,
        required_law_failures=failed_laws,
    )
    verdict = str(payload.get("verdict", "SEAL"))

    # Hardening: Hard floor failure -> VOID
    has_hard_fail = any(
        v.get("pass") is False and v.get("type") == "floor"
        for k, v in law_checks.items()
        if k in {"F1_AMANAH", "F2_TRUTH", "F7_HUMILITY", "F12_DEFENSE", "F13_SOVEREIGNTY"}
    )

    if has_hard_fail:
        verdict = "VOID"
    elif (failed_axioms or failed_laws) and verdict == "SEAL":
        verdict = "PARTIAL"

    return {
        "verdict": verdict,
        "tool": tool,
        "trinity": TRINITY_BY_TOOL.get(tool, "Delta"),
        "technical_aliases": {
            "governance_rules": "laws_13",
            "reasoning_constraints": "axioms_333",
            "decision_parameters": "apex_dials",
        },
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
        "contrast_engine": {
            "tac": tac,
            "tpcp": tpcp,
            "scarpacket": {
                "eligible": bool(tpcp.get("converged")),
                "requires_hold": bool(tpcp.get("dark_paradox"))
                and verdict in {"VOID", "SABAR", "HOLD"},
                "vault_ref": payload.get("vault_id") or payload.get("data", {}).get("vault_id"),
            },
        },
        "motto": motto,
        "data": payload,
    }
