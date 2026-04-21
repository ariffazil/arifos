import os
import json
import asyncio
import hashlib
from datetime import datetime, timezone
from typing import Optional
import asyncpg
from arifos.well.models.state import WellState, WellEvent

class VaultBridge:
    def __init__(self):
        self.dsn = os.getenv("POSTGRES_URL", "postgresql://arifos_admin:ArifPostgresVault2026!@postgres:5432/vault999")
        self.last_write: Optional[datetime] = None

    async def _ensure_table(self, conn):
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS well_events (
                id SERIAL PRIMARY KEY,
                vault_type TEXT DEFAULT 'well_event',
                epoch TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                well_score FLOAT NOT NULL,
                status TEXT NOT NULL,
                violations JSONB NOT NULL,
                w0_assertion TEXT NOT NULL,
                trigger TEXT NOT NULL,
                hash TEXT NOT NULL
            );
        """)

    async def anchor(self, state: WellState, trigger: str, force: bool = False) -> bool:
        # High-signal filter
        should_write = force
        if not should_write:
            if not self.last_write or (datetime.utcnow() - self.last_write.replace(tzinfo=None)).total_seconds() > 86400:
                should_write = True
            elif state.well_score < 50:
                should_write = True
            elif any(f.status in ["WARNING", "CRITICAL"] for f in state.floors_violated):
                should_write = True

        if not should_write:
            return False

        try:
            conn = await asyncpg.connect(self.dsn)
            await self._ensure_table(conn)
            
            event = WellEvent(
                epoch=datetime.now(timezone.utc),
                well_score=state.well_score,
                status="STABLE" if state.well_score > 80 else "LOW" if state.well_score > 50 else "DEGRADED",
                violations=[f.floor_id for f in state.floors_violated if f.status != "PASS"],
                w0_assertion=state.w0_assertion,
                trigger=trigger,
                hash=hashlib.sha256(state.model_dump_json().encode()).hexdigest()
            )

            await conn.execute("""
                INSERT INTO well_events (well_score, status, violations, w0_assertion, trigger, hash)
                VALUES ($1, $2, $3, $4, $5, $6)
            """, event.well_score, event.status, json.dumps(event.violations), event.w0_assertion, event.trigger, event.hash)
            
            await conn.close()
            self.last_write = datetime.utcnow()
            return True
        except Exception as e:
            print(f"Vault anchor failed: {e}")
            # Fallback to local
            with open("/var/lib/arifos/well/local_ledger.jsonl", "a") as f:
                f.write(state.model_dump_json() + "\n")
            return False
