#!/bin/bash
# API Key Validator for OpenClaw Cron Resilience
# Validates API keys before cron execution

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Source environment
source /root/.env.openclaw 2>/dev/null || {
    echo -e "${RED}ERROR: Cannot load .env.openclaw${NC}"
    exit 1
}

# Logging
LOG_FILE="/var/log/openclaw/api-validator.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# API Key validation functions
validate_gemini() {
    local key="${GEMINI_API_KEY:-}"
    if [[ -z "$key" ]]; then
        log "${RED}GEMINI_API_KEY: NOT SET${NC}"
        return 1
    fi
    
    # Quick validation - try to list models
    local response
    response=$(curl -s -w "%{http_code}" \
        "https://generativelanguage.googleapis.com/v1beta/models?key=$key" \
        -H "Content-Type: application/json" 2>/dev/null)
    
    local http_code="${response: -3}"
    
    if [[ "$http_code" == "200" ]]; then
        log "${GREEN}GEMINI_API_KEY: VALID${NC}"
        return 0
    else
        log "${RED}GEMINI_API_KEY: INVALID (HTTP $http_code)${NC}"
        return 1
    fi
}

validate_openai() {
    local key="${OPENAI_API_KEY:-}"
    if [[ -z "$key" ]]; then
        log "${RED}OPENAI_API_KEY: NOT SET${NC}"
        return 1
    fi
    
    local response
    response=$(curl -s -w "%{http_code}" \
        https://api.openai.com/v1/models \
        -H "Authorization: Bearer $key" 2>/dev/null)
    
    local http_code="${response: -3}"
    
    if [[ "$http_code" == "200" ]]; then
        log "${GREEN}OPENAI_API_KEY: VALID${NC}"
        return 0
    else
        log "${RED}OPENAI_API_KEY: INVALID (HTTP $http_code)${NC}"
        return 1
    fi
}

validate_anthropic() {
    local key="${ANTHROPIC_API_KEY:-}"
    if [[ -z "$key" ]]; then
        log "${RED}ANTHROPIC_API_KEY: NOT SET${NC}"
        return 1
    fi
    
    # Anthropic doesn't have a simple list endpoint, try a minimal request
    local response
    response=$(curl -s -w "%{http_code}" \
        https://api.anthropic.com/v1/messages \
        -H "x-api-key: $key" \
        -H "anthropic-version: 2023-06-01" \
        -H "Content-Type: application/json" \
        -d '{"model":"claude-3-haiku-20240307","max_tokens":1,"messages":[{"role":"user","content":"hi"}]}' 2>/dev/null)
    
    local http_code="${response: -3}"
    
    # 400 is OK here (bad request due to empty content), we just want to check auth
    if [[ "$http_code" == "200" || "$http_code" == "400" ]]; then
        log "${GREEN}ANTHROPIC_API_KEY: VALID${NC}"
        return 0
    else
        log "${RED}ANTHROPIC_API_KEY: INVALID (HTTP $http_code)${NC}"
        return 1
    fi
}

validate_firecrawl() {
    local key="${FIRECRAWL_API_KEY:-}"
    if [[ -z "$key" ]]; then
        log "${RED}FIRECRAWL_API_KEY: NOT SET${NC}"
        return 1
    fi
    
    # Firecrawl doesn't have a simple validate endpoint
    log "${YELLOW}FIRECRAWL_API_KEY: SET (validation skipped - no test endpoint)${NC}"
    return 0
}

validate_brave() {
    local key="${BRAVE_API_KEY:-}"
    if [[ -z "$key" ]]; then
        log "${RED}BRAVE_API_KEY: NOT SET${NC}"
        return 1
    fi
    
    local response
    response=$(curl -s -w "%{http_code}" \
        "https://api.search.brave.com/res/v1/web/search?q=test&count=1" \
        -H "X-Subscription-Token: $key" 2>/dev/null)
    
    local http_code="${response: -3}"
    
    if [[ "$http_code" == "200" ]]; then
        log "${GREEN}BRAVE_API_KEY: VALID${NC}"
        return 0
    else
        log "${RED}BRAVE_API_KEY: INVALID (HTTP $http_code)${NC}"
        return 1
    fi
}

# Main validation
main() {
    log "=== API Key Validation Started ==="
    
    local failed=0
    local gemini_ok=false
    local openai_ok=false
    local anthropic_ok=false
    
    # Validate primary AI providers
    if validate_gemini; then
        gemini_ok=true
    else
        ((failed++))
    fi
    
    if validate_openai; then
        openai_ok=true
    else
        ((failed++))
    fi
    
    if validate_anthropic; then
        anthropic_ok=true
    else
        ((failed++))
    fi
    
    # Validate tools
    validate_firecrawl || ((failed++))
    validate_brave || ((failed++))
    
    # Summary
    log "=== Validation Summary ==="
    
    if $gemini_ok; then
        echo "PRIMARY: gemini"
    elif $openai_ok; then
        echo "PRIMARY: openai (Gemini failed, using fallback)"
    elif $anthropic_ok; then
        echo "PRIMARY: anthropic (Gemini/OpenAI failed, using fallback)"
    else
        echo "PRIMARY: NONE_ALL_FAILED"
        log "${RED}CRITICAL: No valid AI provider found!${NC}"
        exit 2
    fi
    
    log "=== API Key Validation Complete ==="
    
    return 0
}

main "$@"