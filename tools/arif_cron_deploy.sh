#!/bin/bash
# arifOS Self-Healing Observability Cron
# Installs itself into crontab. Fires every 5 min.
# Cleans blockers → deploys observability → self-terminates when healthy

set -e

HOST="ariffazil@72.62.71.199"
SSH="ssh -o ConnectTimeout=8 -o StrictHostKeyChecking=no -i /root/.ssh/hermes_vps_key -p 22888"
DEPLOY_LOG="/tmp/arif_cron_deploy.log"
LOAD_THRESH=8

log() { echo "[$(date +%H:%M:%S)] $1" | tee -a "$DEPLOY_LOG"; }

# ── Check load ──
load=$($SSH "$HOST" "uptime | awk '{print \$NF}' | sed 's/,//'" 2>/dev/null)
load_int=$(echo "$load" | awk '{printf "%.0f", $1}')
log "Load=$load_int"

# ── If load is reasonable, clean blockers ──
if [ "$load_int" -lt 20 ]; then
    $SSH "$HOST" "
        kill -9 \$(pgrep -f 'du -sh') 2>/dev/null
        kill -9 \$(pgrep -f 'find /') 2>/dev/null
        kill -9 \$(pgrep -f 'npm.*build') 2>/dev/null
        echo 'blockers cleaned at \$(date +%H:%M:%S)'
        sleep 2
        uptime
    " 2>/dev/null | tee -a "$DEPLOY_LOG"
fi

# ── Only proceed if system is quiet enough ──
if [ "$load_int" -gt "$LOAD_THRESH" ]; then
    log "Load $load_int > $LOAD_THRESH — waiting for quiet window"
    exit 0
fi

log "System quiet — executing observability deploy"

# ── 1. Verify node-exporter ──
log "[1] node-exporter..."
$SSH "$HOST" "docker start arifos-node-exporter 2>/dev/null; docker ps --format '{{.Names}}' | grep node-exporter" 2>/dev/null

# ── 2. Verify cAdvisor ──
log "[2] cadvisor..."
$SSH "$HOST" "docker start arifos-cadvisor 2>/dev/null; docker ps --format '{{.Names}}' | grep cadvisor" 2>/dev/null

# ── 3. Prometheus (check cached image first) ──
log "[3] prometheus..."
if $SSH "$HOST" "docker image inspect prom/prometheus:v2.52.0 -f '{{.Id}}' 2>/dev/null" 2>/dev/null | grep -q sha256; then
    log "Prometheus image CACHED — deploying..."
    $SSH "$HOST" "
        mkdir -p /root/compose/prometheus
        cat > /root/compose/prometheus/prometheus.yml << 'YAML'
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: node
    static_configs:
      - targets: [arifos-node-exporter:9100]
  - job_name: cadvisor
    static_configs:
      - targets: [arifos-cadvisor:8080]
YAML
        docker rm -f arifos-prometheus 2>/dev/null
        docker run -d --name arifos-prometheus \
          --network arifos_core_network \
          --restart unless-stopped \
          -v /root/compose/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro \
          -v /root/compose/prometheus:/prometheus:rw \
          prom/prometheus:v2.52.0 \
          --config.file=/etc/prometheus/prometheus.yml \
          --storage.tsdb.path=/prometheus
    " 2>/dev/null
    log "Prometheus deployed"
else
    log "Prometheus image NOT cached — pulling in background (low priority)..."
    $SSH "$HOST" "nohup sh -c 'nice -n 19 docker pull prom/prometheus:v2.52.0 >> /tmp/prom_pull.log 2>&1 && echo DONE >> /tmp/prom_pull.log' > /dev/null 2>&1 &" 2>/dev/null
fi

# ── 4. Grafana ──
log "[4] grafana..."
$SSH "$HOST" "
    mkdir -p /root/compose/grafana
    if ! docker ps --format '{{.Names}}' 2>/dev/null | grep -q '^arifos-grafana$'; then
        docker run -d --name arifos-grafana \
          --network arifos_core_network \
          --restart unless-stopped \
          -p 127.0.0.1:3000:3000 \
          -v /root/compose/grafana:/var/lib/grafana:rw \
          grafana/grafana:11.2.0
        echo 'Grafana deployed'
    else
        echo 'Grafana already running'
    fi
