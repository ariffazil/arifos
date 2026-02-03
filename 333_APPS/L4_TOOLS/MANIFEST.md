# L4_TOOLS — MCP Production Deployment Manifest

**Location:** `333_APPS/L4_TOOLS/`  
**Canonical Source:** `codebase/mcp/`  
**Status:** 🟢 LIVE at https://arif-fazil.com

---

## 📁 Directory Structure

```
L4_TOOLS/
├── README.md                    # Layer documentation
├── MANIFEST.md                  # This file — deployment guide
└── mcp/                         # MCP server implementation
    ├── __init__.py              # Package initialization
    ├── __main__.py              # CLI entry point
    ├── server.py                # Main MCP server (stdio)
    ├── sse.py                   # SSE transport server
    ├── models.py                # Pydantic models/schemas
    ├── bridge.py                # Constitutional bridge
    ├── mcp_config.json          # Tool schemas & config
    ├── HUMAN_GUIDE.md           # Human usage guide
    └── tools/                   # 7 Canonical Tools
        ├── __init__.py
        ├── canonical_trinity.py # Core 7 tools (_init_, _agi_, etc.)
        ├── agi_tool.py          # AGI (Mind) tool implementation
        ├── asi_tool.py          # ASI (Heart) tool implementation
        ├── apex_tool.py         # APEX (Soul) tool implementation
        ├── vault_tool.py        # VAULT (Seal) tool implementation
        └── mcp_tools_v53.py     # Legacy tool implementations
```

---

## 🔧 The 7 Canonical Tools

| Tool | File | Stage | Floors Enforced | Status |
|------|------|-------|-----------------|--------|
| `_init_` | `canonical_trinity.py` | 000 | F11, F12 | ✅ Production |
| `_agi_` | `agi_tool.py` | 111-333 | F2, F4, F7 | ✅ Production |
| `_asi_` | `asi_tool.py` | 444-666 | F1, F5, F6 | ✅ Production |
| `_apex_` | `apex_tool.py` | 777-888 | F3, F8, F9 | ✅ Production |
| `_vault_` | `vault_tool.py` | 999 | F1 | ✅ Production |
| `_trinity_` | `canonical_trinity.py` | Full cycle | All | ✅ Production |
| `_reality_` | `canonical_trinity.py` | External | F7 | ✅ Production |

---

## 🚀 Deployment Options

### Option 1: Direct from codebase/ (Recommended)
```bash
# Production deployment uses canonical source
python -m mcp
# or
python -m mcp --transport sse
```

### Option 2: From 333_APPS/L4_TOOLS/ (Mirror)
```bash
# This directory is a mirror for documentation completeness
python -m 333_APPS.L4_TOOLS.mcp
```

---

## 🔗 Live Deployment

| Endpoint | URL | Status |
|----------|-----|--------|
| Health Check | `https://arif-fazil.com/health` | 🟢 Online |
| MCP SSE | `https://arif-fazil.com/mcp` | 🟢 Online |
| Dashboard | `https://arif-fazil.com/dashboard` | 🟢 Online |

---

## 📋 Client Configuration

### Claude Desktop (`claude_desktop_config.json`)
```json
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "mcp", "--transport", "stdio"],
      "env": {
        "ARIFOS_HOME": "~/.arifos",
        "ARIFOS_MODE": "PROD"
      }
    }
  }
}
```

### Cursor (`.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "mcp"],
      "env": {
        "ARIFOS_MODE": "PROD"
      }
    }
  }
}
```

---

## 🛡️ Constitutional Enforcement

All tools enforce the 13 Constitutional Floors:

```python
# From canonical_trinity.py
FLOORS_ENFORCED = {
    "_init_": ["F11", "F12"],           # Auth + Injection
    "_agi_": ["F2", "F4", "F7"],        # Truth + Clarity + Humility
    "_asi_": ["F1", "F5", "F6"],        # Amanah + Peace + Empathy
    "_apex_": ["F3", "F8", "F9"],       # Tri-Witness + Genius + Anti-Hantu
    "_vault_": ["F1"],                   # Amanah (audit trail)
    "_trinity_": ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "F13"]
}
```

---

## 📊 Version History

| Version | Date | Changes |
|---------|------|---------|
| v53.0 | 2024-Q4 | Initial MCP implementation |
| v53.5 | 2024-Q4 | Added SSE transport |
| v54.0 | 2025-Q1 | Hardened enforcement |
| v54.1 | 2025-Q1 | Production deployment |
| v55.0 | 2026-Q1 | Universal MCP (planned) |

---

## 🔗 Related Documentation

- [L4_TOOLS README](./README.md) — Layer overview
- [codebase/mcp/](../../codebase/mcp/) — Canonical source
- [000_THEORY/](../../000_THEORY/) — Constitutional theory
- [HUMAN_GUIDE.md](./mcp/HUMAN_GUIDE.md) — User guide

---

## 👑 Authority

**Sovereign:** Muhammad Arif bin Fazil  
**Version:** v54.1-SEAL  
**Live:** [arif-fazil.com](https://arif-fazil.com)  
**Creed:** DITEMPA BUKAN DIBERI
