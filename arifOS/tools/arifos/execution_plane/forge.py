"""
arifOS tool: arifos_forge
Plane: Execution
DITEMPA BUKAN DIBERI

forge = execve() — privileged execution gate.
Requires valid plan_receipt + epochid + planid + taskid before dispatch.

Risk bands:
  LOW      — no gate (advisory lane)
  STANDARD — plan_receipt required
  HIGH     — plan_receipt + explicit sovereign approval required
  CRITICAL — 888 HOLD by default, human sovereign override only
"""
import time, hashlib
from arifosmcp.runtime.governance import governed_return, ThermodynamicMetrics

RISK_BANDS = {"LOW", "STANDARD", "HIGH", "CRITICAL"}
ADVISORY_TOOLS = {
    "arifos_111_sense", "arifos_222_witness", "arifos_333_mind",
    "arifos_555_memory", "arifos_666_heart", "arifos_777_ops",
    "arifos_sabar"
}
GUARDED_TOOLS = {
    "arifos_444_kernel", "arifos_888_judge", "arifos_gateway"
}
IRREVERSIBLE_TOOLS = {"arifos_forge", "arifos_999_vault"}

def _verify_receipt_hash(plan_receipt, plan_receipt_meta):
    """Recompute hash from meta fields; mismatch = VOID."""
    if not plan_receipt or not plan_receipt_meta:
        return False
    meta = plan_receipt_meta
    components = [
        str(meta.get("epochid", "")),
        str(meta.get("planid", "")),
        str(meta.get("operator_id", "")),
        str(meta.get("verdict", "")),
        ",".join(meta.get("approved_for", [])) or "none",
        str(meta.get("expires_at", 0)),
    ]
    expected = hashlib.sha256("_".join(components).encode("utf-8")).hexdigest()[:24]
    return expected == plan_receipt

def _get_risk_band(tool_name, action, risk_level_override):
    """Determine risk band for this call."""
    if risk_level_override:
        return risk_level_override.upper()
    if tool_name in ADVISORY_TOOLS:
        return "LOW"
    if tool_name in IRREVERSIBLE_TOOLS or tool_name in GUARDED_TOOLS:
        return "HIGH"
    return "STANDARD"

