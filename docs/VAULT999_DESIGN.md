# VAULT999 Design Document

**Version:** v1.0  
**Status:** Production Implementation  
**Backend:** PostgreSQL (Railway-managed)  
**Date:** 2026-02-02

---

## 1. Architecture Overview

### 1.1 Core Principle

VAULT999 is a **forensic, institutional memory** — not AI memory. It provides:

- **Append-only** storage (no deletions, no edits)
- **Hash-chained** integrity (each entry links to previous)
- **Merkle-rooted** verification (entire ledger state is attested)
- **Concurrency-safe** writes (no chain forks under multi-replica load)
- **Tamper-evident** detection (any modification breaks verification)

### 1.2 Infrastructure Context

```
┌─────────────────────────────────────────────────────────────┐
│                    Railway Platform                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   App        │  │   Postgres   │  │    Redis     │      │
│  │  Container   │  │  (Persistent)│  │  (Volatile)  │      │
│  │  EPHEMERAL   │  │   DURABLE    │  │  DO NOT USE  │      │
│  └──────┬───────┘  └──────▲───────┘  └──────────────┘      │
│         │                 │                                 │
│         │  writes/reads   │                                 │
│         └─────────────────┘                                 │
│                           vault_ledger table                │
└─────────────────────────────────────────────────────────────┘
```

**Rule:** If it must survive restart → Postgres. Never Redis. Never container memory.

---

## 2. Data Model

### 2.1 vault_ledger (Append-Only Entries)

| Column | Type | Description |
|--------|------|-------------|
| sequence | BIGSERIAL PRIMARY KEY | Monotonic entry number |
| session_id | TEXT NOT NULL | Caller session identifier |
| seal_id | UUID NOT NULL | Unique seal identifier |
| timestamp | TIMESTAMPTZ NOT NULL | UTC timestamp of seal |
| authority | TEXT NOT NULL | Who authorized (human/system/AI) |
| verdict | TEXT NOT NULL | SEAL/VOID/SABAR/PARTIAL/888_HOLD |
| seal_data | JSONB NOT NULL | The sealed decision bundle |
| entry_hash | TEXT NOT NULL UNIQUE | SHA256 of canonical entry |
| prev_hash | TEXT | Previous entry_hash (chain link) |
| merkle_root | TEXT NOT NULL | Root after this append |
| created_at | TIMESTAMPTZ | Insertion timestamp |

### 2.2 vault_head (Singleton Chain Head)

| Column | Type | Description |
|--------|------|-------------|
| id | SMALLINT PRIMARY KEY | Always 1 (singleton) |
| head_sequence | BIGINT NOT NULL | Latest sequence number |
| head_entry_hash | TEXT NOT NULL | Latest entry hash |
| head_merkle_root | TEXT NOT NULL | Current Merkle root |
| updated_at | TIMESTAMPTZ | Last update timestamp |

**Purpose:** Prevents concurrent writers from creating chain forks via row-level locking.

### 2.3 Indexes

```sql
CREATE INDEX idx_vault_ledger_session ON vault_ledger (session_id);
CREATE INDEX idx_vault_ledger_verdict_time ON vault_ledger (verdict, timestamp);
CREATE INDEX idx_vault_ledger_time ON vault_ledger (timestamp);
```

---

## 3. Concurrency Design

### 3.1 Problem

Multiple Railway container replicas may call `vault_seal` simultaneously. Without coordination, this creates:
- Duplicate sequence numbers
- Chain forks (two entries claiming same prev_hash)
- Lost writes

### 3.2 Solution: Advisory Lock + Transaction

```
Client A: BEGIN → ACQUIRE advisory_lock(999911777) → READ head → APPEND → RELEASE → COMMIT
Client B: BEGIN → WAIT for lock → (lock acquired) → READ head → APPEND → RELEASE → COMMIT
```

**Lock Choice:** `pg_advisory_xact_lock(key)` — transaction-scoped, automatically released on rollback.

