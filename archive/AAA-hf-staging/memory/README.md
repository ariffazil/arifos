# A-RIF — Constitutional RAG & Memory Hardening

> **DITEMPA BUKAN DIBERI — Forged, Not Given.**
>
> *Memory is not storage. Memory is governed recall under constitutional authority.*

**Architecture:** A-RIF v1.0 (Autonomous Retrieval-Integrated Floors)
**Floors Active:** F1 F2 F4 F7 F12 F13
**Pipeline:** 000_INIT → 444_ROUTER → 555_MEMORY → 888_JUDGE → 999_VAULT
**Hardening Plan:** H1–H9 (Quantum Memory Hardening Spec v1.0)

---

## What is A-RIF?

**A-RIF** (Autonomous Retrieval-Integrated Floors) is the **Constitutional RAG architecture** of arifOS. It converts the AAA dataset from passive documentation into an **active governance substrate** — a living law that governs every retrieval, store, and forget operation in real time.

Without A-RIF, AAA is a dataset. With A-RIF, AAA is a **running constitution**.

The transformation happens through five mechanisms:

```
╔══════════════════════════════════════════════════════════╗
║              A-RIF CONSTITUTIONAL RAG STACK              ║
╠══════════════════════════════════════════════════════════╣
║  1. CANON LOADING     theory/canons.jsonl → Qdrant M4   ║
║  2. FLOOR RETRIEVAL   F2 · F4 · F12 govern every query  ║
║  3. SENTINEL MONITOR  Drift detection via anchor queries ║
║  4. PROVENANCE BIND   Vault999 seals AAA revision record ║
║  5. REGRESSION GATE   Gold records as CI/CD law tests   ║
╚══════════════════════════════════════════════════════════╝
```

---

## The 5 A-RIF Mechanisms

### 1. Canon Loading

At arifOS runtime startup, every record in `theory/canons.jsonl` (186 records) is:

1. Embedded using **BGE-M3** (1024-dimensional dense vectors)
2. Stored in **Qdrant** (cold, full archive, ~50ms retrieval)
3. Mirrored to **LanceDB** hot cache (top-N most accessed, <10ms retrieval)
4. Floor-scanned before storage: F12 injection check + F4 entropy gate

This converts the static dataset into a live constitutional memory that every arifOS session queries against.

### 2. Floor-Governed Retrieval

Every vector query passes through three constitutional gates before results are returned:

| Gate | Floor | Check | Effect |
|------|-------|-------|--------|
| **Pre-query** | F12 Hifz | Injection scan on query text | Blocks adversarial queries |
| **Post-retrieve** | F2 Haqq | Multi-signal truth verification | Filters low-confidence results |
| **Post-rank** | F4 Nur | Context budget enforcement | Prevents context window overflow |

The retrieval pipeline is:
```
query → F12 scan → hybrid search (LanceDB hot → Qdrant cold)
     → H4 pseudo-embedding quarantine → H5 multi-signal F2 verify
     → H9 composite ranking → H6 context budget → return
```

### 3. Sentinel Monitoring

The file `memory/sentinel_queries.jsonl` contains 25 stable anchor queries — one for each floor (F1–F13) plus key concepts (Trinity, Vault999, pipeline stages, etc.).

**Purpose:** Run sentinel queries periodically (after model upgrades, backend changes, schema migrations) and compare similarity scores against baselines. A drop in sentinel similarity signals **constitutional drift** — the AAA substrate is no longer anchoring reasoning correctly.

**Drift detection protocol:**
- `min_similarity` field per sentinel defines the floor threshold
- Any result below threshold triggers `888_HOLD` — human review required
- Regression failure blocks pipeline advancement to 999_VAULT

### 4. Provenance Binding

Every arifOS session that queries AAA records has its governing revision recorded in the **Vault999 immutable ledger**:

```json
{
  "session_id": "sess_abc123",
  "aaa_revision": "ariffazil/AAA@abc1234",
  "canon_count": 186,
  "floor_version": "13_floors_v2.1",
  "seal": "SHA256:...",
  "vault_timestamp": "2026-01-01T00:00:00Z"
}
```

This creates an auditable chain: every agent decision can be traced to the exact AAA revision that governed it. Complies with **F1 Amanah** (irreversible audit trail).

### 5. Regression Gating

The 50 gold benchmark records in `data/gold/` serve dual purpose:

1. **External eval:** Benchmark any LLM against the constitutional standard
2. **CI/CD gating:** Run `eval/memory_regression.py` before any merge to arifOS main to ensure constitutional behavior hasn't regressed

A merge that causes HOLD_accuracy to drop below 80% or AAA Score below 60 is **automatically blocked** by F8 Sabr (deliberation gate).

---

## Memory Hardening Plan (H1–H9)

The A-RIF architecture identified 9 gaps in the current arifOS memory implementation. The hardening plan addresses them systematically:

