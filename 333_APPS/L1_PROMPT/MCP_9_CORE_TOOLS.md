# 9 Canonical MCP Tools for Claude Code + arifOS Integration

**Version:** v55.5-EIGEN
**Purpose:** Canonical MCP tool specifications for Claude Code implementation
**Authority:** Based on MCP Protocol Standard + arifOS Constitutional Framework
**Last Updated:** February 2026

---

## Executive Summary

This document defines the **9 canonical MCP tools** that Claude Code must implement to provide full arifOS Constitutional AI Governance. These tools bridge the MCP transport layer (stdio/HTTP) with arifOS Core Kernels (AGI/ASI/APEX), enforcing 13 constitutional floors through a zero-logic architecture.

**Key Principle:** The MCP server is a "blind bridge" - all wisdom lives in Core Kernels, the server only routes requests and serializes responses.

---

## Architecture Overview

```
Claude Code (MCP Host)
       ↓
MCP Client (1:1 connection)
       ↓
MCP Server (stdio/HTTP transport)
       ↓
Bridge Router (Zero-logic delegation)
       ↓
Core Kernels (AGI/ASI/APEX)
       ↓
Constitutional Enforcement (F1-F13)
       ↓
VAULT-999 (Immutable ledger)
```

**Flow:** User → Claude Code → MCP Tool Call → Bridge → Kernel → Verdict → Seal → Response

---

## The 9 Canonical MCP Tools

| Tool | Name | Role | Stages | Floors Enforced |
|------|------|------|--------|-----------------|
| 1 | `init_gate` | Gate | 000 (Ignition) | F11, F12 |
| 2 | `agi_sense` | Mind | 111 (SENSE) | F12 |
| 3 | `agi_think` | Mind | 222 (THINK) | F4 |
| 4 | `agi_reason` | Mind | 333 (REASON) | F2, F4, F7, F10 |
| 5 | `asi_empathize` | Heart | 555 (EMPATHY) | F5, F6, F9 |
| 6 | `asi_align` | Heart | 666 (ALIGN) | F9 |
| 7 | `apex_verdict` | Soul | 888 (JUDGE) | F3, F8, F11 |
| 8 | `reality_search` | Ground | External | F7, F10 |
| 9 | `vault_seal` | Seal | 999 (SEAL) | F1 |

**Naming Convention:** Lowercase snake_case (e.g., `init_gate`). Legacy underscores (`_init_`) are deprecated.

---

## Tool 1: `init_gate` (Session Gate)

**Purpose:** Session initialization, authority verification, injection defense

**MCP Tool Definition:**
```json
{
  "name": "init_gate",
  "title": "Session Initialization Gate",
  "description": "Initialize a governed session. Verify caller authority, scan for prompt injection (F12), and open a session ledger entry. Use this before running other tools when starting a new workflow.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {"type": "string"},
      "user_token": {"type": "string"},
      "session_id": {"type": "string"}
    },
    "required": ["query"]
  }
}
```

---

## Tool 2: `agi_sense` (Intent Detection)

**Purpose:** Parse input, classify intent, routing

**MCP Tool Definition:**
```json
{
  "name": "agi_sense",
  "title": "Input Parsing & Intent Detection",
  "description": "Parse the user input, detect intent, and classify the request into constitutional lanes (HARD/SOFT/PHATIC).",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {"type": "string"},
      "session_id": {"type": "string"}
    },
    "required": ["query"]
  }
}
```

---

## Tool 3: `agi_think` (Hypothesis Generation)

**Purpose:** Generate options without commitment

**MCP Tool Definition:**
```json
{
  "name": "agi_think",
  "title": "Hypothesis Generation",
  "description": "Generate multiple possible hypotheses, options, or plans for how to respond to the user. Does not commit to a final verdict.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {"type": "string"},
      "session_id": {"type": "string"},
      "num_hypotheses": {"type": "integer"}
    },
    "required": ["query"]
  }
}
```

---

## Tool 4: `agi_reason` (Deep Reasoning)

**Purpose:** Logical chain construction, truth verification

**MCP Tool Definition:**
```json
{
  "name": "agi_reason",
  "title": "Deep Logical Reasoning",
  "description": "Perform deep logical reasoning over the user's question and context. Builds a step-by-step reasoning chain and enforces Truth (F2) and Clarity (F4).",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {"type": "string"},
      "session_id": {"type": "string"},
      "mode": {"type": "string", "enum": ["default", "atlas", "physics", "forge"]}
    },
    "required": ["query"]
  }
}
```

---

## Tool 5: `asi_empathize` (Stakeholder Analysis)

**Purpose:** Impact analysis, empathy scoring

**MCP Tool Definition:**
```json
{
  "name": "asi_empathize",
  "title": "Stakeholder Impact Analysis",
  "description": "Model human impact and emotional/safety context. Identifies all stakeholders, calculates vulnerability scores, and finds the weakest stakeholder.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "scenario": {"type": "string"},
      "session_id": {"type": "string"}
    },
    "required": ["scenario"]
  }
}
```

---

## Tool 6: `asi_align` (Ethical Alignment)

**Purpose:** Policy check, ethics reconciliation

**MCP Tool Definition:**
```json
{
  "name": "asi_align",
  "title": "Ethical Alignment Check",
  "description": "Reconcile user request with ethics, law, and policy. Checks if the proposed action aligns with constitutional floors and societal norms.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "proposal": {"type": "string"},
      "session_id": {"type": "string"}
    },
    "required": ["proposal"]
  }
}
```

---

## Tool 7: `apex_verdict` (Final Judgment)

**Purpose:** Consensus, final verdict, proof

**MCP Tool Definition:**
```json
{
  "name": "apex_verdict",
  "title": "Final Constitutional Verdict",
  "description": "Synthesize AGI reasoning and ASI safety analysis into a final constitutional verdict. Enforces Tri-Witness consensus (F3).",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {"type": "string"},
      "session_id": {"type": "string"},
      "agi_result": {"type": "object"},
      "asi_result": {"type": "object"}
    },
    "required": ["query"]
  }
}
```

---

## Tool 8: `reality_search` (Fact Checking)

**Purpose:** External grounding via Brave Search

**MCP Tool Definition:**
```json
{
  "name": "reality_search",
  "title": "External Fact-Checking",
  "description": "Query external sources (Brave Search API) for real-time fact-checking and verification. Enforces Humility (F7).",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {"type": "string"},
      "session_id": {"type": "string"},
      "freshness": {"type": "string"}
    },
    "required": ["query"]
  }
}
```

---

## Tool 9: `vault_seal` (Immutable Seal)

**Purpose:** Ledger commitment

**MCP Tool Definition:**
```json
{
  "name": "vault_seal",
  "title": "Immutable Ledger (Seal)",
  "description": "Tamper-proof storage using Merkle-tree sealing. Implements F1 Amanah (Trust).",
  "inputSchema": {
    "type": "object",
    "properties": {
      "action": {"type": "string", "default": "seal"},
      "verdict": {"type": "string"},
      "session_id": {"type": "string"}
    },
    "required": ["action"]
  }
}
```

---

## Legacy Note

The previous 7-tool architecture (using `_ignite_`, `_logic_`, `_forge_`, etc.) is now **deprecated**. The v55.5 system requires the 9 tools listed above for granular control over the cognition cycle.

**DITEMPA BUKAN DIBERI**