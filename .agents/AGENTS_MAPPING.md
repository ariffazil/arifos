# arifOS Agents Mapping

**Purpose:** Quick reference for all agent configurations and their locations  
**Last Updated:** 2026-02-02  
**Canonical Source:** `.agents/`

---

## 🎯 Agent Configuration Matrix

| Agent | Directory | Config File | Format | Status |
|-------|-----------|-------------|--------|--------|
| **arifOS Canon** | `.agents/` | `mcp.json` | JSON | ✅ Master Reference |
| **Claude** | `.claude/` | `mcp.json` | JSON | ✅ Active |
| **Kimi** | `.kimi/` | `mcp.json` | JSON | ✅ Active |
| **Codex** | `~/.codex/` | `config.toml` | TOML | ✅ Active |
| **Antigravity** | `.antigravity/` | `mcp_config.json` | JSON | ✅ Active |
| **Gemini** | `.gemini/` | `mcp.json` | JSON | ⚠️ Limited MCP |

---

## 📁 Directory Structure

```
arifOS/
├── .agents/                    # CANON - Master reference
│   ├── AGENTS_CANON.md         # Full documentation
│   ├── mcp.json                # Canonical MCP config
│   ├── workflows/              # 000-999 standard workflows
│   ├── skills/                 # Reusable skill templates
│   └── adapters/               # Agent-specific guides
│
├── .claude/                    # Claude Desktop/Code
│   └── mcp.json                # ← Copy of .agents/mcp.json
│
├── .kimi/                      # Kimi CLI
│   └── mcp.json                # ← Copy of .agents/mcp.json
│
├── .antigravity/               # Antigravity IDE
│   └── mcp_config.json         # ← Copy of .agents/mcp.json
│
├── .gemini/                    # Gemini (limited)
│   ├── mcp.json                # ← Copy of .agents/mcp.json
│   └── clipboard/              # Image clipboard
│
├── .codex/                     # Codex CLI (if exists)
│   └── (not used - global config)
│
└── 333_APPS/L4_TOOLS/mcp-configs/  # Backup templates
    ├── claude/mcp.json
    ├── kimi/mcp.json
    ├── antigravity/mcp_config.json
    ├── gemini/mcp.json
    └── codex/config.toml
```

---

## 🔄 Synchronization Protocol

When `.agents/mcp.json` is updated, run:

```powershell
# From arifOS root directory
Copy-Item .agents\mcp.json .claude\mcp.json -Force
Copy-Item .agents\mcp.json .kimi\mcp.json -Force
Copy-Item .agents\mcp.json .antigravity\mcp_config.json -Force
Copy-Item .agents\mcp.json .gemini\mcp.json -Force

# Codex requires manual TOML conversion
# See: .agents/adapters/CODEX.md
```

---

## 🔧 MCP Servers Summary (11 Total)

### TIER 0: arifOS Constitutional (1)
| Server | Tools | Description |
|--------|-------|-------------|
| `aaa-mcp` | 9 canonical | arifOS governance (000-999 loop) |

### TIER 1: Official Reference (6)
| Server | Description |
|--------|-------------|
| `filesystem` | Secure file operations |
| `fetch` | Web content fetching |
| `git` | Git repository operations |
| `memory` | Knowledge graph memory |
| `sequential-thinking` | Reflective problem-solving |
| `time` | Time/timezone conversion |

### TIER 2: Development Essentials (4)
| Server | API Key Required |
|--------|------------------|
| `sqlite` | No |
| `context7` | `CONTEXT7_API_KEY` |
| `github` | `GITHUB_TOKEN` |
| `brave-search` | `BRAVE_API_KEY` |

---

## 🔑 Environment Variables

Required in Windows environment:

```powershell
# For TIER 2 MCP servers
$env:CONTEXT7_API_KEY
$env:GITHUB_TOKEN
$env:BRAVE_API_KEY

# For arifOS VAULT999
$env:DATABASE_URL
```

---

## 📚 Documentation Links

- **Full Canon:** `.agents/AGENTS_CANON.md`
- **Adapters:** `.agents/adapters/`
- **Workflows:** `.agents/workflows/`
- **333_APPS/L4_TOOLS:** `333_APPS/L4_TOOLS/mcp-configs/README.md`

---

## ✅ Phase 2 Completion Checklist

- [x] Deleted `agents/` (non-functional duplicate)
- [x] Created `.agents/` (canonical reference)
- [x] Created `.agents/mcp.json` (master config)
- [x] Created `.agents/AGENTS_CANON.md` (documentation)
- [x] Created workflows/ structure
- [x] Created skills/ structure
- [x] Created adapters/ for each agent
- [x] Synchronized configs to all agent directories
- [x] Verified `.claude/mcp.json`
- [x] Verified `.kimi/mcp.json`
- [x] Verified `.antigravity/mcp_config.json`
- [x] Verified `.gemini/mcp.json`
- [x] Verified `~/.codex/config.toml`
- [x] Created AGENTS_MAPPING.md (this file)

---

**Status:** ✅ PHASE 2 COMPLETE

**DITEMPA BUKAN DIBERI — Forged, Not Given**
