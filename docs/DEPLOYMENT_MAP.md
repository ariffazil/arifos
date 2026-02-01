# The Deployment Trinity: Mind, Heart, Soul, and Map

**Version:** v55.1-MAP  
**Date:** 2026-02-01  
**Status:** DEFINED  

---

## 🏛️ The Infrastructure Architecture

Deploying arifOS is not just about running a Python script. It requires a "Trinity" of infrastructure components to ensure the system is **Secure (Sentinel)**, **Accessible (Server)**, and **Comprehensible (Map)**.

```
                  INTERNET
                     │
            ┌────────▼────────┐
            │   THE SENTINEL  │  (Caddy / Heart)
            │  (Auth & TLS)   │
            └────────┬────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌───▼────┐ ┌─────▼──────┐
│  THE SERVER  │ │ THE MAP│ │ THE INSPECTOR
│ (Python MCP) │ │ (Docs) │ │ (Debug UI) │
│    "Mind"    │ │ "Atlas"│ │ "Microscope"
└──────────────┘ └────────┘ └────────────┘
```

---

## 1. The Sentinel (Heart)
**Component:** `caddy` (Docker)  
**Role:** Authentication, TLS Termination, Rate Limiting.  
**Floors Enforced:** F11 (Authority), F12 (Defense).

The Sentinel is the gatekeeper. It ensures that only authorized entities can speak to the Mind.
- **TLS:** Auto-provisioned via Let's Encrypt.
- **Auth:** OAuth2 or Token-based (configured in Caddyfile).
- **Routing:** Directs traffic to API (`/mcp`) or Docs (`/docs`).

## 2. The Server (Mind)
**Component:** `arifos-mcp` (FastAPI / SSE)  
**Role:** The Cognitive Engine (AGI/ASI/APEX).  
**Floors Enforced:** F1-F10, F13.

This is the core logic. It exposes the MCP endpoint via SSE (Server-Sent Events).
- **Endpoint:** `https://arif-fazil.com/sse`
- **Health:** `https://arif-fazil.com/health`

## 3. The Map (Atlas)
**Component:** `caddy` (Static File Server)  
**Role:** Documentation, Schemas, and Canon.  
**URL:** `https://arifos.arif-fazil.com`

The Map provides the "User Manual" for reality. It serves the `docs/` directory directly, ensuring that the documentation is always 1:1 with the deployed code.

## 4. The Inspector (Microscope)
**Component:** `npx @modelcontextprotocol/inspector`  
**Role:** Debugging, Tool Testing, Manual Override.

The Inspector is NOT deployed as a permanent public service (for security). Instead, it is run **locally** by the Sovereign (Developer) and connected via tunnel.

### How to Inspect (The "Sidecar" Pattern)

To inspect the live server:

1.  **Connect via SSH Tunnel:**
    ```bash
    ssh -L 8080:localhost:8080 user@arif-fazil.com
    ```

2.  **Run Inspector Locally:**
    ```bash
    npx @modelcontextprotocol/inspector sse http://localhost:8080/sse
    ```

3.  **Result:**
    Your local browser opens a UI where you can manually trigger `_agi_`, `_vault_`, etc., against the PRODUCTION database, through the secure tunnel.

---

## 🏗️ Docker Composition

See `docker-compose.yml` for the implementation:

- **Service `arifos`:** The Mind.
- **Service `caddy`:** The Sentinel & The Map.
- **Volume `./docs`:** The Atlas Data.
- **Volume `./VAULT999`:** The Soul (Ledger).

---

## 🔒 Security Note

We intentionally **DO NOT** expose the Inspector to the public internet. It is a "God Mode" tool. Accessing it requires F11 (Command) verification via SSH keys.
