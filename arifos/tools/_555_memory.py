from __future__ import annotations

import hashlib
import json
import os
import socket
import time
from arifos.core.governance import (
    ThermodynamicMetrics,
    governed_return,
    append_vault999_event,
    Verdict,
)


async def execute(
    action: str = "query",
    query: str | None = None,
    operator_id: str | None = None,
    session_id: str | None = None,
) -> dict:
    # ─── Phase 1: Pre-flight readiness probe (postgres + redis) ─────────────────
    readiness_probe = "PASS"
    readiness_detail_parts = []

    # Postgres health check
    pg_host = os.getenv("ARIFOS_PG_HOST", "localhost")
    pg_port = os.getenv("ARIFOS_PG_PORT", "5432")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((pg_host, int(pg_port)))
        sock.close()
        readiness_detail_parts.append(f"postgres:{pg_port} ok")
    except Exception as e:
        readiness_probe = "FAIL"
        readiness_detail_parts.append(f"postgres:{pg_port} FAIL({e})")

    # Redis health check
    redis_host = os.getenv("ARIFOS_REDIS_HOST", "localhost")
    redis_port = os.getenv("ARIFOS_REDIS_PORT", "6379")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((redis_host, int(redis_port)))
        sock.close()
        readiness_detail_parts.append(f"redis:{redis_port} ok")
    except Exception as e:
        readiness_probe = "FAIL"
        readiness_detail_parts.append(f"redis:{redis_port} FAIL({e})")

    readiness_detail = ", ".join(readiness_detail_parts) if readiness_detail_parts else "no_checks"

    # ─── Main logic ───────────────────────────────────────────────────────────
    report = {
        "action": action,
        "query": query,
        "memory_status": "GOVERNED_RECALL",
        "temporal_coherence": None,
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

    result = governed_return("arifos_555_memory", report, metrics, operator_id, session_id)

    # ─── Phase 1: Append metabolic_metadata ───────────────────────────────────
    output_str = json.dumps(report, sort_keys=True, ensure_ascii=False)
    source_integrity = hashlib.sha256(output_str.encode("utf-8")).hexdigest()

    result["metabolic_metadata"] = {
        "source_integrity": source_integrity,
        "confidence_score": None,
        "floor_alignment": ["F2", "F4", "F7"],
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
            event_type="arifos_555_memory",
            payload={"report": report, "metabolic_metadata": result["metabolic_metadata"]},
            operator_id=operator_id,
            session_id=session_id,
        )
        result["metabolic_metadata"]["vault_receipt"] = vault_receipt
    except Exception as e:
        result["metabolic_metadata"]["vault_receipt"] = f"FAIL({e})"

    return result
