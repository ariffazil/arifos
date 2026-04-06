# vector_forget Mode Contract

> **Tool:** `engineering_memory`
> **Mode:** `vector_forget`
> **Priority:** H2 (+ H3 ghost recall, H8 audit trail) — P0 CRITICAL BUG FIX
> **Floor Bindings:** F1 · F11 · F13
> **Status:** CONTRACT SEALED

---

## Summary

`vector_forget` is the canonical mode for deleting memories from arifOS constitutional memory. Like `vector_store`, it was declared with synonym mapping (`forget`/`delete`/`remove` → `vector_forget`) but **not implemented** — calls fell through to `raise ValueError`.

This contract defines the complete specification for the H2 implementation, which also integrates:
- **H3:** Ghost recall fix (dual-backend delete: Qdrant + LanceDB)
- **H8:** F1 Amanah audit trail (tombstone schema)

---

## Synonyms

| User Input | Maps To |
|------------|---------|
| `forget` | `vector_forget` |
| `delete` | `vector_forget` |
| `remove` | `vector_forget` |
| `erase` | `vector_forget` |
| `purge` | `vector_forget` |
| `vector_forget` | `vector_forget` (canonical) |

---

## Input Schema

```json
{
  "mode": "vector_forget",
  "payload": {
    "memory_ids": ["uuid1", "uuid2", ...],
    "query": "string (optional if memory_ids not provided)",
    "project_id": "string (optional, default: 'default')",
    "reason": "string (optional, default: 'user_requested')"
  }
}
```

**Either `memory_ids` OR `query` must be provided.** Both empty = SABAR error.

| Field | Type | Description |
|-------|------|-------------|
| `memory_ids` | array of strings | Direct UUID delete — fastest path |
| `query` | string | Find-and-delete: locate top-10 matching memories first |
| `project_id` | string | Project namespace (used for query-based delete) |
| `reason` | string | Audit trail reason — recorded in tombstone |

---

## Processing Pipeline

```
INPUT: engineering_memory(mode="vector_forget", payload={...})
  │
  ├─ 1. Validate: memory_ids OR query required
  │       └─ FAIL → RuntimeEnvelope(ok=False, verdict=SABAR)
  │
  ├─ 2. Identify target memory IDs
  │       ├─ Strategy A (memory_ids provided):
  │       │     └─ Use provided IDs directly
  │       └─ Strategy B (query provided):
  │               └─ vector_query(query, project_id, k=10) → extract IDs
  │
  ├─ 3. Delete from Qdrant cold (existing UnifiedMemory.forget())
  │       └─ collection: {area}_{project_id}
  │
  ├─ 4. H3: Delete from LanceDB hot cache (GHOST RECALL FIX)
  │       ├─ HybridVectorMemory.purge(memory_ids)
  │       ├─ Filter: id = '{id1}' OR id = '{id2}' ...
  │       └─ Non-blocking: log warning on LanceDB failure
  │
  ├─ 5. H7: Set lifecycle_state = "tombstone" in Qdrant payload (if entries still accessible)
  │
  ├─ 6. H8: Write F1 Amanah tombstone
  │       ├─ Build tombstone record (see schema below)
  │       ├─ logger.info("[F1_TOMBSTONE] {json}")
  │       └─ Postgres vault_audit INSERT (if DATABASE_URL available)
  │
  └─ OUTPUT: RuntimeEnvelope(ok=True, verdict=SEAL, payload=response)
```

---

## Output Schema

### Success Response

```json
{
  "ok": true,
  "tool": "engineering_memory",
  "session_id": "sess_...",
  "stage": "555_MEMORY",
  "verdict": "SEAL",
  "status": "SUCCESS",
  "payload": {
    "forgotten": true,
    "forgot_ids": ["550e8400-e29b-41d4-a716-446655440000"],
    "count": 1,
    "reason": "user_requested",
    "audit": "tombstone_logged",
    "lancedb_purged": true
  }
}
```

### Failure Response (no targets specified)

```json
{
  "ok": false,
  "tool": "engineering_memory",
  "stage": "555_MEMORY",
  "verdict": "SABAR",
  "status": "SABAR",
  "payload": {
    "error": "vector_forget requires 'memory_ids' list or 'query' to identify targets"
  }
}
```

---

## Tombstone Schema (H8 — F1 Amanah)

Every successful `vector_forget` operation writes a tombstone record. This is the **audit trail** required by F1 Amanah: destructive operations must leave a permanent, irreversible record.

