---
id: api
title: MCP API Reference (L4 Tools)
sidebar_position: 3
description: JSON-RPC contracts, protocol negotiation, and canonical arifOS AAA MCP tool surface.
---

# MCP API Reference (The "Tools Menu")

If you are building an AI agent or connecting arifOS to an app like Claude Desktop, this page lists the 13 specific tools the AI is allowed to use. 

Unlike a normal API where tools just execute blindly, arifOS exposes a **"governed"** surface using the Model Context Protocol (MCP). This means every time the AI tries to use a tool, arifOS intercepts the request and runs it through the 13 constitutional safety gates before letting the action happen.

## Protocol versioning

- Current protocol: `2025-11-25`
- Supported versions: `2025-11-25`, `2025-03-26`
- Negotiated during `initialize`; one session must use one agreed version.

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-11-25",
    "capabilities": {},
    "clientInfo": {"name": "client", "version": "1.0"}
  }
}
```

## JSON-RPC call shape

```json
{
  "jsonrpc": "2.0",
  "id": 42,
  "method": "tools/call",
  "params": {
    "name": "reason_mind",
    "arguments": {
      "query": "Is this deployment ready?",
      "session_id": "sess_abc"
    }
  }
}
```

## Canonical 13 tools

| Tool | Plain English | Technical Purpose |
|:--|:--|:--|
| `anchor_session` | 🚪 Starts a new session and checks security clearance. | 000 INIT: ignite constitutional session and continuity token. |
| `reason_mind` | 🧠 Asks the AI to logically think through a problem. | 333 REASON: run AGI cognition with grounding and budget controls. |
| `recall_memory` | 📚 Searches past sessions for similar problems. | 444 EVIDENCE: retrieve associative memory traces. |
| `simulate_heart` | ❤️ Checks if a decision will harm any stakeholders. | 555 EMPATHY: evaluate stakeholder impact and care constraints. |
| `critique_thought` | ⚖️ Forces the AI to argue against its own idea to find flaws. | 666 ALIGN: run 7-model critique (inversion, framing, non-linearity). |
| `eureka_forge` | ⚒️ Executes code or material actions in a sandbox. | 777 FORGE: execute action payload behind sovereign control gates. |
| `apex_judge` | 👑 Makes the final pass/fail ruling on whether an action is safe. | 888 APEX: sovereign constitutional verdict synthesis. |
| `seal_vault` | 🔒 Cryptographically saves the decision to an un-editable log. | 999 SEAL: commit immutable session decision record. |
| `search_reality` | 🔍 Searches the web to verify facts. | External evidence discovery (read-only). |
| `fetch_content` | 📄 Reads a specific webpage or document. | Fetch raw evidence content (read-only). |
| `inspect_file` | 📁 Looks at files on your hard drive. | Inspect local filesystem structure and metadata (read-only). |
| `audit_rules` | 📋 Checks the system's own safety rules. | Run constitutional/system rule audit checks (read-only). |
| `check_vital` | 📈 Checks if the server CPU/RAM is healthy. | Read system health telemetry (CPU, memory, IO). |

## Resources and prompt

- Resource: `arifos://aaa/schemas`
- Resource: `arifos://aaa/full-context-pack`
- Prompt: `arifos.prompt.aaa_chain`

## Response envelope

Tool responses include governed fields:

- `verdict`
- `tool`
- `axioms_333`
- `laws_13`
- `telemetry`
- `apex_dials`
- `contrast_engine`
- `motto`
- `data`

Verdict behavior:

*(Curious how these look in practice? [View the live Audit Dashboard](https://arifosmcp-truth-claim.pages.dev/))*

- **✅ `SEAL`** -> Approved (Continue)
- **🟡 `PARTIAL`** -> Approved with warnings
- **⚠️ `SABAR`** -> Blocked temporarily (AI must refine/retry)
- **❌ `VOID`** -> Blocked entirely (Rule violation)
- **🛑 `888_HOLD`** -> Blocked until a human cryptographically signs it
