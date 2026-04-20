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
curl http://localhost:8000/health
```

**Hosted (evaluation only):**
```bash
curl https://mcp.arif-fazil.com/health
```

---

## Status

- Package: `arifos`
- Core imports: zero FastMCP
- SEAL authority: `888_JUDGE` only
- Transport: MCP via `adapters/mcp/`, interchangeable
- Baseline: **2026.04.20 — Sovereign core/adapter architecture**

---

## License

AGPL-3.0 | CC0 (theory/doctrine)
