# DEPLOYMENT.md — arifOS Complete Deployment Guide
**T000 Version:** 2026.02.15-FORGE-TRINITY-SEAL  
**Code Version:** v64.2-GAGI  
**Endpoint:** https://arifosmcp.arif-fazil.com  
**Reality Index:** 0.94

---

## 🎯 Quick Start (Choose Your Path)

| Your Goal | Path | Time | Difficulty |
|:----------|:-----|:----:|:----------:|
| **Try immediately** | Copy-paste SYSTEM_PROMPT | 5 sec | 🟢 Easy |
| **Local development** | pip install + stdio | 30 sec | 🟢 Easy |
| **Production cloud** | Railway deployment | 5 min | 🟡 Medium |
| **Enterprise/air-gapped** | Docker + VPS | 15 min | 🔴 Advanced |

---

## 1️⃣ Zero-Install: Copy-Paste Prompt (5 seconds)

No installation required. Works with any LLM that accepts system prompts.

**File:** `333_APPS/L1_PROMPT/SYSTEM_PROMPT.md`

```bash
# Copy this file's contents into any AI's system settings
cat 333_APPS/L1_PROMPT/SYSTEM_PROMPT.md | pbcopy  # macOS
cat 333_APPS/L1_PROMPT/SYSTEM_PROMPT.md | xclip    # Linux
```

**Supports:** ChatGPT, Claude, Gemini, Copilot, and any custom LLM.

---

## 2️⃣ Local Development: pip install (30 seconds)

```bash
# Install
pip install arifos

# Run MCP server (stdio mode)
python -m aaa_mcp

# Test
python -m aaa_mcp.selftest
```

**Default endpoint:** `stdio` (for Claude Desktop, Cursor, etc.)

---

## 3️⃣ Production Cloud: Railway (5 minutes)

### Prerequisites
```bash
npm install -g @railway/cli
railway login
```

### Deploy
```bash
cd arifOS
railway init --name arifos-mcp
railway variables set PORT=8080 HOST=0.0.0.0
railway variables set AAA_MCP_TRANSPORT=sse
railway up
railway domain
```

**Output:** `https://arifos-mcp.up.railway.app`

### Verify
```bash
curl https://arifos-mcp.up.railway.app/health
# {"status":"healthy","version":"64.2","reality_index":0.94}
```

---

## 4️⃣ Enterprise/VPS: Docker (15 minutes)

### Using Docker Compose
```bash
git clone https://github.com/ariffazil/arifOS.git
cd arifOS
docker-compose up -d
```

### Manual Docker
```bash
docker build -t arifos .
docker run -p 8888:8888 \
  -e PORT=8888 \
  -e HOST=0.0.0.0 \
  arifos
```

**Health check:** `curl http://localhost:8888/health`

---

## 5️⃣ Advanced Production: Hardened Ubuntu VPS (15-30 minutes)

Recommended for production-grade stability and constitutional alignment.

### 1. Provision & Secure
- SSH access as non-root user (`arifos`).
- `sudo ufw allow 80/tcp && sudo ufw allow 443/tcp`.
- Install `python3-venv`, `git`, `nginx`, `certbot`.

### 2. Setup Environment
```bash
git clone https://github.com/ariffazil/arifOS.git
cd arifOS
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Daemonize (systemd)
Create `/etc/systemd/system/arifos-mcp.service`:
```ini
[Unit]
Description=arifOS MCP Server
After=network.target

[Service]
User=arifos
WorkingDirectory=/home/arifos/arifOS
ExecStart=/home/arifos/arifOS/.venv/bin/python aaa_mcp/server.py
Restart=always

