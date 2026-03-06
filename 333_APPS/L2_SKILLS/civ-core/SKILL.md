---
name: civ-core
description: VPS CIV infrastructure — Docker Compose, Traefik, Postgres, Redis, observability, deployment
---

# civ-core

## Scope
Consolidated infrastructure layer — VPS operations, Docker Compose orchestration, Traefik ingress, PostgreSQL, Redis, observability, deployment pipeline.

**Merged from:** `vps-civ-core` + `observability` + `deploy-pipeline`

## Constitutional Alignment
| Floor | Role | Threshold |
|-------|------|-----------|
| F1 | Amanah | LOCKED (deployment gates) |
| F5 | Peace² | P² ≥ 1.0 (service stability) |
| F11 | CommandAuth | LOCKED (access control) |
| F12 | Injection | Risk < 0.85 (config security) |

## Key Components
- **Orchestration**: Docker Compose stack (11 containers)
- **Ingress**: Traefik (80/443, TLS, route control)
- **Database**: PostgreSQL (structured state, audit)
- **Cache**: Redis (sessions, queues, speed)
- **Observability**: Prometheus metrics, health checks, alerts
- **Deployment**: GitHub Actions, webhooks, auto-deploy

## Backend Path
- `deployment/` — Docker Compose configs
- `deployment/traefik/` — Ingress configuration
- `deployment/prometheus/` — Observability stack
- `.github/workflows/` — CI/CD pipelines

## Operational Rules

**Trigger When:**
- Service deployment required
- Infrastructure health check needed
- Container orchestration operations
- TLS/certificate management
- Database backup/restore

**Allowed Operations:**
- Deploy core services (Traefik, Postgres, Redis)
- Check container health status
- Manage Docker networks and volumes
- Rotate TLS certificates
- Execute backup procedures

**888_HOLD Required:**
- **Production deployment** to live environment
- **Database migrations** with schema changes
- **Network topology** changes
- **Secret rotation** in production
- **Mass container restart** (>3 services)

## Service Topology
```
Internet
  → Traefik :80/:443
    → arifos (public)
    → apex control (protected)
    → OpenClaw (private route)
    → AgentZero (private route)

Internal
  → Postgres (state)
  → Redis (cache)
  → Qdrant (gated)
  → Prometheus (metrics)
```

## Quick Reference
```bash
# Deploy core stack
docker compose -f docker-compose.quickstart.yml up -d

# Check health
docker ps

# View logs
docker logs -f arifos

# Backup database
docker exec postgres pg_dump -U arifos > backup.sql
```

## Verification
```bash
docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "(traefik|postgres|redis|arifos)"
```
