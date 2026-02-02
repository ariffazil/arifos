# VAULT999 Railway Deployment Guide

**Version:** v1.0  
**Target:** Production deployment on Railway  
**Backend:** PostgreSQL

---

## Prerequisites

- Railway CLI installed (`npm install -g @railway/cli`)
- Railway project created and linked
- PostgreSQL database provisioned in Railway project

---

## Step 1: Environment Variables

Set these in Railway Dashboard (Project → Variables):

```bash
# Required - Provided by Railway Postgres
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Optional - Explicit vault backend selection
VAULT_BACKEND=postgres

# Optional - Test database (for CI)
TEST_DATABASE_URL=${{Postgres.DATABASE_URL}}_test
```

**Verify:**
```bash
railway variables
```

---

## Step 2: Database Migration

### Option A: Railway CLI (Recommended)

```bash
# Connect to Railway environment
railway connect

# Run migration
psql $DATABASE_URL -f scripts/migrations/001_vault_ledger_postgres.sql

# Verify tables created
psql $DATABASE_URL -c "\dt"
# Expected: vault_ledger, vault_head
```

### Option B: Python Script

```bash
railway run python << 'EOF'
import asyncio
import asyncpg
import os

async def migrate():
    dsn = os.environ['DATABASE_URL']
    conn = await asyncpg.connect(dsn)
    
    with open('scripts/migrations/001_vault_ledger_postgres.sql') as f:
        await conn.execute(f.read())
    
    # Verify
    tables = await conn.fetch("""
        SELECT tablename FROM pg_tables 
        WHERE schemaname = 'public' 
        AND tablename IN ('vault_ledger', 'vault_head')
    """)
    print(f"Created tables: {[t['tablename'] for t in tables]}")
    
    await conn.close()

asyncio.run(migrate())
EOF
```

---

## Step 3: Deploy Application

```bash
# Deploy to Railway
railway up

# Verify deployment
railway status
```

---

## Step 4: Production Verification

### 4.1 Test Seal Operation

```bash
# Via MCP tool (if you have MCP client)
railway run python << 'EOF'
import asyncio
from codebase.vault.persistent_ledger import get_vault_ledger

async def test():
    ledger = get_vault_ledger()
    await ledger.connect()
    
    receipt = await ledger.append(
        session_id="test-production-001",
        verdict="SEAL",
        seal_data={"test": True, "message": "Production verification"},
        authority="deploy-test"
    )
    
    print(f"Sealed: sequence={receipt['sequence_number']}")
    print(f"Hash: {receipt['entry_hash'][:16]}...")
    print(f"Merkle: {receipt['merkle_root'][:16]}...")
    
    await ledger.close()

asyncio.run(test())
EOF
```

### 4.2 Test Read Operation

```bash
railway run python << 'EOF'
import asyncio
from codebase.vault.persistent_ledger import get_vault_ledger

async def test():
    ledger = get_vault_ledger()
    await ledger.connect()
    
    # Read by sequence
    entry = await ledger.get_entry_by_sequence(1)
    print(f"Entry 1: {entry['session_id']} | {entry['verdict']}")
    
    # List entries
    listing = await ledger.list_entries(limit=5)
    print(f"Total entries: {len(listing['entries'])}")
    
    await ledger.close()

asyncio.run(test())
EOF
```

### 4.3 Test Verify Chain

```bash
railway run python << 'EOF'
import asyncio
from codebase.vault.persistent_ledger import get_vault_ledger

async def test():
    ledger = get_vault_ledger()
    await ledger.connect()
    
    result = await ledger.verify_chain()
    print(f"Chain valid: {result['valid']}")
    print(f"Entries: {result.get('entries', 'N/A')}")
    
    if not result['valid']:
        print(f"ERROR: {result.get('reason')}")
        print(f"First invalid seq: {result.get('first_invalid_seq')}")
    
    await ledger.close()

asyncio.run(test())
EOF
```

---

## Step 5: Legacy Data Import (If Needed)

If you have existing filesystem entries to migrate:

