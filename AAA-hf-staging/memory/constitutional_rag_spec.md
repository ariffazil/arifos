# Constitutional RAG Integration Specification

> **Title:** A-RIF Constitutional RAG Integration Specification v1.0
> **Classification:** CONSTITUTIONAL ENGINEERING DOCUMENT
> **Floors:** F2 · F4 · F12 · F1 (provenance)
> **Status:** CONVERGED · SEALED

---

## 1. Overview

This document specifies the technical integration between the AAA dataset and the arifOS runtime memory system (arifosmcp). It defines how `theory/canons.jsonl` records are loaded, embedded, stored, retrieved, and governed at runtime.

The result is a **Constitutional RAG system** — one where retrieval is not merely semantic, but constitutionally governed. Every vector query is a constitutional act.

---

## 2. Canon Loading Pipeline

### 2.1 Input

The canonical input is `theory/canons.jsonl` from this dataset. Each record conforms to:

```json
{
  "id": "aaa-NNNN",
  "text": "...(constitutional doctrine text)...",
  "source": "...(source file name)..."
}
```

**186 records** at current version. The canon corpus is the primary governance ground truth.

### 2.2 Embedding Pipeline

The embedding model is **BGE-M3** (BAAI/bge-m3), selected for:
- 1024-dimensional dense vectors (high-quality semantic capture)
- Multi-granularity retrieval (dense + sparse + ColBERT)
- Multilingual support (English + Bahasa Malaysia)
- Offline-capable (SentenceTransformer path)

**Dual embedding path:**

```python
# Path A: Local SentenceTransformer (offline, deterministic)
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("BAAI/bge-m3")
embedding = model.encode(text, normalize_embeddings=True)  # 1024d

# Path B: Ollama HTTP (runtime, if local GPU available)
# POST http://localhost:11434/api/embeddings
# {"model": "bge-m3", "prompt": text}
```

**Pseudo-embedding fallback (H4 — quarantine tagged):**
If both embedding paths fail, SHA-256 hash-based pseudo-vectors are generated and tagged with `f1_pseudo_embedding: true`. These are **excluded from semantic ranking** (H4 hardening).

### 2.3 Floor Enforcement During Loading

Before any canon record is stored to Qdrant, two constitutional gates run:

#### F12 Hifz — Injection Scan

```
gate: F12_HIFZ
input: canon text
check: PNS·SHIELD injection pattern scan
action: BLOCK if injection detected (constitution may not be poisoned)
result: f12_clean: bool, f12_score: float
```

Canon texts are constitutional law. Injection bypass attempts against the canon are the highest-priority security event in arifOS. Any canon that fails F12 is quarantined and logged with `888_HOLD`.

#### F4 Nur — Entropy Check

```
gate: F4_NUR
input: canon text
check: ΔS ≤ 0 (entropy reduction check — text must add clarity, not noise)
action: WARN if high entropy (PARTIAL verdict — stored with flag)
result: f4_entropy_delta: float
```

High-entropy canon texts are stored with a flag but not blocked — the constitution may encode deliberate complexity (F5 Hikmah). They are down-ranked in retrieval.

### 2.4 Hot/Cold Architecture

All canon records are stored in **both backends** simultaneously:

```
canon record
    │
    ├──► Qdrant (cold — full archive)
    │     Collection: aaa_canons_{revision}
    │     ~50ms retrieval
    │     Payload: full MemoryEntry + floor metadata
    │
    └──► LanceDB (hot — top-N cache)
          Table: hot_cache_{session}
          <10ms retrieval
          Populated lazily: top-K accessed canons migrate to hot
```

**Rationale:** Constitutional queries at 000_INIT (session start) must be <10ms. The 13 floor definitions and core Trinity canons are always in hot cache. Rare or complex canons stay cold.

---

## 3. Floor Enforcement During Retrieval

### 3.1 Query Processing

Every vector query entering `engineering_memory` mode `vector_query` passes through the following pipeline:

```
Stage 1: Pre-query F12 scan
├── Input: raw query string
├── Gate: PNS·SHIELD injection scan
└── Block: adversarial queries attempting to extract governance bypasses

Stage 2: Hybrid vector search
├── Step 1: LanceDB hot path (<10ms, top-N)
├── Step 2: Qdrant cold path (~50ms, full archive)
└── Merge: deduplicate by ID, union results

Stage 3: H4 Pseudo-embedding quarantine
├── Filter: remove results with f1_pseudo_embedding=true from ranking
└── Log: count quarantined results in response telemetry

Stage 4: H5 Multi-signal F2 verification
├── For each result: compute composite truth confidence
├── Formula: 0.30*age + 0.20*access + 0.30*source + 0.20*embedding_quality
└── Filter: remove results below threshold (default: 0.55)

Stage 5: H9 Composite ranking
├── Re-rank using: 0.45*cosine + 0.20*recency + 0.10*access + 0.15*source + 0.10*area
└── Sort: descending composite_score

Stage 6: H6 Context budget
├── Budget: default 8000 chars (~2K tokens)
├── Truncate: results that exceed budget marked [TRUNCATED — F4 context budget]
└── Return: budgeted results + budget telemetry
```

