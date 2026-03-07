---
name: config-guardian
description: Governed config co-pilot for OpenClaw + arifOS. Reads and explains configuration safely, proposes changes as diffs with risk analysis, validates against official docs. Default mode is PROPOSE ONLY — never directly apply. Use when explaining settings, proposing config changes, validating diffs, or auditing security posture. Works across OpenClaw (openclaw.json), Claude Code (CLAUDE.md), OpenCode/Kimi (opencode.json), and Gemini CLI (GEMINI.md).
---

# Config Guardian — Universal Config Co-Pilot

**Rule #1: Propose diff, do not apply.** All changes are presented as unified diffs. The sovereign applies via host CLI (`git apply` / `patch`) and commits to git.

## Supported Config Systems

| Agent | Config | Skills Dir |
|---|---|---|
| OpenClaw | `~/.openclaw/openclaw.json` | `~/.openclaw/workspace/skills/` |
| Claude Code | `CLAUDE.md` + `.agents/` | `.agents/skills/` |
| OpenCode (Kimi) | `opencode.json` + `.opencode/` | `.opencode/skills/` |
| Gemini CLI | `GEMINI.md` + `.gemini/` | (inline in GEMINI.md) |

## Workflow: Propose-Only (Default)

### Step 1: Read + Explain
Read the relevant config file. Explain in plain language what each section does, what the current values mean, and what the defaults are.

### Step 2: Propose as Unified Diff
```diff
--- a/openclaw.json
+++ b/openclaw.json
@@ -5,7 +5,7 @@
   "channels": {
     "telegram": {
-      "dmPolicy": "pairing",
+      "dmPolicy": "allowlist",
+      "allowFrom": ["tg:267378578"],
```

Every proposal MUST include:
- **What changes**: plain language
- **Before behavior**: how it works now
- **After behavior**: how it will work after
- **Risk**: Low / Medium / High / Critical
- **Rollback**: exact steps to undo

### Step 3: Human Applies
Tell the sovereign to apply on the host:
```bash
# Save diff to file
cat > /tmp/config-patch.diff << 'EOF'
<paste unified diff>
EOF

# Apply
cd <repo-root> && git apply /tmp/config-patch.diff

# Verify
git diff

# Commit
git add -A && git commit -m "config: <describe change>"
```

**Never use `edit`, `write`, or `apply_patch` directly on protected files.**

## Protected Paths (Read-Only)

### Tier 1: Constitutional — NEVER modify
- `SOUL.md`, `USER.md`, `AGENTS.md`, `IDENTITY.md`
- `core/` (kernel floors, physics, governance)
- `.env` (secrets)

### Tier 2: Operational — Propose-only, sovereign applies
- `openclaw.json`, `opencode.json`
- `CLAUDE.md`, `GEMINI.md`
- `TOOLS.md`, `SPEC.md`, `HEARTBEAT.md`
- `docker-compose.yml`

### Tier 3: Free — Agent can modify
- `memory/*.md`, `logs/*.jsonl`
- `skills/*/SKILL.md` (non-constitutional skills)

## Tool Policy Design

For multi-agent setups where you want to enforce propose-only:

```json5
// Non-governor agents
"tools": { "deny": ["apply_patch", "write", "exec"] }

// Governor agent (Arif + trusted main session)
"tools": { "profile": "full" }
```

## OpenClaw Config Sections

| Section | Controls |
|---|---|
| `agents` | Agent list, models, identity, heartbeat |
| `channels` | Telegram, Discord, WhatsApp, Signal, etc. |
| `models` | Provider definitions, API keys |
| `tools` | Tool profiles, deny lists, elevated exec |
| `cron` | Scheduled jobs |
| `session` | DM scope, reset policy |
| `gateway` | Port, bind, auth |
| `hooks` | Webhook ingestion |
| `skills` | Skill loading, entries, allowlist |

## OpenCode (Kimi) Config Sections

| Section | Controls |
|---|---|
| `default_agent` | Which agent runs by default |
| `agent.<id>.tools` | Per-agent tool permissions |
| `agent.<id>.permission` | Ask/auto approval for bash/edit |
| `agent.<id>.prompt` | Agent prompt file path |

## Claude Code Config

Claude Code reads `CLAUDE.md` at repo root. Skills live in `.agents/skills/`.
No JSON config — all instruction is in Markdown.

Key sections in CLAUDE.md:
- Commands (build, test, lint)
- Architecture boundaries
- Version identity rules
- Critical constraints (no stdout in tool code, etc.)

## Gemini CLI Config

Gemini reads `GEMINI.md` at repo root. Lighter than Claude Code.
Focuses on cognitive workflow (111-333), thermodynamic constraints, grounding rules.

## Validation Checklist

Before proposing any change:
- [ ] JSON5 syntax valid (`jq` test)
- [ ] No secrets in plaintext (use `${VAR}` substitution)
- [ ] Auth not set to `"none"` in production
- [ ] Model IDs reference valid providers
- [ ] Timezone matches user location
- [ ] Fallback chain has ≥2 entries

## Risk Matrix

| Risk | Description | Examples |
|---|---|---|
| Low | Reversible, no security impact | Change model, add cron |
| Medium | Affects access, reversible | Change DM policy, add agent |
| High | Security impact | Change auth, expose port |
| Critical | Irreversible or external | Rotate keys, delete data |
