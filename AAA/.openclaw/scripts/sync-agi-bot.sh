#!/bin/bash
# Sync script for AGI-bot repo to local memory
# Run this periodically to keep memory in sync with GitHub

REPO_URL="https://github.com/ariffazil/AGI-bot"
SYNC_DIR="$HOME/agi-bot-sync"
LOG_FILE="$HOME/.openclaw/agi-bot-sync.log"

echo "[$(date)] Starting AGI-bot sync..." >> "$LOG_FILE"

# Clone if not exists, pull if exists
if [ -d "$SYNC_DIR/.git" ]; then
    cd "$SYNC_DIR" && git pull origin main >> "$LOG_FILE" 2>&1
else
    git clone "$REPO_URL" "$SYNC_DIR" >> "$LOG_FILE" 2>&1
fi

# Fetch latest README as markdown reference
curl -s "https://raw.githubusercontent.com/ariffazil/AGI-bot/main/README.md" > "$SYNC_DIR/README-latest.md"

echo "[$(date)] Sync complete" >> "$LOG_FILE"
