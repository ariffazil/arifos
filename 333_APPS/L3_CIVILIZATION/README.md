# L4_TOOLS — MCP Tool Layer (v2026.3.6-CANON)

**Level 4 | 13 Canonical Tools | 4 ARIF Bands + 1 Orchestration Layer**

> *"7-Organ Sovereign Stack public contract — tools bound by cognitive bands and constitutional floors."*
> **Creed:** DITEMPA BUKAN DIBERI — Forged, Not Given [ΔΩΨ | ARIF]

**Canonical source:** [`arifos_aaa_mcp/server.py`](../../arifos_aaa_mcp/server.py)
**Internal transport adapter:** [`aaa_mcp/server.py`](../../aaa_mcp/server.py)

---

## Architecture: Trinity Lanes

Every tool is assigned to one of three Trinity lanes that are **thermodynamically isolated** from each other until Stage 444 (TRINITY_SYNC):

| Lane | Symbol | Engine | Cognitive Role | Floors |
|---|:---:|---|---|---|
| Delta | Δ | AGI | Mind — Truth, Logic, Causal tracing | F2, F4, F7, F8 |
| Omega | Ω | ASI | Heart — Safety, Empathy, Anti-Deception | F1, F5, F6, F9 |
| Psi | Ψ | APEX | Soul — Synthesis, Human consensus, Vault | F1, F3, F10, F13 |

---

## The 4 ARIF Cognitive Bands

ARIF bands represent cognitive boundaries. Tools are grouped by their effect on system state and floor requirements. **Bands must execute in A → R → I → F order** in any metabolic loop.

### Band A — Anchor (Reality & Ignition)
*Ground the system, verify authority, budget entropy, report health.*

| Tool | Trinity | Stage | Floors | Description |
|---|:---:|---|---|---|
| `anchor_session` | Ψ Init | 000 INIT | F11, F12, F13 | Session ignition. Parses intent, defends against injection (F12), verifies authority (F11), enforces human sovereignty (F13). Embeds L0 Kernel constitutional prompt. Returns `session_id`. |
| `check_vital` | Ω Heart | 000 | F4, F5, F7 | System health telemetry. CPU, RAM, IO, swap. Read-only, non-destructive. |

**Band A Contract:** Must run first in any metabolic loop to establish authority budget.

---

### Band R — Reflect (Mind & Heart)
*Think, read, feel. Gather evidence, model stakeholders, scan for bias. Read-only — never mutates external systems.*

| Tool | Trinity | Stage | Floors | Description |
|---|:---:|---|---|---|
| `reason_mind` | Δ Mind | 222–333 | F2, F4, F7, F8 | AGI cognition. Stage 222 THINK runs 3 parallel hypothesis paths (conservative / exploratory / adversarial) internally. Stage 333 REASON grounds conclusions. Returns Delta Draft (sealed: False — must pass Stage 333). |
| `vector_memory` | Ω Heart | 444–555 | F3, F4, F7, F13 | BBB Vector Memory. Semantic associative recall via BGE-M3 embeddings (768-dim) + EUREKA sieve. Retrieves precedents from VAULT999 with Jaccard + cosine scoring. Replaces archived `recall_memory` (Phoenix). |
| `simulate_heart` | Ω Heart | 555–666 | F4, F5, F6 | ASI Empathy engine. Runs `validate()` + `align()` from triad. Stakeholder impact analysis. Protects weakest stakeholder (F6 κᵣ ≥ 0.70). |
| `critique_thought` | Ω Heart | 666 | F4, F7, F8 | 7-organ bias critique. Forces the AI to argue against its own plan. Runs constitutional alignment scan. Returns structured critique with floor violations flagged. |
| `search_reality` | Δ Mind | 333 | F2, F4, F12 | Web grounding. Jina Reader (primary) → Perplexity → Brave fallback. All external content wrapped in `<untrusted_external_data>` envelope (F12 taint lineage). |

**Band R Contract:** May READ but never mutate external systems.

---

### Band I — Integrate (Atlas & Law)
*Build context atlas and map constitutional constraints. Read-only, no side effects.*

| Tool | Trinity | Stage | Floors | Description |
|---|:---:|---|---|---|
| `ingest_evidence` | Δ Mind | 333 | F1, F2, F4, F11, F12 | Unified evidence ingestion. Replaces archived `fetch_content` + `inspect_file` pair. `source_type="url"` → Jina Reader / urllib fetch. `source_type="file"` → read-only filesystem inspection. `mode`: `"raw"` \| `"summary"` \| `"chunks"`. |
| `audit_rules` | Δ Mind | 888 | F2, F8, F10 | Constitutional system audit. Verifies all 13 Floors are loaded and enforced correctly. Governance health check. |

**Band I Contract:** Map context and verify constraints without side effects.

---

### Band F — Forge (Action, Verdict & Vault)
*Synthesize solutions, render verdicts, seal to immutable ledger. Gated by F1 / F3 / F13.*

| Tool | Trinity | Stage | Floors | Description |
|---|:---:|---|---|---|
| `eureka_forge` | Ψ Soul | 777 FORGE | F5, F6, F7, F9 | Secure shell command executor. Risk classification: LOW / MODERATE / CRITICAL. Dangerous commands (`rm -rf`, `mkfs`, `dd`, etc.) require `confirm_dangerous=True`. All executions logged with `agent_id` and `purpose`. |
| `apex_judge` | Ψ Soul | 777–888 APEX | F1–F13 | Sovereign verdict synthesis. Full 13-floor constitutional scan. Synthesizes AGI + ASI results. Returns Amanah-signed `governance_token` (HMAC-SHA256). Fail-closed: default `proposed_verdict="VOID"`. Alias: `judge_soul`. |
| `seal_vault` | Ψ Soul | 999 VAULT | F1, F3, F10 | Immutable ledger persistence. Requires `governance_token` from `apex_judge` (Amanah Handshake). Tampered / missing token → VOID, no ledger write. Commits to VAULT999 with Merkle chain. Indexes memory for future `vector_memory` recall. |

