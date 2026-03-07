---
name: openclaw-admin
description: Self-administration skill for configuring, troubleshooting, and maintaining the OpenClaw gateway. Use when: (1) changing AI models, providers, or fallback chains, (2) configuring Telegram/Discord/WhatsApp/Signal channels, (3) managing cron jobs and scheduled tasks, (4) editing openclaw.json settings, (5) managing tools, agents, or skills config, (6) troubleshooting gateway issues (restarts, health, logs), (7) updating API keys or auth, (8) configuring heartbeat, sessions, browser, sandbox, hooks, or TTS, (9) user asks "fix yourself", "update config", "add model", "change settings", "restart gateway", or similar self-management requests.
---

# OpenClaw Admin Skill

Self-repair, self-configure, self-maintain. This skill teaches the agent how to manage its own OpenClaw gateway.

## Config Location

- **Config file**: `~/.openclaw/openclaw.json` (JSON5 — comments + trailing commas OK)
- **Cron store**: `~/.openclaw/cron/jobs.json`
- **Sessions**: `~/.openclaw/agents/main/sessions/sessions.json`
- **Agent dir**: `~/.openclaw/agents/main/`
- **Workspace**: `~/.openclaw/workspace/`
- **Logs**: `/tmp/openclaw/openclaw-YYYY-MM-DD.log`

Always read the current config before making changes:
```bash
cat ~/.openclaw/openclaw.json
```

## Changing Models / Providers

### Set primary model
Edit `agents.list[0].model.primary` in openclaw.json:
```json5
"model": {
  "primary": "kimi/kimi-k2.5",
  "fallbacks": ["anthropic/claude-opus-4-6", "openrouter/google/gemini-2.5-flash"]
}
```

### Add a new provider
Add to `models.providers` with required fields:
```json5
"new-provider": {
  "baseUrl": "https://api.example.com/v1",
  "api": "openai-completions",  // or "anthropic-messages" or "google-generative-ai"
  "apiKey": "${NEW_PROVIDER_API_KEY}",
  "models": [{
    "id": "model-name",
    "name": "Human Name",
    "contextWindow": 128000,
    "maxTokens": 8192
  }]
}
```

### API compatibility
| Provider style | `api` value |
|---|---|
| OpenAI-compatible | `openai-completions` |
| Anthropic-compatible | `anthropic-messages` |
| Google-compatible | `google-generative-ai` |

### Set API keys
Add env var to host `.env` file at `/srv/arifOS/.env` or set inline:
```json5
"env": { "NEW_API_KEY": "sk-..." }
```
Config supports `${VAR_NAME}` substitution from environment.

## Managing Cron Jobs

### List jobs
```bash
openclaw cron list
```

### Add recurring job (isolated, with delivery)
```bash
openclaw cron add \
  --name "Morning brief" \
  --cron "0 7 * * *" \
  --tz "Asia/Kuala_Lumpur" \
  --session isolated \
  --message "Summarize overnight updates." \
  --announce \
  --channel telegram \
  --to "267378578"
```

### Add one-shot reminder
```bash
openclaw cron add \
  --name "Reminder" \
  --at "20m" \
  --session main \
  --system-event "Check deployment status." \
  --wake now \
  --delete-after-run
```

### Edit existing job
```bash
openclaw cron edit <jobId> --message "New prompt" --model "opus"
```

### Manual trigger
```bash
openclaw cron run <jobId>
```

### Session types
| Type | When to use |
|---|---|
| `main` | Uses heartbeat context, shares main session |
| `isolated` | Fresh session per run, clean context, delivery supported |

## Channel Configuration

### Telegram (current)
Config lives at `channels.telegram`:
```json5
"telegram": {
  "enabled": true,
  "botToken": "...",
  "dmPolicy": "pairing",
  "streaming": "partial",  // off | partial | block | progress
  "groupPolicy": "open"    // open | allowlist | disabled
}
```

### Add Discord
```json5
"discord": {
  "enabled": true,
  "token": "${DISCORD_BOT_TOKEN}",
  "dmPolicy": "pairing",
  "streaming": "off"
}
```

### Add WhatsApp
```json5
"whatsapp": {
  "dmPolicy": "pairing",
  "allowFrom": ["+60XXXXXXXXX"]
}
```
Then pair: `openclaw channels whatsapp pair`

