"""
WELL MCP Server — Human Substrate Governance Layer
Phase 1: Immutable Ledger & Observability

W0 Sovereignty Invariant: WELL holds a mirror, not a veto.
WELL informs. arifOS judges. A-FORGE executes. Hierarchy is invariant.
"""

from __future__ import annotations

import hashlib
import json
import datetime
from pathlib import Path
from typing import Any

from fastmcp import FastMCP, Context

# ── Paths ──────────────────────────────────────────────────────────────────────
WELL_DIR = Path(__file__).parent
STATE_PATH = WELL_DIR / "state.json"
EVENTS_PATH = WELL_DIR / "events.jsonl"
VAULT_LEDGER_PATH = Path(
    __import__("os").environ.get("WELL_VAULT_PATH", str(WELL_DIR / "vault_ledger.jsonl"))
)

# ── Server ─────────────────────────────────────────────────────────────────────
mcp = FastMCP(
    name="WELL",
    instructions=(
        "WELL is the Human Substrate Governance Layer for operator Arif. "
        "It tracks biological telemetry (sleep, stress, cognition, metabolism) "
        "and reflects readiness to the arifOS constitutional kernel. "
        "W0: WELL holds a mirror, not a veto. Operator sovereignty is invariant."
    ),
)

# ── Helpers ────────────────────────────────────────────────────────────────────

def _load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "operator_id": "arif",
            "metrics": {},
            "well_score": 50,
            "floors_violated": [],
        }
    with open(STATE_PATH) as f:
        return json.load(f)


