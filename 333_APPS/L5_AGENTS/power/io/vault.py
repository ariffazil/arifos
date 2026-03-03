from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def build_vault_entry(session_id: str, verdict: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "ts": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "verdict": verdict,
        "payload": payload,
    }
