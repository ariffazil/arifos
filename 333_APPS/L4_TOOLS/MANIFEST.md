# L4_TOOLS — MCP Deployment Manifest (v55.5-HARDENED)

**Location:** `333_APPS/L4_TOOLS/`
**Canonical Source:** `aaa_mcp/`
**Status:** 🟢 LIVE (Production)

---

## 📁 Directory Structure

```
L4_TOOLS/
├── README.md                    # Layer documentation
├── MANIFEST.md                  # This file — deployment guide
│
└── mcp-configs/                 # Platform-specific configurations
    ├── antigravity/             # Gemini/Antigravity
    ├── claude/                  # Claude Desktop
    ├── codex/                   # OpenAI Codex
    └── kimi/                    # Kimi AI
```

> **Note:** The actual code implementation lives in `aaa_mcp/` at the project root. This directory contains only documentation and configuration.

---

## 🔧 The 9 Canonical Tools (v55.5)

| Tool | Stage | Role | Floors Enforced | Status |
|------|-------|------|-----------------|--------|
| `init_gate` | 000 | Gate | F11, F12 | ✅ Production |
| `agi_sense` | 111 | Mind | F12 | ✅ Production |
| `agi_think` | 222 | Mind | F4 | ✅ Production |
| `agi_reason` | 333 | Mind | F2, F4, F7, F10 | ✅ Production |
| `asi_empathize` | 555 | Heart | F5, F6, F9 | ✅ Production |
| `asi_align` | 666 | Heart | F9 | ✅ Production |
| `apex_verdict` | 888 | Soul | F3, F8, F11 | ✅ Production |
| `reality_search`| — | Ground | F7, F10 | ✅ Production |
| `vault_seal` | 999 | Seal | F1 | ✅ Production |

---

### Deployment Options

### Option 1: Standard Production (Recommended)
```powershell
# Updates dependencies and runs server
pip install -e ".[dev]"
python -m aaa_mcp
```

### Option 2: SSE Transport (Remote/Railway)
```powershell
# Runs server on port 8000 (default)
python -m aaa_mcp sse
```

---

## 📋 Client Configuration

### Claude Desktop
**File:** `%APPDATA%\Claude\claude_desktop_config.json`
```json
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "aaa_mcp"],
      "env": {
        "ARIFOS_HOME": "C:\\Users\\User\\arifOS",
        "ARIFOS_MODE": "PROD"
      }
    }
  }
}
```

### Cursor
**File:** `.cursor/mcp.json`
```json
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "aaa_mcp"]
    }
  }
}
```

---

## 🛡️ Constitutional Enforcement

All tools bind to the Core Kernels (`codebase.agi`, `codebase.asi`, `codebase.apex`) which implement the **13 Constitutional Floors**.

- **Hard Floors (VOID):** F1, F2, F10, F11, F12
- **Soft Floors (SABAR):** F3, F4, F5, F6, F7, F8, F9, F13

---

## 👑 Authority

**Sovereign:** Muhammad Arif bin Fazil
**Version:** v55.5-HARDENED
**Creed:** DITEMPA BUKAN DIBERI
