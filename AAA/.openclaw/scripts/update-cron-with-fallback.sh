#!/bin/bash
# Update existing cron jobs to use fallback models

set -euo pipefail

JOBS_FILE="/root/.openclaw/cron/jobs.json"
BACKUP_FILE="/root/.openclaw/cron/jobs.json.bak.$(date +%s)"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Backup current jobs
cp "$JOBS_FILE" "$BACKUP_FILE"
log "Backup created: $BACKUP_FILE"

# Update isolated jobs to include model fallback logic
# This modifies the job payload to include model specification

log "Updating cron jobs with fallback models..."

# Read current jobs
jobs=$(cat "$JOBS_FILE")

# Update each isolated job to specify multiple model options
echo "$jobs" | jq '
  .jobs |= map(
    if .sessionTarget == "isolated" then
      .payload.modelPriority = ["gemini/gemini-2.0-flash", "openai/gpt-4o", "anthropic/claude-3-5-sonnet-20241022"]
      | .payload.fallbackOnError = true
    else
      .
    end
  )
' > "$JOBS_FILE.tmp"

mv "$JOBS_FILE.tmp" "$JOBS_FILE"

log "Cron jobs updated with fallback configuration"
log "Models will fallback in order: Gemini → OpenAI → Anthropic"

# Show updated jobs
echo ""
echo "Updated isolated jobs:"
openclaw cron list | grep -E "(isolated|Name)" || true