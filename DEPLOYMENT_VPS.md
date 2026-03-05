# Phase 4: VPS Commissioning and Deployment

## Summary

The thermodynamic cage is hardened and wired. This guide deploys to sovereign infrastructure.

## Quick Start

```bash
# 1. Build
docker-compose -f docker-compose.vps.yml build

# 2. Deploy
git pull origin main
docker-compose up -d

# 3. Verify
curl http://localhost:8080/health
python3 tests/entropy_audit_minimal.py
```

## Pre-Flight

- [ ] Core cage committed
- [ ] MCP gateway wired  
- [ ] Audit passes (6/6)

## Success Criteria

- SEAL rate: 50-60%
- All 6 thermodynamic tests pass
- No server crashes on physics exceptions

**Akal memerintah, amanah mengunci.**

---

## Automated Migration Script (Scorched Earth to Unified AI-First Stack)

*Note: This script destroys existing Coolify deployments and Docker networks. Run with caution under 888_HOLD.*

```bash
#!/bin/bash
# VPS Score Earth & AI-First Deployment Script
# WARNING: This script will DESTROY existing Coolify deployments and Docker networks.
# RUN WITH CAUTION: This explicitly requires user approval under 888_HOLD.

set -e

echo "================================================="
echo "   arifOS: Initializing VPS AI-First Trinity   "
echo "================================================="

echo "1. Stopping legacy native services (BGE embeddings)..."
systemctl stop arifos-embeddings || true
systemctl disable arifos-embeddings || true

echo "2. Tearing down Coolify (Scorched Earth)..."
# Stop all coolify related containers
docker ps -a --filter "name=coolify" -q | xargs -r docker stop
docker ps -a --filter "name=coolify" -q | xargs -r docker rm -f

# Stop lingering postgres and redis instances outside the new unified stack
docker ps -a --filter "name=postgres-q0" -q | xargs -r docker stop
docker ps -a --filter "name=postgres-q0" -q | xargs -r docker rm -f
docker ps -a --filter "name=redis-q0" -q | xargs -r docker stop
docker ps -a --filter "name=redis-q0" -q | xargs -r docker rm -f

echo "3. Pruning unused Docker networks and images..."
docker network prune -f
docker image prune -a -f --filter "until=24h"

echo "4. Setting up new unified directories and Webhooks..."
mkdir -p /opt/arifos/data/core
mkdir -p /opt/arifos/data/qdrant
mkdir -p /opt/arifos/data/postgres
mkdir -p /opt/arifos/data/redis
mkdir -p /opt/arifos/data/ollama
mkdir -p /opt/arifos/letsencrypt
touch /opt/arifos/letsencrypt/acme.json
chmod 600 /opt/arifos/letsencrypt/acme.json

# Install Webhook handlers locally to /opt/arifos so docker can mount them
cp /srv/arifOS/deployment/hooks.json /opt/arifos/hooks.json
cp /srv/arifOS/deployment/deploy_from_git.sh /opt/arifos/deploy_from_git.sh
chmod +x /opt/arifos/deploy_from_git.sh

echo "5. Deploying the AI-First Trinity Stack..."
cd /srv/arifOS
git pull origin main
docker compose -f docker-compose.yml up -d --build

echo "6. Verifying Services..." -n
sleep 10
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | tee /tmp/vps_unified_status.txt

echo "7. Configuring UFW Firewall for strictly 80, 443, 22..."
if command -v ufw >/dev/null 2>&1; then
    # WARNING: Do not lock ourselves out
    ufw allow 22/tcp
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw reload || true
    echo "UFW rules applied."
fi

echo "================================================="
echo "   arifOS AI-First VPS Migration Complete!     "
echo "================================================="
```