**Why not `SELECT FOR UPDATE` on vault_head?**
- Advisory locks are explicit and semantically clearer for "singleton resource"
- `vault_head` may not exist on genesis (first write) — advisory lock always available

### 3.3 Append Transaction Steps

1. **Acquire** `pg_advisory_xact_lock(ADVISORY_LOCK_KEY)`
2. **Fetch** all existing entry_hashes (ordered by sequence) for Merkle computation
3. **Determine** prev_hash = last entry_hash or GENESIS_HASH
4. **Compute** deterministic entry_hash (canonical JSON of fields)
5. **Insert** new row into vault_ledger
6. **Compute** new Merkle root from all hashes
7. **Upsert** vault_head row with new head
8. **Commit** (lock automatically released)

---

## 4. Hashing & Verification

### 4.1 Entry Hash Computation

```python
canonical = {
    "session_id": session_id,
    "timestamp": timestamp.isoformat(),  # ISO8601 UTC
    "authority": authority,
    "verdict": verdict,
    "seal_data": seal_data,  # JSON-serializable dict
    "prev_hash": prev_hash or GENESIS_HASH,
    "seal_id": str(seal_id),  # UUID as string
}
canonical_json = json.dumps(canonical, sort_keys=True, separators=(',', ':'))
entry_hash = sha256(canonical_json.encode('utf-8')).hexdigest()
```

**Critical:** Stable key ordering, no whitespace, UTF-8 encoding.

### 4.2 Merkle Root Computation

```python
def merkle_root(hashes: List[str]) -> str:
    if not hashes:
        return sha256(b"EMPTY_LEDGER").hexdigest()
    level = list(hashes)
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])  # Duplicate last
        next_level = []
        for i in range(0, len(level), 2):
            combined = level[i] + level[i+1]
            next_level.append(sha256(combined.encode()).hexdigest())
        level = next_level
    return level[0]
```

### 4.3 verify_chain() Algorithm

```
Load all entries ordered by sequence ASC
prev = GENESIS_HASH
hashes = []

for each entry in order:
    recompute_hash = compute_entry_hash(entry fields)
    if recompute_hash != entry.entry_hash:
        return {valid: false, first_invalid_seq: entry.sequence, reason: "hash-mismatch"}
    
    if entry.prev_hash != prev:
        return {valid: false, first_invalid_seq: entry.sequence, reason: "prev-hash-mismatch"}
    
    hashes.append(entry.entry_hash)
    prev = entry.entry_hash

computed_root = merkle_root(hashes)
head = read vault_head

if head.head_hash != hashes[-1]:
    return {valid: false, reason: "head-mismatch"}

if head.merkle_root != computed_root:
    return {valid: false, reason: "merkle-mismatch"}

return {valid: true, merkle_root: computed_root, entries: len(hashes)}
```

---

## 5. MCP Tool Interface

### 5.1 Actions

| Action | Purpose | Returns |
|--------|---------|---------|
| `seal` | Append new entry | Receipt with hashes |
| `read` | Get entry by session or sequence | Entry data |
| `list` | Paginated listing (descending) | Entries + cursor |
| `query` | Filter by verdict + time range | Filtered entries |
| `verify` | Run full chain verification | Valid/invalid report |
| `proof` | Get Merkle inclusion proof | Proof path |

### 5.2 Response Format

All successful responses include:

```json
{
  "verdict": "SEAL",
  "authority_notice": "This seal is generated by arifOS infrastructure. ChatGPT/LLM is only the caller, not the authority.",
  "vault_backend": "postgres",
  ... action-specific fields
}
```

### 5.3 VOID Entries

**Critical:** VOID verdicts are still recorded. The vault is forensic truth, not success-only.

```python
# Even if constitutional verdict is VOID:
receipt = await ledger.append(
    session_id=session_id,
    verdict="VOID",  # Stored in the entry
    seal_data={...},
    authority=authority,
)
# Receipt is returned. Entry is persisted. Chain continues.
```

