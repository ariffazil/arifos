# 🏗️ Trinity Deployment Architecture — GEOX + arifOSMCP
═══════════════════════════════════════════════════════════════════════════════
**DITEMPA BUKAN DIBERI** | Version: 2026.04.09

## 1. Executive Summary
The deployment model has transitioned from a monolithic container approach to a **Dedicated Project Stack** within the Trinity Architecture. This ensures that the **Earth Witness (GEOX)** remains a sovereign, modular component that can be updated independently of the central kernel (`arifosmcp`).

## 2. Infrastructure Topology
GEOX is deployed as a standalone Docker Compose project (`-p geox`) on the VPS, communicating with the central Traefik edge router via the `traefik_network`.

### Services
- **geox_gui** (React/Vite): The visual surface. Bound to `geox.arif-fazil.com/`.
- **geox_server** (FastMCP): The intelligence kernel. Bound to `geox.arif-fazil.com/mcp` and `/sse`.

## 3. Traefik Routing & Networking
To resolve cross-container connectivity and "504 Gateway Time-out" issues, the following standards are enforced:
- **Shared Network**: All Trinity services must join the `traefik_network`.
- **Explicit Network Label**: Every service MUST specify `traefik.docker.network=traefik_network` to guide Traefik towards the correct proxy interface.

```yaml
labels:
  # Standard Routing
  - "traefik.http.routers.geox-api.rule=Host(`geox.arif-fazil.com`) && (PathPrefix(`/health`) || PathPrefix(`/mcp`))"
  # Network Enforcement
  - "traefik.docker.network=traefik_network"
```

## 4. Trinity Linking (Cross-Project)
The **GEOX GUI** explicitly metadata-links to other Trinity organs:
- **Central Kernel**: `https://arifosmcp.arif-fazil.com`
- **GeoVault**: `https://vault.arifosmcp.arif-fazil.com`
- **Ω-Wiki**: `https://wiki.arif-fazil.com`

---
*Sealed: 2026.04.09*
*Status: PRODUCTION READY*
