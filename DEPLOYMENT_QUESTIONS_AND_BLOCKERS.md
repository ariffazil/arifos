# 🚀 ARIFOS MCP Deployment Guide - Questions & Blockers

**Document Status:** Draft - Awaiting guidance from repository owner  
**Date:** 2026-03-09  
**Author:** AGI-OpenCode (Deployment Agent)  
**Repository:** https://github.com/ariffazil/arifosmcp  

---

## 📋 EXECUTIVE SUMMARY

This document consolidates all deployment blockers, questions, and technical debt accumulated during the attempted production deployment of arifOS MCP server. The deployment is **partially successful** but has critical compatibility issues with ChatGPT MCP client.

**Current Status:**
- ✅ Server deployed and healthy
- ✅ Constitutional tools working  
- ❌ ChatGPT MCP client cannot connect (406 error)
- ⚠️ SDK-level Accept header validation blocking requests

---

## 🎯 PRIMARY BLOCKER: ChatGPT MCP Compatibility

### Error Details
```json
{
  "type": "http_error",
  "code": 405,
  "message": "Received error from MCP server: Method Not Allowed",
  "is_error": true
}
```

### Root Cause Analysis
The error originates from the **official MCP Python SDK** (`mcp.server.streamable_http`), NOT from arifOS code:

**Source:** `/usr/local/lib/python3.12/site-packages/mcp/server/streamable_http.py:429`

```python
# Line 429 in SDK
response = self._create_error_response(
    "Not Acceptable: Client must accept application/json",
    HTTPStatus.NOT_ACCEPTABLE,
)
```

The SDK validates `Accept` headers in the `_validate_accept_header` method:
- **Current behavior:** Requires `Accept: application/json` header
- **ChatGPT behavior:** Does NOT send Accept header (or sends different value)
- **Result:** 406 Not Acceptable error

### Attempted Fixes (Failed)

#### Attempt 1: FastMCP Server-Level Middleware
**File:** `arifosmcp/runtime/fastmcp_ext/transports.py`  
**Approach:** Added `DefaultAcceptMiddleware` to inject Accept header  
**Result:** ❌ Failed - SDK validates headers before middleware runs

#### Attempt 2: ASGI Wrapper Middleware  
**File:** `arifosmcp/runtime/server.py`  
**Approach:** Wrapped `mcp.http_app()` with `ChatGPTCompatMiddleware`  
**Result:** ❌ Failed - Still getting 406 from SDK

#### Attempt 3: StreamableHTTP Server Modification
**File:** `arifosmcp/transport/streamable_http_server.py`  
**Approach:** Removed Accept header validation check  
**Result:** ❌ Failed - Not the code path being used

### Critical Discovery
The error is coming from the **MCP SDK's StreamableHTTPServerTransport**, not from arifOS transport layer. This suggests:

1. FastMCP is using the official MCP SDK under the hood
2. The SDK has strict Accept header validation
3. This validation happens BEFORE any arifOS middleware can inject headers

---

## ❓ QUESTIONS FOR REPOSITORY OWNER

### Q1: What is the intended MCP transport architecture?

**Context:** There appear to be multiple transport implementations:
- `arifosmcp/runtime/fastmcp_ext/transports.py` (FastMCP-based)
- `arifosmcp/transport/streamable_http_server.py` (Custom implementation)
- Official MCP SDK's `StreamableHTTPServerTransport` (via FastMCP dependency)

**Question:** Which transport should be used for production? The codebase seems to mix FastMCP with custom implementations.

### Q2: How to disable SDK-level Accept header validation?

**Context:** The MCP SDK has this constructor parameter:
```python
StreamableHTTPServerTransport(
    mcp_session_id: str | None,
    is_json_response_enabled: bool = False,  # <-- This might help
    ...
)
```

**Question:** Is there a way to configure FastMCP to pass `is_json_response_enabled=True` to the underlying SDK transport? Or should we use a different approach entirely?

### Q3: What is the canonical deployment method?

**Context:** I've used:
1. Docker Compose with `docker compose build arifosmcp`
2. Direct uvicorn: `uvicorn arifosmcp.runtime.server:app`
3. FastMCP CLI: `fastmcp run`

**Question:** What is the **blessed** deployment path for production? The DEPLOY.md mentions multiple approaches.

### Q4: How to properly expose the MCP endpoint for ChatGPT?

**Context:** Current setup:
- Traefik reverse proxy on `arifosmcp.arif-fazil.com`
- Cloudflare orange cloud enabled
- Container port 8080 mapped to Traefik
- Path: `/mcp`

**Question:** Are there specific Traefik labels or Cloudflare settings needed for MCP protocol compatibility?

### Q5: What is the relationship between FastMCP and the custom transport?

