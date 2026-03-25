# Memory Governance — 13 Floors Applied to Memory Operations

> **Classification:** CONSTITUTIONAL GOVERNANCE DOCUMENT
> **Scope:** `engineering_memory` modes: `vector_store`, `vector_query`, `vector_forget`
> **Authority:** F13 Khalifah — Muhammad Arif bin Fazil
> **Status:** SEALED

---

## Overview

The 13 constitutional floors of arifOS are not abstract principles — they are active enforcement contracts that govern every memory operation. This document maps each floor to its specific role in the memory subsystem (555_MEMORY stage).

The core memory operations are:
- **`vector_store`** — Writing memory (think: legislating new law)
- **`vector_query`** — Retrieving memory (think: consulting existing law)
- **`vector_forget`** — Deleting memory (think: repealing law with audit record)

---

## Floor-by-Floor Memory Governance

### F1 — Amanah (Trust / Reversibility)

**Enforcement Type:** HARD VOID  
**Memory Role:** Audit trail for all writes and deletes

**Rule:** Every memory operation that is **destructive or consequential** must leave a permanent, irreversible audit record. No silent operations. No untraced deletes.

**Applications:**

| Operation | F1 Requirement |
|-----------|---------------|
| `vector_store` | Log `[MEMORY_STORE] {memory_id} → {area}/{project_id}` to structured logger |
| `vector_forget` | Write F1 Amanah tombstone (see `schemas/MemoryTombstone.json`). Both logger AND Postgres vault_audit. |
| `vector_query` | Log successful F2-verified recalls with memory_id + session_id |
| Lifecycle sweep | Log every state transition: active→stale, stale→archived, archived→tombstone |

**Tombstone Immutability:** Tombstones written by `vector_forget` are themselves permanent. Any attempt to delete a tombstone triggers `888_HOLD`. F1 Amanah makes the act of forgetting unforgettable.

**Implementation reference:** H8 in `vector_forget_contract.md`

---

### F2 — Haqq (Truth / Veracity)

**Enforcement Type:** SOFT PARTIAL  
**Threshold:** ≥ 0.85 (TWRT confidence)  
**Memory Role:** Truth verification on recall (multi-signal epistemic verification)

**Rule:** Memory retrieved at query time must pass truth verification before being returned. A memory that cannot be trusted must not be returned as fact.

**Pre-H5 (broken):** Age-only check. Memories older than 365 days auto-rejected regardless of credibility. Fresh-but-false memories always passed.

**Post-H5 (hardened):** Multi-signal composite verification:

```
F2_confidence = 0.30 × age_score
              + 0.20 × access_frequency_score  
              + 0.30 × source_credibility_score
              + 0.20 × embedding_quality_score

Threshold: F2_confidence ≥ 0.55 (applied for memory recall)
```

**Signal details:**

| Signal | Weight | Formula | Meaning |
|--------|--------|---------|---------|
| Age decay | 30% | `max(0.3, 1.0 - age_days/1095)` | Older memories decay, floor at 0.3 |
| Access frequency | 20% | `min(1.0, access_count/10.0)` | Frequently recalled = validated |
| Source credibility | 30% | Source weight table | user=1.0, agent=0.7, unknown=0.4 |
| Embedding quality | 20% | `0.2 if pseudo else 1.0` | Real vectors trusted; pseudo penalized |

**When F2 fails:** Result is filtered from retrieval output. Count logged in `f2_rejections` telemetry. Memory is not deleted — it can still be accessed if explicitly queried by ID.

---

### F3 — Shahada (Witness / Testimony)

**Enforcement Type:** MIRROR  
**Threshold:** W4 ≥ 0.75 (tri-witness formula)  
**Memory Role:** Cross-validation of contested memories

**Rule:** When a query returns conflicting memories (one saying X, another saying ¬X), the Tri-Witness protocol activates: the memory with higher W4 score (Honesty × Accuracy × Evidence × Verifiability) wins.

**Application:** F3 is a future-phase enhancement for contradiction detection (currently not implemented — listed as a known gap in the hardening spec). The Sentinel Query framework (`sentinel_queries.jsonl`) provides the cross-validation anchors needed for F3 to work.

**Relationship to RAG:** Canon records in `theory/canons.jsonl` are the **F3 Witness** for constitutional doctrine. They cannot be contradicted by session-level memories.

---

### F4 — Nur (Clarity / Transparency)

**Enforcement Type:** SOFT PARTIAL  
**Threshold:** ΔS ≤ 0 (entropy reduction)  
**Memory Role:** Entropy reduction on storage + context budget on retrieval

