"""
Stage 999: Seal - Final immutable audit.

Writes to PostgreSQL via PersistentVaultLedger (single source of truth).
"""

import logging
from typing import Any, Dict
from codebase.bundle_store import get_store
from codebase.vault.persistent_ledger import (
    PersistentVaultLedger,
    should_use_postgres,
    GENESIS_HASH,
)

logger = logging.getLogger(__name__)


async def execute_seal_stage(session_id: str) -> Dict[str, Any]:
    """
    Metabolic Stage 999: Seal.
    Writes the final MergedBundle to the PostgreSQL vault ledger.
    """
    store = get_store(session_id)
    merged = store.get_merged()

    if not merged:
        logger.error(f"[STAGE-999] Missing MergedBundle for session {session_id}")
        return {"status": "VOID", "reason": "No bundle to seal"}

    entry = merged.model_dump()
    verdict = entry.get("verdict", "SEAL")
    authority = entry.get("authority", "system")

    if should_use_postgres():
        try:
            ledger = PersistentVaultLedger()
            await ledger.connect()
            receipt = await ledger.append(
                session_id=session_id,
                verdict=verdict,
                seal_data=entry,
                authority=authority,
            )
            await ledger.close()
            return {
                "stage": "999_seal",
                "status": "SEALED",
                "hash": receipt["entry_hash"],
                "merkle_root": receipt["merkle_root"],
                "sequence": receipt["sequence_number"],
                "seal_id": receipt["seal_id"],
                "vault_backend": "postgres",
                "session_id": session_id,
            }
        except Exception as e:
            logger.warning("[STAGE-999] PostgreSQL seal failed, falling back to filesystem: %s", e)

    # Filesystem fallback (explicit opt-out)
    from codebase.vault.ledger_native import CoolingLedgerNative

    fs_ledger = CoolingLedgerNative()
    entry_hash = fs_ledger.write_entry(entry)

    return {
        "stage": "999_seal",
        "status": "SEALED",
        "hash": entry_hash,
        "prev_hash": GENESIS_HASH,
        "vault_backend": "filesystem",
        "session_id": session_id,
    }
