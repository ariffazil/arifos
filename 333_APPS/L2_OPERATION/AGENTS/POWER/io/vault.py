from __future__ import annotations

import json
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any


def build_vault_entry(
    session_id: str, verdict: str, payload: dict[str, Any], agent_id: str
) -> dict[str, Any]:
    timestamp = datetime.now(timezone.utc).isoformat()
    # ZKPC hash must cover ALL fields — including agent_id and payload
    # so any post-hoc tampering is detectable
    payload_str = json.dumps(payload, sort_keys=True, default=str)
    digest = sha256(
        f"{session_id}|{verdict}|{timestamp}|{agent_id}|{payload_str}".encode()
    ).hexdigest()
    return {
        "ts": timestamp,
        "session_id": session_id,
        "verdict": verdict,
        "agent_id": agent_id,
        "zkpc_hash": digest,
        "payload": payload,
    }
