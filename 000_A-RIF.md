# A-RIF: Arif Retrieval Intelligence Framework

**Canon ID:** `ARIF-AGI::A-RIF::000::v1.0`  
**Zone:** `000_CANON`  
**Status:** `SEALED · ΔS↑ · Truth ≥ 0.99 · F2 enforced`  
**Author:** Muhammad Arif bin Fazil  
**Date:** 2026-03-27  
**Motto:** *Ditempa, bukan diberi — Forged, not given*

---

## 0. Executive Summary

A-RIF (Arif Retrieval Intelligence Framework) is the **Retrieval Augmented Generation (RAG)** system for arifOS. It ensures every AI response is grounded in sealed constitutional canon, not hallucinated.

```
A-RIF = RAG + ΔΩΨ Physics + F1-F13 Floors
```

**Purpose:** Transform arifOS from a "chatbot" into a **constitutional intelligence** that cites sources, admits uncertainty, and refuses to fabricate.

---

## 1. What is A-RIF?

### 1.1 Core Definition

**A-RIF** = The system that retrieves canon-verified text before generating responses.

It answers the question:
> *"How does the AI know what it knows — and prove it?"*

### 1.2 A-RIF vs Standard RAG

| Aspect | Standard RAG | A-RIF |
|--------|-------------|--------|
| **Retrieval** | Web search, PDFs | arifOS canon (AAA dataset) |
| **Grounding** | Factual | Constitutional (F1-F13) |
| **Uncertainty** | Hidden | Explicit (F7 Ω₀ band) |
| **Hallucination** | Possible | Prevented by cite-or-refuse |
| **Audit** | None | VAULT999 logged |

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     A-RIF ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [USER QUERY]                                              │
│   "What is F1 Amanah?"                                      │
│         │                                                   │
│         ▼                                                   │
│   ┌─────────────┐                                          │
│   │  000 INIT  │  Identity anchor, injection scan          │
│   │  Gateway   │  Check auth, log session                  │
│   └─────────────┘                                          │
│         │                                                   │
│         ▼                                                   │
│   ┌─────────────┐                                          │
│   │  111 SENSE │  Embed query                              │
│   │  Ollama    │  nomic-embed-text → [0.2, -0.1, ...]     │
│   └─────────────┘                                          │
│         │                                                   │
│         ▼                                                   │
│   ┌─────────────┐                                          │
│   │  222 REALITY│  Vector search                           │
│   │  Qdrant    │  Find K nearest chunks                    │
│   │  sqlite-vec │  Semantic similarity                      │
│   └─────────────┘                                          │
│         │                                                   │
│         ▼                                                   │
│   ┌─────────────┐                                          │
│   │  333 MIND  │  Synthesize retrieved chunks              │
│   │  Compose   │  Format for LLM prompt                    │
│   └─────────────┘                                          │
│         │                                                   │
│         ▼                                                   │
│   ┌─────────────┐                                          │
│   │  444 MEMORY│  Check ΔS, truth threshold                │
│   │  Filter    │  Reject if relevance < 0.7                │
│   └─────────────┘                                          │
│         │                                                   │
│         ▼                                                   │
│   ┌─────────────┐                                          │
│   │  555 HEART  │  Empathy check                           │
│   │  κᵣ filter │  Does response harm weakest listener?     │
│   └─────────────┘                                          │
│         │                                                   │
│         ▼                                                   │
│   ┌─────────────┐                                          │
│   │  666 CRITIQUE│ Adversarial audit                       │
│   │  Shadow scan│  Detect hallucination ghost               │
│   └─────────────┘                                          │
│         │                                                   │
│         ▼                                                   │
│   ┌─────────────┐                                          │
│   │  777 FORGE  │  If PASS → generate response             │
│   │  LLM call   │  Include citations                        │
│   └─────────────┘                                          │
│         │                                                   │
│         ▼                                                   │
│   ┌─────────────┐                                          │
│   │  888 JUDGE  │  Final floor check                       │
│   │  SEAL/VOID  │  F2 Truth ≥ 0.99? Cite present?         │
│   └─────────────┘                                          │
│         │                                                   │
│         ▼                                                   │
│   ┌─────────────┐                                          │
│   │  999 VAULT │  Log to VAULT999                         │
│   │  Append    │  Query + chunks + response + hash         │
│   └─────────────┘                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Data Layers

