# Insight: Security Critical Vectors

**Source**: 2026-03-11 red team analysis  
**Pattern Type**: Security/Risk

## CVSS-Critical Vectors

| Vector | CVSS | Mitigation |
|--------|------|------------|
| Docker socket mount | Critical (container escape) | Rootless Docker migration |
| Qdrant unauthenticated | Critical (memory poisoning) | Auth + network isolation |
| API keys in env vars | High (inspect exposure) | Secret management service |
| Telegram 2FA not enforced | Medium | Enable 2FA on bot account |

## F12 Injection Defense Gap

Prompt injection via untrusted content (PDFs, web results) can potentially bypass constitutional floors. Current defense: manual vetting. Automated defense: content sanitization layer needed.

## F13 Single Point of Failure

By design — not a bug. Centralized sovereignty creates post-siege fragility. Consider backup sovereign or co-pilot architecture for continuity, not replacement.

## 888_HOLD Items

- Invasive VPS scan: DECLINED by F13 (acceptable risk tolerance)
- MCP mTLS: PENDING implementation
- Qdrant auth: PENDING implementation

---
*Extracted: 2026-03-23 hygiene cycle*
