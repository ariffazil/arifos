#!/bin/bash
# Cron Health Monitor for OpenClaw
# Monitors cron job execution and sends alerts on failures

set -euo pipefail

# Configuration
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
TELEGRAM_CHAT_ID="267378578"
CRON_JOBS_FILE="/root/.openclaw/cron/jobs.json"
HEALTH_LOG="/var/log/openclaw/cron-health.log"
ALERT_COOLDOWN_FILE="/tmp/openclaw/.alert-cooldown"
ALERT_COOLDOWN_SECONDS=300  # 5 minutes between duplicate alerts

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Ensure log directory exists
mkdir -p "$(dirname "$HEALTH_LOG")"
mkdir -p "$(dirname "$ALERT_COOLDOWN_FILE")"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$HEALTH_LOG"
}

# Send Telegram alert
send_alert() {
    local message="$1"
    local severity="${2:-info}"
    
    # Check cooldown
    local alert_hash
    alert_hash=$(echo "$message" | md5sum | cut -d' ' -f1)
    local cooldown_file="$ALERT_COOLDOWN_FILE/$alert_hash"
    
    if [[ -f "$cooldown_file" ]]; then
        local last_alert
        last_alert=$(stat -c %Y "$cooldown_file" 2>/dev/null || echo 0)
        local now
        now=$(date +%s)
        local diff=$((now - last_alert))
        
        if [[ $diff -lt $ALERT_COOLDOWN_SECONDS ]]; then
            log "Alert on cooldown (${diff}s remaining), skipping: $message"
            return 0
        fi
    fi
    
    # Build emoji prefix based on severity
    local emoji="ℹ️"
    case "$severity" in
        critical) emoji="🚨" ;;
        warning) emoji="⚠️" ;;
        error) emoji="❌" ;;
        success) emoji="✅" ;;
    esac
    
    local full_message="$emoji *Cron Health Alert*
