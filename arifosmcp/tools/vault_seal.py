from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from typing import Any

from arifosmcp.services.constitutional_metrics import get_last_seal_hash, store_stage_result

logger = logging.getLogger(__name__)

# Import precedent memory (F8 Genius - institutional memory)
try:
    from arifosmcp.vault.precedent_memory import embed_vault_entry
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

    # Wire OTel span attributes after persist
    from arifosmcp.telemetry import OTEL_AVAILABLE
    if OTEL_AVAILABLE:
        from opentelemetry import trace
        span = trace.get_current_span()
        if span and span.is_recording():
            span.set_attribute("vault.seal_id", vault_entry["seal_id"])
            span.set_attribute("vault.verdict", verdict)
            span.set_attribute("vault.eureka_score", governance_context.get("eureka_score", 0.0))
            span.set_attribute("vault.merkle_root", "")  # populated after actual seal
            span.set_attribute("vault.stage", "999_SEAL")
            span.set_attribute("vault.session_id", session_id)
            span.set_attribute("arifos.metabolic_stage", "999_SEAL")

    # F8 Genius: Embed to precedent memory (semantic interpretation)
    precedent_id = None
    if PRECEDENT_MEMORY_AVAILABLE:
        try:
            precedent_id = await embed_vault_entry(vault_entry)
            logger.info("[999_SEAL] Precedent memory updated: %s", precedent_id)
        except Exception as e:
            # F1 Amanah: Don't fail seal if precedent embedding fails
            logger.info("[999_SEAL] Precedent embedding skipped: %s", e)

    return {
        "status": "SEALED",
        "verdict": verdict,
        "session_id": session_id,
        "timestamp": timestamp,
        "precedent_id": precedent_id,
        "precedent_memory_enabled": PRECEDENT_MEMORY_AVAILABLE,
    }
