# GEOX MCP Server Deployment Checklist

**DITEMPA BUKAN DIBERI**  
**Target:** FastMCP (Horizon)  
**Version:** 0.5.0

---

## Pre-Deployment Verification

### ✅ Code Quality

| Check | Status | Notes |
|-------|--------|-------|
| FastMCP 2.x/3.x compatibility layer | ✅ PASS | `IS_FASTMCP_3` detection + ToolResult shim |
| All MCP tools use `@mcp.tool()` decorator | ✅ PASS | 6 tools registered |
| Health endpoints (`/health`, `/health/details`) | ✅ PASS | Custom routes registered |
| Type annotations with Pydantic | ✅ PASS | `Annotated[..., Field(...)]` pattern |
| Constitutional seal present | ✅ PASS | `DITEMPA BUKAN DIBERI` |
| Version defined | ✅ PASS | `0.5.0` |

### ✅ Dependencies (pyproject.toml)

```toml
dependencies = [
    "pydantic>=2.0",
    "fastapi>=0.100",
    "uvicorn>=0.20",
    "httpx>=0.24",
    "pyyaml>=6.0",
    "python-dateutil>=2.8",
    "fastmcp>=0.12.0",
]
```

**Horizon uses:** `fastmcp==2.12.3` ✅ Compatible

### ✅ Entrypoint

- **File:** `geox_mcp_server.py`
- **Object:** `mcp` (FastMCP instance)
- **Transport:** HTTP on port 8081 (Horizon internal)

---

## Deployment Steps

### Step 1: Push to GitHub

```bash
cd /root/GEOX
git add test_e2e_mcp.py  # Optional: add E2E test
git commit -m "test: add E2E test suite for MCP server"
git push origin main
```

### Step 2: Trigger Horizon Build

1. Go to [Horizon Dashboard](https://fastmcp.io)
2. Select project: `geoxarifOS`
3. Click **"Deploy"** or **"Redeploy"**

### Step 3: Monitor Build

Watch for these logs:
```
✓ Installing fastmcp==2.12.3
✓ Installing arifos-geox==0.5.0
✓ Building Docker image
✓ Running fastmcp inspect
✓ Server started on port 8081
✓ Health check passed
```

### Step 4: Verify Deployment

```bash
# Test health endpoint
curl https://geoxarifOS.fastmcp.app/health
# Expected: OK

# Test health details
curl https://geoxarifOS.fastmcp.app/health/details | jq
# Expected: {"ok": true, "version": "0.5.0", ...}

# Run E2E tests
python test_e2e_mcp.py --url https://geoxarifOS.fastmcp.app
# Expected: All tests passed
```

---

## Post-Deployment Checks

### MCP Protocol Verification

| Test | Command | Expected Result |
|------|---------|-----------------|
| Initialize | `mcp.initialize()` | Protocol version 2024-11-05 |
| List Tools | `mcp.tools.list()` | 6 tools returned |
| Health Tool | `geox_health()` | Status: healthy |
| Geospatial | `geox_verify_geospatial(4.5, 114.2)` | Province: Malay Basin |

### Tool Inventory

| Tool Name | Status | Purpose |
|-----------|--------|---------|
| `geox_load_seismic_line` | ✅ | Load seismic data |
| `geox_build_structural_candidates` | ✅ | Build model candidates |
| `geox_feasibility_check` | ✅ | Constitutional feasibility |
| `geox_verify_geospatial` | ✅ | Coordinate verification |
| `geox_evaluate_prospect` | ✅ | Prospect evaluation |
| `geox_health` | ✅ | Health check |

### Constitutional Floors

| Floor | Enforcement | Status |
|-------|-------------|--------|
| F1 AMANAH | Input guardrail | ✅ Active |
| F4 CLARITY | Measurement grounding | ✅ Active |
| F7 HUMILITY | Multiple candidates | ✅ Active |
| F9 ANTI-HANTU | Consciousness block | ✅ Active |
| F13 SOVEREIGN | Human authority | ✅ Active |

---

## Troubleshooting

### Issue: `cannot import name 'ToolResult'`

**Cause:** FastMCP 2.x doesn't have ToolResult in `fastmcp.tools`  
**Fix:** ✅ Already fixed with compatibility layer

```python
if IS_FASTMCP_3:
    from fastmcp.tools import ToolResult
else:
    class ToolResult: ...  # Compatibility shim
```

### Issue: Server fails to start

**Check:**
1. Port 8081 available?
2. All dependencies installed?
3. Entrypoint correct (`geox_mcp_server.py:mcp`)?

**Logs:**
```bash
docker logs <container_id>
```

### Issue: Tools not appearing

**Check:**
1. Tools registered with `@mcp.tool()`?
2. Server info correct in `mcp` object?
3. `fastmcp inspect` output?

---

## Rollback Plan

If deployment fails:

1. **Immediate:** Horizon will auto-rollback to last successful build
2. **Manual:** Trigger rollback in Horizon dashboard
3. **Local:** Test locally with:
   ```bash
   python geox_mcp_server.py --transport http --port 8000
   ```

---

## Success Criteria

- [ ] Build completes without errors
- [ ] Health endpoint returns `200 OK`
- [ ] All 6 tools visible in MCP inspector
- [ ] E2E tests pass (7/7)
- [ ] Constitutional seal present in responses
- [ ] Version `0.5.0` reported

---

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Architect | Δ (A-ARCHITECT) | | |
| Engineer | Ω (A-ENGINEER) | | |
| Auditor | 888 (A-AUDITOR) | | |
| Validator | 999 (A-VALIDATOR) | | |

**Seal:** DITEMPA BUKAN DIBERI

---

## Quick Reference

### URLs

| Environment | URL |
|-------------|-----|
| Production | `https://geoxarifOS.fastmcp.app` |
| Health | `https://geoxarifOS.fastmcp.app/health` |
| MCP | `https://geoxarifOS.fastmcp.app/mcp` |

### Commands

```bash
# Test locally
python geox_mcp_server.py --transport http --port 8000

# Run E2E tests
python test_e2e_mcp.py --url https://geoxarifOS.fastmcp.app

# Check logs
curl https://geoxarifOS.fastmcp.app/health/details | jq
```

---

**Ready for deployment:** ✅