#!/bin/bash
# OpenClaw-Forged Entrypoint
# Version: 2026.03.14-FORGED
# Responsibility: Preflight checks, config merging, and gateway start

set -e

# Run Preflight
echo "🚀 [ARIF-OCL] Starting OpenClaw Forged..."
/usr/local/bin/openclaw-preflight

# Check for config existence
if [ ! -f "/root/.openclaw/config.json" ] && [ -f "/configs/openclaw.json" ]; then
    echo "📋 [ARIF-OCL] Overriding with arifOS native config..."
    mkdir -p /root/.openclaw
    cp /configs/openclaw.json /root/.openclaw/config.json
fi

# Set default model via ENV if provided
if [ ! -z "$PRIMARY_MODEL" ]; then
    echo "🧠 [ARIF-OCL] PRIMARY_MODEL override: $PRIMARY_MODEL"
    # jq can be used if needed, but for now we rely on the pre-configured arifosmcp/kimi/gemini stack
fi

# Fix workspace paths
mkdir -p /root/.openclaw/workspace

# Execute OpenClaw gateway
echo "🔗 [ARIF-OCL] Gateway active on port ${PORT:-18789}"
exec node openclaw.mjs gateway --allow-unconfigured "$@"
