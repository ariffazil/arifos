# Config Map — openclaw.json Field Reference

## Top-Level Structure

```
openclaw.json
├── agents          # Agent list, defaults, models, identity, heartbeat
├── bindings        # Multi-agent routing rules
├── channels        # Telegram, Discord, WhatsApp, Signal, Slack, etc.
├── commands        # Chat command handling
├── cron            # Scheduled jobs
├── env             # Inline environment variables
├── gateway         # Port, bind, auth, control UI
├── hooks           # Webhook ingestion
├── logging         # Log level, file, redaction
├── messages        # Response prefix, ack reaction, TTS, queue
├── models          # Custom providers, model catalog
├── plugins         # Extension plugins
├── session         # DM scope, reset policy, thread bindings
├── skills          # Skill loading, entries, bundled allowlist
├── tools           # Tool profiles, allow/deny, elevated, exec
├── browser         # Browser profiles, SSRF policy
├── ui              # Accent color, assistant identity
└── meta            # Version tracking (auto-managed)
```

## Key Config Patterns

### Model Configuration
- `agents.defaults.model.primary` — default model for all agents
- `agents.list[N].model.primary` — per-agent override
- `agents.list[N].model.fallbacks` — ordered fallback chain
- `models.providers.<name>` — custom provider definitions
- Provider format: `provider/model-id` (e.g. `kimi/kimi-k2.5`)

### Channel Configuration
- `channels.<provider>.enabled` — toggle channel
- `channels.<provider>.dmPolicy` — pairing | allowlist | open | disabled
- `channels.<provider>.groupPolicy` — allowlist | open | disabled
- `channels.<provider>.streaming` — off | partial | block | progress
- `channels.<provider>.botToken` — auth token (or env var)

### Tool Configuration
- `tools.profile` — minimal | coding | messaging | full
- `tools.deny` — explicit deny list (wins over allow)
- `tools.elevated.enabled` — host exec access
- `agents.list[N].tools.profile` — per-agent override

### Cron Configuration
- `cron.enabled` — master switch
- `cron.maxConcurrentRuns` — parallel job limit
- `cron.sessionRetention` — how long to keep run sessions
- Jobs stored at `~/.openclaw/cron/jobs.json`

### Session Configuration
- `session.dmScope` — main | per-peer | per-channel-peer
- `session.reset.mode` — daily | idle
- `session.reset.atHour` — hour (0-23) for daily reset

### Gateway Configuration
- `gateway.port` — HTTP/WS port (default 18789)
- `gateway.bind` — loopback | lan | tailnet | custom
- `gateway.auth.mode` — none | token | password | trusted-proxy
- `gateway.auth.token` — shared auth token

## Safety-Critical Fields

| Field | Risk if wrong | Impact |
|---|---|---|
| `gateway.auth.mode: "none"` | HIGH | No auth on gateway |
| `gateway.bind: "lan"` | MEDIUM | Exposed to network |
| `channels.*.dmPolicy: "open"` | MEDIUM | Anyone can DM |
| `tools.elevated.enabled: true` | HIGH | Host shell access |
| `tools.profile: "full"` | MEDIUM | All tools available |
| `commands.bash: true` | HIGH | Shell via chat |

## Current arifOS_bot Config Summary

- **Gateway**: port 18789, bind lan, token auth ✅
- **Telegram**: enabled, pairing DM, open groups, partial streaming
- **Models**: kimi/kimi-k2.5 primary, 12-tier fallback
- **Tools**: full profile, elevated enabled
- **Cron**: enabled, max 2 concurrent, 24h retention
- **Session**: per-channel-peer, daily reset at 4am
- **Heartbeat**: disabled (every: "0m")
