# SCARS.md — arifOS Architectural Pivot Ledger
**T000 Version:** 2026.02.17-FORGE-TRINITY-SEAL

> *"The scars are the evidence of the forge."*

## I. Infrastructure Scars

### 1. Railway Deprecation (2026-02-17)
- **Status:** 🗑️ DEPRECATED
- **Reason:** Limited control over system-level hardening (systemd, kernel-level optimizations) and desire for self-sovereign VPC containment.
- **Pivoted to:** Hardened Ubuntu VPS (Hostinger/AWS/DO).
- **Seal:** VAULT999 T000-2026.02.17.

## II. Architectural Scars

### 1. Python SDK Library (2026-02-15)
- **Status:** 🗑️ ARCHIVED
- **Reason:** Redundant with the raw Model Context Protocol (MCP). Wrapping MCP in a client library introduces "the wrapper fallacy" (hiding the grain of the metal).
- **Pivoted to:** Native MCP Tool execution.
