# arifOS MCP Server - Fast Deployment Makefile
# DITEMPA BUKAN DIBERI — Forged, Not Given

.PHONY: help build deploy fast-deploy clean logs status stop

# Default target
help:
	@echo "arifOS MCP Server - Deployment Commands"
	@echo "========================================"
	@echo ""
	@echo "🚀 DEPLOYMENT:"
	@echo "  make fast-deploy    Fast redeploy (optimized build)"
	@echo "  make build          Build Docker image"
	@echo "  make deploy         Full deploy with health check"
	@echo ""
	@echo "📊 MONITORING:"
	@echo "  make status         Check service status"
	@echo "  make logs           Follow logs"
	@echo "  make health         Check health endpoint"
	@echo ""
	@echo "🧹 MAINTENANCE:"
	@echo "  make clean          Clean Docker cache and unused images"
	@echo "  make stop           Stop services"
	@echo "  make restart        Restart services"

# Fast deployment - uses optimized Dockerfile with layer caching
fast-deploy:
	@echo "🚀 Fast deploying arifOS MCP..."
	@chmod +x scripts/fast-deploy.sh
	@./scripts/fast-deploy.sh

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

# Follow logs
logs:
	@docker logs -f arifosmcp_server

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

# Development mode - mounts code for instant changes
dev:
	@echo "🔧 Starting in development mode..."
	@docker compose -f docker-compose.yml -f docker-compose.override.yml up -d arifosmcp
	@echo "Code changes will be reflected immediately (no rebuild needed)"
