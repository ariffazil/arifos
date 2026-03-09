# SKILL: OpenClaw Doctor & Troubleshooter

**Name:** openclaw-doctor  
**Version:** 1.0.0  
**Author:** AGI-OpenCode  
**Scope:** OpenClaw Gateway Diagnostics & Remediation  
**Compatibility:** OpenClaw 2026.3.x+

---

## 🩺 OpenClaw Diagnostic Ladder

Run these commands in sequence for systematic troubleshooting:

### 1. Quick Health Check
```bash
docker exec openclaw_gateway openclaw status
docker exec openclaw_gateway openclaw gateway status
docker exec openclaw_gateway curl -fsS http://localhost:18789/healthz
```

**Expected Results:**
- Gateway: `local · ws://127.0.0.1:18789 · reachable`
- Health: `{"ok":true,"status":"live"}`
- RPC probe: `ok`

### 2. Deep Diagnostics
```bash
docker exec openclaw_gateway openclaw status --deep
docker exec openclaw_gateway openclaw doctor --deep
docker exec openclaw_gateway openclaw channels status --probe
```

### 3. Universal Fix Command
```bash
docker exec openclaw_gateway openclaw doctor --deep --yes
```

---

## 🔧 Common Issues & Fixes

### Issue: Telegram Not Responding

**Symptoms:**
- Bot @arifOS_bot shows as offline
- No replies to DMs or mentions

**Diagnostics:**
```bash
docker exec openclaw_gateway openclaw channels status --probe
docker exec openclaw_gateway openclaw config get channels
```

**Fix:**
```bash
# Check if telegram config exists
docker exec openclaw_gateway cat /root/.openclaw/openclaw.json | jq '.channels.telegram'

# If missing, restore from backup or add:
docker exec openclaw_gateway sh -c '
cat > /tmp/telegram-config.json << "EOF"
{
  "enabled": true,
  "dmPolicy": "pairing",
  "botToken": "YOUR_BOT_TOKEN",
  "groupPolicy": "open",
  "streaming": "partial"
}
EOF
jq ".channels.telegram = $(cat /tmp/telegram-config.json)" /root/.openclaw/openclaw.json > /tmp/oc-new.json
mv /tmp/oc-new.json /root/.openclaw/openclaw.json
chmod 600 /root/.openclaw/openclaw.json
'

# Restart gateway
docker restart openclaw_gateway
```

### Issue: Gateway Won't Start

**Symptoms:**
- Container keeps restarting
- Port 18789 not responding

**Diagnostics:**
```bash
docker logs openclaw_gateway --tail 100
docker exec openclaw_gateway openclaw logs --follow
```

**Common Fixes:**
```bash
# Check for port conflicts
docker exec openclaw_gateway lsof -i :18789

# Fix: Bind to loopback only
docker exec openclaw_gateway openclaw config set gateway.bind 127.0.0.1

# Reset and reinstall service metadata
docker exec openclaw_gateway openclaw gateway install --force
docker restart openclaw_gateway
```

### Issue: Model Authentication Failed

**Symptoms:**
- "Unauthorized" or "Invalid API key" errors
- Anthropic 429 rate limit errors

**Diagnostics:**
```bash
docker exec openclaw_gateway openclaw models status
docker exec openclaw_gateway openclaw models status --probe
```

**Fix:**
```bash
# Re-authenticate Anthropic
docker exec openclaw_gateway openclaw models auth setup-token --provider anthropic

# Or set API key directly
docker exec openclaw_gateway openclaw config set models.providers.anthropic.apiKey "YOUR_API_KEY"

# Check fallback chain
docker exec openclaw_gateway openclaw models fallbacks list
```

### Issue: Memory Not Indexing

**Symptoms:**
- Vector search returns no results
- Memory files not being read

**Fix:**
```bash
# Reindex all memory
docker exec openclaw_gateway openclaw memory index --all

# Check memory backend
docker exec openclaw_gateway openclaw config get memory.backend

# Verify memory files exist
docker exec openclaw_gateway ls -la /root/.openclaw/memory/
```

### Issue: Session Context Full

**Symptoms:**
- "Context window exceeded" errors
- Model stops responding

**Fix:**
```bash
# Via Telegram/Chat: /compact
# Or reset sessions:
docker exec openclaw_gateway openclaw reset --scope sessions

# Or full reset (keeps config):
docker exec openclaw_gateway openclaw reset --scope full
```

### Issue: No DM Replies (Pairing Required)

**Symptoms:**
- Bot works in groups but ignores DMs

