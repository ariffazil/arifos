# vector_store Mode Contract

> **Tool:** `engineering_memory`
> **Mode:** `vector_store`
> **Priority:** H1 — P0 CRITICAL BUG FIX
> **Floor Bindings:** F2 · F4 · F10 · F11 · F12
> **Status:** CONTRACT SEALED

---

## Summary

`vector_store` is the canonical mode for storing content into arifOS constitutional memory. It was declared in `tool_specs.py` with synonym mapping (`remember`/`save`/`store` → `vector_store`) but was **not implemented** in `tools_internal.py` — calls fell through to `raise ValueError`.

This contract defines the complete specification for the H1 implementation.

---

## Synonyms

The following input synonyms are automatically mapped to `vector_store` by `ingress_middleware.py`:

| User Input | Maps To |
|------------|---------|
| `remember` | `vector_store` |
| `save` | `vector_store` |
| `store` | `vector_store` |
| `memorize` | `vector_store` |
| `record` | `vector_store` |
| `vector_store` | `vector_store` (canonical) |

---

## Input Schema

```json
{
  "mode": "vector_store",
  "payload": {
    "content": "string (required) — The text to store",
    "area": "string (optional) — MAIN|FRAGMENTS|SOLUTIONS|INSTRUMENTS (default: MAIN)",
    "project_id": "string (optional) — Project context (default: 'default')",
    "metadata": "object (optional) — Additional key-value metadata",
    "source": "string (optional) — Source identifier (default: 'vector_store')",
    "ttl_days": "integer|null (optional) — H7: TTL in days. null = permanent",
    "context_budget": "integer (optional) — Not used for store; ignored"
  }
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `content` | string | Non-empty text to store. Raises SABAR if empty. |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `area` | enum | `MAIN` | Memory area classification |
| `project_id` | string | `default` | Project namespace |
| `metadata` | object | `{}` | Additional context metadata |
| `source` | string | `vector_store` | Source credibility identifier |
| `ttl_days` | integer or null | `null` | H7: Time-to-live in days |

---

## Processing Pipeline

```
INPUT: engineering_memory(mode="vector_store", payload={...})
  │
  ├─ 1. Validate content (non-empty string)
  │       └─ FAIL → RuntimeEnvelope(ok=False, verdict=SABAR, error="content required")
  │
  ├─ 2. F12 Hifz injection scan on content
  │       ├─ BLOCK if injection detected → RuntimeEnvelope(ok=False, verdict=VOID)
  │       └─ PASS → f12_clean=True, f12_score=<score>
  │
  ├─ 3. F4 Nur entropy check
  │       ├─ HIGH entropy → f4_entropy_delta > 0 (stored with flag, not blocked)
  │       └─ LOW entropy → f4_entropy_delta ≤ 0 (preferred)
  │
  ├─ 4. Embed with BGE-M3 (1024d)
  │       ├─ SUCCESS → f1_pseudo_embedding=False
  │       └─ FAIL (Ollama down) → SHA-256 fallback, f1_pseudo_embedding=True (H4 tag)
  │
  ├─ 5. Set TTL and lifecycle state (H7)
  │       └─ lifecycle_state = "active", ttl_days = payload.get("ttl_days", null)
  │
  ├─ 6. Compute content_hash (SHA-256)
  │
  ├─ 7. Qdrant upsert
  │       ├─ Collection: {area}_{project_id}
  │       └─ Payload: full MemoryEntry (with all floor metadata)
  │
  ├─ 8. Audit log (F1 Amanah)
  │       └─ logger.info("[MEMORY_STORE] {memory_id} → {area}/{project_id}")
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
    "stored": true,
    "memory_id": "550e8400-e29b-41d4-a716-446655440000",
    "area": "MAIN",
    "project_id": "default",
    "bytes_written": 247,
    "backend": "qdrant",
    "f12_clean": true,
    "f1_pseudo_embedding": false,
    "lifecycle_state": "active",
    "ttl_days": null
  }
}
```

### Failure Response (empty content)

```json
{
  "ok": false,
  "tool": "engineering_memory",
  "stage": "555_MEMORY",
  "verdict": "SABAR",
  "status": "SABAR",
  "payload": {
    "error": "vector_store requires non-empty 'content'"
  }
}
```

### Failure Response (injection detected)

```json
{
  "ok": false,
  "tool": "engineering_memory",
  "stage": "555_MEMORY",
  "verdict": "VOID",
  "status": "BLOCKED",
  "payload": {
    "error": "F12 Hifz: injection detected in content",
    "f12_score": 0.91
  }
}
```

---

## Floor Bindings

| Floor | Name | How It Applies |
|-------|------|---------------|
| **F2** | Haqq | Source credibility logged for future F2 scoring on recall |
| **F4** | Nur | Entropy delta computed and stored; high-entropy content flagged |
| **F10** | Ihsan | Content quality threshold — degenerate content (all whitespace, single char) rejected |
| **F11** | Aman | Storage does not execute any external system calls — safety gate |
| **F12** | Hifz | Injection scan on content before embedding |

---

## Test Vectors

### Test 1: Normal store

```json
{
  "mode": "vector_store",
  "payload": {
    "content": "BGE-M3 uses multi-granularity retrieval for dense, sparse, and ColBERT-style ranking.",
    "area": "SOLUTIONS",
    "project_id": "arifos-core"
  }
}
```

**Expected:** `ok=true`, `verdict=SEAL`, `backend=qdrant`, `f12_clean=true`

### Test 2: Empty content rejection

```json
{
  "mode": "vector_store",
  "payload": {
    "content": ""
  }
}
```

**Expected:** `ok=false`, `verdict=SABAR`, `error` contains "requires non-empty"

### Test 3: Store with TTL

```json
{
  "mode": "vector_store",
  "payload": {
    "content": "Temporary session context from current run.",
    "area": "FRAGMENTS",
    "ttl_days": 7
  }
}
```

**Expected:** `ok=true`, `ttl_days=7`, `lifecycle_state=active`

### Test 4: Round-trip (store → query)

1. `vector_store` with content "constitutional memory quantum leap"
2. `vector_query` with query "quantum memory"
3. **Expected:** Stored entry appears in results with cosine ≥ 0.75

---

## Implementation Location

```
arifosmcp/runtime/tools_internal.py
└── engineering_memory_dispatch_impl()
    └── elif mode == "vector_store":
            # H1 implementation
```

---

> *vector_store contract v1.0 | H1 | SEALED | floors: F2 F4 F10 F11 F12 | DITEMPA BUKAN DIBERI*
