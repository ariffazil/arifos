"""
aaa_mcp/integrations/openclaw_gateway_client.py

Read-only OpenClaw gateway diagnostics for arifOS MCP.

Protocol note: OpenClaw's management API is a custom WebSocket protocol with a
handshake (`onHelloOk` callback + scoped role negotiation). Implementing a
full WS client here would require mirroring the TS GatewayClient internals.
Instead this module uses:
  1. HTTP reachability probe (GET /healthz → 200 is sufficient for liveness)
  2. Container introspection via `docker inspect` (if docker is available on host)
  3. Environment/config reads for model + version metadata

All functions are synchronous, read-only, and never touch openclaw.json or compose files.
"""

from __future__ import annotations

import json
import os
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any

# Gateway URL: internal Docker network name, reachable from arifosmcp_server container
# when both are on arifos_arifos_trinity (10.0.10.0/24)
_GATEWAY_URL = os.environ.get("OPENCLAW_URL", "http://openclaw_gateway:18789")
_GATEWAY_TOKEN = os.environ.get(
    "OPENCLAW_GATEWAY_TOKEN",
    "8eb24ba06e138bf7affe6f128fdecc2e80a9290d107d83585540ae6ba541ae54",
)
_HEALTHZ_PATH = "/healthz"
_TIMEOUT_S = 5

import logging

logger = logging.getLogger(__name__)


def _http_probe(path: str) -> dict[str, Any]:
    """HTTP GET probe — returns ok, status_code, latency_ms."""
    url = f"{_GATEWAY_URL}{path}"
    t0 = datetime.now(timezone.utc)
    try:
        req = urllib.request.Request(url, headers={"X-OpenClaw-Token": _GATEWAY_TOKEN})
        with urllib.request.urlopen(req, timeout=_TIMEOUT_S) as resp:
            status = resp.status
            latency_ms = round((datetime.now(timezone.utc) - t0).total_seconds() * 1000, 1)
            return {"ok": True, "status_code": status, "latency_ms": latency_ms, "url": url}
    except urllib.error.HTTPError as e:
        return {"ok": False, "status_code": e.code, "error": str(e), "url": url}
    except Exception as e:
        return {"ok": False, "status_code": None, "error": str(e), "url": url}


def _docker_inspect(container: str = "openclaw_gateway") -> dict[str, Any]:
    """docker inspect <container> — returns selected fields only. No-op if docker unavailable."""
    try:
        result = subprocess.run(
            ["docker", "inspect", "--format", "{{json .State}}", container],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        if result.returncode != 0:
            return {"available": False, "error": result.stderr.strip()}
        state = json.loads(result.stdout.strip())
        return {
            "available": True,
            "running": state.get("Running", False),
            "health": state.get("Health", {}).get("Status") if state.get("Health") else None,
            "started_at": state.get("StartedAt"),
        }
    except FileNotFoundError:
        return {"available": False, "error": "docker not in PATH"}
    except Exception as e:
        return {"available": False, "error": str(e)}


def openclaw_get_health() -> dict[str, Any]:
    """
    Liveness probe: HTTP GET /healthz.
    Returns ok, status_code, latency_ms.
    Floors: F2 (truth), F4 (clarity — returns only what we can verify).
    """
    probe = _http_probe(_HEALTHZ_PATH)
    container = _docker_inspect()
    return {
        "gateway_url": _GATEWAY_URL,
        "http_probe": probe,
        "container": container,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "note": (
            "HTTP /healthz returns 200 when the OpenClaw Node.js gateway process is alive. "
            "Full gateway health (models, channels, memory) requires the OpenClaw WS protocol "
            "or the `openclaw health --json` CLI from inside the container."
        ),
    }


def openclaw_get_status() -> dict[str, Any]:
    """
    Gateway status: reachability + container state + config snapshot.
    Reads openclaw.json for model/version metadata (no secrets returned).
    Floors: F2 (truth), F4 (clarity), F7 (humility — marks unknowns explicitly).
    """
    probe = _http_probe(_HEALTHZ_PATH)
    container = _docker_inspect()

    # Read openclaw.json for model config (no auth fields returned)
    config_snapshot: dict[str, Any] = {}
    config_path = os.environ.get(
        "OPENCLAW_CONFIG_PATH",
        "/opt/arifos/data/openclaw/openclaw.json",
    )
    try:
        import json5  # type: ignore

        with open(config_path) as f:
            raw = json5.load(f)
        config_snapshot = {
            "primary_model": raw.get("agents", {})
            .get("defaults", {})
            .get("model", {})
            .get("primary", "unknown"),
            "fallbacks": raw.get("agents", {})
            .get("defaults", {})
            .get("model", {})
            .get("fallbacks", []),
            "gateway_bind": raw.get("gateway", {}).get("bind", "unknown"),
            "gateway_port": raw.get("gateway", {}).get("port", "unknown"),
            "version": raw.get("meta", {}).get("lastTouchedVersion", "unknown"),
        }
    except ImportError:
        # json5 not available — try stdlib json (will fail on comments)
        try:
            with open(config_path) as f:
                raw = json.load(f)
            config_snapshot["primary_model"] = (
                raw.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "unknown")
            )
        except Exception as e:
            config_snapshot = {"error": f"config read failed: {e}"}
    except Exception as e:
        config_snapshot = {"error": f"config read failed: {e}"}

    return {
        "gateway_url": _GATEWAY_URL,
        "http_probe": probe,
        "container": container,
        "config": config_snapshot,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "limitations": {
            "models_list": "UNAVAILABLE — requires openclaw WS protocol or docker exec",
            "channels_status": "UNAVAILABLE — requires openclaw WS protocol or docker exec",
            "vector_memory": "UNAVAILABLE — requires openclaw WS protocol or docker exec",
            "workaround": "Run `docker exec openclaw_gateway openclaw <cmd> --json` from VPS host",
        },
    }
