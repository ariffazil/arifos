# ⚠️ ARCHIVE — DO NOT USE FOR DEPLOYMENT

**This folder contains OLD configuration files that caused deployment failures.**

## Why These Are Archived

- `railway.json` — Used Nixpacks builder with WRONG start command (`python -m mcp.transports sse`)
- `railway.toml` — Old version that referenced deleted files
- `Dockerfile.old` — Outdated build steps

## What Broke

These files were causing Railway to use **Nixpacks instead of Dockerfile**, which:
1. Used the WRONG import path (`mcp.transports` instead of `mcp_server.transports`)
2. Caused `ImportError: No module named mcp.transports`
3. Failed health checks for 4+ hours

## Active Config (USE THIS)

```
/root/arifOS/railway.toml  ← Current Railway config (DOCKERFILE builder)
/root/arifOS/Dockerfile    ← Current Docker build
```

## Lessons

- **Never** have both `railway.json` and `railway.toml` — Railway picks one arbitrarily
- **Always** use `railway.toml` with `builder = "DOCKERFILE"`
- **Verify** with `git ls-files | grep railway` — should only show one file

## See Also

- `DEPLOYMENT_TIPS.md` — Quick reference for common errors
- `docs/DEPLOYMENT_WISDOM.md` — Full post-mortem

---
*Archived: 2026-02-03 after v55.3 deployment crisis*
