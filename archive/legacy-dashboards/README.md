# ⚠️ LEGACY DASHBOARDS — DO NOT USE FOR MCP SERVER

**This folder contains OLD static site configuration, NOT the MCP server.**

## What's Here

- `Dockerfile` — nginx static site server (for portfolio website)
- `railway.json` — Legacy config for old dashboard deployment

## Why It Caused Confusion

During v55.3 deployment, Railway was picking up `railway.json` from various locations, causing:
- Wrong builder (Nixpacks vs Dockerfile)
- Wrong start command
- Import path errors

## Active MCP Server Config (USE THIS)

```
/root/arifOS/railway.toml  ← Current Railway config
/root/arifOS/Dockerfile    ← Current MCP server build
```

## How to Verify You're Using Right Config

```bash
# Should ONLY show:
# ./railway.toml
git ls-files | grep railway

# Should show:
# ./Dockerfile
git ls-files | grep "^./Dockerfile"
```

---
*This folder is for historical reference only. Do not deploy from here.*
