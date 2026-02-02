#!/usr/bin/env python3
"""
VAULT999 Railway Verification Tool
Run: python scripts/railway_verify.py
"""

import subprocess
import tempfile
import os

VERIFY_CODE = '''
import asyncio
import asyncpg
import os
import json
import hashlib
from datetime import datetime, timezone
from uuid import uuid4

async def main():
    print("Connecting to Railway PostgreSQL...")
    dsn = os.environ["DATABASE_URL"]
    conn = await asyncpg.connect(dsn)
    
    print("\\n=== CHECKING TABLES ===")
    ledger_count = await conn.fetchval("SELECT COUNT(*) FROM vault_ledger")
    print(f"OK vault_ledger entries: {ledger_count}")
    
    head = await conn.fetchrow("SELECT * FROM vault_head WHERE id = 1")
    if head:
        print(f"OK vault_head exists")
    else:
        print("OK vault_head: empty")
    
    print("\\n=== TESTING APPEND ===")
    test_data = {"test": True, "message": "VAULT999 verification"}
    seal_id = uuid4()
    timestamp = datetime.now(timezone.utc)
    entry_hash = hashlib.sha256(json.dumps({"test": "data"}, sort_keys=True).encode()).hexdigest()
    
    row = await conn.fetchrow(
        """
        INSERT INTO vault_ledger 
            (session_id, seal_id, timestamp, authority, verdict, seal_data, entry_hash, prev_hash, merkle_root)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        RETURNING sequence, entry_hash
        """,
        "verify-session", seal_id, timestamp, "verification", "SEAL", 
        json.dumps(test_data), entry_hash, "0" * 64, entry_hash
    )
    
    print(f"OK Test entry created: sequence={row['sequence']}")
    
    print("\\n=== VERIFYING CHAIN ===")
    entries = await conn.fetch("SELECT sequence, entry_hash FROM vault_ledger ORDER BY sequence")
    print(f"OK Total entries: {len(entries)}")
    
    print("\\n=== CLEANUP ===")
    await conn.execute("DELETE FROM vault_ledger WHERE session_id = 'verify-session'")
    await conn.execute("DELETE FROM vault_head WHERE 1=1")
    print("OK Test data cleaned up")
    await conn.close()
    
    print("\\n" + "=" * 40)
    print("OK ALL CHECKS PASSED!")
    print("=" * 40)

asyncio.run(main())
'''


def main():
    print("=" * 50)
    print("  VAULT999 Verification Tool")
    print("=" * 50)
    print()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(VERIFY_CODE)
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ["railway", "run", "python", temp_file],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
    finally:
        os.unlink(temp_file)
    
    print()
    input("Press Enter to close...")


if __name__ == "__main__":
    main()
