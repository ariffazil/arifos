# Config Guardian — Safety Policies

## Core Rule: Propose, Don't Apply

Every config change follows a 3-step workflow:

1. **Read + Explain** — read the current value, explain in plain language
2. **Propose as Diff** — generate a unified diff with risk analysis
3. **Human Applies** — sovereign approves and the Governor session applies

Non-governor agents STOP at step 2. They may never proceed to step 3.

## Protected Path Registry

### Tier 1: Constitutional (NEVER modify, even in Governor session without explicit F13 approval)

| Path | Contains | Why protected |
|---|---|---|
| `SOUL.md` | Machine operating constraints | Defines what arifOS_bot IS |
| `USER.md` | Human identity | Human source of truth |
| `AGENTS.md` | Operating manual + floors | Governance backbone |
| `IDENTITY.md` | Name, symbol, role | First act of creation |
| `/mnt/arifos/core/` | Kernel floors | Constitutional law |
| `/mnt/arifos/.env` | All secrets | Never read or expose |

### Tier 2: Operational (Governor session can modify with confirmation)

| Path | Contains | Modify when |
|---|---|---|
| `openclaw.json` | Gateway config | Adding channels, models, tools |
| `TOOLS.md` | Tool capability map | Updating after config change |
| `HEARTBEAT.md` | Heartbeat checklist | Adding/removing checks |
| `SPEC.md` | System specification | Architecture changes |
| `MEMORY.md` | Memory rules | Updating memory workflow |

### Tier 3: Operational (Agent can modify freely)

| Path | Contains |
|---|---|
| `memory/*.md` | Daily memory logs |
| `logs/*.jsonl` | Audit logs |
| `skills/*/SKILL.md` | Skill definitions |

## Validation Rules

Before proposing any change, check:

### Structural
- [ ] JSON5 syntax valid (test with `jq`)
- [ ] All required fields present for new entries
- [ ] No duplicate keys
- [ ] Provider IDs match `models.providers.*` keys

### Security
- [ ] No secrets in plaintext (use `${VAR_NAME}` substitution)
- [ ] Auth mode is not `"none"` in production
- [ ] Elevated exec not enabled for untrusted agents
- [ ] DM policy is not `"open"` without allowlist
- [ ] No kernel paths exposed via new tool permissions

### Operational
- [ ] Model IDs reference valid providers
- [ ] Fallback chain has at least 2 entries
- [ ] Cron timezone matches user's timezone (Asia/Kuala_Lumpur)
- [ ] Session reset hour is reasonable for timezone
- [ ] Port doesn't conflict with existing services

## Risk Classification

| Risk Level | Description | Examples |
|---|---|---|
| **Low** | Easily reversible, no security impact | Change model, add cron job |
| **Medium** | Affects access or behavior, reversible | Change DM policy, add agent |
| **High** | Security impact or hard to undo | Change auth mode, expose port |
| **Critical** | Irreversible or external impact | Rotate keys, delete data |

## Rollback Protocol

Every proposed change MUST include:
1. The exact `edit` operation to reverse the change
2. Whether gateway restart is needed after rollback
3. Any side effects of rollback (e.g., sessions lost on restart)

## Escalation

If a proposed change touches multiple tiers:
- Tier 3 + Tier 2 → Governor session applies both
- Tier 2 + Tier 1 → 888_HOLD — explicit F13 approval required
- Any doubt → 888_HOLD — ask the sovereign