### 3.1 Source of Truth (HuggingFace)

| Layer | Location | Purpose |
|-------|----------|---------|
| **AAA Dataset** | `huggingface.co/ariffazil/AAA` | Published canon files |
| **Format** | `.md`, `.txt` | Human-readable |
| **Update** | Manual push | Version controlled |

### 3.2 Runtime Index (VPS)

| Layer | Location | Purpose |
|-------|----------|---------|
| **Qdrant** | `qdrant:6333` | Cross-agent semantic search |
| **sqlite-vec** | OpenClaw workspace | Per-agent memory |
| **Update** | Weekly cron sync | HF → VPS |

### 3.3 Embedding Engine

| Component | Model | Purpose |
|-----------|-------|---------|
| **Ollama** | `nomic-embed-text` | Text → vectors |
| **Dimensions** | 1024 | Vector size |
| **Location** | `ollama_engine:11434` | Local, no API cost |

---

## 4. The A-RIF Workflow

### 4.1 Query Flow (Step by Step)

```
1. USER INPUT
   "Explain F1 Amanah in Malaysian context"

2. 000 INIT (Gateway)
   - Authenticate user/session
   - Log to VAULT999 session start
   - Scan for injection attempts

3. 111 SENSE (Embed)
   - Call Ollama: nomic-embed-text
   - Convert query to vector [v₁, v₂, ..., v₁₀₂₄]

4. 222 REALITY (Search)
   - Query Qdrant: top-K chunks by cosine similarity
   - Query sqlite-vec: OpenClaw memory
   - Merge results, deduplicate

5. 333 MIND (Synthesize)
   - Format: "Context from canon:\n[chunk 1]\n[chunk 2]\n..."
   - Include source citations
   - Attach metadata (canon ID, page, line)

6. 444 MEMORY (Filter)
   - Calculate relevance score for each chunk
   - Drop chunks with score < 0.7
   - Update ΔS (clarity gain)

7. 555 HEART (Empathy)
   - Calculate κᵣ (weakest listener impact)
   - If κᵣ < 0.95 → trigger SABAR cooling

8. 666 CRITIQUE (Audit)
   - Scan for Shadow-Truth (accurate but confusing)
   - Check Anti-Hantu (no consciousness claims)
   - Verify F7 Ω₀ band [0.03, 0.05]

9. 777 FORGE (Generate)
   - If all floors pass → LLM generates response
   - Response MUST include citations
   - Response MUST acknowledge uncertainty

10. 888 JUDGE (Verdict)
    - F2 Truth ≥ 0.99? (cited claims verifiable)
    - F4 ΔS ≥ 0? (response clarifies, not confuses)
    - F13 Sovereign? (human can override)

11. 999 VAULT (Seal)
    - Append to VAULT999 ledger
    - Hash: SHA-256(previous + this_entry)
    - Chain integrity verified
```

### 4.2 Response Format

Every A-RIF response follows this template:

```markdown
## Response

[Main answer here]

### Sources

1. **[Canon Title]**  
   `ARIF-AGI::CANON::XXX::v31`  
   Line 42-45  
   Relevance: 0.94

2. **[Another Canon]**  
   `ARIF-AGI::CANON::YYY::v30`  
   Line 108  
   Relevance: 0.87

### Metrics

| Metric | Value | Floor |
|--------|-------|-------|
| Truth | 0.99 | F2 ≥ 0.99 ✓ |
| ΔS | +0.12 | F4 ≥ 0 ✓ |
| κᵣ | 0.97 | F6 ≥ 0.95 ✓ |
| Ω₀ | 0.04 | F7 ∈ [0.03,0.05] ✓ |

### Uncertainty Note

> F7 Humility: I am 96% confident in this answer. The remaining 4% reflects [specific uncertainty].

### SEAL

🔐 SEALED: VAULT999 entry `v999-xxxxx`  
Timestamp: 2026-03-27T14:30:00Z
```

