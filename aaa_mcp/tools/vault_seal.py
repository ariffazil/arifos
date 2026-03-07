from aaa_mcp.services.constitutional_metrics import store_stage_result, get_last_seal_hash


async def vault_seal(
    session_id: str,
    verdict: str,
    payload: dict[str, Any],
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    999_SEAL: Immutable Audit Ledger.
    Final stage of the metabolic loop (F1 Amanah).

    Persists the final decision and payload to the session ledger.
    """
    if metadata is None:
        metadata = {}

    # Capture Merkle Chain Hash (F1 Amanah)
    metadata["ledger_chain_hash"] = get_last_seal_hash(session_id)

    # Persist to ledger
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

    return {
        "status": "SEALED",
        "verdict": verdict,
        "session_id": session_id,
        "timestamp": metadata.get("timestamp"),
    }