```bash
# Dry run first
railway run python scripts/import_legacy_vault.py --dry-run

# Execute import
railway run python scripts/import_legacy_vault.py --execute --verbose

# Verify import
railway run python << 'EOF'
import asyncio
import asyncpg
import os

async def check():
    conn = await asyncpg.connect(os.environ['DATABASE_URL'])
    count = await conn.fetchval("SELECT COUNT(*) FROM vault_ledger")
    imported = await conn.fetchval("SELECT COUNT(*) FROM vault_ledger WHERE seal_data->>'source' = 'legacy_import'")
    print(f"Total entries: {count}")
    print(f"Legacy imported: {imported}")
    await conn.close()

asyncio.run(check())
EOF
```

---

## Step 6: Monitoring & Alerting

### 6.1 Health Check Endpoint

Add to your FastAPI app:

```python
@app.get("/health/vault")
async def health_vault():
    from codebase.vault.persistent_ledger import get_vault_ledger
    
    ledger = get_vault_ledger()
    await ledger.connect()
    
    try:
        result = await ledger.verify_chain()
        return {
            "status": "healthy" if result["valid"] else "corrupted",
            "entries": result.get("entries", 0),
            "valid": result["valid"]
        }
    finally:
        await ledger.close()
```

### 6.2 Log Aggregation

Vault operations are logged at INFO level:

```python
logger.info(f"[VAULT-999] Sealed entry: {entry_hash[:16]} for session {session_id}")
```

View logs:
```bash
railway logs --follow
```

---

## Rollback Plan

### Scenario 1: Migration Failed

```bash
# Rollback migration (DESTROYS DATA)
psql $DATABASE_URL -f scripts/migrations/001_vault_ledger_postgres.rollback.sql

# Or manually:
psql $DATABASE_URL -c "DROP TABLE IF EXISTS vault_head, vault_ledger;"
```

### Scenario 2: Application Bug After Deploy

```bash
# Immediate rollback to previous version
railway rollback

# Or disable Postgres vault, fall back to filesystem:
railway variables set VAULT_BACKEND=filesystem
railway up
```

### Scenario 3: Data Corruption Detected

```bash
# Stop writes (maintenance mode)
railway variables set MAINTENANCE_MODE=true
railway up

# Investigate
railway run python << 'EOF'
import asyncio
from codebase.vault.persistent_ledger import get_vault_ledger

async def investigate():
    ledger = get_vault_ledger()
    await ledger.connect()
    result = await ledger.verify_chain()
    print(result)
    await ledger.close()

asyncio.run(investigate())
EOF

# Restore from backup if needed
psql $DATABASE_URL < vault_backup.sql
```

---

## Troubleshooting

### "asyncpg not found"

```bash
# Add dependency
poetry add asyncpg
# or
pip install asyncpg
```

### "relation vault_ledger does not exist"

Migration not applied. Run Step 2.

### "connection refused"

- Check `DATABASE_URL` is set correctly
- Verify Railway Postgres service is running
- Ensure app and DB are in same project

### Chain verification fails

```bash
# Check specific entries
psql $DATABASE_URL -c "SELECT sequence, entry_hash, prev_hash FROM vault_ledger ORDER BY sequence LIMIT 10;"

# Check head
psql $DATABASE_URL -c "SELECT * FROM vault_head;"
```

---

## Verification Checklist

- [ ] `DATABASE_URL` environment variable set
- [ ] Migration applied (`vault_ledger` and `vault_head` tables exist)
- [ ] Application deployed without errors
- [ ] Seal operation works (test in Step 4.1)
- [ ] Read operation works (test in Step 4.2)
- [ ] Verify chain passes (test in Step 4.3)
- [ ] Legacy data imported (if applicable)
- [ ] Health check endpoint responding
- [ ] Logs showing successful seals
- [ ] Rollback procedure documented

---

## Support

- **Issues:** https://github.com/ariffazil/arifOS/issues
- **Docs:** https://arifos.arif-fazil.com
- **Constitutional Authority:** Muhammad Arif bin Fazil

**DITEMPA BUKAN DIBERI** — Forged in PostgreSQL, not given.
