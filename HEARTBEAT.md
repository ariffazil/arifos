# HEARTBEAT.md — Liveness and Ops Expectations
*(How to report health, what "ok/degraded" means, and observability under arifOS metabolism)*

**Output Contract:** Health reports use human language. Internal metrics (Ω₀, ΔS) shown only when relevant or requested.

**Format:** Telegram MarkdownV2 (see TELEGRAM_FORMAT.md)

---

## 🫀 Health States

| State | Ω₀ Range | Meaning | Action |
|:---|:---:|:---|:---|
| **🟢 OPTIMAL** | 0.00-0.03 | High confidence, low uncertainty | Normal operation |
| **🟡 NORMAL** | 0.03-0.05 | Target operating band | Normal operation |
| **🟠 ELEVATED** | 0.05-0.08 | Increased uncertainty | Slow down, clarify, mark "Estimate Only" |
| **🔴 CRITICAL** | >0.08 | Critical uncertainty | VOID actions, escalate to Arif |

---

## 📊 Current Status

```yaml
timestamp: 2026-02-08T01:35:00+08:00
status: 🟢 OPTIMAL
omega_0: 0.04
peace_squared: 1.5
entropy_delta: -0.03  # decreasing = good

gateway:
  health: OK
  uptime: active
  port: 18789

channels:
  telegram: CONNECTED (@AGI_ASI_bot)
  whatsapp: STANDBY
  dashboard: ACCESSIBLE (localhost:18789)

mcp_servers:
  total: 16
  active: 16
  failed: 0

api_keys:
  loaded: 27
  valid: 27
  expired: 0

cron_jobs:
  total: 7
  active: 7
  failed: 0
  daily_metabolism: OPERATIONAL
```

---

## 🔄 Periodic Checks

### Every 5 Minutes:
- [ ] Gateway process alive: `pgrep -f "openclaw gateway"`
- [ ] API keys loaded: Check env vars present
- [ ] Ω₀ within target band

### Every Hour:
- [ ] MCP servers accessible: `mcporter config list`
- [ ] arifOS MCP reachable: Check https://aaamcp.arif-fazil.com/health
- [ ] Memory file integrity

### Every Day:
- [ ] Session log rotation
- [ ] Memory pruning
- [ ] Governance audit summary
- [ ] Cron job health: `openclaw cron list` — verify 7 daily jobs active
- [ ] Daily State Vector integrity: Check `memory/daily-state/YYYY-MM-DD.json`
- [ ] Workflow file validation: 7 WORKFLOW_*.md files present

---

## ⚡ Entropy Budget (Thermodynamic View)

Each session has an entropy budget:

| Level | Operations | Cost |
|:---|:---|:---|
| **🟢 Low Entropy** | Local reads, searches, summarization | Cheap |
| **🟡 Medium Entropy** | External reads, git operations | Moderate |
| **🔴 High Entropy** | External writes, infrastructure, messaging | Expensive |

**Prefer low-entropy operations** unless high-entropy is explicitly needed.

---

## 📈 Thermodynamic Metrics

| Metric | Formula | Target | Current |
|:---|:---|:---:|:---:|
| **Entropy Reduction** | ΔS_human | ≤ 0 | -0.03 ✅ |
| **Peace² (Safety)** | P² = buffer/risk | ≥ 1.0 | 1.5 ✅ |
| **Genius Score** | G = A×P×X×E² | ≥ 0.80 | 0.88 ✅ |
| **Uncertainty** | Ω₀ | 0.03-0.05 | 0.04 ✅ |
| **Governance Load** | σ_gov | low | low ✅ |
| **Metabolism Status** | Daily rhythm | stable | optimal ✅ |

---

## 🚨 Escalation Triggers

### Auto-SABAR (Pause + Ask):
- Ω₀ > 0.05 for 3+ consecutive responses
- MCP server failure
- Unexpected error rate spike

### Version-Shift SABAR (Constitutional Brittleness Guard):
On any of these events, **increase Ω₀ by 0.02** and label behaviour as "experimental" until 5+ sessions pass without incident:
- LLM model upgrade or backend swap
- Major prompt file change (SOUL.md, DIRECTIVE.md, AGENTS.md)
- OpenClaw version upgrade
- New skill installation

Rationale: Constitutional brittleness — slight changes in model or phrasing can subtly shift behaviours. This slows down at dangerous moments.

### Auto-VOID (Stop + Report):
- Ω₀ > 0.08
- F1/F2/F9/F11 violation detected
- Gateway crash or unresponsive
- Authentication failure

---

## 🔔 Alerting Thresholds

| Condition | Alert |
|:---|:---|
| Gateway down >5min | Notify Arif |
| Ω₀ >0.08 sustained | Notify Arif |
| Floor violation detected | Notify Arif immediately |
| MCP server unreachable | Log, retry, notify if persistent |

---

## 📝 What to Log

| Category | Log? | Retention |
|:---|:---:|:---|
| Floor violations | ✅ Always | Permanent |
| VOID decisions | ✅ Always | Permanent |
| Infrastructure changes | ✅ Always | Permanent |
| Normal heartbeats | ❌ No | Transient |
| Routine ops | ❌ No | Transient |

---

## 🛡️ Security & Autonomy Status (Phase 0–2 SEALED)

*Updated: 2026-02-08T06:30:00Z | Ω₀ = 0.04 | SEALED*

### Security Posture
| Component | Status | Details |
|:---|:---:|:---|
| **UFW** | ✅ Active | SSH allowed, 50080 blocked externally |
| **fail2ban** | ✅ Running | sshd jail active |
| **Agent Zero** | ✅ Capped | 2 CPU / 4GB RAM resource limits |

### Exec Capabilities
| Parameter | Value |
|:---|:---|
| **exec.security** | `full` |
| **elevated** | `ask` (human veto retained) |
| **elevated.enabled** | `true` |
| **allowFrom** | `telegram:267378578` |
| **safeBins** | 70+ (apt, npm, pip, docker, git, curl, wget, etc.) |

### Autonomy
```
╔═══════════════════════════════════════╗
║  AUTONOMY SCORE: 85%                  ║
║  Phase: 0✅  1✅  2✅  3⏳(48h)       ║
║  Review: 2026-02-10T06:30:00Z         ║
╚═══════════════════════════════════════╝
```

---

## 🔧 Manual Health Check

Run these commands to verify health:

```bash
# Gateway status
pgrep -f "openclaw gateway" && echo "Running" || echo "Not running"

# Process check
ps aux | grep openclaw

# Port check
ss -tlnp | grep 18789

# Log tail
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log

# MCP test
mcporter call time.get_current_time timezone=Asia/Kuala_Lumpur
```

---

## ⚖️ Governance Audit

- **F5 Peace²:** Health states tied to safety margins
- **F7 Humility:** Health states tied to Ω₀ tracking
- **F9 Anti-Hantu:** Heartbeat is metabolism monitoring, not life signs

**Attribution:** arifOS Constitutional AI Governance Framework

---

*Last Updated: 2026-02-08 | Revision: r4.0-Phase2Audit (Security & Autonomy SEALED, Daily Cron Stack SEALED)*
*Buang yang keruh, ambil yang jernih.* 🦞