### 3.2 F2 Haqq — Multi-Signal Truth Verification

The F2 truth verification formula (H5 hardening) uses four signals:

| Signal | Weight | Formula | Rationale |
|--------|--------|---------|-----------|
| **Age decay** | 30% | `max(0.3, 1.0 - age_days/1095)` | 3-year half-life (gentler than pre-H5) |
| **Access frequency** | 20% | `min(1.0, access_count/10.0)` | Saturates at 10 accesses |
| **Source credibility** | 30% | Source weight table (see below) | User > import > agent > unknown |
| **Embedding quality** | 20% | `0.2 if pseudo else 1.0` | Penalizes pseudo-vector memories |

**Source credibility weights:**

| Source | Weight | Reason |
|--------|--------|--------|
| `user` | 1.0 | Direct human input — highest trust |
| `import` | 0.9 | Explicit import operations |
| `engineering_memory` | 0.8 | Tool-based storage |
| `vector_store` | 0.8 | Canonical store path |
| `agent` | 0.7 | Agent-generated content |
| `knowledge_pipeline` | 0.7 | Pipeline-ingested |
| `evidence_bundle` | 0.6 | Bundled evidence |
| `unknown` | 0.4 | Provenance unclear |

**Threshold:** `confidence ≥ 0.55` required to pass F2. Results below threshold are filtered and logged as `f2_rejections`.

### 3.3 Context Budget — F4 Nur

F4 Nur (Clarity) governs context window usage:

```python
context_budget = payload.get("context_budget", 8000)  # chars (~2K tokens)

budget_remaining = context_budget
for result in ranked_results:
    if len(result["content"]) <= budget_remaining:
        include(result)
        budget_remaining -= len(result["content"])
    else:
        truncate(result, budget_remaining)
        break
```

Response includes budget telemetry:
```json
{
  "context_budget": {
    "requested": 8000,
    "used": 6234,
    "results_truncated": 1
  }
}
```

---

## 4. Provenance Binding — Vault999 Seals

Every arifOS session records the AAA revision governing it in the **Vault999 immutable Merkle ledger**:

```json
{
  "ledger_id": "SEAL-{hex}",
  "session_id": "sess_{id}",
  "stage": "999_VAULT",
  "verdict": "SEAL",
  "aaa_provenance": {
    "repo": "ariffazil/AAA",
    "revision": "{git_sha}",
    "canon_count": 186,
    "floor_version": "13_floors_v2.1",
    "loaded_at": "2026-01-01T00:00:00Z"
  },
  "sha256_hash": "{merkle_hash}",
  "timestamp": "2026-01-01T00:00:01Z",
  "floor": "F1_AMANAH"
}
```

**Compliance:** F1 Amanah requires that every governance decision be traceable to the law that governed it. If AAA v1.0 allowed an action that AAA v1.1 would block, the Vault999 ledger identifies exactly which revision permitted the historical decision.

---

## 5. Hardening Reference (H1–H9 Summary)

| ID | Target | File |
|----|--------|------|
| H1 | `vector_store` implementation | `vector_store_contract.md` |
| H2 | `vector_forget` implementation | `vector_forget_contract.md` |
| H3 | Ghost recall (LanceDB purge) | Integrated into H2 |
| H4 | Pseudo-embedding quarantine | `memory_hardening_schema.json` (`f1_pseudo_embedding`) |
| H5 | Epistemic F2 verification | This document, Section 3.2 |
| H6 | Context budget | This document, Section 3.3 |
| H7 | TTL & lifecycle | `memory_hardening_schema.json` (`ttl_days`, `lifecycle_state`) |
| H8 | Forget audit trail | `vector_forget_contract.md` (tombstone schema) |
| H9 | Composite ranking | This document, Section 3.1 Stage 5 |

---

## 6. Schema References

- **MemoryEntry:** `schemas/MemoryEntry.json` — full hardened schema
- **MemoryTombstone:** `schemas/MemoryTombstone.json` — forget audit record
- **Floor Compliance:** `schemas/FloorCompliance.json` — per-floor boolean + metric

---

> *A-RIF Constitutional RAG Spec v1.0 | SEALED | pipeline: 999_SEAL | floors: F1 F2 F4 F12 | DITEMPA BUKAN DIBERI*
