# arifOS ARCHITECTURE: THE TRINITY (AAA-BBB-CCC)

> **Motto:** *Ditempa Bukan Diberi* — One constitution, three tiers: HUMAN → AI → MACHINE.

## 1. Overview

arifOS is a **constitutional control plane** for AI systems. It governs, it does not replace.

-   **One Constitution**: 13 Floors (F1–F13) apply to *all* AI actions.
-   **Three Tiers**: HUMAN (AAA), AI (BBB), MACHINE (CCC).
-   **One Audit Trail**: VAULT999 records every significant decision.

---

## 2. THE TOPOLOGY

```text
┌─────────────────────────────────────────────────────────────────┐
│                    HUMAN–AI–MACHINE TRINITY                     │
│                                                                 │
│   AAA MCP        BBB MCP          CCC MCP                       │
│   ═══════        ═══════          ═══════                       │
│   SOVEREIGN      AGENT            MACHINE                       │
│   (Human)        (AI)             (System)                      │
│                                                                 │
│   "Should we?"   "How do we?"     "Execute it"                  │
│                                                                 │
│   Governance ──► Orchestration ──► Infrastructure               │
└─────────────────────────────────────────────────────────────────┘
```

## 3. TIER DEFINITIONS

### AAA MCP: The Sovereign Tier (Human)
*   **Role**: Governance & Intent.
*   **Question**: "Should we do this?"
*   **Components**:
    *   Human-AI Interaction SDK (Constitutional Link).
    *   `init_gate`: Authority verification.
    *   `apex_judge`: Final verdicts on high-stakes decisions.
*   **Filesystem**: `aaa_mcp/` (The current active workspace).

### BBB MCP: The Agent Tier (AI)
*   **Role**: Orchestration & Planning.
*   **Question**: "How do we do this?"
*   **Components**:
    *   `agi_genius`: Reasoning & Planning.
    *   `asi_empathize`: Stakeholder Simulation.
    *   `recall_memory`: Semantic Retrieval (RAG via BGE + Qdrant).
    *   Multi-agent coordination (Swarm).
*   **Memory**:
    *   **RAG**: 7,706 semantic chunks from 515 canonical documents.
    *   **Session**: Operational context (conversational state).
    *   **Constraint**: No persistent user data; batch-indexed only.
*   **Filesystem**: `bbb_mcp/` (Future implementation).

### CCC MCP: The Machine Tier (System)
*   **Role**: Infrastructure & Execution.
*   **Question**: "Execute it."
*   **Components**:
    *   `vault_seal`: Cryptographic Ledger.
    *   `k8s_ops`: Infrastructure management.
    *   Hardware interfaces.
*   **Filesystem**: `ccc_mcp/` (Future implementation or `core/`).

---

## 4. INTEGRATION
All tiers share the **Constitutional Kernel** (The 13 Floors).
Data flows from AAA ("I want X") -> BBB ("Plan X") -> CCC ("Run X") -> AAA ("Result X").
The **Metabolic Loop** (000-999) spans across these tiers, with approval gates at each transition.
