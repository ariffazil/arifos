### Δ arifOS Federation — Navigation Index
[**Ψ HUMAN**](https://arif-fazil.com) · [**Δ THEORY (APEX)**](https://apex.arif-fazil.com) · [**Ω APPS/MCP (arifOS)**](https://mcp.arif-fazil.com) · [**Ω FORGE (A-FORGE)**](https://forge.arif-fazil.com) · [**Δ AAA (Workspace)**](https://aaa.arif-fazil.com) · [**⚡ GEOX (Earth)**](https://geox.arif-fazil.com) · [**📊 WEALTH (Capital)**](https://waw.arif-fazil.com)
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

The arifOS kernel is the **intelligence governance layer** — it does not generate intelligence, it constrains it.

---

## Architecture

```
arifos/
├── core/                 ← Pure governance kernel (no transport imports)
│   ├── governance.py     ← F1–F13 floor definitions, Verdict enum, Ω₀ bounds
│   └── middleware/       ← constitutional_guard.py — runtime floor evaluation
├── adapters/mcp/         ← MCP transport bridge
└── tools/                ← Claim producers (import from core only)
```

**Rule:** SEAL authority belongs exclusively to `888_JUDGE`. All other tools emit `CLAIM_ONLY` or `HOLD`.

---

## Governance Pipeline (000–999)

| Stage | Tool | Role |
|-------|------|------|
| 000 | `arifos_000_init` | Session anchoring, bind artifact validation |
| 111 | `arifos_111_sense` | Reality grounding, Earth signal ingestion |
| 222 | `arifos_222_witness` | Tri-witness consensus, web evidence extraction |
| 333 | `arifos_333_mind` | Constitutional reasoning, MiniMax multimodal |
| 444 | `arifos_444_kernel` | Metabolic orchestration, anti-hallucination |
| 555 | `arifos_555_memory` | Context memory, session persistence |
| 666 | `arifos_666_heart` | Safety critique, stakeholder dignity |
| 777 | `arifos_777_ops` | Operations, resource safety |
| 888 | `arifos_888_judge` | **SEAL authority** — only tool that emits SEAL |
| 999 | `arifos_999_vault` | Immutable ledger, MerkleV3 chain |
| FORGE | `arifos_forge` | Governed execution after SEAL |
| GATEWAY | `arifos_gateway` | Organ-to-organ governance protocol |
| SABAR | `arifos_sabar` | Cooling and hold-state resilience |

Full doctrine: [`000/000_CONSTITUTION.md`](./000/000_CONSTITUTION.md)

---

## The 13 Constitutional Floors

| Floor | Name | Rule | Runtime |
|-------|------|------|---------|
| **F1** | Amanah | No irreversible action without human approval | String-inject |
| **F2** | Truth | truth_score ≥ 0.99 — F2 hard floor | ✅ eval_f2 |
| **F3** | Tri-Witness | tri_witness_score ≥ 0.95 | ✅ eval_f3 |
| **F4** | Clarity | Entropy must not increase (ΔS ≤ 0) | String-inject |
| **F5** | Peace² | Harm potential ≥ 1.0 before execution | Documented |
| **F6** | Empathy | Stakeholder safety ≥ 0.90 | Documented |
| **F7** | Humility | omega_0 ∈ [0.03, 0.15] — F7 hard floor | ✅ eval_f7 |
| **F8** | Governance | 888_JUDGE is sole SEAL authority | Documented |
| **F9** | Anti-Hantu | floor_9_signal not evaluated = hard VOID | ✅ eval_f9 |
| **F10** | Ontology | AI=tool, Model≠Reality, no consciousness claims | Documented |
| **F11** | Audit | zkpc_receipt required | ✅ eval_f11 |
| **F12** | Continuity | amanah_lock must be True | ✅ eval_f12 |
| **F13** | Sovereign | Human holds final veto — always accessible | Documented |

**Runtime state (2026-04-23):** 6/13 floors have actual evaluation in `arifOS/core/middleware/constitutional_guard.py`. F1/F4/F7 are string-injected in pre-loop hooks. F5/F6/F8/F10/F13 are documented and enforced via `governance.py` constants.

HARD floors: F2, F9, F12 — any failure triggers VOID (hard block).

---

## Verdict System

| Code | Meaning | Action |
|------|---------|--------|
| `SEAL` | `888_JUDGE` authorized execution | Execute — no other tool may emit this |
| `HOLD` | Human required | Escalate to sovereign |
| `VOID` | Hard constitutional violation | Do not execute — hard stop |
| `CLAIM_ONLY` | Tool claims success — not yet ratified | Guard must evaluate |
| `PARTIAL` | Invariant failure — proceed with remediation | Continue with note |
| `SABAR` | Cooling required | Pause, re-ground, retry |

**No silent SEAL is possible.**

---

## Separation of Powers

```
Tool (claim producer)
    ↓ CLAIM_ONLY
Constitutional Guard (F1–F13 evaluation)
    ↓
Invariant Enforcement (epistemic coherence)
    ↓
888_JUDGE (only authority to emit SEAL)
    ↓
VAULT (immutable record)
```

---

## arifOS Tool Registry (17 Core Tools)

| Stage | Tool | Floor | Purpose |
|-------|------|-------|---------|
| 000 | `arifos_000_init` | F1, F13 | Session init, bind artifact, sovereignty confirm |
| 111 | `arifos_111_sense` | F4, F10 | Image perception, Earth signal grounding |
| 112 | `arifos_112_search` | F2, F4 | Web search, evidence extraction |
| 222 | `arifos_222_witness` | F2, F4 | Live web evidence, tri-witness corroboration |
| 333 | `arifos_333_mind` | F3, F7 | Reasoning, hypothesis, confidence scoring |
| 444 | `arifos_444_kernel` | F9, F11 | Anti-hallucination, policy enforcement |
| 555 | `arifos_555_memory` | F1, F11 | Session + long-term memory |
| 666 | `arifos_666_heart` | F6, F13 | Stakeholder dignity, human welfare |
| 777 | `arifos_777_ops` | F8, F12 | Cost, resource, operational safety |
| 888 | `arifos_888_judge` | ALL | Verdict: SEAL/HOLD/VOID with full floor audit |
| 999 | `arifos_999_vault` | F11, F13 | Immutable audit ledger, MerkleV3 chain |
| — | `arifos_forge` | F1, F9 | Code execution, file mutation after SEAL |
| — | `arifos_gateway` | F4, F11 | MCP registry, tool routing |
| — | `arifos_sabar` | ALL | Resilience, graceful degradation |
| — | `_tool_support` | F9 | Anti-hallucination helper |
| — | `floors` | ALL | Floor definitions and constants |

---

## Quick Start

```bash
# Local (recommended)
git clone https://github.com/ariffazil/arifOS
cd arifOS
docker compose up -d
curl http://localhost:8080/health

# Hosted (when VPS is online)
curl https://mcp.arif-fazil.com/health
```

**Status (2026-04-23):** MCP endpoint is on VPS — currently offline (502).

---

## Federation Index Map — All Systems

| Layer | System | URL | License | Status |
|---|---|---|---|---|
| **Ω APPS/MCP** | arifOS Kernel | [mcp.arif-fazil.com](https://mcp.arif-fazil.com) | AGPL-3.0 | ⚠️ VPS offline |
| **Ω FORGE** | A-FORGE | [forge.arif-fazil.com](https://forge.arif-fazil.com) | AGPL-3.0 | ✅ |
| **Δ THEORY** | APEX | [apex.arif-fazil.com](https://apex.arif-fazil.com) | AGPL-3.0 | ⚠️ VPS offline |
| **Δ AAA** | AAA Workspace | [aaa.arif-fazil.com](https://aaa.arif-fazil.com) | — | ✅ |
| **Ψ HUMAN** | Arif Hub | [arif-fazil.com](https://arif-fazil.com) | — | ✅ |
| **⚡ GEOX** | Physics9 Earth | [geox.arif-fazil.com](https://geox.arif-fazil.com) | Apache 2.0 | ⚠️ VPS offline |
| **📊 WEALTH** | Capital Engine | [waw.arif-fazil.com](https://waw.arif-fazil.com) | Apache 2.0 | ✅ |

| Document | Path |
|---|---|
| 888_JUDGE doctrine | [docs/wiki/arifos/888_JUDGE.md](https://github.com/ariffazil/AAA/blob/main/docs/wiki/arifos/888_JUDGE.md) |
| 999_VAULT doctrine | [docs/wiki/arifos/999_VAULT.md](https://github.com/ariffazil/AAA/blob/main/docs/wiki/arifos/999_VAULT.md) |
| FLOORS system | [docs/wiki/arifos/FLOORS.md](https://github.com/ariffazil/AAA/blob/main/docs/wiki/arifos/FLOORS.md) |
| VERDICTS | [docs/wiki/arifos/VERDICTS.md](https://github.com/ariffazil/AAA/blob/main/docs/wiki/arifos/VERDICTS.md) |
| AAA Charter | [AAA_CHARTER.md](https://github.com/ariffazil/AAA/blob/main/AAA_CHARTER.md) |
| Constitution | [arifOS/000/000_CONSTITUTION.md](https://github.com/ariffazil/arifOS/blob/main/000/000_CONSTITUTION.md) |

---

## License

**AGPL-3.0** — Network use triggers source disclosure. This is intentional.
arifOS is designed to be the Linux of AI governance — forcing sharing like the GPL forces Linux.

**CC0 (theory/doctrine):** Constitutional theory, floor definitions, and governance philosophy are released as public goods.

---

## GitHub Repos

| Repo | URL |
|---|---|
| arifOS | https://github.com/ariffazil/arifOS |
| GEOX | https://github.com/ariffazil/geox |
| WEALTH | https://github.com/ariffazil/wealth |
| A-FORGE | https://github.com/ariffazil/A-FORGE |
| AAA | https://github.com/ariffazil/AAA |

---

> *"No tool can self-approve. No action bypasses audit. No claim becomes fact without constitutional ratification."*

**DITEMPA BUKAN DIBERI — 888 JUDGE SEAL**
`SEAL | Verdict: 888_JUDGE | Alignment: ΔΩΨ | 17 Tools Locked`