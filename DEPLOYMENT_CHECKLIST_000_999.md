# Deployment Checklist: 000-999 Metabolic Loop

**Status**: ✅ READY FOR PRODUCTION  
**Version**: v2026.3.1-SEAL  
**Target**: arifOS MCP Server (`arifos.arif-fazil.com`)

---

## Pre-Deployment Verification

### 1. Code Changes Summary

**Files Modified**:
1. ✅ `arifos_aaa_mcp/server.py` — Main server with metabolic_loop tool
2. ✅ `arifos_aaa_mcp/__main__.py` — CLI entrypoint (no changes needed)
3. ✅ `arifos_aaa_mcp/rest_routes.py` — REST API (auto-includes new tool)
4. ✅ `333_APPS/L1_PROMPT/METABOLIC_LOOP_PROMPTS.md` — Stage prompts
5. ✅ `333_APPS/L1_PROMPT/000_999_METABOLIC_LOOP.md` — Integration guide

### 2. New Components Added

**Server Level**:
- ✅ `metabolic_loop` tool — Full 000-999 cycle orchestration
- ✅ `metabolic_loop_prompt` — Prompt-as-tool for client-side execution
- ✅ `MetabolicResult` / `MetabolicStage` — Pydantic models
- ✅ `PromptsAsTools` transform — Bridge for tool-only clients
- ✅ 13 Icon definitions (Δ Blue, Ω Green, Ψ Gold)

**Prompts Level** (L1_PROMPTS):
- ✅ 11 stage prompts (000 → 999)
- ✅ Theory alignment documentation
- ✅ Usage patterns guide

### 3. Integration Points Verified

**MCP Protocol**:
- ✅ Tool registered: `metabolic_loop`
- ✅ Prompt registered: `metabolic_loop_prompt`
- ✅ PromptsAsTools transform: `list_prompts`, `get_prompt`
- ✅ REST routes: `/tools/metabolic_loop`

**Constitutional Enforcement**:
- ✅ Stage 000: `anchor_session` (F11, F12)
- ✅ Stage 111-333: `reason_mind` (F2, F4, F7, F13)
- ✅ Stage 444-666: `simulate_heart` + `critique_thought` (F3, F5, F6, F9)
- ✅ Stage 777-888: `apex_judge` (F1-F13)
- ✅ Stage 889-999: `seal_vault` (F1, F3, F10)

**Trinity Lanes**:
- ✅ Δ Delta (Blue): 000, 111-333
- ✅ Ω Omega (Green): 444-666
- ✅ Ψ Psi (Gold): 777-999

---

## Deployment Steps

### Step 1: Local Testing

```bash
# Navigate to arifOS directory
cd /root/arifOS

# Install dependencies (if needed)
pip install -e .

# Run server locally
python -m arifos_aaa_mcp stdio

# Or with HTTP transport for testing
HOST=0.0.0.0 PORT=8080 python -m arifos_aaa_mcp http
```

**Verify Tools Available**:
```bash
# Check tool listing
curl http://localhost:8080/tools | jq '.tools[].name'

# Expected output includes:
# - anchor_session
# - reason_mind
# - metabolic_loop  ← NEW
# - ... (13 total)
```

### Step 2: Test Metabolic Loop

```bash
# Test metabolic_loop via REST
curl -X POST http://localhost:8080/tools/metabolic_loop \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Analyze the ethical implications of AI in healthcare",
    "risk_tier": "medium",
    "actor_id": "test@arifos.com"
  }' | jq

# Expected: {"verdict": "SEAL|SABAR|VOID", "stages": {...}, "telemetry": {...}}
```

### Step 3: Test PromptsAsTools

```bash
# List prompts via tool
curl -X POST http://localhost:8080/tools/list_prompts \
  -H "Content-Type: application/json" \
  -d '{}' | jq

# Get specific prompt
curl -X POST http://localhost:8080/tools/get_prompt \
  -H "Content-Type: application/json" \
  -d '{
    "name": "metabolic_loop",
    "arguments": {
      "query": "Test query",
      "risk_tier": "low"
    }
  }' | jq
```

### Step 4: Push to Main