### Add Signal
```json5
"signal": {
  "enabled": true,
  "dmPolicy": "pairing",
  "allowFrom": ["+60XXXXXXXXX"]
}
```

## Tools Configuration

### Tool profiles
| Profile | Includes |
|---|---|
| `minimal` | session_status only |
| `coding` | fs + runtime + sessions + memory + image |
| `messaging` | messaging + session tools |
| `full` | Everything (current setting) |

### Enable/disable specific tools
```json5
"tools": {
  "profile": "full",
  "deny": ["browser", "canvas"],  // deny wins over allow
  "elevated": { "enabled": true }
}
```

### Elevated exec
Controls host-level shell access. Current: enabled.
```json5
"tools": {
  "elevated": {
    "enabled": true,
    "allowFrom": {
      "telegram": ["267378578"]
    }
  }
}
```

## Agent Configuration

### Current agent
```json5
"agents": {
  "list": [{
    "id": "main",
    "name": "arifOS_bot",
    "workspace": "~/.openclaw/workspace",
    "model": { "primary": "...", "fallbacks": [...] },
    "identity": { "name": "arifOS_bot", "emoji": "⚡" }
  }]
}
```

### Add second agent (multi-agent)
```json5
"agents": {
  "list": [
    { "id": "main", "default": true, ... },
    { "id": "ops", "workspace": "~/.openclaw/workspace-ops", "model": { "primary": "..." } }
  ]
},
"bindings": [
  { "agentId": "ops", "match": { "channel": "telegram", "peer": { "kind": "group", "id": "-100..." } } }
]
```

## Heartbeat Configuration

### Enable heartbeat
```json5
"heartbeat": {
  "every": "30m",       // 0m = disabled (current)
  "model": "kimi/kimi-k2.5",
  "target": "telegram",  // none | last | telegram | discord | ...
  "to": "267378578"
}
```
Set at `agents.list[0].heartbeat` for per-agent, or `agents.defaults.heartbeat` for global.

### Heartbeat vs Cron
| Need | Use |
|---|---|
| Periodic self-check with main context | Heartbeat |
| Specific scheduled task with delivery | Cron (isolated) |
| "Poke me in 20 minutes" | Cron (one-shot) |

## Session Configuration

### Current: daily reset at 4am, per-channel-peer DM scope
```json5
"session": {
  "dmScope": "per-channel-peer",
  "reset": { "mode": "daily", "atHour": 4 }
}
```

### Options
| dmScope | Behavior |
|---|---|
| `main` | All DMs share one session |
| `per-peer` | Per sender across channels |
| `per-channel-peer` | Per sender per channel (current) |

## Troubleshooting

### Check gateway status
```bash
openclaw status
openclaw gateway health
```

### View logs
```bash
tail -100 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log
```

### Restart gateway
```bash
openclaw gateway restart
```
⚠️ This interrupts active sessions. Use only when necessary.

### Run diagnostics
```bash
openclaw doctor
openclaw doctor --fix  # auto-fix common issues
```

### Common issues
| Symptom | Check |
|---|---|
| Model not responding | `openclaw status` — check provider health |
| Messages not arriving | Check `channels.telegram.enabled`, bot token |
| Cron not firing | Check `cron.enabled`, timezone, `openclaw cron list` |
| High memory | `docker stats --no-stream` — check container limits |
| Config won't load | JSON syntax — use `jq . < ~/.openclaw/openclaw.json` |

## Config Edit Workflow (F1 Safe)

1. **Read current**: `cat ~/.openclaw/openclaw.json`
2. **Show diff**: Use `edit` tool with exact old/new text
3. **Confirm with Arif** if irreversible (888_HOLD for: API key rotation, channel removal, agent deletion)
4. **Apply**: Edit the file
5. **Reload**: `openclaw gateway restart` (only if runtime config — models, channels, tools)
6. **Verify**: `openclaw status`

Some settings take effect immediately (model selection via /model). Others require gateway restart.

## Advanced: Hooks

### Current hook config
Hooks endpoint at `/hooks` with token auth. Used for external automation triggering the agent.

### Add a webhook mapping
```json5
"hooks": {
  "mappings": [{
    "match": { "path": "deploy" },
    "action": "agent",
    "sessionKey": "hook:deploy",
    "messageTemplate": "Deploy event: {{body}}"
  }]
}
```

## Reference Files

For complete field-by-field config reference: read `references/config-reference.md`
For cron job details: read `references/cron-reference.md`
