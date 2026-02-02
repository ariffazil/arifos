#!/usr/bin/env python3
"""Read VAULT999 seal directly from Railway PostgreSQL"""

import asyncio
import asyncpg
import os
import json

# Get DSN from environment or use Railway connection
DSN = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:fyIXICkJENclZpNldXHfigCPkiWSXWVl@gondola.proxy.rlwy.net:36406/railway"
)

async def read_seal(sequence: int):
    conn = await asyncpg.connect(DSN)
    
    row = await conn.fetchrow(
        """
        SELECT sequence, session_id, seal_id, timestamp, authority, 
               verdict, seal_data, entry_hash, prev_hash, merkle_root
        FROM vault_ledger 
        WHERE sequence = $1
        """,
        sequence
    )
    
    await conn.close()
    
    if row:
        return {
            "sequence": row["sequence"],
            "session_id": row["session_id"],
            "seal_id": str(row["seal_id"]),
            "timestamp": row["timestamp"].isoformat(),
            "authority": row["authority"],
            "verdict": row["verdict"],
            "seal_data": row["seal_data"],
            "entry_hash": row["entry_hash"],
            "prev_hash": row["prev_hash"],
            "merkle_root": row["merkle_root"],
        }
    return None

async def list_seals(limit: int = 10):
    conn = await asyncpg.connect(DSN)
    
    rows = await conn.fetch(
        """
        SELECT sequence, session_id, timestamp, authority, verdict, entry_hash
        FROM vault_ledger 
        ORDER BY sequence DESC
        LIMIT $1
        """,
        limit
    )
    
    await conn.close()
    
    return [
        {
            "sequence": r["sequence"],
            "session_id": r["session_id"],
            "timestamp": r["timestamp"].isoformat(),
            "authority": r["authority"],
            "verdict": r["verdict"],
            "entry_hash": r["entry_hash"][:16] + "..."
        }
        for r in rows
    ]

async def main():
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        print("\n=== Last 10 Seals ===\n")
        seals = await list_seals(10)
        for s in seals:
            print(f"#{s['sequence']:2d} | {s['verdict']:5s} | {s['session_id']} | {s['timestamp']}")
    
    elif len(sys.argv) > 1:
        seq = int(sys.argv[1])
        print(f"\n=== Reading Seal #{seq} ===\n")
        seal = await read_seal(seq)
        if seal:
            print(json.dumps(seal, indent=2, default=str))
        else:
            print(f"Seal #{seq} not found")
    
    else:
        print("Usage: python read_vault.py list")
        print("       python read_vault.py 12")

if __name__ == "__main__":
    asyncio.run(main())
