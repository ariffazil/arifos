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
# Usually accessed via host.docker.internal or direct IP
MCP_URL=${ARIFOS_MCP_URL:-"http://host.docker.internal:8080/mcp"}
echo "   Checking arifOS MCP: $MCP_URL"
if curl -s --max-time 3 -X POST "$MCP_URL" -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"ocl-preflight","version":"1.0"}}}' | grep -q 'protocolVersion'; then
    echo -e "   [${GREEN}OK${NC}] arifOS MCP Governance Plane reachable"
else
    echo -e "   [${YELLOW}WARN${NC}] arifOS MCP at $MCP_URL not responding (sovereign access only)"
fi

echo "✅ Preflight Complete."
exit 0
