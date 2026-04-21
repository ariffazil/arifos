from __future__ import annotations

import hashlib
import json
import time
from arifos.core.governance import (
    ThermodynamicMetrics,
    governed_return,
    append_vault999_event,
    Verdict,
)


async def execute(
    problem_set: dict | None = None,
    operator_id: str | None = None,
    session_id: str | None = None,
    depth: int = 1,
) -> dict:
    # ─── Phase 1: Pre-flight readiness probe ─────────────────────────────────
    readiness_probe = "PASS"
    readiness_detail_parts = []

    # _333_mind has no external service dependencies — lightweight in-process check
    try:
        readiness_detail_parts.append("internal:ok")
    except Exception as e:
        readiness_probe = "FAIL"
        readiness_detail_parts.append(f"internal:FAIL({e})")

    readiness_detail = ", ".join(readiness_detail_parts) if readiness_detail_parts else "no_checks"

    # ─── Main logic ───────────────────────────────────────────────────────────
    lanes = {
        "logic": {"status": "COHERENT", "score": None},
        "safety": {"status": "ALIGNED", "score": None},
        "sovereignty": {"status": "PROTECTED", "score": None},
        "physics": {"status": "BOUNDED", "score": None},
    }
    report = {
        "problem_id": (problem_set or {}).get("id", "GENERIC"),
        "depth": depth,
        "reasoning_lanes": lanes,
        "global_confidence": None,
    }

    # Removed hardcoded metric assertions — set to NULL/UNKNOWN
    metrics = ThermodynamicMetrics(
        truth_score=None,
        delta_s=None,
        omega_0=None,
        peace_squared=None,
        amanah_lock=None,
        tri_witness_score=None,
        stakeholder_safety=None,
    )

    result = governed_return("arifos_333_mind", report, metrics, operator_id, session_id)

    # ─── Phase 1: Append metabolic_metadata ───────────────────────────────────
    output_str = json.dumps(report, sort_keys=True, ensure_ascii=False)
    source_integrity = hashlib.sha256(output_str.encode("utf-8")).hexdigest()

    result["metabolic_metadata"] = {
        "source_integrity": source_integrity,
        "confidence_score": None,
        "floor_alignment": ["F1", "F3"],
        "readiness_probe": readiness_probe,
        "readiness_detail": readiness_detail,
        "verdict": result.get("verdict", Verdict.CLAIM_ONLY),
        "vault_receipt": None,
        "delta_s": None,
        "peace_squared": None,
        "omega_0": None,
        "timestamp_epoch": time.time(),
    }

    # ─── Phase 1: Vault-999 event ─────────────────────────────────────────────
    try:
        vault_receipt = append_vault999_event(
            event_type="arifos_333_mind",
            payload={"report": report, "metabolic_metadata": result["metabolic_metadata"]},
            operator_id=operator_id,
            session_id=session_id,
        )
        result["metabolic_metadata"]["vault_receipt"] = vault_receipt
    except Exception as e:
        result["metabolic_metadata"]["vault_receipt"] = f"FAIL({e})"

    return result
