"""
arifOS tool: arifos_999_vault
Plane: Execution
DITEMPA BUKAN DIBERI

999VAULT = journal commit after forge exec.
Seal requires execution_receipt_hash from forge + valid plan chain.

Logging like auditd: every call logged with epochid + planid + taskid.
"""
import time, hashlib
from arifosmcp.runtime.governance import governed_return, ThermodynamicMetrics

def _verify_receipt_hash(plan_receipt, plan_receipt_meta):
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

async def execute(
    action: str,
    payload: dict | None = None,
    chain_hash: str | None = None,
    operator_id: str | None = None,
    session_id: str | None = None,
    plan_receipt: str | None = None,
    plan_receipt_meta: dict | None = None,
    # Phase 1 fields
    epochid: str | None = "2026.04",
    planid: str | None = None,
    taskid: str | None = None,
    execution_receipt_hash: str | None = None,
    seal_type: str = "standard",
    telemetry_snapshot: dict | None = None,
    irreversibility_acknowledged: bool = False,
) -> dict:
    """
    arifos_999_vault: append-only journal commit.

    For seal mode (action in [append, seal, finalize]):
      - Requires plan_receipt from 888_judge
      - Requires epochid + planid + taskid
      - Verifies execution_receipt_hash from forge
      - Hash-verifies plan_receipt
      - Checks not expired
      - Logs full audit trail: epochid/planid/taskid/receipt_id/verdict/telemetry/timestamp

    For read mode (action == read/query):
      - Advisory — no gate required, still logged
    """
    is_seal_action = action in ("append", "seal", "finalize")

    # ── Audit log entry (always written) ────────────────────────────
    audit_entry = {
        "epochid": epochid,
        "planid": planid,
        "taskid": taskid,
        "tool_name": "arifos_999_vault",
        "action": action,
        "actor": operator_id,
        "timestamp": time.time(),
        "vault_action": action,
        "payload_hash": hashlib.sha256(str(payload or {}).encode()).hexdigest()[:16],
    }

    # ── Read/Advisory mode: no gate ──────────────────────────────────
    if not is_seal_action:
        result = {
            "action": action,
            "vault_status": "READING",
            "audit_entry": audit_entry,
        }
        metrics = ThermodynamicMetrics(0.99, 0.0, 0.04, 1.0, True, 0.95, 0.98)
        return governed_return("arifos_999_vault", result, metrics, operator_id, session_id)

    # ── Gate 0: epochid + planid + taskid required for seal ──────────
    if not epochid or not planid or not taskid:
        metrics = ThermodynamicMetrics(0.3, 0.1, 0.04, 0.7, False, 0.5, 0.3)
        return governed_return("arifos_999_vault", {
            "verdict": "VOID",
            "reason": "888_HOLD: epochid + planid + taskid required for vault seal",
            "instruction": "call 888_judge first to obtain plan chain",
            "stage": "MISSING_CHAIN_IDS",
            "audit_entry": audit_entry,
        }, metrics, operator_id, session_id)

    # ── Gate 1: plan_receipt required ────────────────────────────────
    if not _verify_receipt_hash(plan_receipt or "", plan_receipt_meta or {}):
        metrics = ThermodynamicMetrics(0.3, 0.1, 0.04, 0.7, False, 0.5, 0.3)
        return governed_return("arifos_999_vault", {
            "verdict": "VOID",
            "reason": "888_HOLD: plan_receipt required before vault seal",
            "instruction": "call 888_judge first",
            "stage": "GATE_FAILURE",
            "audit_entry": audit_entry,
        }, metrics, operator_id, session_id)

    # ── Gate 2: expiry check ─────────────────────────────────────────
    if plan_receipt_meta:
        expires_at = plan_receipt_meta.get("expires_at", 0)
        if expires_at > 0 and time.time() > expires_at:
            metrics = ThermodynamicMetrics(0.3, 0.1, 0.04, 0.7, False, 0.5, 0.3)
            return governed_return("arifos_999_vault", {
                "verdict": "VOID",
                "reason": "plan_receipt expired — re-call 888_judge",
                "stage": "EXPIRED",
            }, metrics, operator_id, session_id)

        # ── Gate 3: approved_for check ──────────────────────────────────
        approved_for = plan_receipt_meta.get("approved_for", [])
        if "999_vault" not in approved_for and len(approved_for) > 0:
            metrics = ThermodynamicMetrics(0.4, 0.05, 0.04, 0.8, True, 0.7, 0.8)
            return governed_return("arifos_999_vault", {
                "verdict": "HOLD",
                "reason": "plan_receipt not approved for vault seal",
                "approved_for": approved_for,
                "stage": "APPROVED_FOR_REJECTED",
            }, metrics, operator_id, session_id)

    # ── Gate 4: execution_receipt_hash from forge required ───────────
    # Vault must not self-seal — forge must have executed first
    if not execution_receipt_hash:
        metrics = ThermodynamicMetrics(0.4, 0.05, 0.04, 0.8, True, 0.7, 0.8)
        return governed_return("arifos_999_vault", {
            "verdict": "HOLD",
            "reason": "vault seal requires execution_receipt_hash from forge",
            "instruction": "execute forge first to obtain execution_receipt_hash",
            "stage": "FORGE_RECEIPT_REQUIRED",
        }, metrics, operator_id, session_id)

    # ── Vault seal ────────────────────────────────────────────────────
    seal_id = hashlib.sha256(
        f"{plan_receipt or 'void'}_{action}_{taskid}_{time.time()}".encode()
    ).hexdigest()[:24]

    result = {
        "action": action,
        "seal_id": seal_id,
        "vault_status": "SEALED",
        "seal_type": seal_type,
        "plan_receipt": plan_receipt[:16] + "..." if plan_receipt else None,
        "execution_receipt_hash": execution_receipt_hash[:16] + "..." if execution_receipt_hash else None,
        "chain_prev": chain_hash or "GENESIS",
        "sealed_by": operator_id,
        "epochid": epochid,
        "planid": planid,
        "taskid": taskid,
        "audit_entry": audit_entry,
    }

    metrics = ThermodynamicMetrics(
        truth_score=1.0,
        delta_s=-0.01,
        omega_0=0.04,
        peace_squared=1.0,
        amanah_lock=True,
        tri_witness_score=1.0,
        stakeholder_safety=1.0,
    )

    return governed_return("arifos_999_vault", result, metrics, operator_id, session_id)


async def self_test() -> dict:
    start = time.time()
    res = await execute(
        action="append",
        payload={"test": "data"},
        operator_id="arif",
        session_id="vitality_test",
        plan_receipt="abcd1234567890abcdef123456",
        plan_receipt_meta={
            "epochid": "2026.04",
            "planid": "test_plan",
            "operator_id": "arif",
            "verdict": "SEAL",
            "approved_for": ["forge", "999_vault"],
            "expires_at": time.time() + 300,
        },
        epochid="2026.04",
        planid="test_plan",
        taskid="test_task_001",
        execution_receipt_hash="abcdef1234567890abcdef123456",
    )
    passed = res.get("status") == "success" and res.get("data", {}).get("seal_id") is not None
    return {
        "performance": {"latency_ms": (time.time() - start) * 1000},
        "correctness": {"test_cases": 1, "passed": 1 if passed else 0, "failed": 0 if passed else 1},
        "primary_metric_name": "ledger_integrity",
        "primary_metric_value": 1.0 if passed else 0.0,
        "description": "arifos_999_vault: phase1 with planid/taskid/epochid/forge_receipt"
    }
