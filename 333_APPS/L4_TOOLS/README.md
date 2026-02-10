# L4_TOOLS — MCP Tool Layer (v55.5.0)

**Level 4 | 80% Coverage | Production MCP Tools**

> *"13 canonical tools exposing the arifOS Metabolic Loop via MCP."*

---

## 🚀 Quick Start

```powershell
# stdio (Claude, Cursor, Kimi)
python -m aaa_mcp

# SSE (Railway/Remote)
python -m aaa_mcp sse

# HTTP (Streamable HTTP)
python -m aaa_mcp http
```

---

## The 13 Canonical Tools

| # | Tool | Stage | Trinity | Floors | Annotations |
|---|------|-------|---------|--------|-------------|
| 1 | `init_gate` | 000 | Gate | F11, F12 | readOnly:❌ destructive:❌ openWorld:❌ |
| 2 | `forge_pipeline` | 000-999 | All | F1-F13 | readOnly:❌ destructive:✅ openWorld:✅ |
| 3 | `agi_sense` | 111 | Δ Mind | F4 | readOnly:✅ destructive:❌ openWorld:❌ |
| 4 | `agi_think` | 222 | Δ Mind | F2, F4, F7 | readOnly:✅ destructive:❌ openWorld:✅ |
| 5 | `agi_reason` | 333 | Δ Mind | F2, F4, F7, F10 | readOnly:✅ destructive:❌ openWorld:❌ |
| 6 | `asi_empathize` | 555 | Ω Heart | F5, F6, F9 | readOnly:✅ destructive:❌ openWorld:❌ |
| 7 | `asi_align` | 666 | Ω Heart | F5, F6, F9 | readOnly:✅ destructive:❌ openWorld:❌ |
| 8 | `apex_verdict` | 888 | Ψ Soul | F3, F8, F11 | readOnly:❌ destructive:✅ openWorld:❌ |
| 9 | `reality_search` | — | External | F2, F7, F10 | readOnly:✅ destructive:❌ openWorld:✅ |
| 10 | `vault_seal` | 999 | VAULT | F1, F3 | readOnly:❌ destructive:✅ openWorld:❌ |
| 11 | `vault_query` | — | VAULT | F1 | readOnly:✅ destructive:❌ openWorld:❌ |
| 12 | `tool_router` | — | Trinity | F4 | readOnly:✅ destructive:❌ openWorld:❌ |
| 13 | `truth_audit` | 888 | Ψ Soul | F2 | readOnly:✅ destructive:❌ openWorld:❌ |

**Protocol:** MCP 2025-11-25 (Streamable HTTP, SSE, stdio)  
**FastMCP:** 2.0+  
**Auth:** OAuth 2.1

---

## Pipeline Flow

```
000_INIT → 111_AGI → 222_AGI → 333_AGI → 444_SYNC → 555_ASI → 666_ASI → 777_FORGE → 888_APEX → 999_VAULT
   F11/F12      F4         F2/F4/F7   F2/F4/F7/F10           F5/F6/F9   F5/F6/F9              F3/F8/F11   F1/F3
```

**Verdicts:** `SEAL` | `VOID` | `PARTIAL` | `SABAR` | `888_HOLD`

---

## Client Configuration

See [`mcp-configs/`](./mcp-configs/) for copy-paste configs:

| Platform | Config |
|----------|--------|
| Claude Desktop | `mcp-configs/claude/mcp.json` |
| Kimi | `mcp-configs/kimi/mcp.json` |
| Codex | `mcp-configs/codex/mcp.json` |
| Antigravity | `mcp-configs/antigravity/mcp_config.json` |

### Claude Desktop Example
```json
{
  "mcpServers": {
    "aaa-mcp": {
      "command": "python",
      "args": ["-m", "aaa_mcp"],
      "env": {"ARIFOS_MODE": "PROD"}
    }
  }
}
```

---

## Implementation

| Component | Location |
|-----------|----------|
| MCP Server | [`aaa_mcp/server.py`](../../aaa_mcp/server.py) |
| 5-Organs | [`core/organs/`](../../core/organs/) |
| Floors | [`core/shared/floors.py`](../../core/shared/floors.py) |

---

**Version:** v55.5.0  
**Protocol:** MCP 2025-11-25  
**Creed:** DITEMPA BUKAN DIBERI