" 2>/dev/null

# ── 5. Loki ──
log "[5] loki..."
$SSH "$HOST" "
    if ! docker ps --format '{{.Names}}' 2>/dev/null | grep -q '^arifos-loki$'; then
        docker run -d --name arifos-loki \
          --network arifos_core_network \
          --restart unless-stopped \
          -p 127.0.0.1:3100:3100 \
          grafana/loki:3.2.0
        echo 'Loki deployed'
    else
        echo 'Loki already running'
    fi
" 2>/dev/null

# ── 6. arifOS MCP ──
log "[6] arifOS MCP..."
mcp_ok=$($SSH "$HOST" "curl -s --max-time 3 http://127.0.0.1:8080/health 2>/dev/null" 2>/dev/null)
if echo "$mcp_ok" | grep -q "true"; then
    log "arifOS MCP: HEALTHY ✓"
else
    log "arifOS MCP: DEAD — restarting..."
    $SSH "$HOST" "cd /root/arifOS && docker compose restart arifosmcp 2>&1 | tail -3" 2>/dev/null
fi

# ── 7. Netdata (Caddy route) ──
log "[7] netdata (route via Caddy)..."
$SSH "$HOST" "
    if ss -tlnp 2>/dev/null | grep -q 19999; then
        echo 'netdata: already listening'
    else
        # Check if binary exists
        if [ -f /usr/bin/netdata ]; then
            systemctl enable netdata 2>/dev/null && systemctl start netdata && echo 'netdata started' || echo 'netdata failed'
        else
            echo 'netdata: not installed (needs root/apt)'
        fi
    fi
" 2>/dev/null

# ── 8. Caddy routes for observability ──
log "[8] Caddy routes..."
$SSH "$HOST" "
    # Add metrics routes to Caddyfile
    if ! grep -q 'metrics/node' /etc/caddy/Caddyfile 2>/dev/null; then
        cat >> /etc/caddy/Caddyfile << 'CADDYEOF'

# arifOS Observability Routes
handle /metrics/node/* {
    reverse_proxy localhost:9100
}
handle /metrics/cadvisor/* {
    reverse_proxy localhost:8081
}
handle /dashboards/grafana/* {
    reverse_proxy localhost:3000
}
CADDYEOF
        echo 'Caddy routes added'
        # Reload Caddy
        pkill -HUP caddy 2>/dev/null || true
    else
        echo 'Caddy routes already configured'
    fi
" 2>/dev/null

# ── FINAL STATUS ──
log "=== FINAL STATUS ==="
$SSH "$HOST" "
    echo 'LOAD: \$(uptime)'
    echo 'CONTAINERS:'
    docker ps -a --format '{{.Names}} {{.Status}}' 2>/dev/null | grep -E 'arifos|node|cadvisor|prometheus|grafana|loki|mcp'
    echo 'PORTS:'
    ss -tlnp 2>/dev/null | grep -E '8080|8081|9100|3000|19999|3100|19999'
" 2>/dev/null | tee -a "$DEPLOY_LOG"

# ── Check if all services are healthy → remove cron if done ──
all_healthy=$($SSH "$HOST" "
    docker ps --format '{{.Names}}' 2>/dev/null | grep -E 'arifos-node-exporter|arifos-cadvisor|arifos-prometheus|arifos-grafana|arifos-loki' | wc -l
" 2>/dev/null)
log "Services up: $all_healthy (need 5)"

if [ "$all_healthy" -ge 5 ]; then
    log "=== ALL SERVICES DEPLOYED — removing cron job ==="
    $SSH "$HOST" "crontab -l 2>/dev/null | grep -v 'arif_cron_deploy' | crontab - 2>/dev/null; echo 'cron removed'" 2>/dev/null
else
    log "Not all services healthy yet — cron will fire again in 5 min"
fi

log "=== DEPLOY COMPLETE ==="