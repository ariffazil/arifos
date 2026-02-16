"""
arifOS v60: Constitutional Memory Engine (The Memory)
======================================================

Immutable audit trail (VAULT999 - Stage 999).

Floors: F1 (Amanah - Reversibility), F13 (Sovereign - Audit Trail)
Operations: write, read, query

Version: v60.0-FORGE
Author: Muhammad Arif bin Fazil
License: AGPL-3.0-only
DITEMPA BUKAN DIBERI 💎🔥🧠
"""

import json
from pathlib import Path
from typing import List, Literal, Optional, Dict, Any
from datetime import datetime, timezone

from shared.types import VaultOutput, VaultEntry
from shared.crypto import sha256_hash, sha256_hash_dict, merkle_root

# ============================================================================
# MEMORY STORAGE BACKEND
# ============================================================================


class MemoryBackend:
    """
    Constitutional memory backend (file-based for v60).

    F1 Amanah: Immutable, append-only.
    F13 Sovereign: Complete audit trail.

    Future: PostgreSQL, Redis, or distributed ledger.
    """

    def __init__(self, memory_dir: str = "VAULT999"):
        """
        Initialize memory backend.

        Args:
            memory_dir: Directory for vault storage
        """
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        # Index file for fast queries
        self.index_file = self.memory_dir / "index.json"
        self._load_index()

    def _load_index(self) -> None:
        """Load memory index from disk."""
        if self.index_file.exists():
            with open(self.index_file, "r") as f:
                self._index = json.load(f)
        else:
            self._index = {
                "entries": [],
                "merkle_roots": [],
                "last_updated": None,
            }

    def _save_index(self) -> None:
        """Save memory index to disk."""
        self._index["last_updated"] = datetime.now(timezone.utc).isoformat()
        with open(self.index_file, "w") as f:
            json.dump(self._index, f, indent=2)

    def write(
        self,
        session_id: str,
        verdict: str,
        floor_scores: Dict[str, Any],
        query: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> tuple[str, str]:
        """
        Write entry to constitutional memory.

        F1 Amanah: Entry is immutable once written.

        Args:
            session_id: Session identifier
            verdict: SEAL/VOID/PARTIAL/888_HOLD/SABAR
            floor_scores: All 13 floor scores
            query: Original user query
            metadata: Additional metadata

        Returns:
            (seal_hash, merkle_root): Cryptographic proofs
        """
        timestamp = datetime.now(timezone.utc).isoformat()

        # Build entry
        entry_data = {
            "session_id": session_id,
            "query": query,
            "verdict": verdict,
            "floor_scores": floor_scores,
            "timestamp": timestamp,
            "metadata": metadata or {},
        }

        # Compute seal hash
        seal_hash = sha256_hash_dict(entry_data)
        entry_data["seal_hash"] = seal_hash

        # Write entry to disk (one file per session)
        entry_file = self.memory_dir / f"{session_id}.json"
        with open(entry_file, "w") as f:
            json.dump(entry_data, f, indent=2)

        # Update index
        self._index["entries"].append(
            {
                "session_id": session_id,
                "seal_hash": seal_hash,
                "timestamp": timestamp,
                "verdict": verdict,
            }
        )

        # Recompute Merkle root with all seal hashes
        all_seal_hashes = [e["seal_hash"] for e in self._index["entries"]]
        new_merkle_root = merkle_root(all_seal_hashes)
        self._index["merkle_roots"].append(
            {
                "root": new_merkle_root,
                "timestamp": timestamp,
                "entry_count": len(all_seal_hashes),
            }
        )

        self._save_index()

        return seal_hash, new_merkle_root

    def read(self, session_id: str) -> Optional[VaultEntry]:
        """
        Read single entry by session ID.

        Args:
            session_id: Session to retrieve

        Returns:
            VaultEntry or None if not found
        """
        entry_file = self.memory_dir / f"{session_id}.json"

        if not entry_file.exists():
            return None

        with open(entry_file, "r") as f:
            data = json.load(f)

        # Get current Merkle root
        current_merkle = (
            self._index["merkle_roots"][-1]["root"] if self._index["merkle_roots"] else ""
        )

        return VaultEntry(
            session_id=data["session_id"],
            query=data.get("query", ""),
            verdict=data["verdict"],
            floor_scores=data["floor_scores"],
            timestamp=data["timestamp"],
            seal_hash=data["seal_hash"],
            merkle_root=current_merkle,
        )

    def query(
        self, verdict: Optional[str] = None, limit: int = 100, offset: int = 0
    ) -> List[VaultEntry]:
        """
        Query memory with filters.

        Args:
            verdict: Filter by verdict type
            limit: Maximum entries to return
            offset: Pagination offset

        Returns:
            List of VaultEntry objects
        """
        # Filter entries
        filtered = self._index["entries"]

        if verdict:
            filtered = [e for e in filtered if e["verdict"] == verdict]

        # Sort by timestamp (newest first)
        filtered = sorted(filtered, key=lambda e: e["timestamp"], reverse=True)

        # Paginate
        paginated = filtered[offset : offset + limit]

        # Load full entries
        entries = []
        for index_entry in paginated:
            full_entry = self.read(index_entry["session_id"])
            if full_entry:
                entries.append(full_entry)

        return entries


# ============================================================================
# GLOBAL MEMORY BACKEND INSTANCE
# ============================================================================

_memory_backend = MemoryBackend()


# ============================================================================
# CORE MEMORY FUNCTION — Main Entry Point
# ============================================================================


async def core_memory(
    action: Literal["write", "read", "query"],
    session_id: str = "",
    payload: Optional[Dict[str, Any]] = None,
    filters: Optional[Dict[str, Any]] = None,
) -> VaultOutput:
    """
    Constitutional Memory Engine: Immutable audit trail operations.

    Actions:
        write: Seal session verdict to Merkle chain
        read: Retrieve specific session by ID
        query: Search memory (by verdict, date, violations, etc.)

    Args:
        action: Operation to perform
        session_id: Session identifier (required for write/read)
        payload: Data to write (required for write)
        filters: Query filters (optional for query)

    Returns:
        VaultOutput with:
        - entries: List[VaultEntry] (for read/query)
        - seal_hash: str (for write)
        - merkle_root: str (for write)
        - status: SUCCESS | ERROR
    """
    try:
        if action == "write":
            # Validate payload
            if not payload:
                return VaultOutput(
                    action=action,
                    status="ERROR",
                    error_message="Payload required for write operation",
                )

            if not session_id:
                return VaultOutput(
                    action=action,
                    status="ERROR",
                    error_message="Session ID required for write operation",
                )

            # Extract data from payload
            verdict = payload.get("verdict", "UNKNOWN")
            floor_scores = payload.get("floor_scores", {})
            query = payload.get("query", "")
            metadata = payload.get("metadata", {})

            # Write to memory
            seal_hash, merkle_root_hash = _memory_backend.write(
                session_id=session_id,
                verdict=verdict,
                floor_scores=floor_scores,
                query=query,
                metadata=metadata,
            )

            return VaultOutput(
                action=action, seal_hash=seal_hash, merkle_root=merkle_root_hash, status="SUCCESS"
            )

        elif action == "read":
            # Validate session_id
            if not session_id:
                return VaultOutput(
                    action=action,
                    status="ERROR",
                    error_message="Session ID required for read operation",
                )

            # Read from memory
            entry = _memory_backend.read(session_id)

            if entry:
                return VaultOutput(
                    action=action, entries=[entry], merkle_root=entry.merkle_root, status="SUCCESS"
                )
            else:
                return VaultOutput(
                    action=action, status="ERROR", error_message=f"Session {session_id} not found"
                )

        elif action == "query":
            # Extract filters
            filters = filters or {}
            verdict_filter = filters.get("verdict")
            limit = filters.get("limit", 100)
            offset = filters.get("offset", 0)

            # Query memory
            entries = _memory_backend.query(verdict=verdict_filter, limit=limit, offset=offset)

            # Get current Merkle root
            current_merkle = ""
            if _memory_backend._index["merkle_roots"]:
                current_merkle = _memory_backend._index["merkle_roots"][-1]["root"]

            return VaultOutput(
                action=action, entries=entries, merkle_root=current_merkle, status="SUCCESS"
            )

        else:
            return VaultOutput(
                action=action, status="ERROR", error_message=f"Unknown action: {action}"
            )

    except Exception as e:
        return VaultOutput(
            action=action, status="ERROR", error_message=f"Memory engine error: {str(e)}"
        )


# ============================================================================
# EXPORT PUBLIC API
# ============================================================================

__all__ = [
    "core_memory",
    "MemoryBackend",
]
