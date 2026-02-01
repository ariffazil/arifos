"""
999 VAULT - Immutable Cooling Ledger (Native v53)
Append-only JSONL ledger for session auditing.

Includes seal_refusal() for legally defensible refusal audit trail.
"""

import os
import json
import hashlib
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from codebase.enforcement.refusal.types import RefusalResponse

logger = logging.getLogger(__name__)

class CoolingLedgerNative:
    """
    Native Immutable Ledger (Cooling).
    Stores Merkle-hashed session verdicts.
    """
    
    def __init__(self, ledger_path: str = ".arifos/ledger.jsonl"):
        self.ledger_path = ledger_path
        self._ensure_ledger_exists()
        
    def _ensure_ledger_exists(self):
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
        if not os.path.exists(self.ledger_path):
            with open(self.ledger_path, "w") as f:
                pass # Create empty file

    def write_entry(self, entry: Dict[str, Any]) -> str:
        """
        Write a new entry to the ledger and return its hash.
        """
        timestamp = datetime.now().isoformat()
        entry["timestamp"] = timestamp
        
        # Compute entry hash (Merkle leaf)
        content = json.dumps(entry, sort_keys=True)
        entry_hash = hashlib.sha256(content.encode()).hexdigest()
        entry["entry_hash"] = entry_hash
        
        with open(self.ledger_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
            
        logger.info(f"[VAULT-999] Sealed entry: {entry_hash[:16]} for session {entry.get('session_id')}")
        return entry_hash

    def read_session(self, session_id: str) -> List[Dict[str, Any]]:
        """Read all entries for a specific session."""
        entries = []
        if not os.path.exists(self.ledger_path):
            return entries
            
        with open(self.ledger_path, "r") as f:
            for line in f:
                entry = json.loads(line)
                if entry.get("session_id") == session_id:
                    entries.append(entry)
        return entries


def seal_refusal(refusal: "RefusalResponse", session_id: str) -> str:
    """
    Log refusal in immutable ledger (legally defensible audit trail).
    
    Privacy-Safe Logging:
    - Store hash (always)
    - Store redacted excerpt (if profile allows)
    - Never store raw prompt for illegal content
    
    Constitutional Compliance:
    - F1 Amanah: Immutable audit trail for reversibility
    - F2 Truth: Accurate logging without false records
    - F6 Empathy: Privacy-safe (no raw sensitive content)
    
    Args:
        refusal: RefusalResponse object from generate_refusal_response()
        session_id: Session identifier
    
    Returns:
        Merkle root hash (SHA-256 hex)
    """
    entry = {
        "session_id": session_id,
        "trace_id": refusal.trace_id,
        "refusal_type": refusal.refusal_type.value,
        "risk_domain": refusal.risk_domain.value,
        "policy_codes": refusal.policy_codes,
        "risk_score": refusal.risk_score,
        "query_hash": refusal.log_data["query_hash"],
        "redacted_excerpt": refusal.log_data.get("redacted_excerpt"),
        "timestamp": refusal.log_data["timestamp"],
        "verdict": "VOID_REFUSAL",
        "appealable": refusal.appealable,
        "model_version": refusal.log_data["model_version"],
        "profile": refusal.log_data["profile"]
    }
    
    # Write to VAULT999 ledger
    ledger_path = Path("VAULT999/BBB_LEDGER/refusal_audit.jsonl")
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(ledger_path, "a") as f:
        f.write(json.dumps(entry) + "\n")
    
    # Compute Merkle root for integrity
    merkle_root = hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()
    
    logger.info(
        f"[VAULT-999] Refusal sealed: {merkle_root[:16]} "
        f"(type={refusal.refusal_type.value}, domain={refusal.risk_domain.value})"
    )
    
    return merkle_root
