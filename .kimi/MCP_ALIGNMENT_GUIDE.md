# arifOS Kimi CLI MCP Configuration Guide

> **T000 Version:** 2026.02.15-FORGE-TRINITY-SEAL  
> **Code Version:** 2026.02.15-FORGE-TRINITY-SEAL  
> **Last Updated:** 2026-02-15  
> **Motto:** *DITEMPA BUKAN DIBERI* 💎🔥🧠

---

## 📋 Overview

This guide documents the MCP server architecture for both **Kimi CLI** and **Claude Code** in arifOS, using a **Global + Project split** to eliminate duplication. Generic MCPs live in global config; project-specific MCPs (aaa-mcp, filesystem, git, memory) live in project config.

---

## 🏛️ Constitutional Architecture

### The Trinity: 9 Canonical Tools + 3 Core External MCPs

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         arifOS MCP ECOSYSTEM                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  LAYER 1: GOVERNANCE (Constitutional - 9 Tools)                             │
│  ═══════════════════════════════════════════════                            │
│                                                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ init_gate   │ │ agi_sense   │ │ agi_think   │ │ agi_reason  │           │
│  │ (000_INIT)  │ │ (Δ Stage 1) │ │ (Δ Stage 2) │ │ (Δ Stage 3) │           │
│  │ F11, F12    │ │ F2, F4      │ │ F2, F4, F7  │ │ F2, F4, F7  │           │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘           │
│                                                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ asi_empath  │ │ asi_align   │ │ apex_verdict│ │ vault_seal  │           │
│  │ (Ω Stage 1) │ │ (Ω Stage 2) │ │ (Ψ Stage)   │ │ (999_VAULT) │           │
│  │ F5, F6      │ │ F5, F6, F9  │ │ F3, F5, F8  │ │ F1, F3      │           │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘           │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │ reality_search (Auxiliary)                                       │       │
│  │ F2, F7 - External fact-checking via Brave/DuckDuckGo             │       │
│  └─────────────────────────────────────────────────────────────────┘       │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  LAYER 2: EXECUTION (3 Core External MCPs)                                  │
│  ═════════════════════════════════════════                                  │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │   filesystem    │  │      git        │  │     memory      │             │
│  │  (@modelcontext │  │  (uvx mcp-      │  │  (@modelcontext │             │
│  │   /server-fs)   │  │   server-git)   │  │   /server-mem)  │             │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤             │
│  │   F1 Amanah     │  │   F2 Truth      │  │   F8 Wisdom     │             │
│  │   F6 Clarity    │  │   F3 Tri-Witness│  │   F5 Peace²     │             │
│  │   F11 Sovereign │  │   F7 Humility   │  │   F3 Tri-Witness│             │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘             │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  LAYER 3: AUXILIARY (4 Support MCPs)                                        │
│  ═══════════════════════════════════                                        │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐                                   │
│  │   perplexity    │  │  sequential-    │                                   │
│  │  (@perplexity-  │  │   thinking      │                                   │
│  │   ai/mcp-srv)   │  │  (@modelcontext │                                   │
│  ├─────────────────┤  │   /server-st)   │                                   │
│  │   F2 Truth      │  ├─────────────────┤                                   │
│  │   (Reality +)   │  │   F8 Wisdom     │                                   │
│  └─────────────────┘  │   (Reasoning +) │                                   │
│                       └─────────────────┘                                   │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐                                   │
│  │     fetch       │  │      time       │                                   │
│  │  (uvx mcp-     │  │  (uvx mcp-      │                                   │
│  │   server-fetch) │  │   server-time)  │                                   │
│  ├─────────────────┤  ├─────────────────┤                                   │
│  │   F2 Truth      │  │   F2 Truth      │                                   │
│  │   (Web content) │  │   (Temporal)    │                                   │
│  └─────────────────┘  └─────────────────┘                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔗 Alignment Matrix: 3 Core MCPs × 9 Canonical Tools

### 1️⃣ Filesystem MCP → Aligns with `vault_seal` + `init_gate`

| Aspect | Details |
|--------|---------|
| **Constitutional Floors** | **F1 Amanah** (reversible file ops), **F6 Clarity** (organized structure), **F11 Sovereignty** (access controls) |
| **aaa_mcp Alignment** | `vault_seal` (immutable ledger persistence) + `init_gate` (session initialization) |
| **Pipeline Position** | 000_INIT → File Operations → 999_VAULT |
| **Key Tools** | `read_file`, `write_file`, `edit_file`, `list_directory`, `search_files` |

