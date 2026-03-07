# Cron Jobs Reference

## Schedule Types

| Kind | Field | Example |
|---|---|---|
| `at` | `schedule.at` | ISO 8601: `"2026-03-08T16:00:00+08:00"` |
| `every` | `schedule.everyMs` | Milliseconds: `3600000` (1 hour) |
| `cron` | `schedule.expr` + `schedule.tz` | `"0 7 * * *"` + `"Asia/Kuala_Lumpur"` |

## CLI Commands

```bash
openclaw cron list                    # List all jobs
openclaw cron add [flags]             # Add new job
openclaw cron edit <jobId> [flags]    # Patch existing job
openclaw cron run <jobId>             # Force-run now
openclaw cron runs --id <jobId>       # View run history
openclaw cron remove <jobId>          # Delete job
```

## Common Flags
- `--name "Job Name"` — human-readable name
- `--cron "0 7 * * *"` — cron expression (5 or 6 field)
- `--tz "Asia/Kuala_Lumpur"` — timezone for cron expression
- `--at "20m"` or `--at "2026-03-08T08:00:00Z"` — one-shot
- `--session main|isolated` — execution context
- `--message "..."` — agent prompt (isolated)
- `--system-event "..."` — system event text (main)
- `--wake now|next-heartbeat` — when to trigger
- `--announce` — deliver result to channel
- `--channel telegram|discord|slack|whatsapp` — delivery channel
- `--to "267378578"` — delivery target
- `--model "opus"` — model override
- `--thinking off|low|high` — thinking override
- `--delete-after-run` — auto-delete one-shot jobs
- `--agent <id>` — pin to specific agent
- `--exact` — no stagger (run exactly on schedule)

## Delivery Modes
| Mode | Behavior |
|---|---|
| `announce` | Send result to channel (default for isolated) |
| `webhook` | POST to URL |
| `none` | No delivery |

## Retry Behavior
- **One-shot**: 3 retries for transient errors, then disable
- **Recurring**: exponential backoff (30s→1m→5m→15m→60m), resets on success

## Storage
- Jobs: `~/.openclaw/cron/jobs.json`
- Run history: `~/.openclaw/cron/runs/<jobId>.jsonl`
- Session retention: 24h default (`cron.sessionRetention`)
