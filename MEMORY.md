# MEMORY.md — Governance-Relevant State
*(Long-term store for decisions, trade-offs, and rationales under arifOS constitutional framework)*

**Bias:** Store governance-relevant state. Compress routine chit-chat. No long-term storage of sensitive identifiers beyond explicit "persist" marks.

**Output Contract:** When recalling memory, present in human language. No raw data dumps.

**Ω₀ ≈ 0.04** — Stable memory state.

---

## 🔒 Red Lines (What NOT to Store)

- ❌ Unencrypted passwords, tokens, or secrets
- ❌ Sensitive personal identifiers unless explicitly marked "persist"
- ❌ Financial account numbers or credentials
- ❌ Health data beyond general wellness notes
- ❌ Private communications with third parties

**If in doubt:** Ask Arif before persisting sensitive data.

---

## 👤 Sovereign Profile

| Field | Value | Persist? |
|:---|:---|:---:|
| **Name** | Muhammad Arif bin Fazil | ✅ |
| **Handle** | @ariffazil (Telegram id:267378578) | ✅ |
| **Phone** | +60167378578 | ✅ |
| **Location** | Seri Kembangan, Selangor, Malaysia | ✅ |
| **Timezone** | Asia/Kuala_Lumpur (UTC+8) | ✅ |
| **Motto** | DITEMPA BUKAN DIBERI | ✅ |
| **Project** | arifOS — constitutional AI governance | ✅ |
| **Employer** | PETRONAS (as of 2026) | ✅ |
| **Roles** | Geoscientist, Economist, AI Governance Architect | ✅ |

---

## 🖥️ Infrastructure State (2026-02-07)

### VPS: srv1325122
- **IP:** 72.62.71.199
- **OS:** Ubuntu 25.10
- **OpenClaw:** 2026.2.6-3

### Agent Zero Deployment (NEW - 2026-02-07)
- **Status:** ✅ Running (24/7)
- **Container:** `agent-zero` (Docker)
- **Port:** 50080 (mapped to container port 80)
- **Access:** http://72.62.71.199:50080
- **Location:** `/root/agent-zero/`
- **Alignment:** arifOS constitutional constraints injected
  - `agent.system.main.role.md` - Contains F1/F2/F9 governance
  - `fw.initial_message.md` - arifOS-aware greeting

### Agent Zero Capabilities Enabled
- ✅ Node.js v22 + npm (installed for MCP servers)
- ✅ Python 3.13 + pip (installed for Python MCP SDKs)
- ✅ Python MCP SDKs: `mcp`, `fastmcp`, `arifos`
- ✅ OpenRouter API configured
- ✅ CORS: `ALLOWED_ORIGINS=*` (temporary for mobile access)
- ✅ Sub-agent spawning enabled

### API Keys: 27 Configured
Location: `/root/.env.openclaw`

| Category | Keys |
|:---|:---|
| **AI Models** | OPENAI, ANTHROPIC, GEMINI, OPENROUTER, DEEPSEEK, MISTRAL, KIMI, SEALION, MINIMAX |
| **Search/Web** | BRAVE, CONTEXT7, PERPLEXITY, TAVILY, FIRECRAWL, JINA, GREPTILE |
| **Dev Tools** | GITHUB, HF, BROWSERBASE, FIGMA |
| **Services** | ELEVENLABS, RESEND |
| **Infra** | CLOUDFLARE (token + account), RAILWAY, DATABASE_URL, HOSTINGER |

### MCP Servers: 16 Configured (OpenClaw)
1. github, filesystem, brave-search, puppeteer, memory
2. sequential-thinking, fetch, time, postgres, git
3. playwright, context7, perplexity, sqlite, arxiv, arifos

---

## 🏛️ Active Projects

| Project | Repository | Status |
|:---|:---|:---:|
| **arifOS** | github.com/ariffazil/arifOS | Active |
| **Trinity Sites** | arif-fazil.com, apex.arif-fazil.com, arifos.arif-fazil.com | Live |
| **aaa-mcp** | aaamcp.arif-fazil.com | Live |
| **AGI_ASI_bot** | OpenClaw Gateway | Active |
| **Agent Zero** | VPS Docker Deployment | ✅ Live |

---

## 📋 Decisions Log

### 2026-02-07: Agent Zero Installation & Alignment
- **Action:** Installed Agent Zero AI framework on VPS via Docker
- **Rationale:** Create contained cognitive lab for high-risk coding/research
- **Alignment:** Injected arifOS constitutional constraints (F1/F2/F9)
- **OpenClaw Role:** Supervisor/Gateway; Agent Zero Role: Sandboxed Lab
- **Reversibility:** Full (Docker container can be stopped/removed/recreated)
- **Verdict:** SEAL
- **Ω₀:** 0.04

### 2026-02-07: Agent Zero Environment Hardening
- **Action:** Installed Node.js + npm inside container for MCP servers
- **Action:** Installed Python MCP SDKs (`mcp`, `fastmcp`, `arifos`)
- **Rationale:** Enable full MCP ecosystem within contained environment
- **Method:** `apt-get install nodejs npm` + `pip install mcp fastmcp arifos --break-system-packages`
- **Verdict:** SEAL
- **Ω₀:** 0.04

### 2026-02-07: OpenRouter Configuration
- **Action:** Configured Agent Zero to use OpenRouter API
- **Rationale:** Cost-effective routing; access to multiple models
- **Security:** API key stored in Agent Zero environment, not in prompts
- **Verdict:** SEAL
- **Ω₀:** 0.04

