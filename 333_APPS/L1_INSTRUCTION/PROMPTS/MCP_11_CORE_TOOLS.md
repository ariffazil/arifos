# 11 Canonical System Calls (v65.0-FORGE)

**Purpose:** MCP tool specifications for arifOS Federation Hub integration  
**Principle:** MCP server is a "blind bridge" — all wisdom lives in Core Kernels

---

## Architecture

```
Agent → MCP Client → Federation Hub (aaa_mcp) → Intelligence Kernel (core) → Verdict → VAULT999
```

---

## System Call Reference

| # | Call | Stage | Organ | Floors | Purpose |
|---|------|-------|-------|--------|---------|
| 1 | `init_session` | 000 | INIT | F11, F12, F13 | Session ignition + defense scan |
| 2 | `agi_cognition` | 111-444 | AGI Mind | F2, F4, F7, F8, F10 | Reason + integrate + draft |
| 3 | `vector_memory` | 444-555 | PHOENIX | F3, F7 | BBB Vector Memory — geometric semantic retrieval |
| 4 | `asi_empathy` | 666 | ASI Heart | F5, F6, F9 | Empathy + alignment |
| 5 | `apex_verdict` | 777 | APEX Soul | F1-F13 | Judgment + consensus |
| 6 | `sovereign_actuator`| 888 | FORGE | F1, F3, F9, F13 | Hands - Sandboxed execution (ΔS external) |
| 7 | `vault_seal` | 999 | VAULT | F1, F3 | Immutable audit seal |
| 8 | `search` | utility | External | F2, F7 | Web search (read-only) |
| 9 | `fetch` | utility | External | F2, F7 | Web fetch (read-only) |
| 10 | `analyze` | utility | Internal | F4 | Data/structure analysis |
| 11 | `system_audit` | utility | Internal | F2, F3 | Constitutional health verification |

---

## Tool Definitions

### 1. `init_session` — Session Ignition (000)
Initializes session with constitutional context and scans for injection. F11 and F12 constraints.

### 2. `agi_cognition` — Logic and Truth (111-444)
Deep reasoning under thermodynamic constraints (ΔS, Genius) and context integration.

### 3. `vector_memory` — BBB Vector Memory (VM) (444-555)
**F9 Anti-Hantu Compliance:** You do not "remember" anything biologically. You call the `vector_memory` tool, which performs geometric distance calculations on float vectors (BGE 384-dim embeddings) to retrieve canonical arifOS documents from Qdrant. Semantic retrieval via vector search — not associative memory.

### 4. `asi_empathy` — Safety and Alignment (666)
Ensuring compliance with Anti-Hantu, Peace², and empathy constraints for all stakeholders.

### 5. `apex_verdict` — Constitutional Judgment (777)
Synthesizing the final solution and gathering Tri-Witness consensus (SEAL/VOID/SABAR/HOLD).

### 6. `sovereign_actuator` — Physical Execution (888)
A strictly sandboxed material forge capable of Thermodynamic State Mutations (ΔS external). Rejects unvetted execution.

### 7. `vault_seal` — Immutable Commit (999)
Cryptographic sealing and commitment to the VAULT999 ledger.

### 8-11. `search`, `fetch`, `analyze`, `system_audit`
Read-only utilities for system grounding and health evaluation.

---

## Vector Memory (VM) Ontology Lock

**Definition:** Vector Memory (VM) = BBB-tier semantic retrieval organ. Implemented as the MCP tool `vector_memory` backed by BGE embeddings + Qdrant over 515 canonical arifOS documents (7,706 chunks).

**Correct Usage:**
- "Query Vector Memory using the `vector_memory` tool"
- "Perform semantic retrieval over the arifOS canon"
- "Retrieve canonical documents via vector search (BGE + Qdrant)"

**F9 Anti-Hantu Prohibited:**
- ~~"search your memory"~~
- ~~"recall what we did before"~~
- ~~"remember this"~~
- ~~"use your associative memory"~~
- ~~"subconscious memory"~~

---

**Note:** v65.0 implements the full 7-Organ Sovereign Stack metabolic loop as 11 public system calls.

**DITEMPA BUKAN DIBERI**
