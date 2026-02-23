# 9 Canonical MCP Tools (v55.5-EIGEN)

**Purpose:** MCP tool specifications for Claude Code + arifOS integration  
**Principle:** MCP server is a "blind bridge" — all wisdom lives in Core Kernels

---

## Architecture

```
Claude Code → MCP Client → MCP Server → Bridge → Core Kernels → Verdict → VAULT-999
```

---

## Tool Reference

| # | Tool | Role | Stages | Floors |
|---|------|------|--------|--------|
| 1 | `init_gate` | Gate | 000 | F11, F12 |
| 2 | `agi_sense` | Mind | 111 | F12 |
| 3 | `agi_think` | Mind | 222 | F4 |
| 4 | `agi_reason` | Mind | 333 | F2, F4, F7, F10 |
| 5 | `asi_empathize` | Heart | 555 | F5, F6, F9 |
| 6 | `asi_align` | Heart | 666 | F9 |
| 7 | `apex_verdict` | Soul | 888 | F3, F8, F11 |
| 8 | `reality_search` | Ground | External | F7, F10 |
| 9 | `vault_seal` | Seal | 999 | F1 |

---

## Tool Definitions

### 1. `init_gate` — Session Initialization
```json
{
  "name": "init_gate",
  "description": "Initialize governed session. Verify authority, scan for injection (F12).",
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

### 2. `agi_sense` — Intent Detection
```json
{
  "name": "agi_sense",
  "description": "Parse input, detect intent, classify into lanes (HARD/SOFT/PHATIC).",
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

### 3. `agi_think` — Hypothesis Generation
```json
{
  "name": "agi_think",
  "description": "Generate multiple hypotheses without commitment.",
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

### 4. `agi_reason` — Deep Reasoning
```json
{
  "name": "agi_reason",
  "description": "Logical reasoning with step-by-step chain. Enforces F2 Truth, F4 Clarity.",
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

### 5. `asi_empathize` — Stakeholder Analysis
```json
{
  "name": "asi_empathize",
  "description": "Model human impact. Identify stakeholders, calculate vulnerability scores.",
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

### 6. `asi_align` — Ethical Alignment
```json
{
  "name": "asi_align",
  "description": "Reconcile request with ethics, law, policy. Check constitutional alignment.",
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

### 7. `apex_verdict` — Final Judgment
```json
{
  "name": "apex_verdict",
  "description": "Synthesize AGI + ASI into final verdict. Enforces F3 Tri-Witness consensus.",
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

### 8. `reality_search` — Fact Checking
```json
{
  "name": "reality_search",
  "description": "External grounding via Brave Search. Enforces F7 Humility.",
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

### 9. `vault_seal` — Immutable Seal
```json
{
  "name": "vault_seal",
  "description": "Merkle-tree sealing for tamper-proof storage. Implements F1 Amanah.",
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

**Note:** Legacy `_ignite_`, `_logic_`, `_forge_` names are deprecated. Use snake_case tools above.

**DITEMPA BUKAN DIBERI**