### Critical Bug Fixes (Phase 1 — P0)

| ID | Hardening | Gap | Status |
|----|-----------|-----|--------|
| **H1** | `vector_store` implementation | Mode declared but raises `ValueError` at runtime | Contract in `vector_store_contract.md` |
| **H2** | `vector_forget` implementation | Mode declared but raises `ValueError` at runtime | Contract in `vector_forget_contract.md` |
| **H3** | Ghost recall fix (LanceDB) | Deleted vectors persist in hot cache, causing undead recall | Integrated into H2 |

### Search Quality (Phase 2 — P1)

| ID | Hardening | Gap | Fix |
|----|-----------|-----|-----|
| **H4** | Pseudo-embedding quarantine | SHA-256 fallback vectors poison cosine ranking | Tag + exclude from ranking |
| **H5** | Epistemic F2 verification | Age-only check rejects valid old memories | Multi-signal: age (30%) + access (20%) + source (30%) + embedding quality (20%) |
| **H6** | Context budget management | No token/character limit on retrieval results | `context_budget` parameter, F4 enforcement |

### Memory Hygiene (Phase 3 — P2)

| ID | Hardening | Gap | Fix |
|----|-----------|-----|-----|
| **H7** | TTL & lifecycle | Memories persist forever, no eviction | `ttl_days`, `lifecycle_state` fields + `enforce_lifecycle()` |
| **H8** | Forget audit trail | Silent deletes violate F1 Amanah | Tombstone schema + vault_audit write |
| **H9** | Composite ranking | Single cosine signal misses recency/frequency/source | 5-signal ranking: cosine (45%) + recency (20%) + access (10%) + source (15%) + area (10%) |

**Total effort estimate:** 18–28 hours across 3 phases.

---

## Directory Contents

```
memory/
├── README.md                    ← This file: A-RIF overview
├── constitutional_rag_spec.md   ← Technical: canon loading, retrieval pipeline, provenance
├── sentinel_queries.jsonl       ← 25 anchor queries for drift detection
├── memory_hardening_schema.json ← JSON Schema: hardened MemoryEntry (H7/H8/H9 fields)
├── vector_store_contract.md     ← Contract: H1 vector_store mode spec
└── vector_forget_contract.md    ← Contract: H2 vector_forget mode spec + tombstone
```

### Related Files (Other Directories)

```
schemas/
├── MemoryEntry.json             ← Formal JSON Schema for hardened MemoryEntry
└── MemoryTombstone.json         ← Formal JSON Schema for forget audit tombstone

governance/
└── memory_governance.md         ← How 13 floors map to memory operations

eval/
└── memory_regression.py         ← Regression test harness using sentinel queries
```

---

## Integration with arifosmcp

The MCP server at [arifosmcp.arif-fazil.com/mcp](https://arifosmcp.arif-fazil.com/mcp) uses A-RIF as its memory backbone:

```
Client → MCP Protocol → arifosmcp
                              │
                    ┌─────────▼─────────┐
                    │   555_MEMORY      │
                    │ (engineering_mem) │
                    └─────────┬─────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        vector_store     vector_query    vector_forget
        (H1 — fixed)    (hardened with   (H2 — fixed)
                         H4/H5/H6/H9)
              │               │               │
              └───────────────┼───────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   Qdrant + LanceDB│
                    │   (BGE-M3, 1024d) │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │   999_VAULT       │
                    │  (Merkle seal +   │
                    │  enforce_lifecycle│
                    │   H7 sweep)       │
                    └───────────────────┘
```

**Tool synonyms** (ingress_middleware.py):
- `remember` / `save` / `store` → `vector_store`
- `forget` / `delete` / `remove` → `vector_forget`
- `query` / `recall` / `search` → `vector_query`

---

## The Quantum Memory Thesis

After H1–H9 are implemented, arifOS memory exhibits four emergent properties:

1. **Superposition** — A memory exists in multiple lifecycle states (active/stale/archived/tombstone) and collapses to a specific state only when queried in context (H7 + H9)

2. **Entanglement** — Storing to SOLUTIONS influences MAIN retrieval through cross-area ranking weights (H9)

3. **Observer Effect** — Querying changes the memory: `access_count` increments, `last_accessed` updates, F2 confidence recalculates (H5 + H9)

4. **Decoherence** — Unobserved memories naturally decay through lifecycle enforcement: `active → stale → archived → tombstone` (H7)

No single hardening creates intelligence. The intelligence emerges from all nine hardenings operating within the **13-floor constitutional framework** — that is the quantum leap that separates arifOS from memento-mcp and every other memory system that has zero governance.

---

> *A-RIF telemetry v1.0 | floors: F1 F2 F4 F7 F12 F13 | pipeline: 999_SEAL | seal: DITEMPA BUKAN DIBERI*
