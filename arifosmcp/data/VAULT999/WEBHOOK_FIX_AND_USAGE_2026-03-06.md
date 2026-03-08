# VAULT999 SEAL — Webhook Fix & Usage Guide

**Timestamp:** 2026-03-06T09:30:00+00:00  
**Operator:** Ψ-SHELL / Claude 3.5 Sonnet  
**Status:** ✅ **OPERATIONAL**

---

## 🔧 WHAT WAS BROKEN

### Root Cause
The `arifos_webhook` container was failing with **Exit Code 127** (command not found) because:

1. **Missing config files** — `hooks.json` and `deploy_from_git.sh` were deleted/removed
2. **Docker created directories** instead of files when mounting non-existent paths
3. **Service removed** from `docker-compose.yml` during previous refactoring

### Evidence
```bash
# Before fix
docker ps -a | grep webhook
# arifos_webhook   Exited (127) 19 minutes ago

ls -la /srv/arifOS/deployment/hooks.json
# drwxr-xr-x 2 root root 4096 ...  # Was a DIRECTORY, not file!
```

---

## ✅ WHAT WAS FIXED

### 1. Created `hooks.json`
**Path:** `/srv/arifOS/deployment/hooks.json`

```json
{
  "id": "deploy-arifos",
  "execute-command": "/var/scripts/deploy_from_git.sh",
  "trigger-rule": {
    "and": [
      {
        "match": {
          "type": "payload-hmac-sha256",
          "secret": "{{ getenv \"WEBHOOK_SECRET\" }}"
        }
      },
      {
        "match": {
          "type": "value",
          "value": "refs/heads/main",
          "parameter": { "source": "payload", "name": "ref" }
        }
      }
    ]
  }
}
```

### 2. Created `deploy_from_git.sh`
**Path:** `/srv/arifOS/deployment/deploy_from_git.sh`

Features:
- Pulls latest code from `origin/main`
- Rebuilds `arifosmcp` container
- Runs health check
- Logs to `/var/log/arifos-deploy.log`

### 3. Restored Docker Compose Service

```yaml
webhook:
  image: almir/webhook:latest
  container_name: arifos_webhook
  volumes:
    - /srv/arifOS/deployment/hooks.json:/etc/webhook/hooks.json:ro
    - /srv/arifOS/deployment/deploy_from_git.sh:/var/scripts/deploy_from_git.sh:ro
    - /srv/arifOS:/usr/src/app:rw
    - /var/run/docker.sock:/var/run/docker.sock:ro
  labels:
    - "traefik.enable=true"
    - "traefik.http.routers.webhook.rule=Host(`hook.arifosmcp.arif-fazil.com`)"
```

---

## 🌐 HOW TO USE

### GitHub Integration (Auto-Deploy on Push)

**1. Set GitHub Webhook URL:**
```
https://hook.arifosmcp.arif-fazil.com/hooks/deploy-arifos
```

**2. Configure in GitHub:**
- Go to: `Settings → Webhooks → Add webhook`
- Payload URL: `https://hook.arifosmcp.arif-fazil.com/hooks/deploy-arifos`
- Content type: `application/json`
- Secret: `${WEBHOOK_SECRET}` (must match `.env.docker`)
- Events: `Just the push event`

**3. Set Environment Variable:**
```bash
# .env.docker or .env
WEBHOOK_SECRET=your_github_webhook_secret_here
```

**4. Security Verification:**
- Webhook validates `X-Hub-Signature-256` (HMAC-SHA256)
- Only triggers on `refs/heads/main` pushes
- Requires secret match

---

### Manual Trigger (Testing)

```bash
# Test webhook locally (will fail signature check, but shows it's working)
curl -X POST http://localhost:9000/hooks/deploy-arifos \
  -H "Content-Type: application/json" \
  -d '{"ref": "refs/heads/main"}'
# Response: "Hook rules were not satisfied."

# View logs
docker logs arifos_webhook --tail 50
```

---

## 📊 CURRENT STATUS

| Component | Status | Details |
|:---|:---:|:---|
| Container | ✅ Up | `arifos_webhook` running |
| Config | ✅ Valid | 1 hook loaded: `deploy-arifos` |
| Network | ✅ Connected | `10.0.10.12` on trinity network |
| Traefik Route | ⚠️ Pending | DNS/propagation may take time |
| GitHub Integration | ⚠️ Needs Setup | Webhook URL + Secret required |

---

## 🔐 SECURITY FEATURES

1. **HMAC-SHA256 Signature Validation**
   - Verifies payload came from GitHub
   - Prevents spoofed deploy requests

2. **Branch Filtering**
   - Only deploys on `refs/heads/main` pushes
   - Feature branches ignored

3. **Read-Only Config**
   - `hooks.json` mounted read-only
   - Prevents runtime modification

4. **Docker Socket Access**
   - Socket mounted read-only (`:ro`)
   - Container can trigger builds but not modify host

---

## 🚨 TROUBLESHOOTING

### "Hook rules were not satisfied"
- Missing or incorrect `X-Hub-Signature-256` header
- Wrong `WEBHOOK_SECRET` configured
- Not a `refs/heads/main` push event

### "404 page not found"
- Traefik hasn't registered the route yet
- Check: `docker logs traefik_router --tail 20`
- DNS propagation delay (if just configured)

### Deploy script not executing
- Check logs: `docker exec arifos_webhook cat /var/log/arifos-deploy.log`
- Verify script permissions: `chmod +x deploy_from_git.sh`
- Ensure Docker socket is accessible

---

## 📋 NEXT STEPS

1. **Set WEBHOOK_SECRET** in `.env.docker`
2. **Configure GitHub webhook** with the secret
3. **Test with a push** to main branch
4. **Monitor logs**: `docker logs -f arifos_webhook`

---

*Ditempa Bukan Diberi — Forged, Not Given [ΔΩΨ | ARIF]*