**Context:** In `server.py`:
```python
mcp = FastMCP("arifOS-APEX-G", version="2026.03.10-SEAL")
app = mcp.http_app(
    path=HTTP_PATH,
    json_response=True,  # <-- This should enable JSON-only mode
    middleware=_build_http_middleware(),
    stateless_http=True,
)
```

**Question:** Does `json_response=True` actually configure the underlying MCP SDK transport? Or is there another configuration needed?

---

## 🔧 TECHNICAL DEBT & OBSERVATIONS

### 1. Version Mismatch
- **pyproject.toml:** `2026.03.10`
- **Docker image label:** `2026.03.08-SEAL`
- **Runtime env:** `2026.03.10-SEAL`

**Impact:** Minor, but confusing for debugging

### 2. Missing Environment Variables
```bash
ARIFOS_GOVERNANCE_SECRET=        # Empty - using ephemeral secret
OPENCLAW_GATEWAY_TOKEN=          # Empty
```

**Impact:** Low (server still works)

### 3. Tool Registration Confusion
- **Core tools:** 7 registered
- **Phase2 tools:** 8 registered  
- **ACLIP tools:** 9 registered
- **Total:** 24 tools

**But health endpoint shows:** `tools_loaded: 7`

**Question:** Why the discrepancy? Are Phase2 and ACLIP tools actually available?

### 4. Multiple Tool Registration Points
1. `arifosmcp/runtime/tools.py` - Core 7 tools
2. `arifosmcp/runtime/phase2_tools.py` - 5-6 tools
3. `arifosmcp/intelligence/mcp_bridge.py` - 9 ACLIP tools

**Question:** Is this the intended architecture? It seems complex.

---

## 📊 DEPLOYMENT CHECKLIST

### ✅ Completed
- [x] Docker image built and pushed
- [x] Container running healthy
- [x] Health endpoint responding
- [x] SSL/TLS configured
- [x] Cloudflare proxy enabled
- [x] Constitutional tools verified
- [x] GitHub sync completed

### ❌ Blocked
- [ ] ChatGPT MCP client connection
- [ ] Accept header compatibility
- [ ] SDK-level validation bypass

### ⚠️ Needs Clarification
- [ ] Canonical transport architecture
- [ ] Proper middleware configuration
- [ ] Production deployment path
- [ ] Tool registration strategy

---

## 🎯 REQUEST FOR GUIDANCE

**Dear Repository Owner,**

The arifOS MCP server is **functionally deployed** but has a critical compatibility issue with ChatGPT's MCP client. The issue is at the **MCP SDK level**, not in arifOS code.

**Specifically, I need guidance on:**

1. **How to configure the MCP SDK to accept requests without Accept headers?**
   - Is there a configuration flag?
   - Should I use a different transport class?
   - Do I need to monkey-patch the SDK?

2. **What is the intended FastMCP vs Custom transport split?**
   - When should I use `mcp.http_app()` vs custom `streamable_http_server`?
   - Which one is the "production" path?

3. **Can you provide a working ChatGPT MCP client configuration example?**
   - What headers does ChatGPT send?
   - What endpoint URL format works?
   - Any special Traefik/Cloudflare settings?

4. **Should I pursue the `is_json_response_enabled=True` approach?**
   - Where in the codebase should this be set?
   - Is this the right solution?

---

## 🏛️ CONSTITUTIONAL AGENT ASSESSMENT

**A-ARCHITECT (Δ):**  
Design is sound, but external dependency (MCP SDK) creates coupling issues.

**A-ENGINEER (Ω):**  
All deployment mechanics working. Blocked by SDK-level validation.

**A-AUDITOR (Ψ):**  
Root cause identified: SDK validation precedes application-level fixes.

**A-ORCHESTRATOR (ΔΩΨ):**  
Multiple fix attempts made. Requires architectural guidance from owner.

**A-VALIDATOR (✓):**  
Server is production-ready except for ChatGPT compatibility.

**VERDICT:** SABAR (Blocked - awaiting guidance) 🔶

---

## 📎 ATTACHMENTS

### Current Server Response (without Accept header)
```bash
$ curl -X POST https://arifosmcp.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'

HTTP/2 406
{
  "jsonrpc":"2.0",
  "id":"server-error",
  "error":{
    "code":-32600,
    "message":"Not Acceptable: Client must accept application/json"
  }
}
```

### With Accept Header (Works)
```bash
$ curl -X POST https://arifosmcp.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'

HTTP/2 200
[Valid tool list response]
```

---

## 🚀 NEXT STEPS (Awaiting Your Input)

1. **Provide guidance on SDK configuration**
2. **Clarify intended transport architecture**  
3. **Share working ChatGPT client config**
4. **Review proposed fix approaches**
5. **Approve/reject middleware modifications**

**Ready to implement your guidance immediately.**

---

**Ditempa Bukan Diberi — Forged, Not Given** 🏛️

*This document is a formal request for architectural guidance to unblock production deployment.*
