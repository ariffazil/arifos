from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from arifosmcp.transport.services.constitutional_metrics import (
    get_last_seal_hash,
    store_stage_result,
)

# Import precedent memory (F8 Genius - institutional memory)
try:
    from arifosmcp.transport.vault.precedent_memory import embed_vault_entry

    PRECEDENT_MEMORY_AVAILABLE = True
except ImportError:
    PRECEDENT_MEMORY_AVAILABLE = False


async def vault_seal(
    session_id: str,
    verdict: str,
    payload: dict[str, Any],
    metadata: dict[str, Any] | None = None,
    governance_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    999_SEAL: Immutable Audit Ledger.
    Final stage of the metabolic loop (F1 Amanah).

    Persists the final decision and payload to the session ledger.
    Optionally embeds governance explanation to precedent memory (F8 Genius).

    Args:
        session_id: Constitutional session identifier
        verdict: Final verdict (SEAL, VOID, SABAR, 888_HOLD, PARTIAL)
        payload: Sealed data payload
        metadata: Additional metadata
        governance_context: Optional context for precedent memory embedding
    """
    if metadata is None:
        metadata = {}
    if governance_context is None:
        governance_context = {}

    # Capture Merkle Chain Hash (F1 Amanah)
    metadata["ledger_chain_hash"] = get_last_seal_hash(session_id)
    timestamp = metadata.get("timestamp") or datetime.now(timezone.utc).isoformat()
    metadata["timestamp"] = timestamp

    # Build vault entry for ledger
    vault_entry = {
        "seal_id": f"SEAL-{session_id}-{int(time.time())}",
        "session_id": session_id,
        "timestamp": timestamp,
        "verdict": verdict,
        "payload": payload,
        "metadata": metadata,
        "floors_failed": governance_context.get("floors_failed", []),
        "eureka_score": governance_context.get("eureka_score", 0.0),
        "thermodynamics": governance_context.get("thermodynamics", {}),
    }

    # Persist to ledger (exact truth)
    store_stage_result(
        session_id=session_id,
        stage="999_SEAL",
        result={
            "verdict": verdict,
            "payload": payload,
            "metadata": metadata,
            "sealed": True,
        },
    )

    # F8 Genius: Embed to precedent memory (semantic interpretation)
    precedent_id = None
    if PRECEDENT_MEMORY_AVAILABLE:
        try:
            precedent_id = await embed_vault_entry(vault_entry)
            print(f"[999_SEAL] Precedent memory updated: {precedent_id}")
        except Exception as e:
            # F1 Amanah: Don't fail seal if precedent embedding fails
            print(f"[999_SEAL] Precedent embedding skipped: {e}")

    return {
        "status": "SEALED",
        "verdict": verdict,
        "session_id": session_id,
        "timestamp": timestamp,
        "precedent_id": precedent_id,
        "precedent_memory_enabled": PRECEDENT_MEMORY_AVAILABLE,
    }
