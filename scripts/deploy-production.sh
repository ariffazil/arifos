#!/bin/bash
# arifOS Production Deployment Script
# DITEMPA BUKAN DIBERI — Forged, Not Given

set -euo pipefail

ARIFOS_ROOT="/opt/arifos"
SECRETS_DIR="$ARIFOS_ROOT/secrets"
SERVICE_NAME="arifos-mcp"

echo "🏛️  arifOS Production Deployment"
echo "================================"

# 1. Check prerequisites
echo "📋 Checking prerequisites..."
command -v python3 >/dev/null 2>&1 || { echo "❌ python3 required"; exit 1; }
command -v systemctl >/dev/null 2>&1 || { echo "⚠️  systemctl not found (non-systemd system)"; }

# 2. Verify governance secret
echo "🔐 Verifying governance secret..."
if [ -f "$SECRETS_DIR/governance.secret" ]; then
    echo "✅ Governance secret file exists"
    SECRET_CHECK=$(python3 -c "
import os
os.environ['ARIFOS_GOVERNANCE_SECRET_FILE'] = '$SECRETS_DIR/governance.secret'
from core.enforcement.auth_continuity import _load_governance_token_secret
secret = _load_governance_token_secret()
print('VALID' if len(secret) == 64 else 'INVALID')
" 2>/dev/null || echo "CHECK_FAILED")
    
    if [ "$SECRET_CHECK" = "VALID" ]; then
        echo "✅ Secret validation passed"
    else
        echo "⚠️  Secret validation warning - continuing anyway"
    fi
else
    echo "❌ Governance secret file not found at $SECRETS_DIR/governance.secret"
    echo "   Run: python3 -c \"import secrets; print(secrets.token_hex(32))\" > $SECRETS_DIR/governance.secret"
    exit 1
fi

# 3. Install dependencies
echo "📦 Installing dependencies..."
cd "$ARIFOS_ROOT"
pip3 install -e ".[dev]" --quiet

# 4. Run pre-flight tests
echo "🧪 Running pre-flight tests..."
python3 -m pytest tests/test_constitutional_core.py -q --tb=short || {
    echo "❌ Constitutional tests failed - aborting deployment"
    exit 1
}

# 5. Restart service
echo "🔄 Restarting arifOS MCP service..."
if systemctl is-active --quiet "$SERVICE_NAME" 2>/dev/null; then
    sudo systemctl restart "$SERVICE_NAME"
    echo "✅ Service restarted via systemctl"
else
    echo "⚠️  Service not running via systemctl - manual restart required"
    echo "   Command: pkill -f 'python.*arifosmcp' && python3 -m arifosmcp.runtime http"
fi

# 6. Health check
echo "🏥 Health check..."
sleep 2
HEALTH_STATUS=$(curl -s http://localhost:8080/health | python3 -c "import sys, json; print(json.load(sys.stdin).get('status', 'UNKNOWN'))" 2>/dev/null || echo "UNREACHABLE")

if [ "$HEALTH_STATUS" = "healthy" ]; then
    echo "✅ Health check passed"
else
    echo "⚠️  Health check returned: $HEALTH_STATUS"
fi

echo ""
echo "🎯 Deployment Complete!"
echo "======================="
echo "Secret: File-based ($SECRETS_DIR/governance.secret)"
echo "Health: http://localhost:8080/health"
echo "Tools:  http://localhost:8080/tools"
echo ""
echo "DITEMPA BUKAN DIBERI — Forged, Not Given 🔥"
