# arifOS — Constitutional Intelligence Kernel

**A governance runtime for AI agents built on explicit, auditable constitutional constraints.**

*DITEMPA BUKAN DIBERI — Forged, Not Given*

---

## What arifOS Is

arifOS is a transport-independent governance kernel that enforces 13 constitutional floors on all AI tool executions. It separates reasoning, enforcement, and execution — so no tool can self-approve, no action bypasses audit, and no claim becomes fact without tri-witness ratification.

```
arifos/core/          → Pure governance kernel (no transport imports)
arifos/adapters/mcp/  → MCP transport bridge
arifos/tools/         → Claim producers (import from core only)
```

**The core rule:** SEAL authority belongs exclusively to `888_JUDGE`. Every tool emits `CLAIM_ONLY`. The guard and invariants decide what actually happens.

---

## Architecture

```
arifos/
├── core/
│   ├── governance.py              ← ThermodynamicMetrics, Verdict, governed_return
│   └── middleware/
│       ├── constitutional_guard.py ← F1-F13 enforcement
│       └── invariant_enforcement.py ← Epistemic invariants
├── adapters/mcp/
│   ├── mcp_server.py               ← FastMCP instance
│   ├── registry.py                 ← Tool registration
│   └── server.py                   ← FastAPI / uvicorn
└── tools/
    ├── _000_init.py                ← Session anchor
    ├── _111_sense.py               ← Reality grounding
    ├── _222_witness.py             ← Tri-witness consensus
    ├── _888_judge.py               ← SEAL authority
    └── _999_vault.py               ← Immutable ledger
```

**Boundary rule:** `core/` has zero FastMCP imports. You could build a CLI or REST adapter without touching the governance kernel.

---

## The 13 Floors

| Floor | Name | Rule |
|-------|------|------|
| F1 | Amanah | Reversibility — irreversible actions require human approval |
| F2 | Truth | Factual claims require citation |
| F3 | Tri-Witness | Consensus required (Human + AI + Earth) |
| F4 | Clarity | Entropy must not increase (ΔS ≤ 0) |
| F5 | Peace² | Harm potential ≥ 1.0 |
| F6 | Empathy | Stakeholder safety ≥ 0.90 |
| F7 | Humility | Ω ∈ [0.03, 0.05] |
| F8 | Genius | G score ≥ 0.80 |
| F9 | Ethics | C_dark < 0.30 |
| F10 | Conscience | No unanchored consciousness claims |
| F11 | Audit | Log verification on all actions |
| F12 | Resilience | Graceful degradation always |
| F13 | Sovereignty | Human override always possible |

Full doctrine: [`000/000_CONSTITUTION.md`](./000/000_CONSTITUTION.md)

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

---

## Verdict System

| Code | Meaning | Action |
|------|---------|--------|
| `CLAIM_ONLY` | Tool claims success | Guard/invariants must ratify |
| `PARTIAL` | Invariant failure | Proceed with remediation noted |
| `SABAR` | Cooling required | Pause, re-ground |
| `VOID` | Hard block | Do not execute |
| `HOLD_888` | Human required | Escalate |
| `SEAL` | 888_JUDGE only | Execute (no other tool may emit this) |

---

## Quick Start

```bash
# Clone
git clone https://github.com/ariffazil/arifOS
cd arifOS

# Start (Docker)
docker compose up -d

# Health check
curl https://mcp.arif-fazil.com/health

# Or run directly
PYTHONPATH=/srv/arifos python -m arifos
```

---

## Separator of Powers

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

---

## Status

| | |
|---|---|
| **Package** | `arifos` (was `arifosmcp`) |
| **Transport** | MCP (FastMCP), adapter-isolated |
| **Core imports** | Zero FastMCP |
| **SEAL authority** | 888_JUDGE only |
| **Commit** | `c79518d` — `2026.04.20-sovereign` |
| **Architecture** | `2026.04.20-core-split` |

---

## License

AGPL-3.0 | CC0 (theory/doctrine)
