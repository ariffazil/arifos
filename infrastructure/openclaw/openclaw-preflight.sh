#!/bin/bash
# OpenClaw-Forged Preflight - Constitutional Readiness Check
# Version: 2026.03.14-PREFLIGHT
# Checks for: Qdrant, Ollama, and arifOS MCP connectivity

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 OpenClaw-Forged: Initiating Preflight..."

# 1. Qdrant connectivity
QDRANT_URL=${QDRANT_URL:-"http://qdrant:6333"}
echo "   Checking Qdrant: $QDRANT_URL"
if curl -s --max-time 3 "$QDRANT_URL" | grep -q 'title\|result'; then
    echo -e "   [${GREEN}OK${NC}] Qdrant Vector Store reachable"
else
    echo -e "   [${YELLOW}WARN${NC}] Qdrant at $QDRANT_URL not responding (using local memory if builtin)"
fi

# 2. Ollama connectivity (Embeddings)
OLLAMA_URL=${OLLAMA_URL:-"http://ollama:11434"}
echo "   Checking Ollama: $OLLAMA_URL"
if curl -s --max-time 3 "$OLLAMA_URL/api/tags" | grep -q 'models'; then
    echo -e "   [${GREEN}OK${NC}] Ollama Embeddings Engine reachable"
else
    echo -e "   [${YELLOW}WARN${NC}] Ollama at $OLLAMA_URL not responding (using external APIs)"
fi

# 3. arifOS MCP connectivity (Governance)
# Usually accessed via service name 'arifosmcp' or host.docker.internal
MCP_URL=${ARIFOS_MCP_URL:-"http://arifosmcp:8080/mcp"}
echo "   Checking arifOS MCP: $MCP_URL"
if curl -s --max-time 3 -X POST "$MCP_URL" -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"ocl-preflight","version":"1.0"}}}' | grep -q 'protocolVersion'; then
    echo -e "   [${GREEN}OK${NC}] arifOS MCP Governance Plane reachable"
else
    # Fallback to host.docker.internal for local/development environments
    MCP_URL_FALLBACK="http://host.docker.internal:8080/mcp"
    if curl -s --max-time 2 -X POST "$MCP_URL_FALLBACK" -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"ocl-preflight","version":"1.0"}}}' | grep -q 'protocolVersion'; then
        echo -e "   [${GREEN}OK${NC}] arifOS MCP reachable via host.docker.internal"
    else
        echo -e "   [${YELLOW}WARN${NC}] arifOS MCP not responding (sovereign access only)"
    fi
fi

# 4. Redis connectivity (Session State)
REDIS_URL=${REDIS_URL:-"redis://redis:6379"}
# Extract host and port for curl check
REDIS_HOST=$(echo "$REDIS_URL" | sed -e 's|redis://||' -e 's|:.*||')
REDIS_PORT=$(echo "$REDIS_URL" | sed -e 's|.*:||')
REDIS_PORT=${REDIS_PORT:-6379}

echo "   Checking Redis: $REDIS_HOST:$REDIS_PORT"
if curl -s --max-time 2 "telnet://$REDIS_HOST:$REDIS_PORT" > /dev/null 2>&1 || [ $? -eq 52 ]; then
     # curl telnet often returns 52 (Empty reply) which means it connected successfully
     echo -e "   [${GREEN}OK${NC}] Redis Session Store reachable"
else
     echo -e "   [${YELLOW}WARN${NC}] Redis at $REDIS_HOST:$REDIS_PORT not responding (ephemeral mode)"
fi

echo -e "✅ Preflight Complete."
exit 0