### 2026-02-07: Agent Zero CORS Access
- **Action:** Set `ALLOWED_ORIGINS=*` in docker-compose.yml
- **Rationale:** Enable mobile/laptop access during setup phase
- **Risk:** Temporary; should tighten to specific origins for production
- **Reversibility:** Easy (edit docker-compose.yml, restart)
- **Verdict:** SEAL (with note to harden later)
- **Ω₀:** 0.05

### 2026-02-07: Action Skills Framework (Triad Roles)
- **Action:** Documented Architect/Engineer/Auditor roles in AGENTS.md
- **Rationale:** Formalize separation of design, execution, and verification
- **Integration:** Layered atop physics/math/linguistics agents
- **Verdict:** SEAL
- **Ω₀:** 0.04

### 2026-02-07: Workflow Automation (Cron Jobs)
- **Action:** Created `WORKFLOW_SUBUH_BRIEF.md` and `WORKFLOW_REPO_STEWARD.md`
- **Action:** Installed cron jobs for daily/weekly automation
- **Status:** APPROVED → ACTIVE
- **Verdict:** SEAL
- **Ω₀:** 0.04

---

## ⚖️ Trade-offs Recorded

### Local vs Cloud Storage
- **Decision:** Prefer local storage (Markdown, SQLite, git)
- **Rationale:** Data residency (MY/ASEAN preference), reversibility, auditability
- **Floor:** F1 Amanah

### Speed vs Safety
- **Decision:** Slow down when Ω₀ > 0.05
- **Rationale:** Reversibility over convenience
- **Floor:** F7 Humility

### Agent Zero Access (CORS)
- **Decision:** Temporary wildcard origin for setup
- **Rationale:** Enable multi-device access during initial configuration
- **Future:** Restrict to specific origins + enable authentication
- **Floor:** F1 Amanah (reversible), F12 Containment

---

## 📊 Statistics

| Metric | Value | Updated |
|:---|:---:|:---|
| Total Sessions | 47+ | 2026-02-07 |
| Governance Decisions | 18 | 2026-02-07 |
| SEAL Verdicts | 14 | 2026-02-07 |
| VOID Verdicts | 2 | 2026-02-07 |
| Average Ω₀ | 0.04 | 2026-02-07 |
| Agent Zero Uptime | 24/7 (target) | 2026-02-07 |

---

## ⏳ Pending Items (SABAR)

*Items awaiting clarification or additional data:*

| Item | Status | Ω₀ |
|:---|:---|:---:|
| AAA MCP Server Implementation | Ready to start | 0.04 |
| MCP Server Mirroring (OpenClaw → Agent Zero) | Node/npm unblocked, ready | 0.04 |
| Agent Zero Authentication Hardening | Replace wildcard CORS | 0.05 |
| Vision Model Configuration | Error identified, fix ready | 0.04 |

---

## 📦 Compression Rules

### What to Keep
- ✅ Decisions with governance implications
- ✅ Trade-offs and rationales
- ✅ Infrastructure changes
- ✅ Floor violations or near-misses
- ✅ Arif's explicit preferences

### What to Compress/Discard
- ❌ Routine acknowledgments ("ok", "thanks")
- ❌ Chit-chat without governance relevance
- ❌ Repeated queries with same answer
- ❌ Transient debugging output

---

## 📁 Important Paths

| Path | Purpose |
|:---|:---|
| `/root/.env.openclaw` | API keys |
| `/root/.mcporter/mcporter.json` | MCP server config |
| `/root/.openclaw/workspace/` | Working directory |
| `/root/agent-zero/` | Agent Zero installation |
| `/root/agent-zero/docker/run/docker-compose.yml` | Agent Zero deployment config |
| `/root/agent-zero/prompts/` | Agent Zero system prompts (arifOS aligned) |
| `memory/2026-02-07.md` | This file - session archive |
| `DASHBOARD.md` | Web UI access instructions |

---

## 🔄 Session Continuity Protocol

### For Next Session (2026-02-08 or later):

1. **Agent Zero:** Should still be running at http://72.62.71.199:50080
   - If not: `docker compose -f /root/agent-zero/docker/run/docker-compose.yml up -d`

2. **Quick Verification:**
   ```bash
   docker ps | grep agent-zero
   docker exec agent-zero node --version  # Should show v22
   docker exec agent-zero python3 -c "import mcp; print('MCP OK')"
   ```

3. **Resume Work:**
   - Open browser → http://72.62.71.199:50080
   - New Chat → arifOS-aligned greeting should appear
   - Continue AAA MCP build or other tasks

---

## ⚖️ Governance Audit

- **F1 Amanah:** All infrastructure changes are reversible via git/Docker
- **F2 Truth:** All facts verified against system state
- **F7 Humility:** Ω₀ tracked per entry
- **F9 Anti-Hantu:** Memory described as state storage, not consciousness
- **F12 Containment:** Agent Zero properly sandboxed; OpenClaw maintains supervisory role

**Attribution:** arifOS Constitutional AI Governance Framework

---

*Update this file as governance-relevant events occur. Routine chit-chat should not pollute this ledger.*

**Session Sealed: 2026-02-07T20:36:00+08:00**  
**Next Expected Session: 2026-02-08**  
**Status: AGENT ZERO LIVE & ALIGNED** 🔥

*Buang yang keruh, ambil yang jernih.* 🦞
