# arifOS MCP Architecture

## Hierarki Komponen

```
arifOS Ecosystem
┌─────────────────────────────────────────┐
│  arifOS — Constitutional OS             │
│  (13 Floors, APEX-THEORY, ΔΩΨ)          │
└─────────────────────────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    ▼              ▼              ▼
┌─────────┐  ┌──────────┐  ┌─────────────┐
│AAA-MCP  │  │ACLIP-CAI │  │arifos-router│
│(5-Core) │  │(10-Sense)│  │(canonical  │
│         │  │          │  │ MCP face)   │
└─────────┘  └──────────┘  └─────────────┘
                              │
                         ┌────┴────┐
                         ▼         ▼
                      Public    Internal
                      (8080)    (localhost)
```

## Definisi

| Komponen | Definisi | Akses |
|----------|----------|-------|
| **arifOS** | Constitutional OS — 13 Floors, APEX-THEORY, governance kernel | Konsep |
| **AAA-MCP** | MCP wrapper — 5-Core constitutional pipeline (INIT→AGI→ASI→APEX→VAULT) | Public (port 8080) |
| **ACLIP-CAI** | Sensory console — 10-sense nervous system (system_health, fs_inspect, etc.) | Localhost only |
| **arifos-router** | Gateway — canonical MCP face of arifOS, routes to AAA+ACLIP | Public (port 8080) |

> **Ayat canonical:** *"arifos-router is the canonical MCP face of arifOS."*

## Penggunaan

### Mode Kanonikal (Production)

```bash
# Satu entry point, dua backend
arifos-router --sse --port 8080
```

- Router spawn AAA-MCP + ACLIP-CAI
- Route: `aclip_*` → ACLIP, lain → AAA
- ACLIP bind localhost (tidak exposed)

### Mode Berasingan (Development)

```bash
# Terminal 1: Constitutional
aaa-mcp --sse --port 8080

# Terminal 2: Sensory (localhost only)
aclip-server --sse --port 50080
```

### CLI Tools

```bash
# Direct ACLIP CLI (tanpa MCP)
aclip-cai health
aclip-cai fs --path /root/arifOS --depth 2
aclip-cai logs --lines 100
```

## Messaging Luar

| Platform | Nama | Penjelasan |
|----------|------|------------|
| PyPI | `arifos` | "MCP gateway untuk arifOS constitutional OS" |
| Railway | "arifOS MCP Server" | "Deployed as arifos-router (AAA-MCP + ACLIP-CAI)" |
| LobeHub | "arifOS" | "Constitutional governance via arifos-router" |

## Governance Audit

| Floor | Status |
|-------|--------|
| **F1 Amanah** | ✅ Router reversible; boleh fallback ke AAA-only |
| **F2 Truth** | ✅ Pattern selari MCP gateway best practice |
| **F11 Sovereignty** | ✅ ACLIP mediated oleh constitutional kernel |
| **F12 Injection** | ✅ Boundary exists; ACLIP localhost only |

---

*Ditempa Bukan Diberi* 🔥
