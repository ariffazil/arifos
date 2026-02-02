# arifOS MCP Configuration Hub

**Location:** `333_APPS/L4_TOOLS/mcp-configs/`  
**Standard:** Option B (TIER 0-2)  
**Last Updated:** 2026-02-02

---

## 📁 Structure

```
mcp-configs/
├── README.md                          # This file
├── claude/mcp.json                    # Claude Desktop/Code config
├── kimi/mcp.json                      # Kimi CLI config
├── antigravity/mcp_config.json        # Antigravity IDE config
└── codex/config.toml                  # Codex CLI config (TOML format)
```

---

## 🎯 MCP Server Tiers (Option B - Standard)

### TIER 0: arifOS Constitutional Core
| Server | Tools | Purpose |
|--------|-------|---------|
| **aaa-mcp** | 9 canonical tools | arifOS governance (000-999 loop) |

Tools: `init_gate`, `agi_sense`, `agi_think`, `agi_reason`, `asi_empathize`, `asi_align`, `apex_verdict`, `reality_search`, `vault_seal`

### TIER 1: Official Reference Servers
| Server | Source | Functionality |
|--------|--------|---------------|
| **filesystem** | `@modelcontextprotocol/server-filesystem` | Secure file operations |
| **fetch** | `@modelcontextprotocol/server-fetch` | Web content fetching |
| **git** | `mcp-server-git` | Git repository operations |
| **memory** | `@modelcontextprotocol/server-memory` | Knowledge graph memory |
| **sequential-thinking** | `@modelcontextprotocol/server-sequential-thinking` | Reflective problem-solving |
| **time** | `mcp-server-time` | Time/timezone conversion |

### TIER 2: Development Essentials
| Server | Source | Functionality | API Key Required |
|--------|--------|---------------|------------------|
| **sqlite** | `@modelcontextprotocol/server-sqlite` | Database operations | No |
| **github** | `@modelcontextprotocol/server-github` | GitHub API | `GITHUB_TOKEN` |
| **context7** | `@upstash/context7-mcp` | Documentation search | `CONTEXT7_API_KEY` |
| **brave-search** | `@modelcontextprotocol/server-brave-search` | Web search | `BRAVE_API_KEY` |

---

## 🔧 Agent Working Directories

Configs are **deployed to** (working locations):

| Agent | Working Config Path | Format |
|-------|---------------------|--------|
| **Claude** | `.claude/mcp.json` | JSON |
| **Kimi** | `.kimi/mcp.json` | JSON |
| **Antigravity** | `.antigravity/mcp_config.json` | JSON |
| **Codex** | `~/.codex/config.toml` | TOML |

---

## 🔑 Required Environment Variables

Ensure these are set in your Windows environment:

```powershell
# Required for TIER 2 MCP servers
$env:BRAVE_API_KEY          # For brave-search
$env:CONTEXT7_API_KEY       # For context7
$env:GITHUB_TOKEN           # For github

# Optional (for arifOS internal)
$env:DATABASE_URL          # For VAULT999 PostgreSQL
```

---

## 🚀 Verification Commands

### Claude
```bash
# In Claude Code, run:
/mcp
# Should list: aaa-mcp, filesystem, fetch, git, memory, sequential-thinking, time, sqlite, context7, github, brave-search
```

### Kimi
```bash
kimi mcp list
```

### Codex
```bash
codex --list-mcp-servers
```

---

## 📝 Updating Configs

To update all agent configs:

```powershell
# 1. Edit centralized config
notepad 333_APPS/L4_TOOLS/mcp-configs/claude/mcp.json

# 2. Redeploy to agent directories
Copy-Item "333_APPS/L4_TOOLS/mcp-configs/claude/mcp.json" ".claude/mcp.json" -Force
Copy-Item "333_APPS/L4_TOOLS/mcp-configs/kimi/mcp.json" ".kimi/mcp.json" -Force
Copy-Item "333_APPS/L4_TOOLS/mcp-configs/antigravity/mcp_config.json" ".antigravity/mcp_config.json" -Force
Copy-Item "333_APPS/L4_TOOLS/mcp-configs/codex/config.toml" "$env:USERPROFILE/.codex/config.toml" -Force
```

---

## ⚠️ Security Notes

| Server | Risk Level | Mitigation |
|--------|------------|------------|
| filesystem | Medium | Restricted to `C:/Users/User/arifOS` |
| git | Low | Read-only by default |
| sqlite | Low | Project directory only |
| github | Medium | Uses token auth |
| brave-search | Low | Read-only search |

---

## 🏛️ Constitutional Alignment

All MCP servers are routed through arifOS `init_gate` (F12 Injection Defense) before execution. External servers:
- ✅ **F1 Amanah**: Reversible operations (where possible)
- ✅ **F2 Truth**: Direct API calls, verifiable
- ⚠️ **F12 Injection**: Scanned by init_gate

---

**Authority:** Muhammad Arif bin Fazil  
**Motto:** *DITEMPA BUKAN DIBERI — Forged, Not Given*
