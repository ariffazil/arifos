#!/bin/bash
# Cron Resilience Setup Script
# Sets up all cron resilience components

set -euo pipefail

echo "🔧 OpenClaw Cron Resilience Setup"
echo "=================================="

# Create necessary directories
mkdir -p /var/log/openclaw
mkdir -p /tmp/openclaw/.alert-cooldown
mkdir -p /root/.openclaw/scripts

# Make scripts executable
chmod +x /root/.openclaw/scripts/*.sh

echo "✅ Scripts installed and made executable"

# Create systemd service for health monitoring (optional)
if command -v systemctl &> /dev/null; then
    cat > /etc/systemd/system/openclaw-cron-health.service << 'EOF'
[Unit]
Description=OpenClaw Cron Health Monitor
After=network.target

[Service]
Type=oneshot
ExecStart=/root/.openclaw/scripts/cron-health-monitor.sh
User=root
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

    cat > /etc/systemd/system/openclaw-cron-health.timer << 'EOF'
[Unit]
Description=Run OpenClaw Cron Health Monitor every 5 minutes

[Timer]
OnBootSec=5min
OnUnitActiveSec=5min

[Install]
WantedBy=timers.target
EOF

    systemctl daemon-reload
    systemctl enable openclaw-cron-health.timer
    systemctl start openclaw-cron-health.timer
    
    echo "✅ Systemd timer installed (runs every 5 minutes)"
fi

# Add crontab entries for additional monitoring
if ! crontab -l 2>/dev/null | grep -q "cron-health-monitor"; then
    (crontab -l 2>/dev/null || echo "") | {
        cat
        echo "# OpenClaw Cron Resilience - Health check every 5 minutes"
        echo "*/5 * * * * /root/.openclaw/scripts/cron-health-monitor.sh > /dev/null 2>&1"
        echo "# OpenClaw Cron Resilience - API key validation every hour"
        echo "0 * * * * /root/.openclaw/scripts/api-key-validator.sh > /dev/null 2>&1"
    } | crontab -
    
    echo "✅ Crontab entries added"
fi

# Test the setup
echo ""
echo "🧪 Testing setup..."

if /root/.openclaw/scripts/api-key-validator.sh > /dev/null 2>&1; then
    echo "✅ API key validator: OK"
else
    echo "⚠️  API key validator: Some keys may be invalid (check logs)"
fi

if /root/.openclaw/scripts/cron-health-monitor.sh > /dev/null 2>&1; then
    echo "✅ Health monitor: OK"
else
    echo "⚠️  Health monitor: Some checks failed (check logs)"
fi

echo ""
echo "📝 View logs:"
echo "   tail -f /var/log/openclaw/api-validator.log"
echo "   tail -f /var/log/openclaw/cron-health.log"
echo "   tail -f /var/log/openclaw/cron-wrapper.log"
echo ""
echo "🎯 Setup complete!"
echo ""
echo "Features enabled:"
echo "  • API key validation (hourly)"
echo "  • Cron job health monitoring (every 5 minutes)"
echo "  • Automatic Telegram alerts on failures"
echo "  • Self-heal attempts for gateway crashes"
echo "  • Fallback provider detection"
echo ""
echo "To manually check health:"
echo "  /root/.openclaw/scripts/cron-health-monitor.sh"
echo ""
echo "To validate API keys:"
echo "  /root/.openclaw/scripts/api-key-validator.sh"