# 🦞 OpenClaw Dashboard Access

## Quick Access

### Step 1: SSH Tunnel (run on Windows first)
```powershell
ssh -N -L 18789:127.0.0.1:18789 root@72.62.71.199
```

### Step 2: Open Dashboard
```
http://localhost:18789/?token=779d97c3cdfa0271d1b982aae5322870fdc296ed79a3eae1
```

---

## Info

| Item | Value |
|------|-------|
| **Telegram Bot** | @AGI_ASI_bot |
| **VPS IP** | 72.62.71.199 |
| **VPS Hostname** | srv1325122 |
| **API Keys** | 27 loaded ✅ |
| **MCP Servers** | 9 configured ✅ |

---

## Troubleshooting

If the tunnel disconnects, just run the SSH command again.

If the dashboard doesn't load:
```bash
# On VPS, check if gateway is running:
pgrep -f "openclaw gateway" || openclaw gateway &
```

---

*Last updated: 2026-02-07*
