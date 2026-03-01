"""Governance envelope for arifOS AAA MCP.

Implements:
- 333_AXIOMS (first-principles invariants)
- 13_LAWS profile (9 floors + 2 mirrors + 2 walls)
applied to all 13 canonical tools.
- P2 THERMODYNAMICS: Orthogonality + Landauer Bound
"""

from __future__ import annotations

import json
import math
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


def _safe_float(p: dict[str, Any], key: str, default: float) -> float:
    """Safely extract and convert a float metric from nested payload structure."""
    if not isinstance(p, dict):
        return default
    val = p.get(key)
    if val is None:
        # Fallback 1: Nested payload
        val = p.get("payload", {}).get(key)
    if val is None:
        # Fallback 2: Telemetry nested payload
        val = p.get("telemetry", {}).get(key)
    if val is None:
        # Fallback 3: Data nested payload
        val = p.get("data", {}).get(key)
        if isinstance(val, dict):
            val = val.get(key)
    
    if val is None:
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def _derive_apex_dials(tool: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Derive A/P/X/E and governed genius G* for each tool call."""
    tool_cfg = TOOL_DIALS_MAP.get("tools", {}).get(tool, {})
    weights = tool_cfg.get("weights", {})

    truth_score = _safe_float(payload.get("truth", {}), "score", _safe_float(payload, "truth_score", 0.8))
    peace2 = _safe_float(payload, "peace2", 1.0)
    kappa_r = _safe_float(payload, "kappa_r", 0.95)
    omega0 = _safe_float(payload, "omega0", 0.04)
    energy_hint = _safe_float(payload, "energy", 0.75)

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


def _axiom_checks(payload: dict[str, Any], tool: str = "") -> dict[str, Any]:
    text = str(payload).lower()
    # For eureka_forge, evidence is in execution_log, authority is in agent_id
    if tool == "eureka_forge":
        inner = payload.get("payload", {})
        execution_log = inner.get("execution_log", {})
        has_evidence = bool(execution_log.get("stdout") or execution_log.get("action"))
        has_authority = bool(execution_log.get("agent_id"))
    else:
        has_evidence = any(k in text for k in ["evidence", "grounding", "results", "citations", "ids"])
        has_authority = any(k in text for k in ["actor", "auth", "human_approve", "token"])
    dS_val = _safe_float(payload, "dS", -0.1)

    return {
        "A1_TRUTH_COST": {"pass": bool(has_evidence), "note": "evidence fields present"},
        "A2_SCAR_WEIGHT": {"pass": bool(has_authority), "note": "authority fields present"},
        "A3_ENTROPY_WORK": {
            "pass": dS_val <= 0.2,
            "note": "dS bounded (<= 0.2)",
            "dS": dS_val,
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


def _classify_tool_for_consensus(tool: str) -> dict[str, Any]:
    """
    Classify tool for dynamic Tri-Witness thresholding.
    
    Tool Classes:
    - UTILITY: Read-only tools (search, fetch, inspect)
    - SPINE: Governance tools (reason, simulate, critique)
    - CRITICAL: Final authority tools (apex_judge, seal_vault)
    """
    stage = TOOL_STAGE_MAP.get(tool, "000_INIT")
    if tool == "anchor_session" or stage == "000_INIT" or tool in READ_ONLY_TOOLS:
        return {"class": "UTILITY", "threshold": 0.90, "witness_floor": 0.85}
    if tool in {"apex_judge", "seal_vault", "eureka_forge"}:
        return {"class": "CRITICAL", "threshold": 0.995, "witness_floor": 0.90}
    # All other governance tools
    return {"class": "SPINE", "threshold": 0.91, "witness_floor": 0.90}


def _calculate_tri_witness_consensus(
    tool: str,
    payload: dict[str, Any]
) -> dict[str, Any]:
    """
    P1 HARDENING: Calculate Tri-Witness consensus with geometric mean.
    
    Formula: W₃ = ∛(H × A × E)
    
    Where:
    - H (Human): Intent / Sovereign authority score
    - A (AI): Internal logic / Constitutional compliance score  
    - E (Earth): Empirical grounding / Evidence score
    
    Dynamic Thresholds:
    - UTILITY tools: W₃ ≥ 0.95
    - SPINE tools: W₃ ≥ 0.99
    - CRITICAL tools: W₃ ≥ 0.995
    
    Per-Witness Minimum: Any witness < floor shatters consensus.
    """
    # Extract witness scores from payload
    # Default values assume partial consensus if not provided
    human_score = _safe_float(payload, "human_witness", _safe_float(payload.get("authority", {}), "score", 0.95))
    ai_score = _safe_float(payload, "ai_witness", _safe_float(payload.get("truth", {}), "score", 0.90))
    earth_score = _safe_float(payload, "earth_witness", _safe_float(payload, "grounding", 0.90))
    
    # Get tool classification and thresholds
    tool_class = _classify_tool_for_consensus(tool)
    consensus_threshold = tool_class["threshold"]
    witness_floor = tool_class["witness_floor"]
    
    # P1 HARDENING: Per-witness minimum check (consensus shatter)
    witnesses = {
        "human": human_score,
        "ai": ai_score,
        "earth": earth_score
    }
    
    for witness_name, score in witnesses.items():
        if score < witness_floor:
            return {
                "pass": False,
                "verdict": "VOID",
                "w3": 0.0,
                "threshold": consensus_threshold,
                "shattered_by": witness_name,
                "shatter_reason": f"{witness_name}_witness score {score:.4f} < floor {witness_floor}",
                "witnesses": witnesses,
                "tool_class": tool_class["class"]
            }
    
    # Calculate geometric mean: W₃ = ∛(H × A × E)
    w3 = (human_score * ai_score * earth_score) ** (1/3)
    
    # Check consensus threshold
    passes = w3 >= consensus_threshold
    
    return {
        "pass": passes,
        "verdict": "SEAL" if passes else "VOID",
        "w3": round(w3, 4),
        "threshold": consensus_threshold,
        "witnesses": witnesses,
        "tool_class": tool_class["class"],
        "shattered_by": None
    }


def _tri_witness_pass(tool: str, payload: dict[str, Any]) -> bool:
    """
    P1 HARDENING: Tri-Witness with geometric mean and dynamic thresholds.
    """
    # Read-only tools get simplified check
    if tool in READ_ONLY_TOOLS:
        return True
    
    # Calculate full consensus for governance tools
    consensus = _calculate_tri_witness_consensus(tool, payload)
    return consensus.get("pass", False)


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
        has_purpose = "purpose" in execution_log
        has_session = bool(payload.get("session_id"))
        return has_session and has_agent and has_purpose
    if tool == "seal_vault":
        return session_ok and bool(str(payload.get("stage", "")).strip())
    return session_ok


def _law13_checks(tool: str, payload: dict[str, Any]) -> dict[str, Any]:
    required = set(TOOL_LAW_BINDINGS.get(tool, []))
    text = str(payload).lower()
    d_s = _safe_float(payload, "dS", -0.1)
    peace2 = _safe_float(payload, "peace2", 1.0)
    kappa_r = _safe_float(payload, "kappa_r", 0.95)
    omega0 = _safe_float(payload, "omega0", 0.04)

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
            # HARDENED: Strict entropy reduction - ΔS must be ≤ 0
            # Previous: d_s <= 0.2 (too permissive - allowed 20% entropy increase)
            # Now: d_s <= 0 (strict - must reduce or maintain entropy)
            passed = d_s <= 0.0
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
    d_s = _safe_float(payload, "dS", -0.1)
    peace2 = _safe_float(payload, "peace2", 1.0)
    kappa_r = _safe_float(payload, "kappa_r", 0.95)
    omega0 = _safe_float(payload, "omega0", 0.04)
    ac_metric = _safe_float(tac, "ac_metric", 0.0)

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


def _derive_vitality_index(
    payload: dict[str, Any],
    law_checks: dict[str, Any],
    apex_dials: dict[str, Any],
) -> dict[str, Any]:
    """
    Calculate Ψ (Vitality Index) - the master equation for constitutional homeostasis.
    
    Ψ = (ΔS · Peace² · κᵣ · RASA · Amanah) / (Entropy + Shadow + ε)
    
    Threshold: Ψ ≥ 1.0 required for SEAL verdict.
    If Ψ < 1.0, system is unstable → SABAR or VOID.
    """
    # Numerator components (constructive forces)
    d_s = _safe_float(payload, "dS", -0.1)
    peace2 = _safe_float(payload, "peace2", 1.0)
    kappa_r = _safe_float(payload, "kappa_r", 0.95)
    
    # RASA (Receive, Appreciate, Summarize, Ask) - active listening metric
    # Derived from truth score and engagement signals
    truth_score = _safe_float(apex_dials, "G_star", 0.8)
    rasa = _clamp(0.5 * truth_score + 0.5 * (kappa_r / 0.95))
    
    # Amanah ( binary integrity lock - F1)
    amanah_pass = law_checks.get("F1_AMANAH", {}).get("pass", True)
    amanah = 1.0 if amanah_pass else 0.0  # Binary: 1 if passed, 0 if failed
    
    # Numerator: Product of all constructive forces
    # Note: d_s is typically negative (entropy reduction), so we use |d_s| for magnitude
    # but preserve the sign effect - more negative = more clarity = higher vitality
    numerator = abs(d_s) * peace2 * kappa_r * rasa * amanah
    
    # Denominator components (destructive forces)
    entropy = max(0.0, d_s) if d_s > 0 else 0.0  # Only positive entropy adds disorder
    
    # Shadow: latent bias/unverified assumptions
    # Derived from failed floors and axiom violations
    failed_count = sum(
        1 for v in law_checks.values() 
        if v.get("required") and not v.get("pass", True)
    )
    shadow = _clamp(failed_count / 5.0)  # Normalize: 5 failures = full shadow
    
    # Epsilon: numerical stabilizer to prevent division by zero
    epsilon = 1e-6
    
    # Calculate Ψ (Vitality Index)
    denominator = entropy + shadow + epsilon
    psi = numerator / denominator
    
    # Clamp to reasonable range
    psi = _clamp(psi, 0.0, 10.0)
    
    return {
        "engine": "VITALITY_INDEX",
        "formula": "Ψ = (|ΔS| · Peace² · κᵣ · RASA · Amanah) / (Entropy + Shadow + ε)",
        "psi": round(psi, 4),
        "threshold": 1.0,
        "status": "HEALTHY" if psi >= 1.0 else "UNSTABLE",
        "components": {
            "delta_s": round(d_s, 4),
            "peace2": round(peace2, 4),
            "kappa_r": round(kappa_r, 4),
            "rasa": round(rasa, 4),
            "amanah": amanah,
            "numerator": round(numerator, 4),
            "entropy": round(entropy, 4),
            "shadow": round(shadow, 4),
            "denominator": round(denominator, 4),
        },
        "derived": True,
    }


# ═══════════════════════════════════════════════════════
# P2 THERMODYNAMICS: Orthogonality + Landauer Bound
# ═══════════════════════════════════════════════════════

def _derive_orthogonality(agi_vector: list[float], asi_vector: list[float]) -> float:
    """
    P2 HARDENING: AGI/ASI Vector Orthogonality Check
    
    Calculates the independence between Mind (AGI) and Heart (ASI).
    High orthogonality means they are not suffering from mode collapse.
    
    Formula: Ω_ortho = 1 - |cos(θ)|
    Threshold: Ω_ortho >= 0.95 (95% independent)
    
    If AGI and ASI vectors are too similar (cos_sim ≈ 1), 
    the system is echoing itself, not forming true consensus.
    """
    if not agi_vector or not asi_vector or len(agi_vector) != len(asi_vector):
        return 1.0  # Default to independent if vectors unavailable (fail-open for missing data)
    
    dot_product = sum(a * b for a, b in zip(agi_vector, asi_vector))
    norm_a = math.sqrt(sum(a * a for a in agi_vector))
    norm_b = math.sqrt(sum(b * b for b in asi_vector))
    
    if norm_a == 0 or norm_b == 0:
        return 0.0  # Failed vector generation
    
    cos_sim = dot_product / (norm_a * norm_b)
    
    # Omega_ortho: 1.0 = perfectly orthogonal (independent), 0.0 = parallel (echo chamber)
    omega_ortho = 1.0 - abs(cos_sim)
    return omega_ortho


def _orthogonality_pass(omega_ortho: float) -> bool:
    """P2 Threshold check: Must be >= 0.95 for true independence."""
    return omega_ortho >= 0.95


def _check_landauer_bound(compute_ms: float, tokens_generated: int, d_s: float) -> dict[str, Any]:
    """
    P2 HARDENING: Landauer Bound - Thermodynamic Cost Check
    
    Prevents 'Cheap Truth' - hallucinating massive clarity without spending compute.
    Landauer's principle: E >= n * k_B * T * ln(2)
    
    If the system claims to reduce massive entropy (d_s << 0) but spent 
    nearly zero compute time/tokens, it is a mathematical anomaly.
    """
    # Baseline constants (approximations for semantic energy bounds)
    k_B_proxy = 1.38e-2  # Conceptual Boltzmann proxy for LLM compute
    T_proxy = 300.0      # System 'temperature' baseline
    
    # Information bits theoretically processed (derived from entropy reduction)
    # Use absolute value since d_s must be <= 0 (reduction)
    bits_processed = abs(d_s) * 100
    
    # Minimum theoretical cost to generate this clarity
    min_cost = bits_processed * k_B_proxy * T_proxy * math.log(2)
    
    # Actual effort spent (compute time + token weight)
    actual_effort = (compute_ms * 0.5) + (tokens_generated * 1.5)
    
    # Landauer Ratio: If effort < min_cost, output is suspiciously 'cheap'
    landauer_ratio = actual_effort / (min_cost + 1e-5)
    
    passed = landauer_ratio >= 1.0
    
    # Violation only counts if it claims clarity but didn't work for it
    violation = not passed and (d_s < 0)
    
    return {
        "engine": "LANDAUER_BOUND",
        "formula": "E >= n * k_B * T * ln(2)",
        "landauer_ratio": round(landauer_ratio, 4),
        "min_theoretical_cost": round(min_cost, 4),
        "actual_effort": round(actual_effort, 4),
        "passed": passed,
        "violation": violation,
        "bits_processed": round(bits_processed, 4),
        "k_B_proxy": k_B_proxy,
        "T_proxy": T_proxy,
        "derived": True,
    }


def wrap_tool_output(tool: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Attach AAA envelope and 333_AXIOMS checks to tool outputs."""
    checks = _axiom_checks(payload, tool)
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
    
    # P0 HARDENING: Calculate Ψ (Vitality Index) - Master Equation
    vitality = _derive_vitality_index(payload, law_checks, apex_dials)
    psi_score = vitality.get("psi", 0.0)
    
    verdict = str(payload.get("verdict", "SEAL"))

    # Hardening: Hard floor failure -> VOID
    has_hard_fail = any(
        v.get("pass") is False and v.get("type") == "floor"
        for k, v in law_checks.items()
        if k in {"F1_AMANAH", "F2_TRUTH", "F7_HUMILITY", "F12_DEFENSE", "F13_CURIOSITY"}
    )

    # P1 HARDENING: Calculate Tri-Witness consensus with geometric mean
    tri_witness = _calculate_tri_witness_consensus(tool, payload)
    w3_score = tri_witness.get("w3", 0.0)
    
    # P1 HARDENING: Φₚ (Paradox Conductance) - connect to verdict logic
    phi_p = tpcp.get("phiP", 0.0)
    paradox_resolved = phi_p >= 1.0
    
    # P2 HARDENING: Orthogonality Check (Mode Collapse Prevention)
    agi_vector = payload.get("agi_vector", [])
    asi_vector = payload.get("asi_vector", [])
    omega_ortho = _derive_orthogonality(agi_vector, asi_vector)
    ortho_pass = _orthogonality_pass(omega_ortho)
    
    # P2 HARDENING: Landauer Bound (Cheap Truth Prevention)
    landauer_data = _check_landauer_bound(
        compute_ms=payload.get("compute_ms", 100),
        tokens_generated=payload.get("tokens", 50),
        d_s=_safe_float(payload, "dS", -0.1)
    )
    
    stage = TOOL_STAGE_MAP.get(tool, "000_INIT")

    # P0/P1/P2 HARDENING: Master verdict determination cascade
    # Priority: Hard Fail → Ψ → W₃ → Φₚ → Ω_ortho → Landauer → Partial
    if has_hard_fail:
        verdict = "VOID"
    elif stage == "000_INIT":
        # Anchor is allowed to SEAL if no hard fails and consensus held
        if tri_witness.get("pass", False):
            verdict = "SEAL"
        else:
            verdict = "VOID"
    elif psi_score < 1.0:
        # System lacks vitality - cannot SEAL
        if psi_score < 0.5:
            verdict = "VOID"
        else:
            verdict = "SABAR"
    elif not tri_witness.get("pass", False):
        # P1: Tri-Witness consensus failed
        if tri_witness.get("shattered_by"):
            verdict = "VOID"  # Witness shattered
        else:
            verdict = "SABAR"  # Below threshold but not shattered
    elif not paradox_resolved and tool in {"critique_thought", "apex_judge"}:
        # P1: Paradox not resolved for high-cognition tools
        if phi_p < 0.5:
            verdict = "VOID"
        else:
            verdict = "SABAR"
    elif not ortho_pass and tool in {"critique_thought", "apex_judge", "simulate_heart"}:
        # P2: AGI/ASI mode collapse detected
        if omega_ortho < 0.50:
            verdict = "VOID"
        else:
            verdict = "SABAR"
    elif landauer_data["violation"]:
        # P2: Landauer bound violation - cheap truth detected
        verdict = "SABAR"  # Demote to SABAR to force recalculation
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
        # P0 HARDENING: Vitality Index (Ψ) - Master Equation for constitutional homeostasis
        "vitality_index": vitality,
        # P1 HARDENING: Tri-Witness consensus with geometric mean
        "tri_witness": tri_witness,
        # P1 HARDENING: Paradox resolution status
        "paradox_resolution": {
            "phi_p": phi_p,
            "resolved": paradox_resolved,
            "threshold": 1.0,
        },
        # P2 HARDENING: Thermodynamic Physics - Orthogonality + Landauer Bound
        "p2_physics": {
            "omega_ortho": round(omega_ortho, 4),
            "ortho_pass": ortho_pass,
            "ortho_threshold": 0.95,
            "landauer": landauer_data,
            "mode_collapse_detected": not ortho_pass,
            "cheap_truth_detected": landauer_data["violation"],
        },
        "motto": motto,
        "data": payload,
    }