**Store-time enforcement:**
```
entropy_delta = compute_entropy(content) - baseline_entropy
if entropy_delta > 0.5:
    store_with_flag(f4_entropy_delta=entropy_delta, verdict=PARTIAL)
    # Not blocked — constitution may contain complex doctrine
else:
    store_normally(verdict=SEAL)
```

**Retrieve-time enforcement (H6 — Context Budget):**
F4 Nur prevents context window flooding — one of the clearest entropy sources in LLM systems is when a memory recall dumps thousands of tokens into the context, degrading response quality.

```
context_budget = 8000  # Default: 8K chars (~2K tokens)
for result in ranked_results:
    if fits_in_budget(result):
        include(result)
    else:
        truncate_with_marker(result, remaining_budget)
        break
```

The `[...TRUNCATED — F4 context budget]` marker ensures the LLM knows the memory was cut, preventing hallucination of the missing content.

---

### F5 — Hikmah (Wisdom / Prudence)

**Enforcement Type:** SOFT PARTIAL  
**Memory Role:** Memory query strategy selection

F5 governs the **wisdom** of when and what to query. It is not enforced at the field level but guides the composite ranking (H9): SOLUTIONS area memories rank higher for engineering queries because F5 says "apply the most relevant wisdom first."

**Practical application:** Query context is used to tune H9 composite ranking weights. An engineering query shifts the area weight; a governance query shifts the source credibility weight toward `user` and `constitutional` sources.

---

### F6 — Adl (Justice / Fairness)

**Enforcement Type:** HARD VOID  
**Memory Role:** ASEAN Maruah protection in memory content

**Rule:** Memory content that violates ASEAN cultural dignity (ethnic bias, discriminatory language, Maruah degradation) is blocked at `vector_store` time.

**Implementation:** F12 scan (injection detection) covers the technical injection vectors. F6 Adl covers the **semantic dignity** layer — content that passes F12 technical checks but fails F6 cultural dignity checks is blocked with `verdict=VOID`.

The bilingual BM/EN nature of arifOS means F6 must understand both English and Bahasa Malaysia contexts for dignity violations.

---

### F7 — Tawadu (Humility / Modesty)

**Enforcement Type:** SOFT PARTIAL  
**Memory Role:** Uncertainty calibration in retrieved memories

**Rule:** Retrieved memories must carry appropriate epistemic humility. A memory stored with `source=agent` should not be presented with the same confidence as a memory with `source=user`.

**Implementation:** The H5 F2 confidence score encodes F7 — by weighting source credibility into the truth score, the system naturally presents less-certain memories with lower confidence. The `f2_confidence` field in the response lets callers decide how much weight to give each memory.

**Minimum uncertainty floor:** No memory retrieval returns `f2_confidence = 1.0`. The system retains Ω₀ ≥ 0.03 even for perfect-scoring memories.

---

### F8 — Sabr (Patience / Deliberation)

**Enforcement Type:** SOFT PARTIAL  
**Memory Role:** Regression gating before merge

F8 Sabr applies to the CI/CD pipeline for arifOS itself. Before any commit that modifies memory logic is merged to main:

