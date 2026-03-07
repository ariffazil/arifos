# OpenClaw Config Quick Reference

## Config Path
`~/.openclaw/openclaw.json` (JSON5 format)

## Top-Level Keys

| Key | What it controls |
|---|---|
| `agents` | Agent list, defaults, model, identity, heartbeat, sandbox, compaction |
| `bindings` | Multi-agent routing rules |
| `channels` | Telegram, Discord, WhatsApp, Signal, Slack, iMessage, IRC, etc. |
| `commands` | Chat command handling (/commands) |
| `cron` | Scheduled jobs |
| `gateway` | Port, bind, auth, control UI, tailscale |
| `hooks` | Webhook ingestion |
| `logging` | Log level, file, redaction |
| `messages` | Response prefix, ack reaction, TTS, queue, debounce |
| `models` | Custom providers, base URLs, model catalog |
| `plugins` | Extension plugins |
| `session` | DM scope, reset policy, thread bindings |
| `skills` | Skill loading, entries, bundled allowlist |
| `tools` | Tool profiles, allow/deny, elevated, exec, web, media |
| `browser` | Browser profiles, SSRF policy |
| `ui` | Accent color, assistant identity |
| `env` | Inline env vars |

## Model Format
Always `provider/model-id` (e.g. `anthropic/claude-opus-4-6`, `kimi/kimi-k2.5`).

## Environment Variable Substitution
Use `${VAR_NAME}` in any config string. Only uppercase names matched.

## Applying Changes
- Model/thinking: `/model <alias>` or `/thinking <level>` — immediate, no restart
- Most config: requires `openclaw gateway restart`
- Cron: changes apply on next scheduled tick

## Current Setup (arifOS_bot)
- Gateway: port 18789, bind lan, token auth
- Telegram: enabled, partial streaming
- Cron: enabled, max 2 concurrent
- Tools: full profile, elevated enabled
- Session: per-channel-peer, daily reset at 4am
- Models: kimi primary, 12-tier fallback chain
