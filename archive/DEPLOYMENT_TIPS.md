# Deployment Anti-Patterns (Learned the Hard Way)

## The 5 Failures That Broke v55.3 Deployment

1. **Namespace Collision** — Local `mcp/` shadowed PyPI `mcp` → renamed to `mcp_server/`
2. **Config Proliferation** — `railway.json` + `railway.toml` = confusion → deleted JSON
3. **Relative Import Hell** — `from ...enforcement` went above package root → use absolute imports
4. **Ghost Builds** — Railway cached old Nixpacks config → added cache-bust timestamp
5. **Incomplete Refactor** — Removed `_trinity_` but left references in 3 files → grep everything

## Quick Fixes for Common Errors

| Error | Fix |
|-------|-----|
| `No module named mcp.X` | Check for local folder shadowing PyPI package |
| `relative import beyond top-level` | Replace `...` with absolute import (`codebase.X`) |
| Wrong start command | Ensure only `railway.toml` exists, delete `railway.json` |
| Old code running | Add `# Cache-bust: YYYY-MM-DD` to Dockerfile |

## Pre-Deployment Checklist

```bash
# 1. One config file only
rm railway.json nixpacks.toml 2>/dev/null

# 2. No bad relative imports
grep -r "from \.\.\." --include="*.py" mcp_server/

# 3. Test imports locally
docker run --rm -v $(pwd):/app -w /app python:3.12-slim \
  sh -c "pip install -e . && python -c 'from mcp_server.core.tool_registry import ToolRegistry'"
```

## Full Wisdom

See `docs/DEPLOYMENT_WISDOM.md` for detailed post-mortem.

---
*Last updated: 2026-02-03 (v55.3 deployment)*
