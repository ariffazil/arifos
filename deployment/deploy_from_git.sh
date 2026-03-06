#!/bin/bash
# arifOS Auto-Deploy Hook
# Triggered by GitHub webhook on push to main

set -e

LOG_FILE="/var/log/arifos-deploy.log"
REPO_DIR="/srv/arifOS"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Deployment started ==="
log "Trigger: GitHub webhook push to main"

# Pull latest code
cd "$REPO_DIR"
log "Pulling latest code..."
git fetch origin
git reset --hard origin/main

# Rebuild and restart
docker compose build arifosmcp
docker compose up -d arifosmcp

# Health check
log "Waiting for health check..."
sleep 10
HEALTH=$(curl -fsS http://localhost:8080/health | jq -r '.status' 2>/dev/null || echo "unknown")

if [ "$HEALTH" = "healthy" ]; then
    log "✅ Deployment successful - MCP server healthy"
else
    log "⚠️ Deployment warning - health check returned: $HEALTH"
fi

log "=== Deployment complete ==="
