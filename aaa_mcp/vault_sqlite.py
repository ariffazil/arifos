# aaa_mcp/vault_sqlite.py — Constitutional Fallback (F1 Reversible)
"""
SQLite-based VAULT999 untuk DEV_MODE.
F1 Amanah: Reversible migration path ke PostgreSQL.
"""

import sqlite3
import hashlib
import json
from datetime import datetime
from typing import Dict, Optional, List
from pathlib import Path


class SQLiteVault:
    """Constitutional vault dengan SQLite backend (DEGRADED mode)."""

    def __init__(self, db_path: str = "/tmp/arifos_vault.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize vault table dengan Merkle chain structure."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS vault_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    seal_id TEXT UNIQUE NOT NULL,
                    timestamp TEXT NOT NULL,
                    verdict TEXT NOT NULL,
                    risk_level TEXT,
                    category TEXT,
                    seal_data TEXT,
                    entry_hash TEXT NOT NULL,
                    prev_hash TEXT,
                    merkle_root TEXT,
                    floors_checked TEXT  -- JSON array
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_session ON vault_entries(session_id)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON vault_entries(timestamp)
            """)
            conn.commit()

    def _get_prev_hash(self) -> str:
        """Get previous entry hash untuk Merkle chain."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT entry_hash FROM vault_entries ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            return row[0] if row else "GENESIS"

    def seal(
        self,
        session_id: str,
        seal_id: str,
        verdict: str,
        risk_level: str = "low",
        category: str = "general",
        seal_data: str = "",
        floors_checked: Optional[List[str]] = None,
    ) -> Dict:
        """
        Seal constitutional decision ke VAULT999.

        Returns:
            Dict dengan vault_id, merkle_root, prev_hash, status
        """
        timestamp = datetime.utcnow().isoformat() + "Z"

        # Calculate entry hash
        entry_content = f"{session_id}:{seal_id}:{verdict}:{timestamp}"
        entry_hash = hashlib.sha256(entry_content.encode()).hexdigest()[:16]

        # Get previous hash untuk chain
        prev_hash = self._get_prev_hash()

        # Calculate Merkle root (simplified: hash of current + prev)
        merkle_root = hashlib.sha256(f"{entry_hash}:{prev_hash}".encode()).hexdigest()[:16]

        # Insert to vault
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO vault_entries 
                (session_id, seal_id, timestamp, verdict, risk_level, category,
                 seal_data, entry_hash, prev_hash, merkle_root, floors_checked)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    session_id,
                    seal_id,
                    verdict,
                    timestamp,
                    risk_level,
                    category,
                    seal_data,
                    entry_hash,
                    prev_hash,
                    merkle_root,
                    json.dumps(floors_checked or []),
                ),
            )
            conn.commit()

            # Get inserted ID
            cursor = conn.execute("SELECT last_insert_rowid()")
            vault_id = cursor.fetchone()[0]

        return {
            "vault_id": vault_id,
            "vault_status": "PERSISTED_SQLITE",
            "mode": "DEGRADED",
            "merkle_root": merkle_root,
            "prev_hash": prev_hash,
            "entry_hash": entry_hash,
            "timestamp": timestamp,
            "warning": "SQLite fallback — migrate to PostgreSQL for production",
        }

    def verify_chain(self) -> Dict:
        """Verify Merkle chain integrity (F1 audit)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id, entry_hash, prev_hash FROM vault_entries ORDER BY id")
            entries = cursor.fetchall()

        if not entries:
            return {"status": "EMPTY", "count": 0}

        # Verify chain
        breaks = []
        for i, (id_, hash_, prev_) in enumerate(entries):
            if i == 0:
                if prev_ != "GENESIS":
                    breaks.append({"id": id_, "expected": "GENESIS", "got": prev_})
            else:
                expected_prev = entries[i - 1][1]  # Previous entry's hash
                if prev_ != expected_prev:
                    breaks.append({"id": id_, "expected": expected_prev, "got": prev_})

        return {"status": "BROKEN" if breaks else "INTACT", "count": len(entries), "breaks": breaks}

    def get_entry(self, vault_id: int) -> Optional[Dict]:
        """Retrieve vault entry by ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM vault_entries WHERE id = ?", (vault_id,))
            row = cursor.fetchone()

            if row:
                return dict(row)
            return None

    def migrate_to_postgres(self, postgres_url: str) -> Dict:
        """
        F1 Amanah: Reversible migration ke PostgreSQL.

        Returns:
            Migration report dengan counts
        """
        # TODO: Implement PostgreSQL migration
        # This ensures F1 — SQLite was always reversible
        return {
            "status": "NOT_IMPLEMENTED",
            "source": self.db_path,
            "target": postgres_url,
            "message": "Migration path reserved for v65.1",
        }


# Global vault instance (singleton untuk DEGRADED mode)
vault = SQLiteVault()
