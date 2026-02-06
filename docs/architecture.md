# AAA MCP Architecture Overview

**Version:** v55.5 | **Date:** 2026-02-02 | **Status:** SEALED

---

## System Architecture

AAA MCP is a **constitutional governance control-plane**, not an autonomous reasoning engine.
It enforces structure, rejects unsafe outputs, maintains control invariants, and normalizes decision flow.

```
                         LLM-Agnostic
                              |
Client --> LLM Provider (Claude/GPT/Gemini/etc.) --> AAA MCP --> Verdict --> Output
                                                       |
                                            Constitutional Floors (F1-F13)
                                            Thermodynamic Wall (Bundle Isolation)
                                            Tri-Witness Consensus
```

### What AAA MCP Does

- Enforces 13 constitutional safety floors at code level
- Maintains thermodynamic isolation between reasoning (AGI) and safety (ASI) engines
- Issues verdicts: SEAL, VOID, 888_HOLD, PARTIAL, SABAR
- Provides immutable audit trail via hash-chained ledger
- Normalizes input across diverse MCP clients

### What AAA MCP Does NOT Do

- Generate reasoning (requires an upstream LLM)
- Replace or contain an LLM
- Perform autonomous cognition or self-directed learning

---

## Trinity Flow

```
000_INIT -> AGI (Delta, 111-333) -> ASI (Omega, 444-666) -> APEX (Psi, 777-888) -> 999_VAULT
   ^                                                                                    |
   +------------------------------- 000<->999 Loop ------------------------------------+
```

| Engine | Symbol | Role | Provider (configurable) | Floors |
|--------|--------|------|------------------------|--------|
| AGI (Delta) | D | Reasoning, precision, hierarchy | Any LLM | F2, F4, F7, F10 |
| ASI (Omega) | O | Safety, empathy, stakeholder care | Any LLM | F1, F5, F6, F9 |
| APEX (Psi) | Y | Judgment, 9-paradox equilibrium | Any LLM | F3, F8, F11, F12 |

**Provider assignment** is configured in `VAULT999/unified_trinity_governance_config.json`.
The MCP kernel itself is LLM-agnostic; any MCP-compatible client can invoke the 7 canonical tools.

---

## 7 Canonical MCP Tools

| Tool | Stage | Purpose |
|------|-------|---------|
| `_init_` | 000 | Session ignition, identity verification |
| `_agi_` | 111-333 | AGI reasoning engine (sense/think/reason) |
| `_asi_` | 444-666 | ASI safety engine (empathy/alignment) |
| `_apex_` | 777-888 | APEX judgment (9-paradox equilibrium) |
| `_vault_` | 999 | Cryptographic seal, immutable ledger |
| `_trinity_` | Full | Complete 000->999 metabolic loop |
| `_reality_` | -- | External fact-checking and grounding |

---

## Transport Layer

| Transport | Entry Point | Use Case |
|-----------|------------|----------|
| stdio | `aaa-mcp-stdio` | Claude Desktop, local MCP clients |
| SSE | `aaa-mcp-sse` | HTTP-based MCP clients |
| Streamable HTTP | `aaa-mcp` | Production (MCP spec 2025-03-26+) |

All transports consume the same `ToolRegistry` and route through the same constitutional kernel.

---

## Thermodynamic Wall

AGI and ASI **cannot see each other's reasoning** until stage 444 (TRINITY_SYNC).
This is enforced through immutable bundle isolation:

- **DeltaBundle**: AGI output (precision, hypotheses, entropy). Sealed after stage 333.
- **OmegaBundle**: ASI output (stakeholders, empathy, reversibility). Sealed after stage 666.
- **MergedBundle**: Created at stage 444 via `compute_consensus()`. Both engines converge here.

---

## Verdict Hierarchy

```
SABAR > VOID > 888_HOLD > PARTIAL > SEAL
```

- **SEAL**: All 13 floors pass. Approved.
- **PARTIAL**: Soft floor warning. Proceed with caution.
- **888_HOLD**: High-stakes. Requires human confirmation.
- **VOID**: Hard floor failed. Cannot proceed.
- **SABAR**: Floor violated. Stop and repair first.
