# arifOS Hardened v2 — Production Deployment Checklist

**Version:** 2026.03.22-HARDENED-V2  
**Date:** 2026-03-22  
**Status:** ✅ Code Complete — Ready for Integration

---

## Pre-Flight Validation

### ✅ Code Validation (Completed)

```bash
# Run standalone validation
python test_hardened_standalone.py
```

**Results:**
- [x] contracts_v2.py — 431 lines, syntax OK
- [x] init_anchor_hardened.py — 588 lines, syntax OK
- [x] truth_pipeline_hardened.py — 510 lines, syntax OK
- [x] tools_hardened_v2.py — 561 lines, syntax OK
- [x] hardened_toolchain.py — 312 lines, syntax OK
- [x] **Total: 2,402 lines of hardened code**

### ✅ Feature Verification

- [x] ToolEnvelope standard implemented
- [x] Fail-closed defaults validated
- [x] Cross-tool trace IDs required
- [x] Human decision markers explicit
- [x] Entropy budgets calculated
- [x] 4-lane reasoning in agi_reason
- [x] Counter-seal veto in asi_critique
- [x] Two-phase execution in agentzero
- [x] Machine-verifiable conditions in apex_judge
- [x] Decision objects in vault_seal
- [x] Session classification in init_anchor
- [x] Evidence bundles in reality_compass
- [x] Claim graphs in reality_atlas

---

## Deployment Steps

### Phase 1: Environment Preparation

- [ ] Backup existing arifosmcp/runtime/ directory
- [ ] Verify Python 3.11+ available
- [ ] Check disk space (minimum 10MB for hardened files)
- [ ] Ensure write permissions to arifosmcp/runtime/

### Phase 2: File Deployment

Deploy these files to `arifosmcp/runtime/`:

```
arifosmcp/runtime/
├── contracts_v2.py              [NEW] Core hardened contracts
├── init_anchor_hardened.py      [NEW] Hardened init_anchor
├── truth_pipeline_hardened.py   [NEW] Hardened compass/atlas
├── tools_hardened_v2.py         [NEW] 8 hardened tools
└── hardened_toolchain.py        [NEW] Master integration
```

**Deployment Commands:**
```bash
# Copy hardened files to runtime directory
cp arifosmcp/runtime/contracts_v2.py /path/to/production/arifosmcp/runtime/
cp arifosmcp/runtime/init_anchor_hardened.py /path/to/production/arifosmcp/runtime/
cp arifosmcp/runtime/truth_pipeline_hardened.py /path/to/production/arifosmcp/runtime/
cp arifosmcp/runtime/tools_hardened_v2.py /path/to/production/arifosmcp/runtime/
cp arifosmcp/runtime/hardened_toolchain.py /path/to/production/arifosmcp/runtime/

# Verify deployment
ls -la /path/to/production/arifosmcp/runtime/*hardened* /path/to/production/arifosmcp/runtime/contracts_v2.py
```

### Phase 3: Integration

- [ ] Update tool routing to use hardened implementations
- [ ] Configure trace collection endpoints
- [ ] Set up entropy monitoring
- [ ] Configure human escalation notifications
- [ ] Enable counter-seal alerts

### Phase 4: Configuration

#### Required Environment Variables

```bash
# Constitutional policy version
export ARIFOS_POLICY_VERSION="v2026.03.22-hardened"

# Trace collection
export ARIFOS_TRACE_ENABLED="true"
export ARIFOS_TRACE_STORAGE="/var/log/arifos/traces"

# Entropy thresholds
export ARIFOS_ENTROPY_AMBIGUITY_THRESHOLD="0.6"
export ARIFOS_ENTROPY_CONTRADICTION_THRESHOLD="3"

# Human decision routing
export ARIFOS_HUMAN_ESCALATION_WEBHOOK="https://alerts.example.com/arifos"
export ARIFOS_COUNTER_SEAL_ALERT="critical"
```

#### Optional Tuning

```bash
# Critique threshold (default: 0.6)
export ARIFOS_CRITIQUE_THRESHOLD="0.6"

# Session expiry (default: 3600 seconds)
export ARIFOS_SESSION_EXPIRY="3600"

# Evidence freshness (default: 24 hours)
export ARIFOS_EVIDENCE_FRESHNESS_HOURS="24"
```

### Phase 5: Testing

#### Unit Tests

```bash
# Run hardened toolchain tests
pytest tests/test_hardened_toolchain.py -v

# Expected: 12+ tests passing
```

#### Integration Tests

```bash
# Test full pipeline
python -c "
from arifosmcp.runtime.hardened_toolchain import HardenedToolchain
import asyncio

chain = HardenedToolchain()
result = asyncio.run(chain.execute(
    query='test query',
    declared_name='test',
    session_id='test-001',
    risk_tier='low',
    auth_context={'actor_id': 'test'}
))
print(f'Status: {result.status}')
"
```

#### Fail-Closed Verification

```bash
# Test fail-closed behavior
python -c "
from arifosmcp.runtime.init_anchor_hardened import HardenedInitAnchor
import asyncio

async def test():
    tool = HardenedInitAnchor()
    result = await tool.init(
        declared_name='test',
        intent='test',
        requested_scope=['query'],
        risk_tier='medium',
        auth_context=None,  # Missing auth
        session_id='test'
    )
    assert result.status == 'hold', f'Expected hold, got {result.status}'
    print('✅ Fail-closed working')

asyncio.run(test())
"
```

