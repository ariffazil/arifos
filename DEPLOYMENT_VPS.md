# Phase 4: VPS Commissioning and Deployment

## Summary

The thermodynamic cage is hardened and wired. This guide deploys to sovereign infrastructure.

## Quick Start

```bash
# 1. Build
docker-compose -f docker-compose.vps.yml build

# 2. Deploy
git pull origin main
docker-compose up -d

# 3. Verify
curl http://localhost:8080/health
python3 tests/entropy_audit_minimal.py
```

## Pre-Flight

- [ ] Core cage committed
- [ ] MCP gateway wired  
- [ ] Audit passes (6/6)

## Success Criteria

- SEAL rate: 50-60%
- All 6 thermodynamic tests pass
- No server crashes on physics exceptions

**Akal memerintah, amanah mengunci.**
