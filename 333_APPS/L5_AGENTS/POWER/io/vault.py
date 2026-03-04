from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from typing import Any


def build_vault_entry(
    session_id: str, verdict: str, payload: dict[str, Any], agent_id: str
) -> dict[str, Any]:
    timestamp = datetime.now(timezone.utc).isoformat()
    digest = sha256(f"{session_id}|{verdict}|{timestamp}".encode("utf-8")).hexdigest()
    return {
        "ts": timestamp,
        "session_id": session_id,
        "verdict": verdict,
        "agent_id": agent_id,
        "zkpc_hash": digest,
        "payload": payload,
    }
