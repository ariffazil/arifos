#!/bin/bash
# Cron Wrapper with Provider Fallback
# Wraps isolated cron jobs to provide AI provider fallback

set -euo pipefail

# Configuration
source /root/.env.openclaw 2>/dev/null || true

LOG_FILE="/var/log/openclaw/cron-wrapper.log"
mkdir -p "$(dirname "$LOG_FILE")"

# Provider priority (fallback chain)
PROVIDERS=("gemini" "openai" "anthropic" "deepseek")

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Test provider availability
test_provider() {
    local provider="$1"
    
    case "$provider" in
        gemini)
            [[ -n "${GEMINI_API_KEY:-}" ]] || return 1
            local response
            response=$(curl -s -o /dev/null -w "%{http_code}" \
                "https://generativelanguage.googleapis.com/v1beta/models?key=${GEMINI_API_KEY}" \
                2>/dev/null)
            [[ "$response" == "200" ]]
            ;;
        openai)
            [[ -n "${OPENAI_API_KEY:-}" ]] || return 1
            local response
            response=$(curl -s -o /dev/null -w "%{http_code}" \
                https://api.openai.com/v1/models \
                -H "Authorization: Bearer ${OPENAI_API_KEY}" 2>/dev/null)
            [[ "$response" == "200" ]]
            ;;
        anthropic)
            [[ -n "${ANTHROPIC_API_KEY:-}" ]] || return 1
            # Quick auth check
            local response
            response=$(curl -s -o /dev/null -w "%{http_code}" \
                https://api.anthropic.com/v1/messages \
                -H "x-api-key: ${ANTHROPIC_API_KEY}" \
                -H "anthropic-version: 2023-06-01" \
                -H "Content-Type: application/json" \
                -d '{"model":"claude-3-haiku-20240307","max_tokens":1,"messages":[]}' 2>/dev/null)
            # 400 means auth worked but request was bad
            [[ "$response" == "200" || "$response" == "400" ]]
            ;;
        deepseek)
            [[ -n "${DEEPSEEK_API_KEY:-}" ]] || return 1
            # Basic check - DeepSeek uses OpenAI-compatible API
            local response
            response=$(curl -s -o /dev/null -w "%{http_code}" \
                https://api.deepseek.com/models \
                -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" 2>/dev/null)
            [[ "$response" == "200" ]]
            ;;
        *)
            return 1
            ;;
    esac
}

# Get working provider
get_working_provider() {
    for provider in "${PROVIDERS[@]}"; do
        if test_provider "$provider"; then
            echo "$provider"
            return 0
        fi
    done
    return 1
}

# Update OpenClaw config to use specific provider
set_provider() {
    local provider="$1"
    local config_file="${HOME}/.openclaw/config.json"
    
    if [[ ! -f "$config_file" ]]; then
        log "Warning: OpenClaw config not found at $config_file"
        return 1
    fi
    
    # Create backup
    cp "$config_file" "$config_file.bak.$(date +%s)"
    
    case "$provider" in
        gemini)
            jq '.model = "gemini/gemini-2.0-flash"' "$config_file" > "$config_file.tmp" && mv "$config_file.tmp" "$config_file"
            ;;
        openai)
            jq '.model = "openai/gpt-4o"' "$config_file" > "$config_file.tmp" && mv "$config_file.tmp" "$config_file"
            ;;
        anthropic)
            jq '.model = "anthropic/claude-3-5-sonnet-20241022"' "$config_file" > "$config_file.tmp" && mv "$config_file.tmp" "$config_file"
            ;;
        deepseek)
            jq '.model = "deepseek/deepseek-chat"' "$config_file" > "$config_file.tmp" && mv "$config_file.tmp" "$config_file"
            ;;
    esac
    
    log "Switched to provider: $provider"
}

# Main wrapper logic
main() {
    local job_name="${1:-unknown}"
    local job_id="${2:-unknown}"
    
    log "=== Cron Wrapper Started for: $job_name ($job_id) ==="
    
    # Check current provider
    local current_provider
    current_provider=$(get_working_provider)
    
    if [[ -z "$current_provider" ]]; then
        log "CRITICAL: No working AI provider found!"
        # Send alert via Telegram if possible
        if [[ -n "${TELEGRAM_BOT_TOKEN:-}" ]]; then
            curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
                -d "chat_id=267378578" \
                -d "text=🚨 CRITICAL: Cron job '$job_name' cannot run - no AI providers available" \
                > /dev/null 2>&1 || true
        fi
        exit 1
    fi
    
    log "Using provider: $current_provider"
    
    # Optionally switch provider in config (if needed)
    # set_provider "$current_provider"
    
    # The actual job execution happens after this wrapper
    # The OpenClaw gateway handles the execution
    
    log "=== Cron Wrapper Complete ==="
}

main "$@"