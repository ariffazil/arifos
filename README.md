---
### Δ arifOS Federation
[**Ψ HUMAN**](https://arif-fazil.com) · [**Δ THEORY**](https://apex.arif-fazil.com) · [**Ω APPS/MCP**](https://mcp.arif-fazil.com) · [**Ω FORGE**](https://forge.arif-fazil.com) · [**Δ AAA**](https://aaa.arif-fazil.com)
*Ditempa Bukan Diberi*
---

# arifOS — Constitutional Intelligence Kernel

A transport-independent governance runtime for AI agents built on explicit, auditable constitutional constraints.

*DITEMPA BUKAN DIBERI — Forged, Not Given*

---

## What arifOS Is

arifOS enforces 13 constitutional Floors on all AI tool executions. It separates reasoning, enforcement, and execution so that:

- No tool can self-approve.
- No action bypasses audit.
- No claim becomes fact without constitutional ratification.

---

## Architecture

```
arifos/
├── core/            ← Pure governance kernel (no transport imports)
├── adapters/mcp/    ← MCP transport bridge
└── tools/           ← Claim producers (import from core only)
```

**Rule:** SEAL authority belongs exclusively to `888_JUDGE`. All other tools emit `CLAIM_ONLY`.

---

## Governance Pipeline (000–999)

| Stage | Tool | Role |
|-------|------|------|
| 000 | `arifos_000_init` | Session anchoring |
| 111 | `arifos_111_sense` | Reality grounding |
| 222 | `arifos_222_witness` | Tri-witness consensus |
| 333 | `arifos_333_mind` | Constitutional reasoning |
| 444 | `arifos_444_kernel` | Metabolic orchestration |
| 555 | `arifos_555_memory` | Context memory |
| 666 | `arifos_666_heart` | Safety critique |
| 777 | `arifos_777_ops` | Operations |
| 888 | `arifos_888_judge` | **SEAL authority** |
| 999 | `arifos_999_vault` | Immutable ledger |
| FORGE | `arifos_forge` | Governed execution after SEAL |
| GATEWAY | `arifos_gateway` | Governed organ-to-organ interaction |
| SABAR | `arifos_sabar` | Cooling and hold-state governance |

Full doctrine: [`000/000_CONSTITUTION.md`](./000/000_CONSTITUTION.md)

---

## The 13 Floors

| Floor | Name | Rule |
|-------|------|------|
| F1 | Amanah | No irreversible action without human approval |
| F2 | Truth | Factual claims require citation |
| F3 | Tri-Witness | Human + AI + Earth consensus required |
| F4 | Clarity | Entropy must not increase (ΔS ≤ 0) |
| F5 | Peace² | Harm potential must be ≥ 1.0 |
| F6 | Empathy | Stakeholder safety ≥ 0.90 |
| F7 | Humility | Confidence bounded within defined Ω range |
| F8 | Genius | Quality score ≥ constitutional threshold |
| F9 | Ethics | Dark pattern score below constitutional threshold |
| F10 | Conscience | No unanchored consciousness claims |
| F11 | Audit | Log verification on all actions |
| F12 | Resilience | Graceful degradation always |
| F13 | Sovereignty | Human override always possible |

---

## Verdict System

| Code | Meaning | Action |
|------|---------|--------|
| `CLAIM_ONLY` | Tool claims success — **not executable** | Guard/invariants must ratify |
| `PARTIAL` | Invariant failure | Proceed with remediation noted |
| `SABAR` | Cooling required | Pause, re-ground |
| `VOID` | Hard constitutional violation | Do not execute |
| `HOLD_888` | Human required | Escalate |
| `SEAL` | `888_JUDGE` only | Execute — no other tool may emit this |

---

## Separation of Powers

```
Tool (claim producer)
    ↓ CLAIM_ONLY
Constitutional Guard (F1-F13 evaluation)
    ↓
Invariant Enforcement (epistemic coherence)
    ↓
888_JUDGE (only authority to emit SEAL)
    ↓
VAULT (immutable record)
```

No silent SEAL is possible.

---

## Quick Start

**Local (recommended for reproducibility):**
```bash
git clone https://github.com/ariffazil/arifOS
cd arifOS
docker compose up -d
curl http://localhost:8080/health
```

**Hosted (evaluation only):**
```bash
curl https://arifOS.arif-fazil.com/health
```

---

## Status

- Package: `arifos` (was `arifosmcp`)
- Core imports: zero FastMCP
- SEAL authority: `888_JUDGE` only
- Transport: MCP via `adapters/mcp/`, interchangeable
- Live public MCP surface: **13 tools** on `/mcp`
- Live health endpoint: `http://localhost:8080/health`
- `arifos_222_witness` web-search path is normalized for empty/error MiniMax bridge payloads; missing web evidence now degrades honestly instead of raising `NoneType` errors
- Baseline: **2026.04.20 — Sovereign core/adapter architecture**

---

## License

AGPL-3.0 | CC0 (theory/doctrine)

---

## Canonical Tool Registry (33 Tool LOCK — 2026-04-21)

| Stage | Tool | Floor | Purpose |
|-------|------|-------|---------|
| 000 | `arifos_000_init` | F1,F13 | Session init, human anchor, sovereignty confirm |
| 111 | `arifos_111_sense` | F4,F10 | Image perception, Earth signal ingestion |
| 222 | `arifos_222_witness` | F2,F4 | Live web search, evidence extraction |
| 333 | `arifos_333_mind` | F3,F7 | Reasoning, hypothesis, confidence scoring |
| 444 | `arifos_444_kernel` | F9,F11 | Anti-hallucination, policy enforcement |
| 555 | `arifos_555_memory` | F1,F11 | Session + long-term memory read/write |
| 666 | `arifos_666_heart` | F6,F13 | Stakeholder dignity, human welfare |
| 777 | `arifos_777_ops` | F8,F12 | Cost, resource, operational safety |
| 888 | `arifos_888_judge` | ALL | Verdict: SEAL/HOLD/VOID with floor audit |
| 999 | `arifos_999_vault` | F11,F13 | Immutable audit ledger, MerkleV3 chain |
| — | `arifos_forge` | F1,F9 | Code execution, file mutation |
| — | `arifos_gateway` | F4,F11 | MCP registry, tool routing |
| — | `arifos_sabar` | ALL | Resilience, graceful degradation |

**Sealed:** `v2026.04.21-UNIFIED` · 33 tools locked · 24 containers running

## Governance Floors (F1–F13)

| Floor | Name | Enforces |
|-------|------|---------|
| F1 | AMANAH | Reversibility — irreversible → 888_HOLD |
| F2 | TRUTH | τ≥0.99 for CLAIM, or declare UNKNOWN |
| F3 | TRI-WITNESS | human + AI + earth signal corroboration |
| F4 | CLARITY | Scale, CRS, provenance explicit |
| F5 | CONSISTENCY | Internal model consistency |
| F6 | MARUAH | Stakeholder dignity protected |
| F7 | HUMILITY | Confidence ∈ [0.03, 0.15] |
| F8 | SAFETY | Law + safety compliance verified |
| F9 | ANTI-HANTU | Zero hallucination — physics or VOID |
| F10 | ONTOLOGY | AI=tool, Model≠Reality |
| F11 | AUDIT | Every decision logged, full provenance |
| F12 | RESILIENCE | Graceful degradation, no single point of failure |
| F13 | SOVEREIGN | Human holds final veto — supreme |

