# Railway Deployment Fix Guide - Core Module Updates

## Problem
Railway caches Docker build layers, so changes to `core/` don't get deployed even after git push.

## Root Cause
Docker's layer caching mechanism:
```
COPY core/ core/  <- Cached if core/ hasn't changed timestamp
RUN pip install -e .  <- Cached layer
```

## Solutions

### ✅ Solution 1: Cache Bust (ALREADY DONE)
We just updated the Dockerfile cache bust timestamp:
```dockerfile
# CACHE BUST: 2026-02-14T08-00-00Z (v64.2.2 - Core module update)
```

**Railway will now rebuild the Docker image from scratch.**

Monitor the deployment at: https://railway.app/project/[your-project]

---

### Solution 2: Railway Dashboard Manual Redeploy

If cache bust doesn't work immediately:

1. Go to https://railway.app/dashboard
2. Click your arifOS project
3. Click the "arifos" service
4. Click "Deployments" tab
5. Click "Redeploy" button (↻)

This forces a fresh build without cache.

---

### Solution 3: Update DEPLOY_TS Variable

In your `railway.toml`, update the timestamp:

```toml
[variables]
DEPLOY_TS = "2026-02-14T08-00-00"  # Change this timestamp
```

Railway treats this as a config change and rebuilds.

---

### Solution 4: Clear Railway Cache (Nuclear Option)

If nothing else works:

1. In Railway dashboard, go to your service
2. Click "Settings" → "Advanced"
3. Click "Clear Build Cache"
4. Trigger new deployment

---

## How to Verify Fix Worked

### Check Railway Logs
```bash
# In Railway dashboard, check the build logs:
# You should see:
# => Building...
# => Copying core/ core/  <- Should NOT say "using cache"
# => Installing pip dependencies
```

### Test Core Module on Railway
Once deployed, test if the new core code is active:

```bash
# From your VPS, test Railway endpoint:
curl https://your-railway-app.up.railway.app/health

# Check version matches:
# Should show: {"version": "64.1.0"} or newer
```

### Verify Core Imports
```bash
# SSH into Railway container (if available):
railway connect

# Check if core module has your changes:
python3 -c "import core; print(core.__file__)"
# Should show: /app/core/__init__.py

# Check if core code is latest:
ls -la /app/core/
```

---

## Best Practices for Future Updates

### 1. Always Update Cache Bust
When changing `core/`, update both timestamps in Dockerfile:
```dockerfile
# Top of file:
# CACHE BUST: 2026-02-14T08-00-00Z (your change description)

# Bottom of file:
# CACHE BUST: 20260214080000 (same timestamp)
```

### 2. Use Semantic Versioning in Bust Comments
```dockerfile
# CACHE BUST: v64.2.2-core-governance-fix
```

### 3. Commit with Clear Messages
```bash
git commit -m "Update core/governance_kernel.py - Fix F11 authority check"
```

### 4. Verify Before Assuming
```bash
# After push, check Railway:
railway status  # CLI command

# Or check logs:
railway logs
```

---

## FAQ

### Q: Do I need to `pip install` from PyPI?
**A: NO!** The Dockerfile uses `pip install -e .` which installs from local source, not PyPI. Updating PyPI won't help with Railway caching.

### Q: Why does local work but Railway doesn't?
**A:** Local VPS runs the code directly. Railway builds a Docker image first, which gets cached.

### Q: How often should I update cache bust?
**A:** Every time you modify `core/`, `aaa_mcp/`, or `codebase/` directories.

### Q: Can I disable Docker caching?
**A:** Not recommended - builds would be 10x slower. Use cache busting instead.

### Q: What if cache bust doesn't work?
**A:** Try the Railway Dashboard redeploy button (Solution 2) or clear cache (Solution 4).

---

## Quick Checklist

When updating core code:

- [ ] Edit your core/ files
- [ ] Update cache bust timestamp in Dockerfile
- [ ] Commit changes: `git add . && git commit -m "Update core"`
- [ ] Push to main: `git push origin main`
- [ ] Check Railway dashboard for new deployment
- [ ] Verify deployment succeeded (green checkmark)
- [ ] Test endpoint: `curl https://your-app.up.railway.app/health`

---

## Status

✅ **Cache bust updated** - Railway should rebuild now
⏱️ **ETA**: 2-5 minutes for build + deploy
🎯 **Expected result**: New core code active on Railway

---

*Last updated: 2026-02-14*
*Cache bust version: v64.2.2*
