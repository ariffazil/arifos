---
name: mcp-protocol
description: 14 canonical MCP tools — response envelopes, transport adapters, tool registry
---

# MCP Protocol

## Scope
14 canonical MCP tools: transport layer, response envelopes, protocol contracts, and FastMCP integration.

## Constitutional Alignment
- **F12 Injection**: Risk < 0.85 (Prompt injection defense)
- **F11 CommandAuth**: LOCKED (Tool access verification)
- **F4 Clarity**: ΔS ≤ 0 (Response structure)

## Key Components
- `aaa_mcp/server.py` — 14 canonical tools with `@mcp.tool()` decorators
- `aaa_mcp/protocol/` — Response schemas and contracts
- `aaa_mcp/sessions/` — Session management
- `arifos_aaa_mcp/server.py` — Public server factory

## 14 Canonical Tools
| # | Tool | Stage | Description |
|---|------|-------|-------------|
| 1 | `arifos-aaa_anchor_session` | 000/111 | Session initialization |
| 2 | `arifos-aaa_reason_mind` | 333 | AGI reasoning |
| 3 | `arifos-aaa_recall_memory` | 444 | Memory evidence |
| 4 | `arifos-aaa_simulate_heart` | 555 | Empathy simulation |
| 5 | `arifos-aaa_critique_thought` | 666 | 7-model critique |
| 6 | `arifos-aaa_eureka_forge` | 777 | Shell execution |
| 7 | `arifos-aaa_apex_judge` | 888 | Verdict synthesis |
| 8 | `arifos-aaa_seal_vault` | 999 | Immutable seal |
| 9 | `arifos-aaa_search_reality` | — | External evidence |
| 10 | `arifos-aaa_fetch_content` | — | Content retrieval |
| 11 | `arifos-aaa_inspect_file` | — | File inspection |
| 12 | `arifos-aaa_audit_rules` | — | Rule checking |
| 13 | `arifos-aaa_check_vital` | — | Health telemetry |
| 14 | `arifos-aaa_list_prompts` | — | Prompt registry |

## Response Envelope
```python
{
    "verdict": "SEAL" | "PARTIAL" | "SABAR" | "VOID" | "888_HOLD",
    "stage": "000_INIT" | "111-444" | "555-666" | "777-888" | "999_VAULT",
    "session_id": str,
    "floors": {"passed": [], "failed": []},
    "truth": {"score": float, "threshold": float, "drivers": []},
    "next_actions": [],
    "payload": {...}
}
```

## Operational Rules
**Trigger When:**
- Any MCP tool execution needed
- Response envelope validation required
- Protocol conformance testing

**Allowed Operations:**
- Tool registration and discovery
- Response envelope generation
- Session lifecycle management

**888_HOLD Required:**
- Tool registry modification
- Response envelope bypass
- Injection risk override (F12)

## Quick Reference
```bash
# Run MCP server
python -m arifos_aaa_mcp
python -m arifos_aaa_mcp sse
python -m arifos_aaa_mcp stdio
```

## Verification
```bash
python -c "from aaa_mcp.server import create_aaa_mcp_server; print('MCP server factory ready')"
```
