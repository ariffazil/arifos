---
name: agi-autonomous-controller
description: "Run autonomous perception-deliberation-action cycles with constitutional governance. Use when triggering self-healing, self-optimization, system health recovery, or autonomous agentic workflows governed by arifOS F1-F13. Triggers: autonomous cycle, self-heal, agi controller, auto-fix, autonomous action, system recovery."
user-invocable: true
type: flow
---

# AGI Autonomous Controller

Self-healing, self-optimizing controller governed by arifOS F1-F13 constitutional floors and the ΔΩΨ Trinity architecture.

---

## Autonomous Decision Flow

### Phase 1: Perception (Δ Mind)
```bash
arifos anchor '{"query":"Autonomous cycle initiation","actor_id":"agi-controller"}'
health-probe
arifos memory '{"query":"Similar past situations","session_id":"agi-session"}'
```

### Phase 2: Deliberation (Ω Heart)
```bash
arifos heart '{"query":"Impact of proposed action","session_id":"agi-session"}'
critique-thought '{"query":"What could go wrong?","session_id":"agi-session"}'
```

### Phase 3: Action (Ψ Soul)
```bash
arifos judge '{"query":"Should proceed autonomously?","session_id":"agi-session"}'
arifos forge '{"query":"Execute with governance","session_id":"agi-session"}'
arifos seal  '{"query":"Autonomous action complete","session_id":"agi-session"}'
```

---

## Self-Healing Matrix

| Issue | Detection | Auto-Fix | 888_HOLD |
|-------|-----------|----------|----------|
| Container stopped | health-probe | `docker restart` | No |
| High disk usage | Disk check | `docker prune` | No |
| Model unresponsive | Model probe | Switch fallback | No |
| Config drift | doctor --fix | Auto-correct | No |
| Memory corruption | BGE check | Reindex | No |
| Security breach | Security audit | Isolate + alert | **YES** |
| Data loss risk | Backup check | Pause + alert | **YES** |
| Constitutional VOID | Judge verdict | Stop + escalate | **YES** |

---

## 888_HOLD Triggers

1. **Irreversible actions** (F1) — deployments, migrations, deletions
2. **Security events** (F12) — breaches, auth failures
3. **Constitutional VOID** — Judge returns VOID verdict
4. **Resource critical** — Disk >90%, RAM <1 GiB

---

## Capabilities Summary

| Capability | Constitutional Floor |
|------------|---------------------|
| Self-Healing | F1, F4 |
| Self-Optimizing | F2, F8 |
| Self-Protecting | F12 |
| Self-Governing | F3–F13 |
| Self-Learning (VAULT999) | F7 |

---

## Integration

**Skills:** openclaw-doctor, vps-operations, arifos-constitutional, quadwitness-seal, agentic-governance, arifos-mcp-call, health-probe, memory-archivist