---

## 6. Legacy Data Strategy

**Chosen:** Option A — Import script provided

### 6.1 Migration Path

1. **New writes** go to PostgreSQL exclusively
2. **Legacy files** remain readable via `LegacyVaultReader`
3. **One-time import** script converts historical entries:
   ```bash
   python scripts/import_legacy_vault.py --dry-run
   python scripts/import_legacy_vault.py --execute
   ```
4. **Mark imported** rows with `source: "legacy_import"` in seal_data

### 6.2 Legacy Files (Read-Only)

- `VAULT999/BBB_LEDGER/entries/{session_id}.json` — Individual seal files
- `VAULT999/BBB_LEDGER/refusal_audit.jsonl` — Refusal audit trail
- `.arifos/ledger.jsonl` — Native ledger entries

**No new writes** to these locations. PostgreSQL is sole source of truth.

---

## 7. Security Considerations

### 7.1 SQL Injection Prevention

- All queries use **parameterized statements** (`$1`, `$2`)
- `asyncpg` handles escaping automatically
- No string concatenation in SQL

### 7.2 Connection Security

- `DATABASE_URL` provided by Railway (encrypted in transit)
- Connection pooling (`min_size=1, max_size=5`)
- No persistent connections across requests (stateless)

### 7.3 Tamper Detection

- `verify_chain()` can be run anytime to detect corruption
- `entry_hash` unique constraint prevents duplicate inserts
- `prev_hash` linkage ensures ordering

---

## 8. Performance Characteristics

| Operation | Complexity | Expected Latency |
|-----------|------------|------------------|
| Append (seal) | O(n) Merkle | 10-50ms |
| Read by sequence | O(1) | 1-5ms |
| Read by session | O(k) index scan | 2-10ms |
| List (paginated) | O(limit) | 5-20ms |
| Verify chain | O(n) | 50-200ms for 10k entries |
| Merkle proof | O(log n) | 5-15ms |

**Note:** Merkle recomputation on append is O(n). For high-throughput scenarios, consider:
- Incremental Merkle updates (future optimization)
- Batch sealing (accumulate entries, seal periodically)

---

## 9. Failure Modes

### 9.1 Database Unavailable

```python
# vault_tool.py handles gracefully
try:
    ledger = await _get_ledger()
except Exception as e:
    return {"verdict": "VOID", "reason": "Database unavailable", "error": str(e)}
```

### 9.2 Lock Timeout

If advisory lock cannot be acquired within timeout:
- Retry with exponential backoff
- Or return `VOID` with `reason: "concurrency_timeout"`

### 9.3 Tampering Detected

`verify_chain()` returns:
```json
{
  "valid": false,
  "first_invalid_seq": 42,
  "reason": "hash-mismatch"
}
```

**Action:** Manual investigation required. Do not auto-repair.

---

## 10. Operational Checklist

### 10.1 Deployment

- [ ] Run migrations: `psql $DATABASE_URL < scripts/migrations/001_vault_ledger_postgres.sql`
- [ ] Verify tables: `\dt vault_*`
- [ ] Test seal: `vault_seal(action="seal", ...)`
- [ ] Test read: `vault_seal(action="read", sequence=1)`
- [ ] Test verify: `vault_seal(action="verify")`

### 10.2 Monitoring

- [ ] Alert on `verify_chain()` failures
- [ ] Monitor PostgreSQL connection pool exhaustion
- [ ] Track seal latency (p50, p99)

### 10.3 Backup

```bash
# pg_dump for disaster recovery
pg_dump $DATABASE_URL --table=vault_ledger --table=vault_head > vault_backup.sql
```

---

**Constitutional Authority:** Muhammad Arif bin Fazil  
**License:** AGPL-3.0-only  
**Motto:** *DITEMPA BUKAN DIBERI — Forged, Not Given*
