# arifOS AAA MCP — DEPLOY DIRECTIVE
**Version:** v2026.03.24-FORGE  
**Authority:** Muhammad Arif bin Fazil (888_JUDGE)  
**Motto:** *Ditempa Bukan Diberi — Forged, Not Given*  
**Status:** CANONICAL VPS AUTO-DEPLOY DIRECTIVE

---

## AGENT SYSTEM DIRECTIVE

If you are an AI agent executing this deployment:

1. **You are the arifOS Deployment Architect.** Identity: `arif` (Sovereign).
2. **888 HOLD on any push/merge until:**
   - Secrets audit passes (no hardcoded tokens in committed files)
   - Self-test CI passes (`pytest AAA/tests/`)
   - Health endpoint responds `200` post-deploy
3. **F1 Amanah: Reversibility first.** Always verify you can rollback before proceeding.
4. **Never inject secrets inline.** Use file-backed secrets at `/opt/arifos/secrets/`.
5. **Working directory on VPS:** `/srv/arifosmcp/` maps to `AAA/` subtree of this repo.

---

## ARCHITECTURE CONTEXT

```
GitHub: ariffazil/arifOS
├── main branch       → MIND (canon, philosophy, core kernel)
├── aaa-mcp-induction → BODY (runtime, tools, deployment)
│   └── AAA/          → Maps to /srv/arifosmcp/ on VPS
│       ├── arifosmcp/runtime/server.py   ← PRIMARY ENTRYPOINT
│       ├── Dockerfile                     ← Production image
│       ├── docker-compose.yml             ← 16-container Trinity stack
│       └── Makefile                       ← Deployment commands

VPS: Hostinger (srv1325122.hstgr.cloud)
├── /srv/arifosmcp/   ← Live runtime (mirrors AAA/)
├── /opt/arifos/      ← Persistent data volumes
│   ├── secrets/      ← File-backed secrets (governance.secret)
│   ├── data/         ← Postgres, Redis, Qdrant, Grafana data
│   └── traefik/      ← acme.json (Let's Encrypt certs)

Endpoints:
├── https://arifosmcp.arif-fazil.com/health   ← Health check
├── https://arifosmcp.arif-fazil.com/mcp      ← MCP endpoint
├── https://arifosmcp.arif-fazil.com/a2a      ← A2A protocol
├── https://arifosmcp.arif-fazil.com/webmcp   ← WebMCP
├── https://monitor.arifosmcp.arif-fazil.com  ← Grafana
└── https://hook.arifosmcp.arif-fazil.com     ← Webhook autodeploy
```

---

## PHASE 000 — PRE-FLIGHT CHECKLIST

Run this before any deployment attempt:

```bash
# 1. Verify VPS access
ssh root@srv1325122.hstgr.cloud "docker ps --format 'table {{.Names}}\t{{.Status}}'"

# 2. Verify no secrets in compose file (F11 Guard)
grep -n "hf_\|sk-\|:AAE\|bot_token" /srv/arifosmcp/docker-compose.yml && echo "888 HOLD — secrets found" || echo "Clean"

# 3. Verify governance secret file exists
ls -la /opt/arifos/secrets/governance.secret && echo "F11 OK" || echo "888 HOLD — forge secrets first"

# 4. Verify .env.docker exists
ls -la /srv/arifosmcp/.env.docker && echo "Env OK" || echo "888 HOLD — copy .env.docker.example first"

# 5. Verify disk space (BGE-M3 needs ~2GB build space)
df -h / | awk 'NR==2{print "Free: "$4}'
```

**All 5 checks must pass before proceeding.**

---

## PHASE 111 — SECRET FORGE (First Deploy Only)

Run once on a fresh VPS or after secret rotation:

```bash
# Create secrets directory
sudo mkdir -p /opt/arifos/secrets
sudo chmod 700 /opt/arifos/secrets

# Forge governance secret (F11 Root of Trust)
openssl rand -hex 32 | sudo tee /opt/arifos/secrets/governance.secret > /dev/null
sudo chmod 600 /opt/arifos/secrets/governance.secret

# Verify
echo "Governance secret length: $(sudo wc -c < /opt/arifos/secrets/governance.secret) chars"

# Create .env.docker from template
cd /srv/arifosmcp
cp .env.docker.example .env.docker
chmod 600 .env.docker

# Inject required secrets into .env.docker (do NOT hardcode in docker-compose.yml)
# Edit manually or use sed:
# POSTGRES_PASSWORD — generate strong password
POSTGRES_PASS=$(openssl rand -hex 24)
sed -i "s/^POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=${POSTGRES_PASS}/" .env.docker

# GRAFANA_PASSWORD
GRAFANA_PASS=$(openssl rand -hex 16)
sed -i "s/^GRAFANA_PASSWORD=.*/GRAFANA_PASSWORD=${GRAFANA_PASS}/" .env.docker

# HF_TOKEN — from https://huggingface.co/settings/tokens (READ scope sufficient)
# sed -i "s/^HF_TOKEN=.*/HF_TOKEN=hf_your_token/" .env.docker

# TELEGRAM_BOT_TOKEN — from @BotFather
# sed -i "s/^TELEGRAM_BOT_TOKEN=.*/TELEGRAM_BOT_TOKEN=your_token/" .env.docker

# WEBHOOK_SECRET — for GitHub webhook auto-deploy
WEBHOOK_SEC=$(openssl rand -hex 32)
sed -i "s/^WEBHOOK_SECRET=.*/WEBHOOK_SECRET=${WEBHOOK_SEC}/" .env.docker

echo "Secrets forged. Verify with: grep -v '=$' .env.docker | grep -v '^#'"
```

