"""
arifOS tool: arifos_888_judge
Plane: Compute
DITEMPA BUKAN DIBERI

888JUDGE = LSM / policy decision point.
Issues plan_receipt for approved operations.
Persists PlanReceipt to canonical record.
"""
import time, hashlib
from arifosmcp.runtime.governance import governed_return, ThermodynamicMetrics

RISK_BANDS = {"LOW", "STANDARD", "HIGH", "CRITICAL"}

async def execute(
    evidence_bundle: dict | None = None,
    operator_id: str | None = None,
    session_id: str | None = None,
    context: str | None = None,
    risk_level: str = "STANDARD",
    # Phase 1 plan chain fields
    intent: str | None = None,
    planid: str | None = None,
    taskid: str | None = None,
    task_scope: list | str | None = None,
    sovereign_approval: str | None = None,
) -> dict:
    """
    arifos_888_judge: Constitutional review and verdict.

    Phase 1 additions:
      - intent: sovereign intent description
      - planid: first-class plan identifier
      - taskid: specific task within plan
      - task_scope: what this task authorizes (forge, vault, etc.)
      - sovereign_approval: human token for HIGH/CRITICAL overrides

    Returns:
      - verdict: SEAL / COMPLY / CAUTION / HOLD / SABAR / VOID
      - plan_receipt: hash tying this approval to epoch + plan + task
      - plan_receipt_meta: full chain metadata (epochid, planid, taskid, approved_for, expires_at)
    """
    evidence = evidence_bundle or {}
    ctx = context or "general operation"
    risk = risk_level.upper()

    # ── Determine risk band ─────────────────────────────────────────
    if risk not in RISK_BANDS:
        risk = "STANDARD"

    # ── Constitutional review logic ──────────────────────────────────
    if risk == "CRITICAL" and not (sovereign_approval and len(sovereign_approval) >= 16):
        verdict_str = "VOID"
        reason = "CRITICAL risk: 888_HOLD — human sovereign approval required"
        plan_receipt = None
        plan_meta = None
    elif risk == "HIGH" and not (sovereign_approval and len(sovereign_approval) >= 16):
        verdict_str = "HOLD"
        reason = "HIGH risk operations require human sovereign approval"
        plan_receipt = None
        plan_meta = None
    elif evidence.get("force_void"):
        verdict_str = "VOID"
        reason = evidence.get("void_reason", "Evidence requests VOID")
        plan_receipt = None
        plan_meta = None
    elif evidence.get("force_sabar"):
        verdict_str = "SABAR"
        reason = "Humility threshold triggered"
        plan_receipt = None
        plan_meta = None
    elif evidence.get("force_hold"):
        verdict_str = "HOLD"
        reason = evidence.get("hold_reason", "Manual HOLD requested")
        plan_receipt = None
        plan_meta = None
    else:
        verdict_str = "SEAL"
        reason = "Constitutional review passed — all floors satisfied"

    # ── Generate plan_receipt for approved verdicts ───────────────────
    _epoch_str = epochid if 'epochid' in dir() and epochid else "2026.04"
    _op = operator_id or "anon"
    _planid = planid or evidence.get("planid") or hashlib.sha256(
        f"{ctx}_{time.time()}".encode()
    ).hexdigest()[:16]
    _taskid = taskid or evidence.get("taskid") or f"task_{_planid[:8]}_{int(time.time())%1000:03d}"
    _task_scope = task_scope or evidence.get("task_scope") or []

    if verdict_str in ("SEAL", "COMPLY"):
        if risk == "HIGH":
            approved_for = ["888_judge"]  # Needs human sovereign override
        elif risk == "CRITICAL":
            approved_for = ["888_judge", "sovereign_override"]
        else:
            approved_for = _task_scope if _task_scope else ["forge", "999_vault", "kernel_routing"]

        # receipt_hash = sha256(epochid + planid + operator_id + verdict + approved_for + expires_at)
        _expires_at = time.time() + 300
        components = [_epoch_str, _planid, _op, verdict_str, ",".join(approved_for), str(_expires_at)]
        _verdict_hash = hashlib.sha256("_".join(components).encode("utf-8")).hexdigest()[:24]

        plan_meta = {
            "epochid": _epoch_str,
            "planid": _planid,
            "taskid": _taskid,
            "operator_id": _op,
            "verdict": verdict_str,
            "approved_for": approved_for,
            "expires_at": _expires_at,
            "issued_at": time.time(),
            "context": ctx,
            "risk_level": risk,
            "intent": intent or ctx,
        }
        plan_receipt = _verdict_hash
    else:
        approved_for = []
        plan_meta = None
        plan_receipt = None

    report = {
        "verdict": verdict_str,
        "reason": reason,
        "risk_level": risk,
        "context": ctx,
        "intent": intent or ctx,
        "planid": _planid if verdict_str in ("SEAL", "COMPLY") else None,
        "taskid": _taskid if verdict_str in ("SEAL", "COMPLY") else None,
        "plan_receipt": plan_receipt,
        "plan_receipt_meta": plan_meta,
        "evidence_bundle": evidence,
    }

    # ── Metrics ─────────────────────────────────────────────────────
    if verdict_str == "SEAL":
        metrics = ThermodynamicMetrics(1.0, -0.1, 0.04, 1.3, True, 0.98, 1.0)
    elif verdict_str == "HOLD":
        metrics = ThermodynamicMetrics(0.7, 0.05, 0.04, 0.9, True, 0.9, 0.8)
    elif verdict_str == "VOID":
        metrics = ThermodynamicMetrics(0.3, 0.1, 0.04, 0.7, False, 0.5, 0.3)
    else:
        metrics = ThermodynamicMetrics(0.95, 0.0, 0.04, 1.0, True, 0.95, 0.9)

    return governed_return("arifos_888_judge", report, metrics, operator_id, session_id)


async def self_test() -> dict:
    start = time.time()
    res = await execute(
        evidence_bundle={"test": "evidence"},
        operator_id="arif",
        session_id="vitality_test",
        context="forge ping test",
        risk_level="STANDARD",
        intent="Test forge ping",
        planid="test_plan_001",
        taskid="task_001",
        task_scope=["forge", "999_vault"],
    )
    passed = res.get("status") in ("success", "SEAL") and res.get("data", {}).get("plan_receipt") is not None
    return {
        "performance": {"latency_ms": (time.time() - start) * 1000},
        "correctness": {"test_cases": 1, "passed": 1 if passed else 0, "failed": 0 if passed else 1},
        "primary_metric_name": "verdict_calibration",
        "primary_metric_value": 1.0 if passed else 0.0,
        "description": "arifos_888_judge: phase1 with planid/taskid/epochid"
    }
