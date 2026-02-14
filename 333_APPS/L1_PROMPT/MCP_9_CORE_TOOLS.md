# 5 Canonical MCP Tools (v64.1-GAGI)

**Purpose:** MCP tool specifications for Claude Code + arifOS integration  
**Principle:** MCP server is a "blind bridge" — all wisdom lives in Core Kernels

---

## Architecture

```
Claude Code → MCP Client → MCP Server → Core Organs → Verdict → VAULT-999
```

---

## Tool Reference

| # | Tool | Role | Stages | Floors |
|---|------|------|--------|--------|
| 1 | `init_session` | Gate | 000 | F11, F12 |
| 2 | `agi_cognition` | Mind | 111-333 | F2, F4, F7, F8, F10 |
| 3 | `asi_empathy` | Heart | 444-666 | F1, F5, F6, F9 |
| 4 | `apex_verdict` | Soul | 888 | F2, F3, F8, F10-F13 |
| 5 | `vault_seal` | Seal | 999 | F1, F3 |

---

## Tool Definitions

### 1. `init_session` — Session Initialization (000)
```json
{
  "name": "init_session",
  "description": "000_INIT - Session ignition. Verify authority, scan for injection (F11, F12).",
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

### 2. `agi_cognition` — Mind Pipeline (111-333)
```json
{
  "name": "agi_cognition",
  "description": "111-333_AGI - The Mind. Sense → Think → Reason pipeline. Enforces F2, F4, F7, F8, F10.",
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

### 3. `asi_empathy` — Heart Pipeline (444-666)
```json
{
  "name": "asi_empathy",
  "description": "444-666_ASI - The Heart. Empathize → Align pipeline. Enforces F1, F5, F6, F9.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {"type": "string"},
      "session_id": {"type": "string"},
      "context": {"type": "object"}
    },
    "required": ["query"]
  }
}
```

### 4. `apex_verdict` — Soul Judgment (888)
```json
{
  "name": "apex_verdict",
  "description": "666-888_APEX - The Judge. Final constitutional judgment. Enforces F2, F3, F8, F10-F13.",
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

### 5. `vault_seal` — Immutable Seal (999)
```json
{
  "name": "vault_seal",
  "description": "999_VAULT - Immutable Record. Merkle-tree sealing for tamper-proof storage. Implements F1, F3.",
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

**Note:** v64.1 consolidates tools into 5 canonical entry points. Internal stages run sequentially within each tool.

**DITEMPA BUKAN DIBERI**