```bash
# Stage changes
git add arifos_aaa_mcp/server.py
git add 333_APPS/L1_PROMPT/
git add docs/ICONOGRAPHY.md
git add docs/SAMPLING_INTEGRATION.md
git add docs/ARCHITECTURE_AUDIT.md

# Commit with conventional message
git commit -m "feat: add 000-999 metabolic loop with PromptsAsTools

- Implement metabolic_loop tool for full constitutional cycle
- Add 11 stage prompts aligned with 000_THEORY
- Integrate PromptsAsTools for tool-only client support
- Add constitutional iconography (ΔΩΨ lanes)
- Update L1_PROMPTS with metabolic loop documentation

Implements: 000_INIT → 999_VAULT governance pipeline
Breaking: None"

# Push to main
git push origin main
```

### Step 5: Deploy to Production

**Option A: Docker Deployment** (Recommended)

```bash
# Build Docker image
cd /root/arifOS
docker build -t arifos-aaa-mcp:v2026.3.1 .

# Tag for production
docker tag arifos-aaa-mcp:v2026.3.1 arifos-aaa-mcp:latest

# Deploy
docker-compose up -d
```

**Option B: Direct Deployment**

```bash
# SSH to production server
ssh root@arifos.arif-fazil.com

# Pull latest code
cd /opt/arifOS
git pull origin main

# Restart service
systemctl restart arifos-mcp

# Or with PM2
pm2 restart arifos-mcp
```

**Option C: Railway/Fly.io** (Cloud)

```bash
# Railway
cd /root/arifOS
railway deploy

# Or Fly.io
fly deploy
```

### Step 6: Post-Deployment Verification

```bash
# Health check
curl https://arifos.arif-fazil.com/health | jq

# Expected:
# {
#   "status": "healthy",
#   "service": "arifos-aaa-mcp",
#   "version": "2026.3.1",
#   "tools_loaded": 14  ← Was 13, now 14 with metabolic_loop
# }

# Test metabolic loop on production
curl -X POST https://arifos.arif-fazil.com/tools/metabolic_loop \
  -H "Authorization: Bearer $ARIFOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Production test",
    "risk_tier": "low"
  }' | jq '.verdict'

# Expected: "SEAL" or "VOID" (not error)
```

---

## Rollback Plan

If issues detected:

```bash
# Revert commit
git revert HEAD

# Or checkout previous version
git checkout HEAD~1 arifos_aaa_mcp/server.py
git commit -m "revert: roll back metabolic_loop due to [issue]"

# Redeploy
docker-compose up -d
```

---

## Monitoring Checklist

### Metrics to Watch

- [ ] Server uptime: `https://arifos.arif-fazil.com/health`
- [ ] Tool response times: `metabolic_loop` should complete < 5s
- [ ] Error rates: Watch for VOID spikes
- [ ] Memory usage: Pydantic models add some overhead
- [ ] API key auth: Ensure unauthorized requests rejected

### Alerts

Set up alerts for:
- HTTP 500 errors
- `metabolic_loop` latency > 10s
- Memory usage > 80%
- Service down

---

## Documentation Updates

After deployment, update:

1. ✅ **API Documentation**: Add `metabolic_loop` to OpenAPI spec
2. ✅ **Client Examples**: Show usage in Python/JS
3. ✅ **README.md**: Mention new unified pipeline tool
4. ✅ **Changelog**: v2026.3.1 release notes

---

## Success Criteria

- [ ] `metabolic_loop` tool appears in `/tools` listing
- [ ] Tool executes successfully with `SEAL` verdict for safe queries
- [ ] Tool returns `VOID` for injection attempts (F12)
- [ ] PromptsAsTools works: `list_prompts` returns metabolic_loop
- [ ] REST endpoint `/tools/metabolic_loop` functional
- [ ] Health check shows 14 tools loaded
- [ ] No regression in existing 13 tools
- [ ] Server memory usage stable
- [ ] No error spikes in logs

---

## Contact

**Deployer**: Arif Fazil  
**Authority**: 888_APEX_JUDGE  
**Emergency**: Revert to `v2026.2.28` if critical issues

**DITEMPA BUKAN DIBERI** — Deploy with confidence.