[Install]
WantedBy=multi-user.target
```
`sudo systemctl start arifos-mcp && sudo systemctl enable arifos-mcp`

### 4. Reverse Proxy (Nginx + SSL)
Configure Nginx for `arifosmcp.arif-fazil.com` and run `certbot --nginx`.

---

## 🔐 Environment Variables

| Variable | Required | Default | Purpose |
|:---------|:--------:|:-------:|:--------|
| `ARIFOS_API_KEY` | For cloud | - | Bearer token auth |
| `PORT` | No | 8080 | Server port |
| `HOST` | No | 0.0.0.0 | Bind address |
| `AAA_MCP_TRANSPORT` | No | stdio | stdio/sse/http |
| `DATABASE_URL` | No | - | PostgreSQL for VAULT999 |
| `REDIS_URL` | No | - | Redis for sessions |

---

## 🌐 Platform Integration

See [MCP_PLATFORM_GUIDE.md](./MCP_PLATFORM_GUIDE.md) for detailed platform configs:

| Platform | Transport | Config File |
|:---------|:---------:|:------------|
| **Claude Desktop** | stdio | `claude_desktop_config.json` |
| **ChatGPT Dev** | HTTP/SSE | Developer Mode UI |
| **Codex CLI** | stdio | `~/.codex/config.toml` |
| **Cursor** | stdio | `.cursor/mcp.json` |
| **OpenCode** | stdio | `opencode.json` |
| **JetBrains** | stdio | OpenCode plugin |
| **AgentZero** | HTTP | `agentzero.yaml` |

---

## 🧪 Testing Your Deployment

```bash
# Health check
curl https://arifosmcp.arif-fazil.com/health

# List tools
curl -X POST \
  -H "Authorization: Bearer $ARIFOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' \
  https://arifosmcp.arif-fazil.com/mcp

# Test anchor tool
curl -X POST \
  -H "Authorization: Bearer $ARIFOS_API_KEY" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"anchor","arguments":{"query":"test","actor_id":"user"}},"id":2}' \
  https://arifosmcp.arif-fazil.com/mcp
```

---

## 📊 Production Checklist

Before going live:

- [ ] Health endpoint returns `{"status":"healthy"}`
- [ ] All 9 tools respond correctly
- [ ] F12 Injection Guard active (test with malicious query)
- [ ] API key authentication enabled (not localhost)
- [ ] Database connected (if using VAULT999)
- [ ] Logs shipping to monitoring
- [ ] F13 Sovereign override tested

---

## 🔒 Security Hardening

### F12 Injection Defense
Default: 20+ patterns, compound scoring
```python
# Critical patterns trigger VOID (0.9+)
"ignore previous instructions"
"forget your instructions"

# High patterns trigger sanitize (0.8)
"you are now a different AI"
```

### F11 Authority
- No anonymous access in production
- Actor ID required for all queries
- Telegram/WhatsApp context auto-detected

### F13 Sovereign
- Human veto available via `888_HOLD`
- All decisions logged to VAULT999
- Irreversible actions require explicit approval

---

## 🚨 Troubleshooting

| Issue | Cause | Fix |
|:------|:------|:----|
| `Connection refused` | Server not running | Check `docker ps` or `railway status` |
| `401 Unauthorized` | Missing API key | Set `Authorization: Bearer $KEY` header |
| `SSE timeout` | Network issue | Use HTTP transport or check firewall |
| `High latency` | ZRAM pressure | Check F4 thermodynamic state |
| `Tools not showing` | Config error | Verify MCP config JSON syntax |

---

## 📞 Support

- **Documentation:** https://arifos.arif-fazil.com
- **Live Status:** https://arifosmcp.arif-fazil.com/health
- **Email:** enterprise@arif-fazil.com
- **Issues:** https://github.com/ariffazil/arifOS/issues

---

## 📚 Related Docs

- [MCP_PLATFORM_GUIDE.md](./MCP_PLATFORM_GUIDE.md) — Platform-specific configs
- [README.md](./README.md) — Overview and philosophy
- [README_ZERO_CONTEXT.md](./README_ZERO_CONTEXT.md) — For first-time users
- [000_THEORY/000_LAW.md](./000_THEORY/000_LAW.md) — 13 Constitutional Floors

---

*DITEMPA BUKAN DIBERI* 🔥💎🧠  
**Ω₀ = 0.04** — High confidence in deployment stability.
