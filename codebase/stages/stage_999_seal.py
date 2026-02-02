"""
Stage 999: Seal - EUREKA-filtered immutable audit.

Theory of Anomalous Contrast (888_SOUL_VERDICT.md):
- SEAL is EARNED (eureka >= 0.75) -> permanent vault (PostgreSQL or filesystem)
- SABAR is DEFAULT (0.50-0.75) -> cooling ledger (72h hold)
- TRANSIENT (< 0.50) -> not stored

Writes to PostgreSQL via PersistentVaultLedger (single source of truth).
"""

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict
from codebase.bundle_store import get_store
from codebase.vault import (
    PersistentVaultLedger,
    should_use_postgres,
    GENESIS_HASH,
    should_seal_to_vault,
)

logger = logging.getLogger(__name__)


async def execute_seal_stage(session_id: str) -> Dict[str, Any]:
    """
    Metabolic Stage 999: EUREKA-filtered Seal.
    Evaluates novelty via EUREKA Sieve before committing to vault.
    """
    # Deterministic timestamp for the entire seal operation
    seal_ts = datetime.now(timezone.utc).isoformat() + "Z"

    store = get_store(session_id)
    merged = store.get_merged()

    if not merged:
        logger.error(f"[STAGE-999] Missing MergedBundle for session {session_id}")
        return {
            "stage": "999_SEAL",
            "status": "VOID",
            "session_id": session_id,
            "apex_verdict": None,
            "eureka_verdict": None,
            "persisted_as": None,
            "timestamp": seal_ts,
            "reason": "No bundle to seal",
        }

    entry = merged.model_dump()
    apex_verdict = entry.get("verdict", "SEAL")  # preserve original
    authority = entry.get("authority", "system")

    # Ensure seal_id exists (idempotency key)
    seal_id = entry.get("seal_id") or str(uuid.uuid4())
    entry["seal_id"] = seal_id

    # EUREKA Sieve: Theory of Anomalous Contrast
    # Degradation: SABAR (doctrine: "SABAR is the default")
    query = str(entry.get("query", ""))
    response = str(entry.get("response", entry.get("draft", "")))
    trinity_bundle = {
        "agi": entry.get("agi_result", {}),
        "asi": entry.get("asi_result", {}),
        "apex": entry.get("apex_result", {}),
        "init": entry.get("init_result", {}),
    }

    try:
        _should_seal, eureka_metadata = await should_seal_to_vault(
            query=query,
            response=response,
            trinity_bundle=trinity_bundle,
        )
        eureka_verdict = eureka_metadata.get("verdict", "SABAR")
        eureka_score = eureka_metadata.get("eureka_score", 0.5)
    except Exception as e:
        logger.warning(f"[STAGE-999] EUREKA Sieve failed, defaulting to SABAR (doctrine): {e}")
        eureka_verdict = "SABAR"
        eureka_score = 0.5
        eureka_metadata = {
            "verdict": "SABAR", "eureka_score": 0.5,
            "error": str(e), "degraded": True,
        }

    # Idempotency: skip if this seal_id was already committed
    if should_use_postgres():
        try:
            ledger = PersistentVaultLedger()
            await ledger.connect()
            existing = await ledger.get_entries_by_session(session_id)
            await ledger.close()
            if isinstance(existing, list):
                for ex in existing:
                    if (ex.get("seal_id") or (ex.get("seal_data", {}) or {}).get("seal_id")) == seal_id:
                        logger.info(f"[STAGE-999] Idempotency: seal_id {seal_id[:8]} already committed, skipping")
                        return {
                            "stage": "999_SEAL",
                            "status": "ALREADY_SEALED",
                            "session_id": session_id,
                            "seal_id": seal_id,
                            "apex_verdict": apex_verdict,
                            "eureka_verdict": eureka_verdict,
                            "persisted_as": "vault",
                            "timestamp": seal_ts,
                        }
        except Exception as e:
            logger.debug(f"[STAGE-999] Idempotency check skipped: {e}")

    # TRANSIENT: Not meaningful enough to store
    if eureka_verdict == "TRANSIENT":
        logger.info(
            f"[STAGE-999] EUREKA TRANSIENT (score={eureka_score:.2f}): "
            f"session {session_id[:8]} not stored"
        )
        return {
            "stage": "999_SEAL",
            "status": "TRANSIENT",
            "apex_verdict": apex_verdict,
            "eureka_verdict": eureka_verdict,
            "persisted_as": None,
            "eureka": eureka_metadata,
            "session_id": session_id,
            "timestamp": seal_ts,
            "message": f"EUREKA Score {eureka_score:.2f}: Not meaningful enough to store",
        }

    # SABAR: Cooling ledger (72h hold)
    if eureka_verdict == "SABAR":
        logger.info(
            f"[STAGE-999] EUREKA SABAR (score={eureka_score:.2f}): "
            f"session {session_id[:8]} -> cooling ledger"
        )
        from codebase.vault.ledger_native import CoolingLedgerNative

        entry["eureka"] = eureka_metadata
        # Keep apex_verdict intact, don't overwrite entry["verdict"]
        fs_ledger = CoolingLedgerNative()
        entry_hash = fs_ledger.write_entry(entry)
        return {
            "stage": "999_SEAL",
            "status": "SABAR",
            "hash": entry_hash,
            "apex_verdict": apex_verdict,
            "eureka_verdict": eureka_verdict,
            "persisted_as": "cooling",
            "eureka": eureka_metadata,
            "vault_backend": "cooling",
            "session_id": session_id,
            "timestamp": seal_ts,
            "message": f"EUREKA Score {eureka_score:.2f}: Cooling period (72h)",
        }

    # SEAL: Permanent vault (EUREKA >= 0.75)
    logger.info(
        f"[STAGE-999] EUREKA SEAL (score={eureka_score:.2f}): "
        f"session {session_id[:8]} -> permanent vault"
    )
    entry["eureka"] = eureka_metadata

    if should_use_postgres():
        try:
            ledger = PersistentVaultLedger()
            await ledger.connect()
            receipt = await ledger.append(
                session_id=session_id,
                verdict=apex_verdict,
                seal_data=entry,
                authority=authority,
            )
            await ledger.close()
            return {
                "stage": "999_SEAL",
                "status": "SEALED",
                "hash": receipt["entry_hash"],
                "merkle_root": receipt["merkle_root"],
                "sequence": receipt["sequence_number"],
                "seal_id": receipt["seal_id"],
                "apex_verdict": apex_verdict,
                "eureka_verdict": eureka_verdict,
                "persisted_as": "vault",
                "eureka": eureka_metadata,
                "vault_backend": "postgres",
                "session_id": session_id,
                "timestamp": seal_ts,
            }
        except Exception as e:
            logger.warning("[STAGE-999] PostgreSQL seal failed, falling back to filesystem: %s", e)

    # Filesystem fallback
    from codebase.vault.ledger_native import CoolingLedgerNative

    fs_ledger = CoolingLedgerNative()
    entry_hash = fs_ledger.write_entry(entry)

    return {
        "stage": "999_SEAL",
        "status": "SEALED",
        "hash": entry_hash,
        "prev_hash": GENESIS_HASH,
        "apex_verdict": apex_verdict,
        "eureka_verdict": eureka_verdict,
        "persisted_as": "vault",
        "eureka": eureka_metadata,
        "vault_backend": "filesystem",
        "session_id": session_id,
        "timestamp": seal_ts,
    }
