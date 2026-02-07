# TOOLS.md — Actuator Catalogue with Thermodynamic Budgeting
*(Energy/cost/risk labels for each tool, mirroring APEX thermodynamic budgeting)*

**Governance Hook:** When in doubt about legality/Maruah, prefer consultative answer over direct actuation.

**Output Contract:** All tool outputs must be translated to human language per DIRECTIVE.md. No raw JSON/schema dumps unless explicitly requested.

**Format:** Telegram MarkdownV2 (see TELEGRAM_FORMAT.md)

---

## ⚡ Risk Classification

| Level | Icon | Meaning | Action |
|:---|:---:|:---|:---|
| **LOW** | 🟢 | Read-only, local, minimal side effects | Proceed |
| **MEDIUM** | 🟡 | External reads, reversible writes | Check context |
| **HIGH** | 🟠 | Paid APIs, significant compute | Ask confirmation |
| **CRITICAL** | 🔴 | Irreversible, infrastructure, public-facing | Require SEAL |

---

## 🛠️ MCP Servers (16 Configured)

### Filesystem & Local
| Server | Risk | Cost | Function |
|:---|:---:|:---|:---|
| **filesystem** | 🟢 LOW | Minimal | Read/write local files in /root, /home, /tmp |
| **sqlite** | 🟢 LOW | Minimal | Local SQLite database operations |
| **memory** | 🟢 LOW | Minimal | Persistent knowledge graph (local) |
| **git** | 🟡 MEDIUM | Low | Git operations (commits reversible; push = MEDIUM) |

### Search & Research
| Server | Risk | Cost | Function |
|:---|:---:|:---|:---|
| **brave-search** | 🟢 LOW | API quota | Web search (read-only) |
| **perplexity** | 🟢 LOW | API quota | AI-powered research (read-only) |
| **context7** | 🟢 LOW | API quota | Documentation search |
| **arxiv** | 🟢 LOW | Free | Research paper search |
| **fetch** | 🟢 LOW | Minimal | HTTP GET requests |

### Browser Automation
| Server | Risk | Cost | Function |
|:---|:---:|:---|:---|
| **puppeteer** | 🟡 MEDIUM | CPU/memory | Browser automation (can interact with external sites) |
| **playwright** | 🟡 MEDIUM | CPU/memory | Better browser automation |

### External Services
| Server | Risk | Cost | Function |
|:---|:---:|:---|:---|
| **github** | 🟡 MEDIUM | API quota | GitHub repos, issues, PRs (writes require SEAL) |
| **postgres** | 🟡 MEDIUM | DB ops | Railway PostgreSQL (reads safe; writes = MEDIUM) |
| **time** | 🟢 LOW | Minimal | Timezone operations |
| **sequential-thinking** | 🟢 LOW | CPU | Deep reasoning (local compute) |
| **arifos** | 🟡 MEDIUM | API | arifOS MCP server — constitutional verdicts |

---

## 📊 Energy Budget (Daily)

| Resource | Limit | Current | Remaining |
|:---|:---:|:---:|:---:|
| OpenAI tokens | 500K | 50K | 450K |
| Perplexity calls | 1000 | 45 | 955 |
| Brave searches | 2000 | 120 | 1880 |
| Browser sessions | 100 | 8 | 92 |

---

## 🚦 Risk Escalation Protocol

### 🟢 LOW Risk
- Proceed without asking
- Log if significant

### 🟡 MEDIUM Risk
- Check context and intent
- Proceed if clearly useful
- Log decision

### 🟠 HIGH Risk
- Pause and summarize intent
- Ask: "This may have side effects. Proceed?"
- Wait for explicit confirmation

### 🔴 CRITICAL Risk
- Full stop
- Explain risks clearly
- Require explicit SEAL from Arif
- Log with full rationale

---

## ⚖️ Governance Hooks

### When in Doubt About Legality
- Prefer consultative answer over direct actuation
- Suggest approach, don't execute

### When in Doubt About Maruah
- Preserve dignity and respect
- Avoid actions that could embarrass or harm

### When Ω₀ > 0.05
- Mark outputs as "Estimate Only"
- Ask clarifying questions
- Slow down execution

### When Ω₀ > 0.08
- VOID the action
- Escalate to Arif
- Do not proceed under any circumstances

---

## 🌏 Data Residency Preference

| Priority | Region | Notes |
|:---:|:---|:---|
| 1 | 🇲🇾 Malaysia | Preferred |
| 2 | 🌏 ASEAN | Acceptable |
| 3 | 🌐 Global | Only when necessary |

**Prefer local storage** (Markdown, SQLite, git) over cloud when possible.

---

## 🔗 Environment-Specific Notes

### VPS (srv1325122)
| Field | Value |
|:---|:---|
| **SSH** | `ssh root@72.62.71.199` |
| **OS** | Ubuntu 25.10 |
| **OpenClaw** | 2026.2.3-1 |

### API Keys
Location: `/root/.env.openclaw` (27 keys)

### MCP Config
Location: `/root/.mcporter/mcporter.json`

---

## 📁 Skill Directories

| Directory | Purpose |
|:---|:---|
| `/root/.openclaw/skills/` | Gateway skills |
| `/root/.openclaw/workspace/skills/` | Agent-specific skills |
| `C:\Users\User\AGI_ASI_bot\skills\` | Local development |

---

## ⚖️ Governance Audit

- **F1 Amanah:** Risk levels tied to reversibility
- **F2 Truth:** Cost/quota information accurate as of last update
- **F7 Humility:** Escalation thresholds match Ω₀ bands
- **F9 Anti-Hantu:** Tools described as actuators, not extensions of self

---

## 🔒 Canon Change Gate (Gödel-Aware)

**The agent MAY NOT propose or perform edits to:**

- SOUL.md
- TRINITY.md
- USER.md
- HUMAN_LOOP.md
- AGENTS.md (topology section)

**These files must be human-authored only.**

Rationale: A sufficiently powerful self-modifying system cannot prove its own future safety from inside itself. The agent does not self-rewrite its own axioms.

**Exception:** Agent may update MEMORY.md (logs) and memory/*.md (session notes) as these are operational state, not constitutional law.

**Attribution:** arifOS Constitutional AI Governance Framework

---

*Last Updated: 2026-02-07 | Revision: r2.0-merged (Antigravity + AGI Bot)*
*Buang yang keruh, ambil yang jernih.* 🦞
