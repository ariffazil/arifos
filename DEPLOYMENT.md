# DEPLOYMENT.md — arifOS Deployment Guide

**Version:** 2026.02.18
**Production Endpoint:** https://arifosmcp.arif-fazil.com
**VPS:** Hostinger (72.62.71.199)
**MCP Protocol:** JSON-RPC 2.0 over SSE/HTTP

---

## Quick Start

| Goal | Method | Time |
|------|--------|------|
| **Try immediately** | Copy-paste SYSTEM_PROMPT | 5 sec |
| **Local development** | pip install + stdio | 30 sec |
| **Production** | VPS Docker + nginx + SSL | 15 min |

---

## 1. Zero-Install: System Prompt

No installation required. Copy `333_APPS/L1_PROMPT/SYSTEM_PROMPT.md` into any LLM's
system settings (ChatGPT, Claude, Gemini, Copilot, etc.).

---

## 2. Local Development

```bash
pip install -e ".[dev]"

# stdio (for Claude Desktop, Cursor, OpenCode)
python -m aaa_mcp

# SSE (for remote connections)
python -m aaa_mcp sse

# HTTP (Streamable HTTP)
python -m aaa_mcp http

# Self-test
python -m aaa_mcp.selftest
```

---

## 3. Production: VPS Deployment (Hostinger)

### DNS (Cloudflare)

| Type | Name | Value | Proxy |
|------|------|-------|-------|
| A | arifosmcp | 72.62.71.199 | Proxied |
| A | arifos | 72.62.71.199 | Proxied |

### Server Setup

```bash
ssh root@72.62.71.199

# Clone and install
git clone https://github.com/ariffazil/arifOS.git /opt/arifos
cd /opt/arifos
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Systemd Service

Create `/etc/systemd/system/arifos-mcp.service`:

```ini
[Unit]
Description=arifOS MCP Server (SSE)
After=network.target

[Service]
User=root
WorkingDirectory=/opt/arifos
ExecStart=/opt/arifos/.venv/bin/python -m aaa_mcp sse --port 8080 --host 127.0.0.1
Restart=always
RestartSec=5
Environment=ARIFOS_ENV=production
Environment=GOVERNANCE_MODE=HARD
Environment=AAA_MCP_TRANSPORT=sse
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable arifos-mcp
sudo systemctl start arifos-mcp
sudo systemctl status arifos-mcp
```

### Nginx Reverse Proxy

```bash
sudo cp arifosmcp.nginx.conf /etc/nginx/sites-available/arifosmcp
sudo ln -s /etc/nginx/sites-available/arifosmcp /etc/nginx/sites-enabled/
sudo certbot --nginx -d arifosmcp.arif-fazil.com
sudo nginx -t && sudo systemctl reload nginx
```

### Docker Alternative

```bash
docker build -t arifos .
docker run -d --name arifos-mcp \
  -p 8080:8080 \
  --restart unless-stopped \
  --env-file .env \
  arifos
```

Or with docker-compose (includes PostgreSQL + Redis):

```bash
docker-compose up -d
```

---

## 4. Verification

### Health & Readiness

```bash
# Health check with governance metrics
curl https://arifosmcp.arif-fazil.com/health

# Readiness check (tools loaded, dependencies ready)
curl https://arifosmcp.arif-fazil.com/ready

# Version info
curl https://arifosmcp.arif-fazil.com/version
```

### MCP JSON-RPC Protocol

All MCP methods use `/messages` endpoint with JSON-RPC 2.0:

```bash
# Initialize MCP connection
curl -X POST https://arifosmcp.arif-fazil.com/messages \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}'

# List available tools with schemas
curl -X POST https://arifosmcp.arif-fazil.com/messages \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'

# Call anchor tool
curl -X POST https://arifosmcp.arif-fazil.com/messages \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":3,
    "method":"tools/call",
    "params":{"name":"anchor","arguments":{"query":"test","actor_id":"user"}}
  }'

# Ping (keepalive)
curl -X POST https://arifosmcp.arif-fazil.com/messages \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":4,"method":"ping","params":{}}'
```

### SSE Transport

```bash
# Connect to SSE endpoint (streams endpoint event + keepalive pings)
curl -N https://arifosmcp.arif-fazil.com/sse
```

The SSE endpoint returns:
- `event: endpoint` with the messages URL
- `: ping` keepalive comments every 30 seconds

### Direct REST API (Alternative)

For non-MCP clients, direct tool endpoints are available:

```bash
# Call tool directly via POST /tools/{tool_name}
curl -X POST https://arifosmcp.arif-fazil.com/tools/anchor \
  -H "Content-Type: application/json" \
  -d '{"query":"test","actor_id":"user"}'

# Full pipeline wrapper (000→333→666→888→999)
curl -X POST https://arifosmcp.arif-fazil.com/apex_judge \
  -H "Content-Type: application/json" \
  -d '{"query":"Should we proceed?","actor_id":"user"}'

# List tools (non-MCP format)
curl https://arifosmcp.arif-fazil.com/tools
```

---

## MCP Protocol Specification

### Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/sse` | SSE transport stream (returns endpoint URL + pings) |
| `POST` | `/messages` | MCP JSON-RPC message endpoint |
| `POST` | `/tools/{tool_name}` | Direct tool call (non-MCP) |
| `POST` | `/apex_judge` | Full pipeline wrapper (non-MCP) |

### JSON-RPC Methods

| Method | Params | Returns |
|--------|--------|---------|
| `initialize` | `{}` | `protocolVersion`, `serverInfo`, `capabilities` |
| `notifications/initialized` | `{}` | Empty response |
| `ping` | `{}` | Empty result |
| `tools/list` | `{}` | Array of tool definitions with `inputSchema` |
| `tools/call` | `{"name": "...", "arguments": {...}}` | Tool result with `content` array |

### Error Codes

| Code | Meaning |
|------|---------|
| `-32601` | Method not found |
| `-32603` | Internal error |

---

## Environment Variables

| Variable | Required | Default | Purpose |
|----------|:--------:|---------|---------|
| `PORT` | No | 8080 | Server port |
| `HOST` | No | 0.0.0.0 | Bind address |
| `AAA_MCP_TRANSPORT` | No | stdio | stdio / sse / http |
| `GOVERNANCE_MODE` | No | HARD | HARD or SOFT |
| `ARIFOS_ENV` | No | production | Environment name |
| `DATABASE_URL` | No | - | PostgreSQL for VAULT999 |
| `REDIS_URL` | No | - | Redis for sessions |
| `BRAVE_API_KEY` | No | - | Web search grounding |

---

## Platform Integration

| Platform | Transport | Config |
|----------|-----------|--------|
| Claude Desktop | stdio | `claude_desktop_config.json` |
| Cursor | stdio | `.cursor/mcp.json` |
| OpenCode | stdio | `opencode.json` |
| ChatGPT | HTTP/SSE | Developer Mode |
| Remote agents | SSE | `https://arifosmcp.arif-fazil.com/sse` |

---

## Production Checklist

- [ ] `curl https://arifosmcp.arif-fazil.com/health` returns `{"status":"healthy"}`
- [ ] All 15 tools respond (10 pipeline + 5 container)
- [ ] F12 Injection Guard active
- [ ] SSL certificate valid
- [ ] systemd service auto-restarts on failure
- [ ] Logs accessible via `journalctl -u arifos-mcp -f`