**Fix:**
```bash
# List pending pairing requests
docker exec openclaw_gateway openclaw pairing list

# Approve a specific user
docker exec openclaw_gateway openclaw pairing approve --channel telegram --account <USER_ID>

# Or set DM policy to open (less secure)
docker exec openclaw_gateway openclaw config set channels.telegram.dmPolicy open
```

### Issue: Security Audit Failures

**Symptoms:**
- `openclaw doctor` reports security warnings
- Config file permissions issues

**Fix:**
```bash
# Run security audit with auto-fix
docker exec openclaw_gateway openclaw security audit --fix

# Manual permission fix
docker exec openclaw_gateway chmod 600 /root/.openclaw/openclaw.json
docker exec openclaw_gateway chmod 700 /root/.openclaw/credentials/
docker exec openclaw_gateway chmod 700 /root/.openclaw/agents/
```

---

## 📊 Monitoring Commands

### Live Logs
```bash
# Gateway logs
docker logs -f openclaw_gateway

# OpenClaw internal logs
docker exec openclaw_gateway openclaw logs --follow

# Filter for errors only
docker exec openclaw_gateway openclaw logs --follow | grep -i error
```

### Session Management
```bash
# List active sessions
docker exec openclaw_gateway openclaw sessions list

# Get session details
docker exec openclaw_gateway openclaw sessions --json

# Reset specific session type
docker exec openclaw_gateway openclaw reset --scope sessions
```

### Resource Usage
```bash
# Container stats
docker stats openclaw_gateway --no-stream

# Memory usage inside container
docker exec openclaw_gateway ps aux --sort=-%mem | head -10

# Disk usage
docker exec openclaw_gateway du -sh /root/.openclaw/*
```

---

## 🚨 Emergency Procedures

### Full System Reset
```bash
# WARNING: Destroys all sessions and temporary data
docker exec openclaw_gateway openclaw reset --scope full
docker restart openclaw_gateway
```

### Config Recovery
```bash
# Restore from backup
docker exec openclaw_gateway cp /root/.openclaw/openclaw.json.bak /root/.openclaw/openclaw.json
docker restart openclaw_gateway

# Or reset to defaults
docker exec openclaw_gateway openclaw reset --scope config
```

### Container Recovery
```bash
# Complete container rebuild
docker-compose down openclaw
docker-compose up -d openclaw

# With logs
docker-compose up -d openclaw && docker logs -f openclaw_gateway
```

---

## 🔐 Security Hardening

### Production Checklist
- [ ] Config file: `chmod 600 ~/.openclaw/openclaw.json`
- [ ] Gateway bound to localhost: `gateway.bind: "127.0.0.1"`
- [ ] Auth token set: `gateway.auth.token` configured
- [ ] Telegram DM policy: `channels.telegram.dmPolicy: "pairing"`
- [ ] Group allowlist: `channels.telegram.groups` configured
- [ ] No world-readable credentials
- [ ] Sandbox mode enabled: `sandbox.mode: "all"` or `"non-main"`

### Security Audit Command
```bash
docker exec openclaw_gateway openclaw security audit --deep
```

---

## 🎯 Advanced Diagnostics

### Gateway Deep Status
```bash
docker exec openclaw_gateway openclaw gateway status --deep
```

### Model Probe with Token Usage
```bash
docker exec openclaw_gateway openclaw models status --probe
```

### Channel Deep Probe
```bash
docker exec openclaw_gateway openclaw channels status --probe --deep
```

### Health Check with JSON Output
```bash
docker exec openclaw_gateway openclaw health --json --verbose
```

---

## 📋 Quick Reference Card

| Problem | Quick Fix |
|---------|-----------|
| No response | `openclaw doctor --deep --yes` |
| Telegram down | Check `channels status --probe`, restore config |
| Auth failed | `models auth setup-token --provider <name>` |
| Context full | `/compact` or `reset --scope sessions` |
| High memory | `docker restart openclaw_gateway` |
| Config error | Restore from `.bak` or `reset --scope config` |
| Port conflict | `config set gateway.bind 127.0.0.1` |
| Security warnings | `security audit --fix` |

---

## 🔗 Key Files & Paths

| Path | Purpose |
|------|---------|
| `/root/.openclaw/openclaw.json` | Main config |
| `/root/.openclaw/workspace/` | Agent workspace |
| `/root/.openclaw/agents/<id>/` | Per-agent state |
| `/root/.openclaw/memory/` | Vector index |
| `/root/.openclaw/credentials/` | OAuth/API keys |
| `/tmp/openclaw/openclaw-YYYY-MM-DD.log` | Gateway logs |

---

**Last Updated:** 2026-03-09  
**OpenClaw Version:** 2026.3.7  
**Status:** SEALED for arifOS Production

*Ditempa Bukan Diberi — Forged, Not Given*