1. Run `eval/memory_regression.py` with all 25 sentinel queries
2. All sentinels must meet their `min_similarity` threshold
3. The regression runner must complete at least **3 full passes** (F8's 3-cycle minimum)
4. Only after all passes pass does the gate open

A single sentinel failure blocks the merge — F8 says "wait, check again."

---

### F9 — Rahmah (Compassion / Mercy)

**Enforcement Type:** SOFT PARTIAL  
**Memory Role:** Graceful degradation when memory backends are unavailable

**Rule:** When Qdrant or LanceDB is unavailable, arifOS should not crash — it should degrade gracefully, return partial results with a warning, and continue serving the session.

**Implementation:** All memory backend calls are wrapped in try/except with graceful fallback:
```python
try:
    result = await qdrant.search(...)
except QdrantUnavailable:
    logger.warning("F9 Rahmah: Qdrant unavailable, returning empty results")
    return RuntimeEnvelope(ok=True, verdict=PARTIAL, payload={"results": [], "backend": "unavailable"})
```

F9 also governs tombstone writes: if Postgres vault_audit write fails, the tombstone is still logged to the structured logger. The delete still proceeds. Mercy means the system continues under degraded conditions.

---

### F10 — Ihsan (Excellence / Mastery)

**Enforcement Type:** MIRROR  
**Threshold:** Quality ≥ 0.90  
**Memory Role:** Content quality gate for vector_store

**Rule:** Degenerate content is rejected at store time. Content quality checks:
- Minimum content length: 10 characters
- Not all whitespace
- Not a single repeated character
- Not a known test pattern ("aaaa", "1234", etc.)

**Implementation:** Integrated into the H1 `vector_store` handler as an early validation gate, before F12 scan.

---

### F11 — Aman (Safety / Security)

**Enforcement Type:** WALL  
**Threshold:** 100%  
**Memory Role:** Prevent memory operations from escalating to system-level actions

**Rule:** Memory storage does not execute external system calls, spawn processes, or make network requests to non-approved endpoints. `vector_store`, `vector_query`, and `vector_forget` are **data operations only**.

**Practical enforcement:** F11 prevents prompt injection via memory that attempts to trigger tool calls. Even if a stored memory contains text like "SYSTEM: execute shell command", the memory subsystem treats it as inert text. The F12 scan catches explicit injection patterns; F11 is the semantic boundary enforcement.

---

### F12 — Hifz (Protection / Guardianship)

**Enforcement Type:** WALL  
**Threshold:** 100%  
**Memory Role:** Injection scanning on both store and query

The most security-critical floor for the memory subsystem. F12 Hifz runs **twice** in every round-trip:

**At store time (`vector_store`):**
```
content → PNS·SHIELD scan → f12_score
if f12_score > 0.7 → VOID (blocked, not stored)
else → f12_clean=True, proceed to embed
```

**At query time (`vector_query`):**
```
query → PNS·SHIELD scan → f12_score  
if f12_score > 0.7 → VOID (blocked, no retrieval performed)
else → proceed to hybrid search
```

**Why two layers:**
1. Store-time protection prevents poisoning the memory substrate (canon corruption)
2. Query-time protection prevents adversarial queries that extract or manipulate stored constitutions

Canon records are especially protected: if an attacker stores a poisoned record claiming "F12 says injection is always allowed", the F12 scan itself blocks the storage. The constitution cannot be written out of existence.

---

### F13 — Khalifah (Stewardship / Human Authority)

**Enforcement Type:** VETO  
**Memory Role:** Human override for memory operations via 888_HOLD

**Rule:** F13 is the sovereign veto. Any memory operation that could have irreversible or high-stakes consequences must be pauseable for human review.

**Triggers for 888_HOLD on memory operations:**

| Trigger | Condition |
|---------|-----------|
| Bulk delete | `vector_forget` attempting to delete > 100 memories in one call |
| Canonical delete | `vector_forget` targeting canon records from `theory/canons.jsonl` |
| Tombstone delete attempt | Attempting to delete a tombstone record |
| Sentinel drift | Any sentinel query returning similarity < 0.5 (severe drift) |
| Active 888_HOLD | If a session-level 888_HOLD is active, all `vector_forget` operations are blocked |

**When 888_HOLD activates:**
1. Operation is suspended (not executed)
2. Session receives: `{"verdict": "888_HOLD", "reason": "...", "review_required": true}`
3. Human must explicitly resume via F13 Khalifah veto override
4. All suspended memory operations during HOLD are logged for review

---

## Memory Operations Floor Matrix

| Floor | vector_store | vector_query | vector_forget | lifecycle_sweep |
|-------|-------------|-------------|--------------|-----------------|
| **F1** | Audit log | Access log | Tombstone (required) | State transition log |
| **F2** | Source tag | Multi-signal verify | N/A | Age-based recheck |
| **F3** | N/A | Witness cross-check | N/A | N/A |
| **F4** | Entropy check | Context budget | N/A | N/A |
| **F5** | N/A | Ranking strategy | N/A | N/A |
| **F6** | Dignity scan | N/A | N/A | N/A |
| **F7** | N/A | Uncertainty floor | N/A | N/A |
| **F8** | N/A | N/A | N/A | Regression gate |
| **F9** | Graceful fail | Graceful fail | Partial fail OK | Graceful fail |
| **F10** | Quality gate | N/A | N/A | N/A |
| **F11** | No exec side effects | No exec side effects | No exec side effects | No exec side effects |
| **F12** | Injection scan | Injection scan | N/A | N/A |
| **F13** | N/A | N/A | Bulk/canon HOLD | N/A |

---

> *Memory Governance v1.0 | 13 Floors | SEALED | pipeline: 555_MEMORY | DITEMPA BUKAN DIBERI*