### Phase 6: Monitoring Setup

#### Metrics to Track

| Metric | Alert Threshold | Action |
|--------|-----------------|--------|
| `fail_closed_triggers` | > 10/hour | Investigate auth issues |
| `counter_seal_activations` | > 5/hour | Review security posture |
| `human_escalations` | > 20/hour | Tune thresholds |
| `entropy_avg` | > 0.5 | Review data quality |
| `trace_completeness` | < 95% | Fix trace collection |

#### Dashboard Queries

```promql
# Fail-closed trigger rate
rate(arifos_fail_closed_total[5m])

# Counter-seal activation rate
rate(arifos_counter_seal_total[5m])

# Average entropy by tool
avg by (tool) (arifos_entropy_ambiguity)

# Human escalation rate
rate(arifos_human_escalation_total[5m])
```

### Phase 7: Rollout

#### Canary Deployment

1. [ ] Deploy to 5% of traffic
2. [ ] Monitor for 1 hour
3. [ ] Check error rates
4. [ ] Verify trace completeness
5. [ ] Deploy to 25% of traffic
6. [ ] Monitor for 4 hours
7. [ ] Deploy to 100% of traffic

#### Rollback Plan

```bash
# If issues detected, rollback to previous version
mv arifosmcp/runtime/contracts_v2.py.bak arifosmcp/runtime/contracts_v2.py
mv arifosmcp/runtime/init_anchor_hardened.py.bak arifosmcp/runtime/init_anchor_hardened.py
# ... etc

# Restart services
systemctl restart arifos
```

---

## Post-Deployment Verification

### Immediate Checks (within 1 hour)

- [ ] Services starting without errors
- [ ] Trace collection working
- [ ] No spike in fail-closed triggers
- [ ] Human escalation routing functional
- [ ] Counter-seal alerts working

### Daily Checks (first week)

- [ ] Review entropy metrics dashboard
- [ ] Check trace completeness > 95%
- [ ] Verify decision objects being sealed
- [ ] Review human escalation patterns
- [ ] Monitor error logs

### Weekly Reviews

- [ ] Tune entropy thresholds based on data
- [ ] Review counter-seal triggers
- [ ] Optimize human escalation routing
- [ ] Update documentation based on learnings

---

## Troubleshooting

### Issue: High Fail-Closed Rate

**Symptoms:** > 50% of requests returning HOLD

**Diagnosis:**
```bash
# Check auth context passing
grep "auth_context required" /var/log/arifos/errors.log

# Check session ID generation
grep "session_id required" /var/log/arifos/errors.log
```

**Resolution:**
- Verify upstream services passing auth_context
- Check session ID generation in middleware
- Review risk tier assignment

### Issue: Counter-Seal Triggering Too Often

**Symptoms:** > 20% of operations blocked by critique

**Resolution:**
- Increase CRITIQUE_THRESHOLD (default: 0.6)
- Review input data quality
- Adjust safety axis sensitivity

### Issue: Trace Collection Incomplete

**Symptoms:** < 90% of operations have traces

**Diagnosis:**
```bash
# Check trace storage connectivity
ping trace-storage.example.com

# Verify trace generation
grep "TraceContext" /var/log/arifos/debug.log
```

**Resolution:**
- Fix trace storage connectivity
- Check disk space on trace storage
- Verify TraceContext generation in all tools

---

## Files Reference

### Hardened Implementation Files

| File | Size | Purpose |
|------|------|---------|
| `contracts_v2.py` | 13.9 KB | Core contract types |
| `init_anchor_hardened.py` | 19.7 KB | Hardened init_anchor (5 modes) |
| `truth_pipeline_hardened.py` | 17.9 KB | Compass + Atlas |
| `tools_hardened_v2.py` | 20.1 KB | 8 hardened tools |
| `hardened_toolchain.py` | 12.9 KB | Master integration |
| **Total** | **84.5 KB** | **2,402 lines** |

### Documentation Files

| File | Purpose |
|------|---------|
| `docs/HARDENING_V2_GUIDE.md` | Comprehensive deployment guide |
| `HARDENING_V2_SUMMARY.md` | Executive summary |
| `HARDENING_V2_COMPLETE.md` | Completion report |
| `PRODUCTION_READINESS_REPORT.md` | Readiness assessment |
| `DEPLOYMENT_CHECKLIST.md` | This file |

### Test Files

| File | Purpose |
|------|---------|
| `tests/test_hardened_toolchain.py` | Test suite |
| `test_hardened_standalone.py` | Standalone validation |

---

## Support Contacts

| Role | Contact | Escalation |
|------|---------|------------|
| Technical Lead | arif@example.com | P1: 24/7 |
| Security Team | security@example.com | P1: 24/7 |
| Operations | ops@example.com | P2: Business hours |

---

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| Security Reviewer | | | |
| Operations Lead | | | |
| Product Owner | | | |

---

**Version:** 2026.03.22-HARDENED-V2  
**Last Updated:** 2026-03-22  
**Status:** Ready for Deployment