**Why Critical:**
- Provides the "hands" for code manipulation while maintaining **F1 Amanah** (all file operations are tracked and reversible)
- Enables structured codebase navigation (**F6 Clarity**)
- Configurable access controls respect **F11 Sovereignty**

---

### 2️⃣ Git MCP → Aligns with `reality_search` + `agi_reason`

| Aspect | Details |
|--------|---------|
| **Constitutional Floors** | **F2 Truth** (commit history as evidence), **F3 Tri-Witness** (consensus via git), **F7 Humility** (track uncertainty) |
| **aaa_mcp Alignment** | `reality_search` (evidence verification) + `agi_reason` (logical analysis) |
| **Pipeline Position** | AGI Stage 3 (reasoning) + Auxiliary (reality grounding) |
| **Key Tools** | `git_status`, `git_diff`, `git_log`, `git_branch`, `git_commit` |

**Why Critical:**
- Git history serves as **F2 Truth** evidence chain
- Branching enables safe experimentation (**F1 Amanah** reversibility)
- Commit consensus = Human × AI × System (**F3 Tri-Witness**)

---

### 3️⃣ Memory MCP → Aligns with `agi_think` + `vault_seal`

| Aspect | Details |
|--------|---------|
| **Constitutional Floors** | **F8 Wisdom** (pattern storage), **F5 Peace²** (entropy reduction), **F3 Tri-Witness** (persistent facts) |
| **aaa_mcp Alignment** | `agi_think` (hypothesis generation) + `vault_seal` (immutable storage) |
| **Pipeline Position** | AGI Stage 2 → Knowledge Graph → 999_VAULT |
| **Key Tools** | `create_entities`, `create_relations`, `search_nodes`, `read_graph` |

**Why Critical:**
- Knowledge graph extends **VAULT999** with queryable structure
- Pattern recognition enables **F8 Wisdom** accumulation
- Long-term memory reduces cognitive entropy (**F5 Peace²**)

---

## 🔄 Complete Pipeline Flow

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         FULL METABOLIC LOOP (000-999)                        │
└──────────────────────────────────────────────────────────────────────────────┘

000_INIT
    │
    ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  filesystem │◄──►│  init_gate  │◄──►│     git     │
│  (F1, F6)   │    │ (F11, F12)  │    │  (F2, F3)   │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                           ▼
111_SENSE ◄───────┐   ┌─────────────┐
(F2, F4)          └──►│  agi_sense  │
                      └─────────────┘
                           │
                           ▼
222_THINK ◄───────┐   ┌─────────────┐    ┌─────────────┐
(F2, F4, F7)      └──►│  agi_think  │◄──►│   memory    │
                      └─────────────┘    │  (F8, F5)   │
                           │             └─────────────┘
                           ▼
333_REASON ◄──────┐   ┌─────────────┐    ┌─────────────┐
(F2, F4, F7)      └──►│  agi_reason │◄──►│     git     │
                      └─────────────┘    │  (F2, F7)   │
                           │             └─────────────┘
                           ▼
444_TRINITY ──────►   ┌─────────────┐
                      │ asi_empath  │
                      │  (F5, F6)   │
                      └─────────────┘
                           │
                           ▼
555_ALIGN ────────►   ┌─────────────┐
                      │  asi_align  │
                      │ (F5, F6, F9)│
                      └─────────────┘
                           │
                           ▼
777_EUREKA ◄──────┐   ┌─────────────────┐
                  └──►│ sequential-think│
                      │    (F8, F7)     │
                      └─────────────────┘
                           │
                           ▼
888_APEX ─────────►   ┌─────────────┐
                      │ apex_verdict│
                      │(F3, F5, F8) │
                      └─────────────┘
                           │
                           ▼
999_VAULT ◄───────┐   ┌─────────────┐    ┌─────────────┐
(F1, F3)          └──►│  vault_seal │◄──►│  filesystem │
                      │             │    │   memory    │
                      └─────────────┘    └─────────────┘

AUXILIARY (Reality Grounding):
┌─────────────┐    ┌─────────────┐
│   perplexity│◄──►│reality_search│
│   (F2, F7)  │    │  (F2, F7)   │
└─────────────┘    └─────────────┘
```

---

## 📁 Configuration Files (Global + Project Split)

### Architecture
```
GLOBAL (generic MCPs for all projects):
  ~/.mcp.json          — Claude Code / Cursor
  ~/.kimi/mcp.json     — Kimi CLI

PROJECT (project-specific MCPs only):
  arifOS/.mcp.json     — Claude Code / Cursor (aaa-mcp, filesystem, git, memory)
  arifOS/.kimi/mcp.json — Kimi CLI (aaa-mcp, filesystem, git, memory)