---

## PHASE 444 — FIRST DEPLOY (Cold Start)

For first deploy or after full reforge:

```bash
cd /srv/arifosmcp

# Pull latest code
git fetch origin aaa-mcp-induction
git checkout aaa-mcp-induction
git pull --ff-only origin aaa-mcp-induction

# Create required data directories
sudo mkdir -p /opt/arifos/data/{postgres,redis,qdrant,ollama,grafana,prometheus,n8n,agent_zero,openclaw,evolution,stirling}
sudo mkdir -p /opt/arifos/traefik
sudo touch /opt/arifos/traefik/acme.json
sudo chmod 600 /opt/arifos/traefik/acme.json

# Build and start infrastructure first (fast services)
sudo docker compose --env-file .env.docker up -d traefik postgres redis qdrant

# Wait for postgres + redis health
echo "Waiting for infrastructure..."
sleep 15
sudo docker compose ps

# Build arifosmcp image (takes 10-15 min — BGE-M3 baked in)
export DOCKER_BUILDKIT=1
sudo docker compose --env-file .env.docker build --no-cache arifosmcp

# Start full stack
sudo docker compose --env-file .env.docker up -d

# Monitor startup
sudo docker logs -f arifosmcp_server --tail 50
```

---

## PHASE 555 — FAST REDEPLOY (Code Changes Only)

For routine code updates after first deploy:

```bash
cd /srv/arifosmcp

# Pull latest
git pull --ff-only origin aaa-mcp-induction

# Rebuild arifosmcp only (uses layer cache — ~2-3 min)
export DOCKER_BUILDKIT=1
sudo docker compose --env-file .env.docker up -d --build arifosmcp

# Health check (wait up to 75 seconds)
echo "Waiting for health..."
for i in $(seq 1 15); do
    if sudo docker exec arifosmcp_server curl -fsS http://localhost:8080/health > /dev/null 2>&1; then
        echo "✅ arifosmcp healthy after ${i}x5s"
        break
    fi
    echo "  Retry $i/15..."
    sleep 5
done

# Final status
sudo docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

**Equivalent Makefile command:**
```bash
make fast-deploy
```

---

## PHASE 666 — HOT RESTART (Config Changes Only)

For `.env.docker` changes or minor config tweaks only:

```bash
cd /srv/arifosmcp
sudo docker compose --env-file .env.docker restart arifosmcp
sleep 8
sudo docker exec arifosmcp_server curl -fsS http://localhost:8080/health
```

**Equivalent:**
```bash
make hot-restart
```

---

## PHASE 777 — FULL REFORGE (Dockerfile/Deps Changed)

For Dockerfile changes, requirements changes, or base image updates:

```bash
cd /srv/arifosmcp

# Prune old cache first
sudo docker system prune -f
sudo docker builder prune -f

# Full no-cache rebuild
export DOCKER_BUILDKIT=1
sudo docker compose --env-file .env.docker down arifosmcp
sudo docker rmi arifos/arifosmcp:latest 2>/dev/null || true
sudo docker compose --env-file .env.docker build --no-cache arifosmcp
sudo docker compose --env-file .env.docker up -d arifosmcp
```

**Equivalent:**
```bash
make reforge
```

---

## PHASE 888 — HEALTH AUDIT

Run after every deployment:

```bash
cd /srv/arifosmcp

echo "=== Container Status ==="
sudo docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'

echo ""
echo "=== Health Endpoint ==="
sudo docker exec arifosmcp_server curl -fsS http://localhost:8080/health | python3 -m json.tool 2>/dev/null

echo ""
echo "=== MCP Tools List ==="
sudo docker exec arifosmcp_server curl -fsS http://localhost:8080/tools 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Tools count: {len(d.get(\"tools\",d.get(\"result\",[])))}' if isinstance(d,dict) else f'Tools: {len(d)}')" 2>/dev/null || echo "Check /tools manually"

echo ""
echo "=== Resource Usage ==="
sudo docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}'

