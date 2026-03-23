#!/bin/bash
# Cron Recovery Script
# Emergency recovery when cron jobs fail

set -euo pipefail

# Source environment
source /root/.env.openclaw 2>/dev/null || true

TELEGRAM_CHAT_ID="267378578"
LOG_FILE="/var/log/openclaw/cron-recovery.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

send_telegram() {
    local message="$1"
    if [[ -n "${TELEGRAM_BOT_TOKEN:-}" ]]; then
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d "chat_id=$TELEGRAM_CHAT_ID" \
            -d "text=$message" \
            -d "parse_mode=Markdown" \
            > /dev/null 2>&1 || true
    fi
}

# Recovery actions
recover_gateway() {
    log "Attempting gateway recovery..."
    
    # Check if gateway is running
    if pgrep -f "openclaw gateway" > /dev/null; then
        log "Gateway is running, restarting..."
        pkill -f "openclaw gateway" || true
        sleep 2
    fi
    
    # Start gateway
    if command -v openclaw &> /dev/null; then
        nohup openclaw gateway > /var/log/openclaw/gateway.log 2>&1 &
        sleep 5
        
        if pgrep -f "openclaw gateway" > /dev/null; then
            log "Gateway restarted successfully"
            send_telegram "✅ Gateway recovered successfully"
            return 0
        fi
    fi
    
    log "Gateway recovery failed"
    return 1
}

recover_api_keys() {
    log "Attempting API key recovery..."
    
    # Check if backup env exists
    local backup_env="/root/.env-backup-20260208/.env"
    if [[ -f "$backup_env" ]]; then
        log "Restoring from backup: $backup_env"
        cp "$backup_env" /root/.env.openclaw
        log "API keys restored from backup"
        send_telegram "⚠️ API keys restored from backup"
        return 0
    fi
    
    # Check if master env exists
    if [[ -f "/root/.env.master" ]]; then
        log "Restoring from master env"
        cp /root/.env.master /root/.env.openclaw
        log "API keys restored from master"
        send_telegram "⚠️ API keys restored from master"
        return 0
    fi
    
    log "No backup env files found"
    return 1
}

recover_cron_jobs() {
    log "Attempting cron jobs recovery..."
    
    local jobs_file="/root/.openclaw/cron/jobs.json"
    local backup_dir="/root/.openclaw/cron/backups"
    
    # Find latest backup
    if [[ -d "$backup_dir" ]]; then
        local latest_backup
        latest_backup=$(ls -t "$backup_dir"/*.json 2>/dev/null | head -1)
        
        if [[ -n "$latest_backup" ]]; then
            log "Restoring cron jobs from: $latest_backup"
            cp "$latest_backup" "$jobs_file"
            log "Cron jobs restored"
            send_telegram "✅ Cron jobs restored from backup"
            return 0
        fi
    fi
    
    log "No cron jobs backup found"
    return 1
}

# Main recovery
main() {
    local recovery_type="${1:-all}"
    
    log "=== Cron Recovery Started ($recovery_type) ==="
    send_telegram "🚨 Starting cron recovery: $recovery_type"
    
    local failed=0
    
    case "$recovery_type" in
        gateway)
            recover_gateway || ((failed++))
            ;;
        api-keys)
            recover_api_keys || ((failed++))
            ;;
        cron-jobs)
            recover_cron_jobs || ((failed++))
            ;;
        all|*)
            recover_api_keys || true  # Try but don't fail
            recover_gateway || ((failed++))
            recover_cron_jobs || true  # Try but don't fail
            ;;
    esac
    
    if [[ $failed -eq 0 ]]; then
        log "=== Recovery Successful ==="
        send_telegram "✅ Cron recovery completed successfully"
    else
        log "=== Recovery Failed ==="
        send_telegram "❌ Cron recovery failed - manual intervention required"
        exit 1
    fi
}

main "$@"