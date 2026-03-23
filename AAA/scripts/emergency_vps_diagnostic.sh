#!/bin/bash
# EMERGENCY VPS DIAGNOSTIC — Run on srv1325122.hstgr.cloud

echo "=========================================="
echo "arifOS MCP Emergency Diagnostic"
echo "=========================================="
echo ""

# 1. Check container status
echo "1. Container Status:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "arifosmcp|traefik"
echo ""

# 2. Check arifosmcp_server logs (last 50 lines)
echo "2. arifosmcp_server logs (errors only):"
docker logs arifosmcp_server --tail 50 2>&1 | grep -E "ERROR|CRITICAL|Traceback|ImportError|ValidationError" | tail -20
echo ""

# 3. Check Traefik logs
echo "3. Traefik router logs:"
docker logs traefik_router --tail 20 2>&1 | grep -E "error|404|not found" | tail -10
echo ""

# 4. Test endpoint locally
echo "4. Local endpoint test:"
curl -s http://localhost:8080/mcp 2>&1 | head -5
echo ""

# 5. Check container count
echo "5. Container count:"
docker ps -q | wc -l
echo "(should be 16)"
echo ""

# 6. Health endpoint
echo "6. Health check:"
curl -s http://localhost:8080/health 2>&1 | head -3
echo ""

# 7. Git status
echo "7. Git status (last commit):"
cd /srv/arifosmcp && git log --oneline -1
echo ""

# 8. Recent server restart
echo "8. Container uptime:"
docker ps --format "{{.Names}}\t{{.Status}}" | grep arifosmcp_server
echo ""

echo "=========================================="
echo "Diagnostic complete"
echo "=========================================="
