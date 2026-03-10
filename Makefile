# arifOS MCP Server - Constitutional Deployment Makefile
# DITEMPA BUKAN DIBERI — Forged, Not Given
# F4 Entropy Control | F5 Witness | F11 Auth

.PHONY: help build deploy fast-deploy reforge clean logs status stop restart strategy auto-deploy maintenance setup-cron

# Default target
help:
	@echo "arifOS MCP Server - Constitutional Deployment Commands"
	@echo "======================================================="
	@echo ""
	@echo "🚀 DEPLOYMENT STRATEGIES:"
	@echo "  make strategy       Analyze and recommend rebuild strategy"
	@echo "  make fast-deploy    Fast redeploy (2-3 min) - code changes only"
	@echo "  make reforge        Full rebuild (10-15 min) - deps changed"
	@echo "  make auto-deploy    Autonomous deploy based on changes"
	@echo "  make hot-restart    Instant restart - config only"
	@echo ""
	@echo "📊 MONITORING:"
	@echo "  make status         Check service status"
	@echo "  make logs           Follow logs"
	@echo "  make health         Check health endpoint"
	@echo "  make doctor         Run OpenClaw doctor"
	@echo ""
	@echo "🧹 MAINTENANCE (Low Entropy):"
	@echo "  make maintenance    Run automated maintenance"
	@echo "  make setup-cron     Install automated cron jobs"
	@echo "  make clean          Clean Docker cache and unused images"
	@echo "  make stop           Stop services"
	@echo "  make restart        Restart services"
	@echo ""
	@echo "🔧 BUILD:"
	@echo "  make build          Standard build"
	@echo "  make deploy         Full deploy with health check"

# ============================================================================
# REBUILD STRATEGIES (Constitutional Approach)
# ============================================================================

# Analyze and recommend strategy
strategy:
	@echo "🔍 Analyzing changes..."
	@chmod +x scripts/rebuild-strategy.sh
	@./scripts/rebuild-strategy.sh --check

# Fast deployment - uses optimized Dockerfile with layer caching
# Use when: Core code changes, tool additions, minor updates
fast-deploy:
	@echo "⚡ Fast deploying arifOS MCP (2-3 min)..."
	@echo "   Strategy: Layer cache + code only"
	@chmod +x scripts/fast-deploy.sh
	@./scripts/fast-deploy.sh

# Full reforge - rebuilds from scratch
# Use when: Dockerfile, requirements.txt, or base image changed
reforge:
	@echo "🔥 Full reforge arifOS MCP (10-15 min)..."
	@echo "   Strategy: Complete rebuild, no cache"
	@echo "   ⚠️  This will take longer but ensures clean state"
	@export DOCKER_BUILDKIT=1
	@docker compose down arifosmcp
	@docker rmi arifos/arifosmcp:latest 2>/dev/null || true
	@docker compose build --no-cache arifosmcp
	@docker compose up -d arifosmcp
	@echo "⏳ Waiting for health..."
	@sleep 30
	@make health

# Autonomous deployment - decides strategy automatically
auto-deploy:
	@echo "🤖 Autonomous deployment..."
	@chmod +x scripts/auto-deploy.sh
	@./scripts/auto-deploy.sh --auto

# Hot restart - just restart container (10s)
# Use when: Config changes only
hot-restart:
	@echo "🔄 Hot restart (10s)..."
	@docker compose restart arifosmcp
	@sleep 5
	@make health

# Development mode - mounts code for instant changes
dev:
	@echo "🔧 Starting in development mode..."
	@docker compose -f docker-compose.yml -f docker-compose.override.yml up -d arifosmcp
	@echo "Code changes will be reflected immediately (no rebuild needed)"

# ============================================================================
# MONITORING & DIAGNOSTICS
# ============================================================================

# Check status
status:
	@echo "📊 Container Status:"
	@docker ps --filter "name=arifosmcp" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
	@echo ""
	@echo "💾 Resource Usage:"
	@docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" arifosmcp_server 2>/dev/null || echo "Container not running"

# Health check
health:
	@echo "🏥 Health Check:"
	@curl -s http://localhost:8080/health | python3 -m json.tool 2>/dev/null || curl -s http://localhost:8080/health

# OpenClaw doctor
doctor:
	@echo "🏥 Running OpenClaw Doctor..."
	@docker exec openclaw_gateway openclaw doctor 2>&1 || echo "Doctor not available"

# Follow logs
logs:
	@docker logs -f arifosmcp_server

# ============================================================================
# LOW-ENTROPY MAINTENANCE (F4 Entropy Control)
# ============================================================================

# Automated maintenance - minimizes manual intervention
maintenance:
	@echo "🔧 Running low-entropy maintenance..."
	@chmod +x scripts/low-entropy-cron.sh
	@./scripts/low-entropy-cron.sh all

# Setup automated cron jobs
setup-cron:
	@echo "⚙️  Setting up automated cron jobs..."
	@echo "# arifOS Low-Entropy Maintenance" | sudo tee /etc/cron.d/arifos-maintenance
	@echo "*/5 * * * * root /srv/arifosmcp/scripts/low-entropy-cron.sh health >> /var/log/arifos-cron.log 2>&1" | sudo tee -a /etc/cron.d/arifos-maintenance
	@echo "0 */6 * * * root /srv/arifosmcp/scripts/low-entropy-cron.sh all >> /var/log/arifos-cron.log 2>&1" | sudo tee -a /etc/cron.d/arifos-maintenance
	@echo "✅ Cron jobs installed:"
	@echo "   • Health check: every 5 minutes"
	@echo "   • Full maintenance: every 6 hours"

# ============================================================================
# BUILD & DEPLOY (Legacy/Standard)
# ============================================================================

# Standard build
build:
	@echo "📦 Building arifOS MCP..."
	@export DOCKER_BUILDKIT=1
	@docker build -f Dockerfile.optimized -t arifos/arifosmcp:latest .

# Full deployment with health check
deploy: build
	@echo "🔄 Deploying..."
	@docker compose up -d arifosmcp
	@echo "⏳ Waiting for health..."
	@sleep 5
	@curl -s http://localhost:8080/health | python3 -m json.tool 2>/dev/null || curl -s http://localhost:8080/health

# Stop services
stop:
	@echo "🛑 Stopping arifOS MCP..."
	@docker compose stop arifosmcp

# Restart services
restart:
	@echo "🔄 Restarting arifOS MCP..."
	@docker compose restart arifosmcp
	@sleep 3
	@make health

# Clean Docker cache
clean:
	@echo "🧹 Cleaning Docker..."
	@docker system prune -f
	@docker builder prune -f

# ============================================================================
# DECISION TREE (When to use what)
# ============================================================================
#
# DID YOU CHANGE...?                    USE THIS COMMAND
# ───────────────────────────────────────────────────────────────
# Dockerfile/requirements.txt           make reforge    (10-15 min)
# Core code (core/, arifosmcp/)         make fast-deploy (2-3 min)
# Config only (.env, yaml)              make hot-restart (10s)
# Not sure what changed                 make strategy   (analysis)
# Want it to decide automatically       make auto-deploy (smart)
# Just need a quick restart             make restart    (30s)
#
# AUTONOMOUS MODE:
#   make setup-cron → Enables auto-healing & auto-deploy
#
# ============================================================================
