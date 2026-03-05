#!/bin/bash
set -e
LOG_FILE="/tmp/arifos-deploy.log"
COMMIT_ID="$1"
log() { echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE; }

log "Starting arifOS auto-deploy for commit: $COMMIT_ID"

# git not installed in webhook container — run it via a temp alpine container
# with SSH keys mounted from host (docker.sock is available)
docker run --rm \
  -v /srv/arifOS:/repo \
  -v /home/ariffazil/.ssh:/root/.ssh:ro \
  -e GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" \
  alpine sh -c "apk add -q git openssh-client && git -C /repo stash || true && git -C /repo pull origin main"

log "Git pull complete"

# Rebuild and restart MCP server
docker compose -f /srv/arifOS/docker-compose.yml up -d --no-deps --build arifosmcp

sleep 10
if curl -fsS http://arifosmcp_server:8080/health >/dev/null 2>&1; then
    log "Deployment successful! Commit: $COMMIT_ID"
else
    log "Health check failed after deploy!"
    exit 1
fi
