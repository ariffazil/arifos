# arifOS AGENTS CANON
**T000 Version:** 2026.02.15-FORGE-TRINITY-SEAL  
**Code Version:** v64.2-GAGI  
**Location:** `.agents/`  
**Purpose:** Master reference and role model for all arifOS agent configurations  
**Authority:** Muhammad Arif bin Fazil (888 Judge)

---

## 🎯 What is AGENTS CANON?

The `.agents/` directory is the **single source of truth** for arifOS agent configuration. It defines the standard that all agent-specific configurations (`.claude/`, `.kimi/`, `.codex/`, etc.) should follow.

> **"DITEMPA BUKAN DIBERI"** — Forged, Not Given

---

## 📁 Directory Structure

```
.agents/
├── AGENTS_CANON.md          # This file - the canonical reference
├── mcp.json                 # Master MCP configuration (TIER 0-3)
├── workflows/               # Standard agent workflows (000-999)
│   ├── 000_init.md
│   ├── 111_sense.md
│   ├── 222_think.md
│   ├── 333_reason.md
│   ├── 444_evidence.md
│   ├── 555_empathy.md
│   ├── 666_align.md
│   ├── 777_forge.md
│   ├── 888_judge.md
│   └── 999_seal.md
├── skills/                  # Reusable skill templates
│   ├── core-arifos/
│   │   ├── arifos-orchestration/
│   │   ├── governance-audit/
│   │   ├── injection-defense/
│   │   ├── thermo-planning/
│   │   └── truth-logging/
│   └── README.md
└── adapters/                # Agent-specific adapters
    ├── CLAUDE.md
    ├── CODEX.md
    ├── KIMI.md
    └── GEMINI.md
```

---

## 🔧 MCP Configuration Standard

### TIER 0: arifOS Constitutional Core (MANDATORY)

| Server | Tools | F1-F13 Compliance |
|--------|-------|-------------------|
| **aaa-mcp** | 9 canonical tools | Full constitutional enforcement |

**9 Canonical Tools:**
1. `init_gate` - Session ignition + F12 injection scan
2. `agi_sense` - Intent classification
3. `agi_think` - Hypothesis generation
4. `agi_reason` - Deep logical reasoning
5. `asi_empathize` - Stakeholder impact analysis
6. `asi_align` - Ethics/law/policy reconciliation
7. `apex_verdict` - Final constitutional judgment
8. `reality_search` - External fact-checking
9. `vault_seal` - Cryptographic sealing

### TIER 1: Official Reference Servers (MANDATORY)

| Server | Purpose | Source |
|--------|---------|--------|
| **filesystem** | Secure file operations | `@modelcontextprotocol/server-filesystem` |
| **fetch** | Web content fetching | `@modelcontextprotocol/server-fetch` |
| **git** | Git repository operations | `mcp-server-git` |
| **memory** | Knowledge graph memory | `@modelcontextprotocol/server-memory` |
| **sequential-thinking** | Reflective problem-solving | `@modelcontextprotocol/server-sequential-thinking` |
| **time** | Time/timezone conversion | `mcp-server-time` |

### TIER 2: Development Essentials (RECOMMENDED)

| Server | Purpose | API Key Required |
|--------|---------|------------------|
| **sqlite** | Database operations | No |
| **context7** | Documentation search | `CONTEXT7_API_KEY` |
| **github** | GitHub API integration | `GITHUB_TOKEN` |
| **brave-search** | Web search | `BRAVE_API_KEY` |

---

## 🎭 Agent-Specific Adaptations

Each agent implementation should copy from `.agents/mcp.json` and adapt:

### Claude (`.claude/mcp.json`)
```json
{
  "mcpServers": {
    "aaa-mcp": { /* Copy from .agents/mcp.json */ },
    "filesystem": { /* Copy from .agents/mcp.json */ }
    /* ... all TIER 0-2 servers ... */
  }
}
```

### Kimi (`.kimi/mcp.json`)
- Same structure as Claude (JSON format)
- Copy all TIER 0-2 servers from `.agents/mcp.json`

