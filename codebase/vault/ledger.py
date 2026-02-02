"""
canonical_core/vault/ledger.py — Immutable Ledger

Append-only JSONL ledger with hash chaining.
"""

import os
import json
import hashlib
from typing import Dict, Any


class VaultLedger:
    """Immutable Append-Only Ledger."""

    def __init__(self, storage_path: str):
        self.ledger_path = os.path.join(storage_path, "vault.jsonl")
        os.makedirs(storage_path, exist_ok=True)

    def append_entry(self, entry: Dict[str, Any]) -> str:
        """
        Append entry to ledger.
        Computes current_hash = SHA256(entry + previous_hash)
        """
        prev_hash = self.get_last_hash()
        entry["previous_hash"] = prev_hash

        # Serialize deterministically
        serialized = json.dumps(entry, sort_keys=True)
        current_hash = hashlib.sha256(serialized.encode()).hexdigest()
        entry["current_hash"] = current_hash

        with open(self.ledger_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

        return current_hash

    def get_last_hash(self) -> str:
        """Read the last hash from the file."""
        if not os.path.exists(self.ledger_path):
            return "0" * 64  # Genesis hash

        try:
            with open(self.ledger_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if not lines:
                    return "0" * 64
                last = json.loads(lines[-1])
                return last.get("current_hash", "0" * 64)
        except Exception:
            return "0" * 64