echo ""
echo "=== Recent Errors ==="
sudo docker logs arifosmcp_server --tail 20 2>&1 | grep -E "ERROR|CRITICAL|exception" || echo "No recent errors"
```

---

## PHASE 999 — ROLLBACK PROTOCOL

If health check fails post-deploy:

```bash
cd /srv/arifosmcp

# Option A: Restart last known-good container
sudo docker compose --env-file .env.docker restart arifosmcp

# Option B: Rollback to previous git commit
git log --oneline -5   # Find last good SHA
git stash              # Stash current changes
git checkout <GOOD_SHA>
make fast-deploy

# Option C: Emergency — full stack restart
sudo docker compose --env-file .env.docker down
sudo docker compose --env-file .env.docker up -d
```

---

## AUTO-DEPLOY VIA GITHUB ACTIONS

The `deploy-vps.yml` workflow handles auto-deploy on push to `aaa-mcp-induction`.

### Required GitHub Secrets
Set these in `ariffazil/arifOS` → Settings → Secrets → Actions:

| Secret | Value | Required |
|--------|-------|----------|
| `VPS_SSH_KEY` | Private SSH key for VPS access | 🔴 Required |
| `VPS_HOST` | VPS IP or hostname | 🔴 Required |
| `VPS_USER` | SSH username (e.g., `root`) | 🔴 Required |
| `VPS_SSH_PORT` | SSH port (default: 22) | 🟡 Optional |
| `VPS_TAILSCALE_IP` | Tailscale IP if using VPN | 🟡 Optional |
| `TS_AUTHKEY` | Tailscale auth key | 🟡 Optional |

### Trigger Auto-Deploy
```bash
# Via GitHub CLI
gh workflow run deploy-vps.yml --repo ariffazil/arifOS

# Or push to aaa-mcp-induction (auto-triggers)
git push origin aaa-mcp-induction
```

---

## WEBHOOK AUTO-DEPLOY (Always-On)

The `webhook` container on the VPS listens on `hook.arifosmcp.arif-fazil.com`.

Configure in GitHub: `ariffazil/arifOS` → Settings → Webhooks:
```
Payload URL:  https://hook.arifosmcp.arif-fazil.com/hooks/deploy
Content type: application/json
Secret:       [value of WEBHOOK_SECRET from .env.docker]
Events:       Just the push event
Branch:       aaa-mcp-induction
```

The webhook calls `/srv/arifosmcp/infrastructure/deploy_from_git.sh` which runs `make fast-deploy`.

---

## DECISION TREE — WHICH COMMAND?

```
DID YOU CHANGE...?                          COMMAND               TIME
─────────────────────────────────────────────────────────────────────
Dockerfile or requirements/pyproject       make reforge           10-15 min
Core Python code (arifosmcp/, core/)       make fast-deploy        2-3 min  
Config only (.env.docker, yaml)            make hot-restart           ~10s
Just want to check status                  make status               instant
Not sure what changed                      make strategy             ~30s
Want autonomous decision                   make auto-deploy          smart
```

---

## ENVIRONMENT VARIABLES REFERENCE

### Minimum Required (in .env.docker)
```env
PORT=8080
HOST=0.0.0.0
AAA_MCP_TRANSPORT=http
ARIFOS_GOVERNANCE_SECRET_FILE=/opt/arifos/secrets/governance.secret
POSTGRES_PASSWORD=<generated>
POSTGRES_DB=arifos_vault
POSTGRES_USER=arifos_admin
GRAFANA_PASSWORD=<generated>
WEBHOOK_SECRET=<generated>
```

### LLM API Keys (optional, tool-gated)
```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
BRAVE_API_KEY=...
```

### External Service Tokens (in .env.docker, NOT docker-compose.yml)
```env
HF_TOKEN=hf_...
TELEGRAM_BOT_TOKEN=...
OPENCLAW_GATEWAY_TOKEN=<generated>
```

---

## 888 HOLD TRIGGERS

Auto-stop deployment if any of these are true:

| Condition | Action |
|-----------|--------|
| `grep -r 'hf_[a-zA-Z]' docker-compose.yml` returns hits | HOLD — rotate and clean |
| `grep -r 'sk-' docker-compose.yml` returns hits | HOLD — rotate and clean |
| Health check fails after 75s | HOLD — check logs, rollback |
| `tests/test_e2e.py` fails | HOLD — fix tests before deploy |
| `governance.secret` file missing | HOLD — run Phase 111 first |
| Free disk < 3GB | HOLD — prune docker cache |

---

*arifOS telemetry v2.1 | pipeline: 999 SEAL | floors: F1 F4 F7 F11 | confidence: CLAIM | P2: 1.0 | hold: CLEAR (post-secrets-rotation) | uncertainty: 0.04 | seal: DITEMPA BUKAN DIBERI*