def _save_state(state: dict[str, Any]) -> None:
    state["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    STATE_PATH.write_text(json.dumps(state, indent=2))


def _append_event(event: dict[str, Any]) -> None:
    event["epoch"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with open(EVENTS_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")


def _compute_score(metrics: dict[str, Any]) -> tuple[float, list[str]]:
    """Compute WELL score (0-100) and floor violations from metrics."""
    score = 100.0
    violations: list[str] = []

    sleep = metrics.get("sleep", {})
    cognitive = metrics.get("cognitive", {})
    stress = metrics.get("stress", {})
    metabolic = metrics.get("metabolic", {})

    # W1 — Sleep Integrity
    debt = sleep.get("sleep_debt_days", 0)
    quality = sleep.get("quality_score", 10)
    hours = sleep.get("last_night_hours", 8)
    score -= min(debt * 8, 24)
    score -= max(0, (7 - hours) * 3)
    score -= max(0, (8 - quality) * 1.5)
    if debt > 2:
        violations.append("W1_SLEEP_DEBT")

    # W5 — Cognitive Entropy
    clarity = cognitive.get("clarity", 10)
    fatigue = cognitive.get("decision_fatigue", 0)
    score -= max(0, (8 - clarity) * 2)
    score -= fatigue * 1.5
    if clarity < 4:
        violations.append("W5_COGNITIVE_ENTROPY")

    # Stress load
    load = stress.get("subjective_load", 0)
    restless = stress.get("restlessness", 0)
    score -= load * 1.2
    score -= restless * 0.8

    # Metabolic
    stability = metabolic.get("perceived_stability", 10)
    score -= max(0, (7 - stability) * 1.5)
    if metabolic.get("hydration_status") == "DEHYDRATED":
        score -= 5

    # W6 — Incentive Decoupling (static floor, Phase 3)
    score = round(max(0.0, min(100.0, score)), 1)
    return score, violations


# ── Tools ──────────────────────────────────────────────────────────────────────

@mcp.tool()
def well_state(ctx: Context | None = None) -> dict[str, Any]:
    """
    Get the current WELL state — biological telemetry snapshot for operator Arif.
    Returns score, floor violations, and all metric dimensions.
    """
    state = _load_state()
    return {
        "ok": True,
        "operator_id": state.get("operator_id", "arif"),
        "timestamp": state.get("timestamp"),
        "well_score": state.get("well_score", 50),
        "floors_violated": state.get("floors_violated", []),
        "metrics": state.get("metrics", {}),
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
    }


@mcp.tool()
def well_log(
    # Sleep
    sleep_hours: float | None = None,
    sleep_debt_days: float | None = None,
    sleep_quality: float | None = None,
    # Stress
    stress_load: float | None = None,
    restlessness: float | None = None,
    hrv_proxy: float | None = None,
    # Cognitive
    clarity: float | None = None,
    decision_fatigue: float | None = None,
    focus_durability: float | None = None,
    # Metabolic
    fasting_hours: float | None = None,
    metabolic_stability: float | None = None,
    hydration: str | None = None,
    # Structural
    pain_sites: list[str] | None = None,
    movement_count: float | None = None,
    # Optional note
    note: str | None = None,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """
    Log a biological telemetry update for operator Arif.
    Updates state.json, recomputes WELL score, checks floor violations.
    Only provide dimensions you're logging — omitted fields are unchanged.
    """
    state = _load_state()
    metrics = state.get("metrics", {})

    # ── Merge incoming readings ────────────────────────────────────
    if any(v is not None for v in [sleep_hours, sleep_debt_days, sleep_quality]):
        sleep = dict(metrics.get("sleep", {}))
        if sleep_hours is not None:
            sleep["last_night_hours"] = sleep_hours
        if sleep_debt_days is not None:
            sleep["sleep_debt_days"] = sleep_debt_days
        if sleep_quality is not None:
            sleep["quality_score"] = sleep_quality
        metrics["sleep"] = sleep

    if any(v is not None for v in [stress_load, restlessness, hrv_proxy]):
        stress = dict(metrics.get("stress", {}))
        if stress_load is not None:
            stress["subjective_load"] = stress_load
        if restlessness is not None:
            stress["restlessness"] = restlessness
        if hrv_proxy is not None:
            stress["hrv_proxy"] = hrv_proxy
        metrics["stress"] = stress

    if any(v is not None for v in [clarity, decision_fatigue, focus_durability]):
        cog = dict(metrics.get("cognitive", {}))
        if clarity is not None:
            cog["clarity"] = clarity
        if decision_fatigue is not None:
            cog["decision_fatigue"] = decision_fatigue
        if focus_durability is not None:
            cog["focus_durability"] = focus_durability
        metrics["cognitive"] = cog

    if any(v is not None for v in [fasting_hours, metabolic_stability, hydration]):
        meta = dict(metrics.get("metabolic", {}))
        if fasting_hours is not None:
            meta["fasting_window_hours"] = fasting_hours
        if metabolic_stability is not None:
            meta["perceived_stability"] = metabolic_stability
        if hydration is not None:
            meta["hydration_status"] = hydration.upper()
        metrics["metabolic"] = meta

    if any(v is not None for v in [pain_sites, movement_count]):
        struct = dict(metrics.get("structural", {}))
        if pain_sites is not None:
            struct["pain_map"] = pain_sites
        if movement_count is not None:
            struct["movement_frequency_daily"] = movement_count
        metrics["structural"] = struct

    # ── Recompute score ────────────────────────────────────────────
    score, violations = _compute_score(metrics)

    state["metrics"] = metrics
    state["well_score"] = score
    state["floors_violated"] = violations
    _save_state(state)

    event: dict[str, Any] = {
        "event": "WELL_LOG",
        "well_score": score,
        "floors_violated": violations,
    }
    if note:
        event["note"] = note
    _append_event(event)

    return {
        "ok": True,
        "well_score": score,
        "floors_violated": violations,
        "status": "DEGRADED" if violations else "STABLE",
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
    }


@mcp.tool()
def well_pressure(
    load_delta: float,
    source: str = "forge",
    ctx: Context | None = None,
) -> dict[str, Any]:
    """
    Signal cognitive pressure/load from an external source (e.g. A-FORGE).
    Increments decision_fatigue and potentially triggers W6 Metabolic Pause.
    """
    state = _load_state()
    metrics = state.get("metrics", {})
    cog = dict(metrics.get("cognitive", {"clarity": 10, "decision_fatigue": 0}))
    
    # Increment fatigue
    old_fatigue = cog.get("decision_fatigue", 0)
    new_fatigue = min(10.0, old_fatigue + load_delta)
    cog["decision_fatigue"] = new_fatigue
    metrics["cognitive"] = cog
    
    # W6 Logic: Repetitive Pressure Spike
    # If fatigue jumps > 2.0 in a single signal, flag as high-frequency loop
    violations = state.get("floors_violated", [])
    if load_delta > 2.0 and "W6_METABOLIC_PAUSE" not in violations:
        violations.append("W6_METABOLIC_PAUSE")
    
    # Recompute overall score
    score, new_violations = _compute_score(metrics)
    # Merge violations
    for v in new_violations:
        if v not in violations:
            violations.append(v)
            
    state["metrics"] = metrics
    state["well_score"] = score
    state["floors_violated"] = violations
    _save_state(state)
    
    _append_event({
        "event": "PRESSURE_SIGNAL",
        "source": source,
        "load_delta": load_delta,
        "new_fatigue": new_fatigue,
        "w6_triggered": "W6_METABOLIC_PAUSE" in violations
    })
    
    return {
        "ok": True,
        "well_score": score,
        "decision_fatigue": new_fatigue,
        "w6_active": "W6_METABOLIC_PAUSE" in violations,
        "message": "Metabolic Pause active. Step away for 15 minutes." if "W6_METABOLIC_PAUSE" in violations else "Pressure logged."
    }


@mcp.tool()
def well_readiness(ctx: Context | None = None) -> dict[str, Any]:
    """
    Reflect current biological readiness for arifOS JUDGE context.
    Returns score, floor status, and a readiness verdict for the constitutional kernel.
    W0: This is informational only — WELL never blocks unilaterally.
    """
    state = _load_state()
    score = state.get("well_score", 50)
    violations = state.get("floors_violated", [])
    metrics = state.get("metrics", {})

    if violations:
        verdict = "DEGRADED"
        message = f"Substrate flagging: {', '.join(violations)}. Strategic forge bandwidth throttled."
        bandwidth = "RESTRICTED"
    elif score >= 80:
        verdict = "OPTIMAL"
        message = "Substrate stable and high-capacity. Full forge bandwidth available."
        bandwidth = "FULL"
    elif score >= 60:
        verdict = "FUNCTIONAL"
        message = "Substrate functional. Normal forge operations permitted."
        bandwidth = "NORMAL"
    else:
        verdict = "LOW_CAPACITY"
        message = "Substrate low-capacity. Recommend rest before strategic decisions."
        bandwidth = "REDUCED"

    # SABAR protocol — Phase 1 advisory
    sabar_advisory = score < 60 or bool(violations)

    return {
        "ok": True,
        "verdict": verdict,
        "well_score": score,
        "bandwidth": bandwidth,
        "floors_violated": violations,
        "sabar_advisory": sabar_advisory,
        "message": message,
        "snapshot": {
            "sleep_hours": metrics.get("sleep", {}).get("last_night_hours"),
            "clarity": metrics.get("cognitive", {}).get("clarity"),
            "stress_load": metrics.get("stress", {}).get("subjective_load"),
        },
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
    }


@mcp.tool()
async def well_init(
    session_id: str | None = None,
    actor_id: str = "well-substrate",
    ctx: Context | None = None,
) -> dict[str, Any]:
    """
    Open a WELL governance session — writes a 000_INIT event to VAULT999.
    Call this at the start of any WELL-aware session to anchor identity and
    connect to the canonical Merkle chain.
    Returns session_id and chain position for subsequent well_anchor seals.
    W0: WELL holds a mirror, not a veto. Operator sovereignty is invariant.
    """
    import sys
    import uuid as _uuid

    ARIFOS_PATH = "/root/arifOS"
    if ARIFOS_PATH not in sys.path:
        sys.path.append(ARIFOS_PATH)

    sid = session_id or f"well-session-{_uuid.uuid4().hex[:12]}"

    try:
        from arifosmcp.runtime.vault_postgres import seal_to_vault

        state = _load_state()
        score = state.get("well_score", 50)
        violations = state.get("floors_violated", [])

        res = await seal_to_vault(
            event_type="WELL_SESSION_INIT",
            session_id=sid,
            actor_id=actor_id,
            stage="000_INIT",
            verdict="ACTIVE",
            payload={
                "well_score": score,
                "floors_violated": violations,
                "w0": "OPERATOR_VETO_INTACT",
            },
            risk_tier="low",
        )

        _append_event({
            "event": "WELL_INIT",
            "session_id": sid,
            "vault_id": res.ledger_id if hasattr(res, "ledger_id") else str(res),
        })

        return {
            "ok": True,
            "session_id": sid,
            "stage": "000_INIT",
            "well_score": score,
            "chain_hash": res.chain_hash if hasattr(res, "chain_hash") else "",
            "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
        }
    except Exception as e:
        return {"ok": False, "session_id": sid, "error": str(e)}


@mcp.tool()
async def well_anchor(
    force: bool = False,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """
    Anchor current WELL state to arifOS VAULT999 (PostgreSQL + Merkle).
    Ensures human substrate readiness is immutably recorded.
    """
    import sys
    from pathlib import Path
    
    # Ensure arifOS is in path for bridge
    ARIFOS_PATH = "/root/arifOS"
    if ARIFOS_PATH not in sys.path:
        sys.path.append(ARIFOS_PATH)
        
    try:
        from arifosmcp.runtime.well_bridge import anchor_well_to_vault
        res = await anchor_well_to_vault(force=force)
        
        if res["ok"]:
            _append_event({
                "event": "VAULT_ANCHOR_SQL",
                "vault_id": res["vault_id"],
                "hash": res["hash"]
            })
            
        return res
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def well_check_floors(ctx: Context | None = None) -> dict[str, Any]:
    """
    Check WELL floor status against all W-Floors.
    Returns per-floor status, overall verdict, and bandwidth recommendation for arifOS JUDGE.
    """
    state = _load_state()
    metrics = state.get("metrics", {})
    sleep = metrics.get("sleep", {})
    cognitive = metrics.get("cognitive", {})

    floors: dict[str, dict[str, Any]] = {
        "W0": {
            "name": "Sovereignty Invariant",
            "status": "INVARIANT",
            "detail": "Operator veto always intact. WELL never self-authorizes.",
        },
        "W1": {
            "name": "Sleep Integrity",
            "status": "OK",
            "threshold": "sleep_debt_days <= 2",
            "current": sleep.get("sleep_debt_days", 0),
        },
        "W5": {
            "name": "Cognitive Entropy",
            "status": "OK",
            "threshold": "clarity >= 4",
            "current": cognitive.get("clarity", 10),
        },
        "W6": {
            "name": "Incentive Decoupling",
            "status": "PHASE_3_PENDING",
            "detail": "Repetitive intent loop detection pending wearable integration.",
        },
    }

    if sleep.get("sleep_debt_days", 0) > 2:
        floors["W1"]["status"] = "VIOLATED"
    if cognitive.get("clarity", 10) < 4:
        floors["W5"]["status"] = "VIOLATED"

    violated = [k for k, v in floors.items() if v["status"] == "VIOLATED"]
    score = state.get("well_score", 50)

    return {
        "ok": True,
        "floors": floors,
        "violated": violated,
        "well_score": score,
        "verdict": "FLOORS_CLEAR" if not violated else "FLOORS_VIOLATED",
        "bandwidth_recommendation": "RESTRICTED" if violated else "NORMAL",
        "w0": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT",
    }


# ── Entry ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run()