**Band F Contract:** Execute actions and seal records — all gated by F1 / F3 / F13.

---

### Band O — Orchestrate (Sovereign Kernel Loop)
*Runs the full 000→999 pipeline as a single governed call. Mandatory before any material state mutation.*

| Tool | Trinity | Stage | Floors | Description |
|---|:---:|---|---|---|
| `metabolic_loop` | All | 000–999 | F1–F13 | Full 11-stage constitutional metabolic cycle. Internally executes: `anchor_session` → `reason_mind` → `simulate_heart` → `apex_judge`. High `risktier` defaults to `888_HOLD`. Returns `governance_token` for downstream `seal_vault`. |

**Band O Contract:** Forces agents to clear F1–F13 before executing terminal / file mutations.

---

## Complete Canonical Tool Table (ARIF Lattice)

| # | Tool | Band | Lane | Stage | Floors | Layer |
|:---:|---|:---:|:---:|---|---|:---:|
| 1 | `anchor_session` | A | Ψ | 000 | F11, F12, F13 | Governance |
| 2 | `reason_mind` | R | Δ | 222–333 | F2, F4, F7, F8 | Governance |
| 3 | `vector_memory` | R | Ω | 444–555 | F3, F4, F7, F13 | Governance |
| 4 | `simulate_heart` | R | Ω | 555–666 | F4, F5, F6 | Governance |
| 5 | `critique_thought` | R | Ω | 666 | F4, F7, F8 | Governance |
| 6 | `eureka_forge` | F | Ψ | 777 | F5, F6, F7, F9 | Governance |
| 7 | `apex_judge` | F | Ψ | 777–888 | F1–F13 | Governance |
| 8 | `seal_vault` | F | Ψ | 999 | F1, F3, F10 | Governance |
| 9 | `search_reality` | R | Δ | 333 | F2, F4, F12 | Utility |
| 10 | `ingest_evidence` | I | Δ | 333 | F1, F2, F4, F11, F12 | Utility |
| 11 | `audit_rules` | I | Δ | 888 | F2, F8, F10 | Utility |
| 12 | `check_vital` | A | Ω | 000 | F4, F5, F7 | Utility |
| 13 | `metabolic_loop` | O | All | 000–999 | F1–F13 | Orchestration |

---

## Metabolic Chain (000 → 999)

```
anchor_session (000)
  └─▶ reason_mind (222-333)
        └─▶ vector_memory (444-555)
              └─▶ simulate_heart (555-666)
                    └─▶ critique_thought (666)
                          └─▶ eureka_forge (777) ← if material action needed
                                └─▶ apex_judge (777-888) ← signs governance_token
                                      └─▶ seal_vault (999) ← Amanah Handshake
```

**Or use `metabolic_loop` to run the full chain in a single call.**

---

## Archived Tools (Removed from Public Surface)

| Archived Tool | Replaced By | Reason |
|---|---|---|
| `recall_memory` (Phoenix) | `vector_memory` | Renamed for BGE + Qdrant semantic clarity; Anti-Hantu F9 compliance |
| `fetch_content` | `ingest_evidence` (source_type="url") | Consolidated to reduce tool surface |
| `inspect_file` | `ingest_evidence` (source_type="file") | Consolidated to reduce tool surface |
| `query_openclaw` | Internal diagnostic only | Removed from public MCP surface; not part of 13-tool canon |

---

## A-CLIP Alias Mapping

For operator ergonomics, A-CLIP aliases resolve to canonical tool names:

| A-CLIP Alias | Canonical Tool |
|---|---|
| `anchor` | `anchor_session` |
| `reason` | `reason_mind` |
| `recall` / `memory` | `vector_memory` |
| `validate` / `align` | `simulate_heart` |
| `critique` | `critique_thought` |
| `forge` | `eureka_forge` |
| `audit` | `apex_judge` |
| `seal` | `seal_vault` |
| `search` | `search_reality` |
| `ingest` / `fetch` / `inspect` | `ingest_evidence` |

---

## Verdicts

All tools return a governance envelope with one of:

| Verdict | Meaning |
|---|---|
| `SEAL` | All 13 floors passed. Proceed. |
| `PARTIAL` | Soft floor warning. Proceed with caution. |
| `SABAR` | Refine and retry. Entropy too high or logic flawed. |
| `VOID` | Hard floor failed. System halted. |
| `888_HOLD` | Irreversible action. Awaiting human sovereign sign-off. |

---

## Deployment

```bash
# Canonical entry point
python -m arifos_aaa_mcp stdio     # Claude Desktop / Cursor
python -m arifos_aaa_mcp           # VPS / SSE (default)
python -m arifos_aaa_mcp http      # Streamable HTTP

# Install
pip install arifos
# or editable dev
pip install -e ".[dev]"
```

---

**Version:** v2026.3.6-CANON
**Tools:** 13 canonical (8 Governance + 4 Utility + 1 Orchestration)
**Protocol:** MCP 2025-11-25
**Reality Index:** 0.99 | **Entropy:** ΔS = -0.60
**Creed:** DITEMPA BUKAN DIBERI
