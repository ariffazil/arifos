# VAULT999 PostgreSQL Deployment Guide

**Version:** v55.3  
**Status:** Production Ready  
**Backend:** PostgreSQL (Railway-managed)

---

## Quick Start (Railway)

### 1. Environment Variables

Add to your Railway environment:

```bash
# Required
DATABASE_URL=postgresql://user:pass@host:5432/arifos  # Already set by Railway Postgres

# Optional (for test/development)
TEST_DATABASE_URL=postgresql://user:pass@host:5432/arifos_test
```

### 2. Run Migrations

```bash
# SSH into your Railway instance or use Railway CLI
railway run bash

# Run the migration
psql $DATABASE_URL -f scripts/migrations/001_vault_ledger_postgres.sql
```

Or via Python (recommended):

```bash
python -m scripts.apply_migrations
```

### 3. Verify Deployment

```bash
# Check tables exist
psql $DATABASE_URL -c "\dt"

# Expected output:
#  Schema |    Name     | Type  |  Owner
# --------+-------------+-------+----------
#  public | vault_head  | table | postgres
#  public | vault_ledger| table | postgres
```

---

## Migration Commands Reference

### Apply Migration

```bash
# Using psql directly
psql $DATABASE_URL < scripts/migrations/001_vault_ledger_postgres.sql

# Using Python helper
python << 'EOF'
import asyncpg
import asyncio

async def migrate():
    conn = await asyncpg.connect(os.environ['DATABASE_URL'])
    with open('scripts/migrations/001_vault_ledger_postgres.sql') as f:
        await conn.execute(f.read())
    await conn.close()
    print("Migration applied")

asyncio.run(migrate())
EOF
```

### Rollback (DANGER: Destroys all vault data)

```bash
psql $DATABASE_URL < scripts/migrations/001_vault_ledger_postgres.rollback.sql
```

---

## Testing

### Local Testing (before deploy)

```bash
# 1. Start local Postgres (if not running)
docker run -d --name arifos-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 postgres:15

# 2. Set test database URL
export TEST_DATABASE_URL="postgresql://postgres:postgres@localhost:5432/arifos_test"

# 3. Create test database
psql "postgresql://postgres:postgres@localhost:5432/postgres" -c "CREATE DATABASE arifos_test;"

# 4. Run migrations on test DB
psql $TEST_DATABASE_URL < scripts/migrations/001_vault_ledger_postgres.sql

# 5. Run tests
pytest tests/test_vault_postgres.py -v
```

### Staging Verification

```bash
# Verify vault is writable
curl -X POST https://aaamcp.arif-fazil.com/vault/seal \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-staging-001",
    "authority": "test",
    "verdict": "SEAL",
    "seal_data": {"test": true}
  }'

# Verify retrieval
curl https://aaamcp.arif-fazil.com/vault/read?session_id=test-staging-001

# Verify chain integrity
curl https://aaamcp.arif-fazil.com/vault/verify
```

---

## Rollback Plan

### Scenario 1: Migration Failed

```bash
# Rollback to pre-migration state
psql $DATABASE_URL < scripts/migrations/001_vault_ledger_postgres.rollback.sql

# Application continues using legacy filesystem vault (read-only for old entries)
```

### Scenario 2: Application Error After Migration

1. **Immediate**: Set environment variable to disable PostgreSQL vault:
   ```bash
   VAULT_BACKEND=legacy  # Falls back to filesystem
   ```

2. **Debug**: Check logs
   ```bash
   railway logs
   ```

3. **Fix**: Apply fix, redeploy
   ```bash
   git push railway main
   ```

### Scenario 3: Data Corruption Detected

```bash
# 1. Stop writes (maintenance mode)
railway vars set MAINTENANCE_MODE=true

# 2. Verify chain integrity
python -c "
import asyncio
from codebase.vault.persistent_ledger import get_ledger

async def check():
    ledger = get_ledger()
    await ledger.initialize()
    result = await ledger.verify_chain()
    print(result)

asyncio.run(check())
"

# 3. If invalid, restore from backup or investigate tampering
```

---

## Verification Checklist

Deploy to production only when all items are checked:

- [ ] Migration applied successfully (`\dt` shows vault_ledger, vault_head)
- [ ] `DATABASE_URL` env var set and accessible
- [ ] Application starts without errors
- [ ] Can write seal entry (test via MCP or API)
- [ ] Can read seal entry (retrieval works)
- [ ] Chain verification passes (`verify_chain` returns valid=True)
- [ ] Restart simulation passes (stop/start container, verify still valid)
- [ ] Concurrent seal test passes (no fork, sequences consistent)
- [ ] Legacy entries still readable (if applicable)
- [ ] Monitoring/alerting configured for DB connection errors

---

## Architecture Notes

### Why PostgreSQL?

| Requirement | How PostgreSQL Delivers |
|-------------|------------------------|
| Persistence | ACID transactions survive restarts |
| Concurrency | Row-level locking (`FOR UPDATE`) |
| Verifiability | Hash chain stored in table, computable on read |
| Scalability | Index-based queries for retrieval |
| Backup/Restore | Standard pg_dump/pg_restore |

### Concurrency Model

```
Writer 1: BEGIN → LOCK vault_head → INSERT → UPDATE vault_head → COMMIT
Writer 2: BEGIN → WAIT for lock → (lock acquired) → INSERT → UPDATE → COMMIT
```

Guarantees:
- No duplicate sequence numbers
- No gaps in sequence
- No chain forks

### Data Retention

- Vault ledger is **append-only** by design
- No automatic deletion (constitutional requirement)
- For long-term archiving, use `pg_dump` or export to cold storage

---

## Legacy Compatibility

Old filesystem entries remain readable via `LegacyVaultReader`:

```python
from codebase.vault.ledger_compat import LegacyVaultReader

reader = LegacyVaultReader("VAULT999")
legacy_entry = reader.read_session_json("old-session-id")
legacy_entries = reader.list_session_jsons(limit=100)
```

To migrate legacy entries to PostgreSQL:

```python
from codebase.vault.ledger_compat import migrate_legacy_to_postgres, LegacyVaultReader

reader = LegacyVaultReader()
stats = await migrate_legacy_to_postgres(reader, dry_run=False)
print(f"Migrated {stats['session_jsons_migrated']} entries")
```

---

## Troubleshooting

### "asyncpg not found"

```bash
pip install asyncpg
# Or add to pyproject.toml dependencies
```

### "Connection refused"

- Verify `DATABASE_URL` is correct
- Check Railway Postgres service is running
- Ensure app and DB are in same Railway project

### "Relation vault_ledger does not exist"

Migration not applied. Run:
```bash
psql $DATABASE_URL < scripts/migrations/001_vault_ledger_postgres.sql
```

### Chain verification fails

Possible causes:
1. Database corruption (check disk health)
2. Manual tampering (investigate access logs)
3. Bug in hash computation (check code version)

---

## Contact

**Maintainer:** Muhammad Arif bin Fazil  
**Issues:** https://github.com/ariffazil/arifOS/issues  
**Constitutional Authority:** VAULT999 Specification v55.3

> **DITEMPA BUKAN DIBERI** — The vault is forged in PostgreSQL, not given.