```

### What goes where?
| MCP | Where | Why |
|-----|-------|-----|
| aaa-mcp | **Project** | Needs arifOS cwd + venv |
| filesystem | **Project** | Scoped to arifOS path |
| git | **Project** | Needs arifOS cwd |
| memory | **Project** | Custom MEMORY_FILE_PATH |
| fetch, time | **Global** | Python (uvx), generic |
| brave-search, github, context7 | **Global** | Generic, no project deps |
| perplexity, sequential-thinking | **Global** | Generic, no project deps |
| puppeteer, playwright | **Global** | Generic browser tools |

---

## 🛠️ Installation Commands

### Prerequisites
```bash
# Ensure Node.js is installed (for npx-based MCPs: filesystem, memory, sequential-thinking, perplexity)
node --version  # >= 18.0.0

# Ensure uv is installed (for uvx-based MCPs: git, fetch, time)
# IMPORTANT: fetch and time are Python packages — do NOT use npx for them
uv --version
```

### Kimi CLI Registration
```bash
# Navigate to arifOS directory
cd C:\Users\User\arifOS

# Register aaa-mcp (Constitutional Core)
kimi mcp add --transport stdio aaa-mcp -- \
  C:\Users\User\arifOS\.venv\Scripts\python.exe -m aaa_mcp stdio

# Register filesystem (F1 Amanah)
kimi mcp add --transport stdio filesystem -- \
  npx -y @modelcontextprotocol/server-filesystem C:/Users/User/arifOS

# Register git (F2 Truth)
kimi mcp add --transport stdio git -- uvx mcp-server-git

# Register memory (F8 Wisdom)
kimi mcp add --transport stdio memory -- \
  npx -y @modelcontextprotocol/server-memory

# Register fetch (F2 Truth - Web Content)
# NOTE: Python package, use uvx NOT npx
kimi mcp add --transport stdio fetch -- uvx mcp-server-fetch

# Register time (F2 Truth - Temporal)
# NOTE: Python package, use uvx NOT npx
kimi mcp add --transport stdio time -- uvx mcp-server-time

# Verify all servers
kimi mcp list

# Inside Kimi, view loaded tools
/mcp
```

---

## 🔐 Environment Variables

Create `.env` file or set system-wide:

```bash
# Required for aaa-mcp
ARIFOS_CONSTITUTIONAL_MODE=AAA
BRAVE_API_KEY=your_brave_api_key_here
BROWSERBASE_API_KEY=your_browserbase_key_here

# Required for perplexity
PERPLEXITY_API_KEY=your_perplexity_key_here
PERPLEXITY_TIMEOUT_MS=300000

# Optional: Memory file location
MEMORY_FILE_PATH=C:/Users/User/arifOS/.kimi/memory.json
```

---

## ✅ Verification Checklist

### Project MCPs (arifOS/.mcp.json + arifOS/.kimi/mcp.json)
- [ ] `aaa-mcp` responds to all 9 canonical tools
- [ ] `filesystem` can read/write files in arifOS directory
- [ ] `git` can execute git commands in arifOS repo
- [ ] `memory` can create/search knowledge graph with custom path

### Global MCPs (~/.mcp.json + ~/.kimi/mcp.json)
- [ ] `fetch` works (uvx mcp-server-fetch — Python, NOT npx)
- [ ] `time` works (uvx mcp-server-time — Python, NOT npx)
- [ ] `brave-search` can search web (needs BRAVE_API_KEY)
- [ ] `github` can access repos (needs GITHUB_TOKEN)
- [ ] `context7` can query docs (needs CONTEXT7_API_KEY)
- [ ] `perplexity` can search (needs PERPLEXITY_API_KEY)
- [ ] `sequential-thinking` can reason
- [ ] `puppeteer` can automate browser
- [ ] `playwright` can automate browser

### Governance
- [ ] All MCPs follow F1 Amanah (reversible operations)
- [ ] All MCPs respect F11 Sovereignty (user approval for sensitive ops)

---

## 📚 References

| Resource | Location |
|----------|----------|
| AGENTS.md | `C:\Users\User\arifOS\AGENTS.md` |
| MCP Spec | `https://modelcontextprotocol.io` |
| Kimi CLI Docs | `https://moonshotai.github.io/kimi-cli` |
| arifOS Theory | `C:\Users\User\arifOS\000_THEORY\` |
| VAULT999 | `C:\Users\User\arifOS\VAULT999\` |

---

*DITEMPA BUKAN DIBERI* — Forged, Not Given 💎🔥🧠