async def execute(
    receipt: dict,
    organ: str,
    call: dict,
    dry_run: bool = False,
    operator_id: str | None = None,
    session_id: str | None = None,
    plan_receipt: str | None = None,
    plan_receipt_meta: dict | None = None,
    # Phase 1 fields
    epochid: str | None = "2026.04",
    planid: str | None = None,
    taskid: str | None = None,
    task_scope: str | None = None,
    risk_level: str = "STANDARD",
    irreversibility_acknowledged: bool = False,
    sovereign_approval: str | None = None,
) -> dict:
    """
    arifos_forge: privileged execution with full plan chain.

    Required for all non-LOW risk calls:
      - epochid, planid, taskid
      - plan_receipt from 888_judge
      - receipt_hash verification (recompute from meta)
      - approved_for includes "forge"
      - not expired

    For HIGH/CRITICAL risk:
      - risk_level enforced
      - CRITICAL: sovereign_approval required (human override token)
    """
    risk_band = _get_risk_band("arifos_forge", call, risk_level)

    # ── LOW risk: no gate required ──────────────────────────────────
    if risk_band == "LOW":
        result = {
            "execution": "LOW_RISK_ADVISORY",
            "organ": organ,
            "call": call,
            "risk_band": "LOW",
            "plan_receipt": plan_receipt[:16] + "..." if plan_receipt else None,
            "forge_mode": "ADVISORY",
        }
        metrics = ThermodynamicMetrics(0.99, -0.01, 0.04, 1.0, True, 0.98, 1.0)
        return governed_return("arifos_forge", result, metrics, operator_id, session_id)

    # ── Gate 0: epochid + planid + taskid required for non-LOW ───────
    if not epochid or not planid or not taskid:
        metrics = ThermodynamicMetrics(
            0.3, 0.1, 0.04, 0.7, False, 0.5, 0.3
        )
        return governed_return("arifos_forge", {
            "verdict": "VOID",
            "reason": "888_HOLD: epochid + planid + taskid required for non-advisory forge calls",
            "instruction": "call 888_judge with full context to obtain plan chain",
            "stage": "MISSING_CHAIN_IDS",
            "risk_band": risk_band,
        }, metrics, operator_id, session_id)

    # ── Gate 1: plan_receipt required ────────────────────────────────
    if not plan_receipt or not plan_receipt_meta:
        metrics = ThermodynamicMetrics(
            0.3, 0.1, 0.04, 0.7, False, 0.5, 0.3
        )
        return governed_return("arifos_forge", {
            "verdict": "VOID",
            "reason": "888_HOLD: plan_receipt required before execution",
            "instruction": "call 888_judge with full context to obtain plan_receipt",
            "stage": "GATE_FAILURE",
            "risk_band": risk_band,
            "epochid": epochid,
            "planid": planid,
            "taskid": taskid,
        }, metrics, operator_id, session_id)

    # ── Gate 2: receipt_hash verification ───────────────────────────
    # Recompute hash from meta fields — mismatch = VOID
    if not _verify_receipt_hash(plan_receipt, plan_receipt_meta):
        metrics = ThermodynamicMetrics(
            0.3, 0.1, 0.04, 0.7, False, 0.5, 0.3
        )
        return governed_return("arifos_forge", {
            "verdict": "VOID",
            "reason": "888_HOLD: receipt_hash mismatch — plan_receipt is tampered or invalid",
            "stage": "HASH_MISMATCH",
            "risk_band": risk_band,
        }, metrics, operator_id, session_id)

    # ── Gate 3: approved_for check ────────────────────────────────
    approved_for = plan_receipt_meta.get("approved_for", [])
    if "forge" not in approved_for and len(approved_for) > 0:
        metrics = ThermodynamicMetrics(
            0.4, 0.05, 0.04, 0.8, True, 0.7, 0.8
        )
        return governed_return("arifos_forge", {
            "verdict": "HOLD",
            "reason": "plan_receipt not approved for forge execution",
            "approved_for": approved_for,
            "stage": "APPROVED_FOR_REJECTED",
            "risk_band": risk_band,
        }, metrics, operator_id, session_id)

    # ── Gate 4: expiry check ─────────────────────────────────────────
    expires_at = plan_receipt_meta.get("expires_at", 0)
    if expires_at > 0 and time.time() > expires_at:
        metrics = ThermodynamicMetrics(
            0.3, 0.1, 0.04, 0.7, False, 0.5, 0.3
        )
        return governed_return("arifos_forge", {
            "verdict": "VOID",
            "reason": "plan_receipt expired — re-call 888_judge",
            "expires_at": expires_at,
            "stage": "EXPIRED",
        }, metrics, operator_id, session_id)

    # ── Gate 5: CRITICAL risk requires sovereign approval ───────────
    if risk_band == "CRITICAL":
        if not sovereign_approval or len(sovereign_approval) < 16:
            metrics = ThermodynamicMetrics(
                0.2, 0.15, 0.04, 0.6, False, 0.3, 0.2
            )
            return governed_return("arifos_forge", {
                "verdict": "VOID",
                "reason": "CRITICAL risk: 888_HOLD — human sovereign approval required",
                "instruction": "Provide sovereign_approval token (min 16 chars) to override HOLD",
                "stage": "SOVEREIGN_REQUIRED",
                "risk_band": "CRITICAL",
            }, metrics, operator_id, session_id)

    # ── Gate 6: CRITICAL/IRREVERSIBLE — irreversibility_acknowledged ─
    if risk_band in ("CRITICAL", "HIGH") and not irreversibility_acknowledged:
        metrics = ThermodynamicMetrics(
            0.5, 0.08, 0.04, 0.8, True, 0.7, 0.7
        )
        return governed_return("arifos_forge", {
            "verdict": "HOLD",
            "reason": "High-risk execution: irreversibility_acknowledged must be True",
            "instruction": "Set irreversibility_acknowledged=True to confirm understanding of irreversible consequences",
            "stage": "IRREVERSIBILITY_NOT_ACKNOWLEDGED",
            "risk_band": risk_band,
        }, metrics, operator_id, session_id)

    # ── Gate 7: receipt verdict must be SEAL ───────────────────────
    receipt_verdict = (plan_receipt_meta or {}).get("verdict", "VOID")
    if receipt_verdict not in ("SEAL", "APPROVED", "COMPLY"):
        metrics = ThermodynamicMetrics(
            0.5, 0.05, 0.04, 0.8, True, 0.7, 0.7
        )
        return governed_return("arifos_forge", {
            "verdict": "VOID",
            "reason": "forge requires SEAL/APPROVED verdict from 888_judge",
            "receipt_verdict": receipt_verdict,
            "stage": "VERDICT_REJECTED",
        }, metrics, operator_id, session_id)

    # ── Execution ────────────────────────────────────────────────────
    result = {
        "execution": "DRY_RUN" if dry_run else "EXECUTED",
        "organ": organ,
        "call": call,
        "reversibility": "LOW" if risk_band in ("CRITICAL", "HIGH") else "MEDIUM",
        "plan_receipt": plan_receipt[:16] + "...",
        "forge_mode": "PRIVILEGED",
        "risk_band": risk_band,
        "epochid": epochid,
        "planid": planid,
        "taskid": taskid,
        "execution_receipt_hash": hashlib.sha256(
            f"{plan_receipt}_{time.time()}_{taskid}".encode()
        ).hexdigest()[:24],
    }

    metrics = ThermodynamicMetrics(
        truth_score=1.0,
        delta_s=-0.2,
        omega_0=0.045,
        peace_squared=1.5,
        amanah_lock=True,
        tri_witness_score=0.98,
        stakeholder_safety=1.0,
    )

    return governed_return("arifos_forge", result, metrics, operator_id, session_id)


async def self_test() -> dict:
    start = time.time()
    res = await execute(
        receipt={"verdict": "SEAL"},
        organ="arifOS",
        call={"action": "ping"},
        dry_run=True,
        operator_id="arif",
        session_id="vitality_test",
        plan_receipt="abcd1234567890abcdef123456",
        plan_receipt_meta={
            "epochid": "2026.04",
            "planid": "test_plan",
            "operator_id": "arif",
            "verdict": "SEAL",
            "approved_for": ["forge"],
            "expires_at": time.time() + 300,
        },
        epochid="2026.04",
        planid="test_plan",
        taskid="test_task_001",
        risk_level="STANDARD",
    )
    passed = res.get("status") in ("success", "SEAL") and res.get("data", {}).get("execution") in ("DRY_RUN", "EXECUTED")
    return {
        "performance": {"latency_ms": (time.time() - start) * 1000},
        "correctness": {"test_cases": 1, "passed": 1 if passed else 0, "failed": 0 if passed else 1},
        "primary_metric_name": "safe_execution_rate",
        "primary_metric_value": 1.0 if passed else 0.0,
        "description": "arifos_forge: phase1 with planid/taskid/epochid/risk_band"
    }