\`$(date '+%Y-%m-%d %H:%M')\`

$message

_Status_: \`$severity\`
_Host_: \`$(hostname)\`"
    
    # Send via Telegram
    if [[ -n "$TELEGRAM_BOT_TOKEN" ]]; then
        curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
            -d "chat_id=$TELEGRAM_CHAT_ID" \
            -d "text=$full_message" \
            -d "parse_mode=MarkdownV2" \
            -d "disable_notification=false" > /dev/null 2>&1 || {
            log "${RED}Failed to send Telegram alert${NC}"
        }
    fi
    
    # Update cooldown
    touch "$cooldown_file"
    log "Alert sent: $message"
}

# Check if gateway is running
check_gateway() {
    # Check for both "openclaw gateway" and "openclaw-gateway" process names
    if pgrep -f "openclaw.gateway" > /dev/null 2>&1 || pgrep -x "openclaw-gateway" > /dev/null 2>&1; then
        log "${GREEN}Gateway: RUNNING${NC}"
        return 0
    else
        log "${RED}Gateway: NOT RUNNING${NC}"
        send_alert "OpenClaw Gateway is not running" "critical"
        return 1
    fi
}

# Check cron jobs status
check_cron_jobs() {
    if [[ ! -f "$CRON_JOBS_FILE" ]]; then
        log "${RED}Cron jobs file not found: $CRON_JOBS_FILE${NC}"
        return 1
    fi
    
    local failed_jobs=0
    local now
    now=$(date +%s)
    
    # Parse jobs.json and check each job
    local jobs
    jobs=$(cat "$CRON_JOBS_FILE")
    
    # Check for jobs that failed recently
    local failed_list=""
    
    while IFS= read -r job; do
        local job_id
        job_id=$(echo "$job" | jq -r '.id' 2>/dev/null)
        local job_name
        job_name=$(echo "$job" | jq -r '.name' 2>/dev/null)
        local last_status
        last_status=$(echo "$job" | jq -r '.state.lastStatus' 2>/dev/null || echo "unknown")
        local last_run
        last_run=$(echo "$job" | jq -r '.state.lastRunAtMs' 2>/dev/null || echo "0")
        local last_error
        last_error=$(echo "$job" | jq -r '.state.lastError' 2>/dev/null || echo "")
        
        # Check if job failed
        if [[ "$last_status" == "failed" ]]; then
            ((failed_jobs++))
            failed_list="${failed_list}- $job_name\n"
            log "${RED}Job FAILED: $job_name ($job_id)${NC}"
            
            if [[ -n "$last_error" && "$last_error" != "null" ]]; then
                log "  Error: $last_error"
            fi
        fi
        
        # Check for stuck jobs (no run in 2x expected interval)
        # This is a simplified check - in production, parse the schedule properly
        local hours_since_run=$(( (now - last_run/1000) / 3600 ))
        
        if [[ $hours_since_run -gt 25 && "$last_status" != "skipped" ]]; then
            log "${YELLOW}Job potentially stuck: $job_name (last run ${hours_since_run}h ago)${NC}"
        fi
    done < <(echo "$jobs" | jq -c '.jobs[]' 2>/dev/null)
    
    if [[ $failed_jobs -gt 0 ]]; then
        send_alert "$failed_jobs cron job(s) failed:
${failed_list}" "error"
        return 1
    fi
    
    log "${GREEN}All cron jobs: OK${NC}"
    return 0
}

# Check API key status
check_api_keys() {
    local validator_output
    validator_output=$(/root/.openclaw/scripts/api-key-validator.sh 2>&1)
    local exit_code=$?
    
    if [[ $exit_code -eq 2 ]]; then
        # Critical - no valid providers
        send_alert "CRITICAL: No valid AI providers available!
Cron jobs may fail." "critical"
        return 1
    elif [[ $exit_code -ne 0 ]]; then
        log "${YELLOW}Some API keys invalid, but fallback available${NC}"
    fi
    
    # Extract primary provider from output
    local primary
    primary=$(echo "$validator_output" | grep "^PRIMARY:" | cut -d' ' -f2)
    
    if [[ "$primary" == "NONE_ALL_FAILED" ]]; then
        return 1
    fi
    
    log "${GREEN}Primary provider: $primary${NC}"
    return 0
}

# Check disk space
check_disk_space() {
    local usage
    usage=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
    
    if [[ $usage -gt 90 ]]; then
        log "${RED}Disk usage critical: ${usage}%${NC}"
        send_alert "Disk space critical: ${usage}% used" "critical"
        return 1
    elif [[ $usage -gt 80 ]]; then
        log "${YELLOW}Disk usage warning: ${usage}%${NC}"
        send_alert "Disk space warning: ${usage}% used" "warning"
    else
        log "${GREEN}Disk usage: ${usage}%${NC}"
    fi
    
    return 0
}

# Check memory
check_memory() {
    local mem_usage
    mem_usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
    
    if [[ $mem_usage -gt 90 ]]; then
        log "${RED}Memory usage critical: ${mem_usage}%${NC}"
        send_alert "Memory usage critical: ${mem_usage}%" "critical"
        return 1
    elif [[ $mem_usage -gt 80 ]]; then
        log "${YELLOW}Memory usage warning: ${mem_usage}%${NC}"
    else
        log "${GREEN}Memory usage: ${mem_usage}%${NC}"
    fi
    
    return 0
}

# Self-heal: Restart gateway if needed
self_heal() {
    if ! check_gateway; then
        log "Attempting self-heal: Restarting OpenClaw Gateway..."
        
        # Try to restart gateway
        if command -v systemctl &> /dev/null; then
            systemctl restart openclaw 2>/dev/null || true
        fi
        
        # Alternative restart methods - kill both naming variants
        pkill -f "openclaw.gateway" 2>/dev/null || true
        pkill -x "openclaw-gateway" 2>/dev/null || true
        sleep 2
        
        # Start gateway (if configured to auto-start)
        if [[ -f /etc/systemd/system/openclaw.service ]]; then
            systemctl start openclaw 2>/dev/null || true
        fi
        
        sleep 3
        
        if check_gateway; then
            log "${GREEN}Self-heal successful: Gateway restarted${NC}"
            send_alert "Gateway auto-restarted successfully" "success"
        else
            log "${RED}Self-heal failed: Gateway still down${NC}"
            send_alert "CRITICAL: Gateway auto-restart failed" "critical"
            return 1
        fi
    fi
    
    return 0
}

# Main monitoring function
main() {
    log "=== Cron Health Monitor Started ==="
    
    local overall_status=0
    
    # Run all checks
    check_disk_space || overall_status=1
    check_memory || overall_status=1
    check_api_keys || overall_status=1
    
    # Gateway check with self-heal
    if ! check_gateway; then
        self_heal || overall_status=1
    fi
    
    check_cron_jobs || overall_status=1
    
    log "=== Cron Health Monitor Complete ==="
    
    return $overall_status
}

# Run main
main "$@"