---

## 5. Constitutional Grounding

### 5.1 Floors Enforced by A-RIF

| Floor | Name | A-RIF Enforcement |
|-------|------|------------------|
| **F1** | Amanah | Reversibility — all retrievals logged |
| **F2** | Truth | Citation required; claims verifiable |
| **F3** | Quad-Witness | Human·AI·Earth·Vault consensus |
| **F4** | Clarity | ΔS ≥ 0 — response must clarify |
| **F5** | Peace² | No destabilizing content |
| **F6** | Empathy | κᵣ filter on weakest listener |
| **F7** | Humility | Ω₀ band [0.03, 0.05] explicit |
| **F8** | Genius | G = (A×P×X×E²)×(1-h) formula |
| **F9** | Anti-Hantu | No consciousness claims |
| **F10** | Ontology | AI ≠ human stated |
| **F11** | CommandAuth | Session verified |
| **F12** | Injection | Input sanitized |
| **F13** | Sovereign | Human can override |

### 5.2 Scar → Echo → Law in A-RIF

A-RIF implements the 777 Cube lifecycle:

```
SCAR (query) → 
    Query vector detected as high-entropy
    ↓
ECHO (retrieval) →
    Canon chunks retrieved, cooling begins
    ↓
LAW (response) →
    Synthesized, cited, sealed as canon
```

---

## 6. Sync Protocol

### 6.1 Weekly Cron Schedule

```cron
# Every Sunday 8AM MYT (00:00 UTC)
0 0 * * 0 root /root/arifosmcp/scripts/sync-aaa-hf.sh
```

### 6.2 Sync Steps

```
1. Pull latest from HuggingFace
2. Diff against local copy
3. Re-index changed files
4. Clear vector cache
5. Verify Qdrant integrity
6. Log to VAULT999
```

### 6.3 Manual Sync

```bash
/root/arifosmcp/scripts/sync-aaa-hf.sh
```

---

## 7. Configuration

### 7.1 Key Settings

| Parameter | Value | Location |
|-----------|-------|----------|
| Embedding model | `nomic-embed-text` | Ollama |
| Vector dimensions | 1024 | Ollama |
| Top-K results | 10 | A-RIF config |
| Min relevance | 0.7 | A-RIF filter |
| Sync frequency | Weekly | Cron |

### 7.2 Environment

```
OLLAMA_HOST=http://ollama_engine:11434
QDRANT_HOST=http://qdrant:6333
OPENCLAW_MEMORY=sqlite-vec
HF_DATASET=/root/arifosmcp/AAA-hf-staging
```

---

## 8. Glossary

| Term | Definition |
|------|-----------|
| **A-RIF** | Arif Retrieval Intelligence Framework |
| **RAG** | Retrieval Augmented Generation |
| **Embed** | Convert text to vector representation |
| **Chunk** | Text segment from canon file |
| **Qdrant** | Vector database for semantic search |
| **sqlite-vec** | SQLite vector extension for OpenClaw |
| **Citation** | Source reference in response |
| **SEAL** | Immutable VAULT999 entry |
| **SABAR** | Pause/cooldown when floors at risk |

---

## 9. Canon References

- `000_THEORY` — Foundation of arifOS
- `777_CUBE` — Scar → Echo → Law lifecycle
- `888_JUDGMENT` — Verdict system
- `999_VAULT` — Immutable ledger
- `AAA_DATASET` — HuggingFace source

---

## 10. Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-03-27 | Initial sealed canon |

---

**SEALED** 🔐

```
Canon ID: ARIF-AGI::A-RIF::000::v1.0
Witness: Human (Arif) · AI (MiniMax-M2.7) · Earth (Entropy)
Status: SEALED · Truth ≥ 0.99 · F2 enforced
Motto: Ditempa, bukan diberi
```