```json
{
  "type": "MEMORY_TOMBSTONE",
  "memory_ids": ["uuid1", "uuid2"],
  "reason": "user_requested",
  "session_id": "sess_...",
  "actor_id": "anonymous",
  "timestamp": "2026-01-01T00:00:00Z",
  "floor": "F1_AMANAH"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `type` | literal `"MEMORY_TOMBSTONE"` | Distinguishes from other vault records |
| `memory_ids` | array of strings | IDs of deleted memories |
| `reason` | string | Why the memories were deleted |
| `session_id` | string | Session that executed the delete |
| `actor_id` | string | Human or agent actor (from auth context) |
| `timestamp` | ISO 8601 | Exact deletion time |
| `floor` | literal `"F1_AMANAH"` | Constitutional authority for this record |

**Tombstone storage locations (both required):**

1. **Structured logger** (always available): `logger.info("[F1_TOMBSTONE] {json}")`
2. **Postgres vault_audit table** (if `DATABASE_URL` is set): `INSERT INTO vault_audit`

The tombstone itself must **never be deletable** — it is subject to F1 Amanah's irreversibility constraint. Attempting to delete a tombstone raises `888_HOLD`.

---

## Floor Bindings

| Floor | Name | How It Applies |
|-------|------|---------------|
| **F1** | Amanah | Audit trail: every deletion writes permanent tombstone (H8) |
| **F11** | Aman | Safety gate: no cascading deletes or cross-session deletion allowed |
| **F13** | Khalifah | Human override: if `888_HOLD` is active, deletion is blocked pending human review |

---

## Ghost Recall Fix (H3)

### The Problem

Before H2/H3, calling `forget()` on `UnifiedMemory` deleted from Qdrant only. The LanceDB hot cache retained the vectors. On next `vector_query`:

```
hybrid search → LanceDB hot path → finds "deleted" vector → returns as valid result
```

The memory was **undead** — deleted from the source of truth but still retrievable.

### The Fix

`vector_forget` performs dual-backend deletion:

```python
# 1. Delete from Qdrant (cold)
unified_memory.forget(memory_ids)

# 2. Delete from LanceDB (hot) — H3 fix
hybrid_memory.purge(memory_ids)  # New method on HybridVectorMemory
```

`HybridVectorMemory.purge()` uses LanceDB filter syntax:
```python
id_filter = " OR ".join([f"id = '{mid}'" for mid in memory_ids])
table.delete(id_filter)
```

**Validation:** After `vector_forget`, immediately call `vector_query` with identical content. Should return zero results for the forgotten IDs.

---

## Test Vectors

### Test 1: Direct ID delete

```json
{
  "mode": "vector_forget",
  "payload": {
    "memory_ids": ["550e8400-e29b-41d4-a716-446655440000"],
    "reason": "outdated_information"
  }
}
```

**Expected:** `ok=true`, `count=1`, `audit=tombstone_logged`

### Test 2: Query-based delete

```json
{
  "mode": "vector_forget",
  "payload": {
    "query": "temporary session context",
    "project_id": "arifos-core",
    "reason": "session_cleanup"
  }
}
```

**Expected:** `ok=true`, `count` = number of matching memories found, `forgot_ids` listed

### Test 3: Ghost recall prevention (H3)

1. `vector_store`: content = "quantum memory ghost test"
2. `vector_forget`: memory_ids = [returned memory_id]
3. `vector_query`: query = "quantum memory ghost test"
4. **Expected:** Zero results — no ghost recall

### Test 4: Empty targets rejection

```json
{
  "mode": "vector_forget",
  "payload": {}
}
```

**Expected:** `ok=false`, `verdict=SABAR`

### Test 5: Tombstone audit verification

1. `vector_forget` with `memory_ids` and `reason="test_audit"`
2. Check `logger` output for `[F1_TOMBSTONE]` JSON
3. If `DATABASE_URL` set, check `vault_audit` table for tombstone record
4. **Expected:** Tombstone exists with `floor=F1_AMANAH`

---

## Implementation Location

```
arifosmcp/runtime/tools_internal.py
└── engineering_memory_dispatch_impl()
    └── elif mode == "vector_forget":
            # H2 + H3 + H8 implementation

arifosmcp/intelligence/tools/hybrid_vector_memory.py
└── class HybridVectorMemory:
    └── async def purge(self, memory_ids: list[str]) -> int:
            # H3 LanceDB delete
```

---

> *vector_forget contract v1.0 | H2+H3+H8 | SEALED | floors: F1 F11 F13 | DITEMPA BUKAN DIBERI*
