# arifOS VPS — Capabilities Map

**Last Verified:** 2026-03-12 (Highest Intelligence State)
**Reference:** [Unified Architecture Snapshot](./VPS_ARCHITECTURE.md)

> **Mandate:** This document maps the active tooling, networking, and software capabilities of the VPS. It must be updated synchronously with `VPS_ARCHITECTURE.md`.

---

## 1. Core Artificial Intelligence Stack
- **arifOS AAA MCP Server:** Active (systemd: `arifos-mcp`)
- **Reasoning Engines:** `agent_zero_reasoner`, `openclaw_gateway`
- **Local Model Hosting:** `ollama_engine` (Docker, Up 2 hours)
- **Vector Memory:** `qdrant_memory` (Docker, Up 2 hours)
- **Agent Workflow:** `arifos_n8n` (Docker)

## 2. "Office Forge" Toolchain (Human-Centric Output)
*Deployed on 2026-03-12 to enable high-end corporate document generation.*

- **Slide Generation:** `Marp CLI v4.2.3` (Markdown to PPTX/PDF)
- **Diagramming:** `Mermaid CLI` (SVG/PNG Flowcharts)
- **Programmatic Documents:** Python `uv` stack (`python-pptx`, `python-docx`, `pandas`, `plotly`)
- **Image Processing:** `ImageMagick 7.1.2` (Hardened for PDF/SVG)
- **Renderer:** `Chromium` (Headless rendering for Marp/Puppeteer)

## 3. Data & Storage
- **Relational DB:** `arifos_postgres` (Healthy)
- **Cache / Ledger:** `arifos_redis` (Healthy)

## 4. Telemetry & Routing
- **Reverse Proxy:** `traefik_router`
- **Metrics & Dashboards:** `arifos_prometheus`, `arifos_grafana`

## 5. Connectivity & Synchronization Mesh
- **Private Network (VPN):** `Tailscale v1.94.2` (Node: `srv1325122`)
- **File Synchronization:** `Syncthing` (Active via `syncthing@root`)
- **Internal Web Server:** `Caddy` (Port 8081 - Serving Workspace Files)

---
*Note: The VPS is operating at 55% disk capacity (106GB/193GB) and 22% memory usage (3.4GB/15Gi).*