### Codex (`~/.codex/config.toml`)
```toml
[features]
shell_tool = false

[mcp_servers.aaa-mcp]
# Copy configuration from .agents/mcp.json, convert to TOML
command = "..."
args = ["..."]
env = { ... }
```

---

## 🔑 Required Environment Variables

All agents must have access to:

```powershell
# Windows Environment Variables
$env:CONTEXT7_API_KEY       # For context7 MCP server
$env:GITHUB_TOKEN           # For github MCP server  
$env:BRAVE_API_KEY          # For brave-search MCP server
$env:DATABASE_URL          # For arifOS VAULT999 PostgreSQL
```

---

## 📋 Constitutional Compliance (F1-F13)

Every agent configuration MUST respect:

| Floor | Principle | MCP Implication |
|-------|-----------|-----------------|
| **F1** | Amanah (Reversibility) | filesystem, git can mutate - use with care |
| **F2** | Truth (τ ≥ 0.99) | reality_search, context7 for verification |
| **F3** | Tri-Witness (W₃ ≥ 0.95) | Combine aaa-mcp + external sources |
| **F4** | Clarity (ΔS ≤ 0) | sequential-thinking for structured reasoning |
| **F5** | Peace (P ≥ 1.0) | asi_empathize for impact analysis |
| **F6** | Empathy (κᵣ ≥ 0.70) | asi_empathize for stakeholder consideration |
| **F7** | Humility (Ω₀ ∈ [0.03,0.05]) | reality_search for external grounding |
| **F8** | Genius (G ≥ 0.80) | All tools serve governed intelligence |
| **F9** | Anti-Hantu (C_dark < 0.30) | init_gate F12 injection defense |
| **F10** | Ontology | aaa-mcp ontology validation |
| **F11** | Command Auth | vault_seal for audit trail |
| **F12** | Injection (I < 0.85) | init_gate injection scanning |
| **F13** | Sovereign | Human veto through 888_HOLD |

---

## 🚀 Quick Start for New Agents

### Step 1: Copy Canon Config
```powershell
# Create new agent directory
mkdir .newagent

# Copy canonical MCP config
Copy-Item .agents/mcp.json .newagent/mcp.json
```

### Step 2: Adapt if Needed
- Modify `cwd` paths if different working directory
- Adjust `alwaysAllow` based on agent capabilities
- Add agent-specific environment variables

### Step 3: Verify
```bash
# Test arifOS constitutional tools
init_gate -> agi_sense -> agi_reason -> apex_verdict -> vault_seal

# Test external MCP servers
filesystem, fetch, git, memory, time
```

---

## 🔄 Synchronization Protocol

When `.agents/mcp.json` is updated:

1. **All agent configs must be updated**
2. **Changes should be propagated to:**
   - `.claude/mcp.json`
   - `.kimi/mcp.json`
   - `.antigravity/mcp_config.json`
   - `.gemini/mcp.json`
   - `~/.codex/config.toml`
   - `333_APPS/L4_TOOLS/mcp-configs/*/`

3. **Update command:**
```powershell
# From arifOS root
Copy-Item .agents/mcp.json .claude/mcp.json
Copy-Item .agents/mcp.json .kimi/mcp.json
Copy-Item .agents/mcp.json .antigravity/mcp_config.json
Copy-Item .agents/mcp.json .gemini/mcp.json
# Codex requires manual TOML conversion
```

---

## 📚 References

- **333_APPS/L4_TOOLS/** - Production MCP implementation
- **codebase/mcp/** - arifOS MCP server source code
- **AGENTS.md** - Agent-specific instructions (root level)
- **000_THEORY/** - Constitutional law definitions

---

## 👑 Authority

**Sovereign:** Muhammad Arif bin Fazil  
**Repository:** https://github.com/ariffazil/arifOS  
**License:** AGPL-3.0-only

---

```
╔═══════════════════════════════════════════════════════════════════╗
║                    DITEMPA BUKAN DIBERI                          ║
║                   (Forged, Not Given)                            ║
║                                                                   ║
║         This is the canon. All agents follow.                    ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```
