#!/bin/bash
set -e
LOG_FILE="/tmp/arifos-deploy.log"
# Inside the webhook container, /srv/arifOS is mounted at /usr/src/app
REPO_PATH="/usr/src/app"
COMMIT_ID="$1"
log() { echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE; }
log "Starting arifOS auto-deploy..."
log "Commit: $COMMIT_ID"
cd $REPO_PATH
git stash || true
git pull origin main
docker compose -f docker-compose.yml up -d --no-deps --build arifosmcp
sleep 10
if curl -fsS http://arifosmcp_server:8080/health >/dev/null 2>&1; then
    log "Deployment successful! Commit: $COMMIT_ID"
else
    log "Health check failed after deploy!"
    exit 1
fi
