# arifOS AAA MCP Hardening Plan
## Based on MCP Wrapper Specification v2026.03.24

---

## EXECUTIVE SUMMARY

This plan hardens arifOS AAA MCP to be a **production-grade, specification-compliant MCP server** with:
- ✅ Schema-driven tool discovery and validation
- ✅ Canonical contract normalization
- ✅ Strict/compat mode validation
- ✅ Comprehensive error taxonomy
- ✅ Retry/backoff with circuit breaker
- ✅ Audit logging and observability
- ✅ Security hardening (OWASP-aligned)

---

## PHASE 0: FOUNDATION (Day 1)
**Goal: Stabilize current system, fix critical bugs**

### Tasks:
1. ✅ Fix remaining function signature mismatches
2. ✅ Ensure all 11 tools pass E2E tests
3. ✅ Implement proper SSE response parsing
4. ✅ Fix scar_context persistence
5. ✅ Create comprehensive test suite

### Deliverables:
- All 42 tool-mode combinations pass
- 100% E2E success rate
- Zero function signature errors

---

## PHASE 1: SCHEMA INFRASTRUCTURE (Days 2-3)
**Goal: Implement schema-driven architecture**

### Tasks:
1. Create canonical envelope schema
2. Implement tool schema registry
3. Build schema diff detector
4. Create alias mapping system
5. Implement strict/compat validation modes

### Files to Create:
- `arifosmcp/mcp_wrapper/schema.py` - JSON Schema definitions
- `arifosmcp/mcp_wrapper/validator.py` - Validation engine
- `arifosmcp/mcp_wrapper/normalizer.py` - Field alias mapping
- `arifosmcp/mcp_wrapper/registry.py` - Tool schema registry

### Deliverables:
- Canonical envelope validation
- Field alias normalization
- Schema drift detection

---

## PHASE 2: ERROR TAXONOMY & HANDLING (Day 4)
**Goal: Implement MCP-compliant error handling**

### Tasks:
1. Define JSON-RPC error codes
2. Separate protocol errors vs tool execution errors
3. Implement error taxonomy
4. Add structured error responses

### Error Code Mapping:
```
-32602: Invalid params (validation failure)
-32010: Approval required
-32020: Unauthorized/Forbidden
-32030: Upstream unavailable
-32603: Internal error
```

### Files to Modify:
- `arifosmcp/runtime/tools.py` - Add error taxonomy
- `arifosmcp/runtime/models.py` - Add error structures

---

## PHASE 3: RETRY & RESILIENCE (Day 5)
**Goal: Implement single-layer retry with backoff**

### Tasks:
1. Exponential backoff with jitter
2. Circuit breaker pattern
3. Idempotency key handling
4. Rate limiting compliance

### Files to Create:
- `arifosmcp/mcp_wrapper/resilience.py` - Retry logic
- `arifosmcp/mcp_wrapper/circuit_breaker.py` - Circuit breaker

---

## PHASE 4: AUTH & APPROVAL FLOWS (Days 6-7)
**Goal: Implement explicit/implicit approval system**

### Tasks:
1. Privileged tools registry
2. Explicit approval flow
3. Implicit approval for read-only tools
4. Auth context propagation
5. OAuth-compatible token handling

### Files to Create:
- `arifosmcp/mcp_wrapper/approval.py` - Approval engine
- `arifosmcp/mcp_wrapper/auth.py` - Auth context manager

---

## PHASE 5: OBSERVABILITY & AUDIT (Day 8)
**Goal: Comprehensive logging and metrics**

### Tasks:
1. Structured audit logging
2. Token redaction
3. Metrics collection
4. Correlation ID tracking
5. Performance monitoring

### Files to Create:
- `arifosmcp/mcp_wrapper/audit.py` - Audit logging
- `arifosmcp/mcp_wrapper/metrics.py` - Metrics collection

---

## PHASE 6: SECURITY HARDENING (Day 9)
**Goal: OWASP-aligned security controls**

### Tasks:
1. Origin validation (prevent DNS rebinding)
2. Session ID secure handling
3. Token hygiene (no passthrough)
4. Scope minimization
5. SSRF mitigation
6. Input sanitization

### Files to Create:
- `arifosmcp/mcp_wrapper/security.py` - Security middleware

---

## PHASE 7: INTEGRATION & TESTING (Days 10-11)
**Goal: Full integration test suite**

### Tasks:
1. Unit tests for all wrapper components
2. Integration tests for all tools
3. Transport simulation tests
4. Load/stress tests
5. Security penetration tests

### Files to Create:
- `tests/mcp_wrapper/` - Comprehensive test suite

---

## PHASE 8: DOCUMENTATION & DEPLOYMENT (Day 12)
**Goal: Production deployment**

### Tasks:
1. API documentation
2. Deployment guide
3. Migration guide
4. Final seal verification
5. Production deploy

---

## RESOURCE REQUIREMENTS

### Time: 12 days
### Compute: Current VPS sufficient
### Storage: ~2GB for new modules and tests

---

## RISK MITIGATION

| Risk | Mitigation |
|------|------------|
| Breaking changes | Phase 0 ensures backward compatibility |
| Performance degradation | Single-layer retry, caching |
| Security vulnerabilities | OWASP alignment, audit trails |
| Schema drift | Automated diff detection |

---

## SUCCESS CRITERIA

- ✅ 100% E2E test pass rate
- ✅ Zero critical security vulnerabilities
- ✅ <100ms latency overhead
- ✅ 99.9% uptime with circuit breaker
- ✅ Full MCP specification compliance

---

**Motto: Ditempa Bukan Diberi** 🔥
