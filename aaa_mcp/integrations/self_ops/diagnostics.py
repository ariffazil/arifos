"""
Self-Ops Module for arifOS MCP Bridge

Infrastructure health monitoring, protocol compatibility checks,
and auto-remediation for the MCP transport layer.

This is NOT part of the constitutional kernel — it's operational
plumbing that keeps the bridge healthy so the kernel can govern.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import asyncio
import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import httpx
from starlette.requests import Request
from starlette.responses import JSONResponse


@dataclass
class HealthCheckResult:
    """Result of a single health check."""

    name: str
    status: str  # "healthy", "degraded", "failed"
    latency_ms: float
    details: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    remediation: Optional[str] = None


@dataclass
class SelfOpsReport:
    """Complete self-operations report."""

    timestamp: str
    overall_status: str  # "healthy", "degraded", "critical"
    version: str
    checks: List[HealthCheckResult]
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "overall_status": self.overall_status,
            "version": self.version,
            "checks": [
                {
                    "name": c.name,
                    "status": c.status,
                    "latency_ms": round(c.latency_ms, 2),
                    "details": c.details,
                    "error": c.error,
                    "remediation": c.remediation,
                }
                for c in self.checks
            ],
            "recommendations": self.recommendations,
        }


class SelfOpsDiagnostics:
    """
    Self-operations diagnostics for arifOS MCP bridge.

    Monitors:
    - REST API reachability
    - /health endpoint status
    - MCP protocol compatibility
    - SSE handshake completion
    - All expected endpoints responding
    """

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv("ARIFOS_BASE_URL", "http://localhost:8080")
        self.version = "2026.02.17-FORGE-VPS-SEAL"

    async def run_full_diagnostic(self) -> SelfOpsReport:
        """Run complete self-diagnostic suite."""
        checks = []

        # Run all checks concurrently
        check_results = await asyncio.gather(
            self._check_rest_api(),
            self._check_health_endpoint(),
            self._check_mcp_endpoints(),
            self._check_protocol_compatibility(),
            self._check_sse_handshake(),
            self._check_well_known_endpoint(),
            return_exceptions=True,
        )

        for result in check_results:
            if isinstance(result, Exception):
                checks.append(
                    HealthCheckResult(
                        name="unknown",
                        status="failed",
                        latency_ms=0.0,
                        error=str(result),
                    )
                )
            else:
                checks.append(result)

        # Determine overall status
        failed = sum(1 for c in checks if c.status == "failed")
        degraded = sum(1 for c in checks if c.status == "degraded")

        if failed >= 2:
            overall = "critical"
        elif failed == 1 or degraded >= 2:
            overall = "degraded"
        else:
            overall = "healthy"

        # Generate recommendations
        recommendations = self._generate_recommendations(checks)

        return SelfOpsReport(
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            overall_status=overall,
            version=self.version,
            checks=checks,
            recommendations=recommendations,
        )

    async def _check_rest_api(self) -> HealthCheckResult:
        """Check if REST API is reachable."""
        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/")
                latency = (time.time() - start) * 1000

                if response.status_code == 200:
                    return HealthCheckResult(
                        name="rest_api",
                        status="healthy",
                        latency_ms=latency,
                        details={"status_code": response.status_code},
                    )
                else:
                    return HealthCheckResult(
                        name="rest_api",
                        status="degraded",
                        latency_ms=latency,
                        details={"status_code": response.status_code},
                        error=f"Unexpected status: {response.status_code}",
                        remediation="Check application logs for errors",
                    )
        except Exception as e:
            latency = (time.time() - start) * 1000
            return HealthCheckResult(
                name="rest_api",
                status="failed",
                latency_ms=latency,
                error=str(e),
                remediation="Verify server is running and base_url is correct",
            )

    async def _check_health_endpoint(self) -> HealthCheckResult:
        """Check /health endpoint."""
        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/health")
                latency = (time.time() - start) * 1000

                if response.status_code == 200:
                    data = response.json()
                    return HealthCheckResult(
                        name="health_endpoint",
                        status="healthy",
                        latency_ms=latency,
                        details=data,
                    )
                else:
                    return HealthCheckResult(
                        name="health_endpoint",
                        status="failed",
                        latency_ms=latency,
                        details={"status_code": response.status_code},
                        error=f"Health check failed: {response.status_code}",
                        remediation="Check server health and dependencies",
                    )
        except Exception as e:
            latency = (time.time() - start) * 1000
            return HealthCheckResult(
                name="health_endpoint",
                status="failed",
                latency_ms=latency,
                error=str(e),
                remediation="Verify /health endpoint is implemented",
            )

    async def _check_mcp_endpoints(self) -> HealthCheckResult:
        """Check all MCP tool endpoints."""
        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/tools")
                latency = (time.time() - start) * 1000

                if response.status_code == 200:
                    data = response.json()
                    tool_count = data.get("count", 0)

                    if tool_count >= 9:  # Expect at least 9 A-CLIP tools
                        return HealthCheckResult(
                            name="mcp_endpoints",
                            status="healthy",
                            latency_ms=latency,
                            details={"tool_count": tool_count, "tools": data.get("tools", [])},
                        )
                    else:
                        return HealthCheckResult(
                            name="mcp_endpoints",
                            status="degraded",
                            latency_ms=latency,
                            details={"tool_count": tool_count},
                            error=f"Only {tool_count} tools registered, expected 9+",
                            remediation="Check tool registration in server.py",
                        )
                else:
                    return HealthCheckResult(
                        name="mcp_endpoints",
                        status="failed",
                        latency_ms=latency,
                        details={"status_code": response.status_code},
                        error=f"/tools endpoint failed: {response.status_code}",
                    )
        except Exception as e:
            latency = (time.time() - start) * 1000
            return HealthCheckResult(
                name="mcp_endpoints",
                status="failed",
                latency_ms=latency,
                error=str(e),
                remediation="Verify MCP tools are properly registered",
            )

    async def _check_protocol_compatibility(self) -> HealthCheckResult:
        """Check MCP protocol compatibility."""
        start = time.time()
        try:
            # Check if server.json is valid MCP schema
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/.well-known/mcp/server.json")
                latency = (time.time() - start) * 1000

                if response.status_code == 200:
                    data = response.json()
                    required_fields = ["name", "version", "tools"]
                    missing = [f for f in required_fields if f not in data]

                    if not missing:
                        return HealthCheckResult(
                            name="protocol_compatibility",
                            status="healthy",
                            latency_ms=latency,
                            details={
                                "schema_valid": True,
                                "server_name": data.get("name"),
                                "version": data.get("version"),
                            },
                        )
                    else:
                        return HealthCheckResult(
                            name="protocol_compatibility",
                            status="degraded",
                            latency_ms=latency,
                            details={"missing_fields": missing},
                            error=f"Missing required fields: {missing}",
                            remediation="Update server.json with required MCP schema fields",
                        )
                else:
                    return HealthCheckResult(
                        name="protocol_compatibility",
                        status="failed",
                        latency_ms=latency,
                        error=f"server.json not accessible: {response.status_code}",
                        remediation="Verify .well-known/mcp/server.json endpoint",
                    )
        except Exception as e:
            latency = (time.time() - start) * 1000
            return HealthCheckResult(
                name="protocol_compatibility",
                status="failed",
                latency_ms=latency,
                error=str(e),
                remediation="Check MCP registry auto-discovery endpoint",
            )

    async def _check_sse_handshake(self) -> HealthCheckResult:
        """Check SSE endpoint availability."""
        start = time.time()
        try:
            # SSE endpoints don't respond to regular GET with body,
            # but we can check if the endpoint exists
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    f"{self.base_url}/sse", headers={"Accept": "text/event-stream"}
                )
                latency = (time.time() - start) * 1000

                # SSE endpoint might return 200 with stream or require specific headers
                # We consider it healthy if it's reachable (not 404)
                if response.status_code in [
                    200,
                    405,
                    401,
                ]:  # 405 = method not allowed (expected for GET on POST endpoint)
                    return HealthCheckResult(
                        name="sse_handshake",
                        status="healthy",
                        latency_ms=latency,
                        details={"status_code": response.status_code},
                    )
                elif response.status_code == 404:
                    return HealthCheckResult(
                        name="sse_handshake",
                        status="failed",
                        latency_ms=latency,
                        details={"status_code": 404},
                        error="SSE endpoint not found",
                        remediation="Verify SSE transport is enabled in server configuration",
                    )
                else:
                    return HealthCheckResult(
                        name="sse_handshake",
                        status="degraded",
                        latency_ms=latency,
                        details={"status_code": response.status_code},
                    )
        except Exception as e:
            latency = (time.time() - start) * 1000
            return HealthCheckResult(
                name="sse_handshake",
                status="failed",
                latency_ms=latency,
                error=str(e),
                remediation="Verify SSE endpoint is properly configured",
            )

    async def _check_well_known_endpoint(self) -> HealthCheckResult:
        """Check .well-known/mcp/server.json endpoint."""
        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/.well-known/mcp/server.json")
                latency = (time.time() - start) * 1000

                if response.status_code == 200:
                    data = response.json()
                    return HealthCheckResult(
                        name="well_known_endpoint",
                        status="healthy",
                        latency_ms=latency,
                        details={
                            "accessible": True,
                            "content_type": response.headers.get("content-type"),
                            "size_bytes": len(response.content),
                        },
                    )
                else:
                    return HealthCheckResult(
                        name="well_known_endpoint",
                        status="failed",
                        latency_ms=latency,
                        details={"status_code": response.status_code},
                        error=f"Well-known endpoint returned {response.status_code}",
                        remediation="Verify .well-known/mcp/server.json route is registered",
                    )
        except Exception as e:
            latency = (time.time() - start) * 1000
            return HealthCheckResult(
                name="well_known_endpoint",
                status="failed",
                latency_ms=latency,
                error=str(e),
                remediation="Check if static/.well-known/mcp/server.json exists and is served",
            )

    def _generate_recommendations(self, checks: List[HealthCheckResult]) -> List[str]:
        """Generate remediation recommendations based on failed checks."""
        recommendations = []

        for check in checks:
            if check.status in ["failed", "degraded"] and check.remediation:
                recommendations.append(f"[{check.name}] {check.remediation}")

        # Add general recommendations if multiple failures
        failed_count = sum(1 for c in checks if c.status == "failed")
        if failed_count >= 3:
            recommendations.append(
                "[CRITICAL] Multiple system failures detected. "
                "Consider restarting the MCP server and checking logs."
            )

        if not any(c.name == "well_known_endpoint" and c.status == "healthy" for c in checks):
            recommendations.append(
                "[REGISTRY] MCP registry auto-discovery may fail. "
                "Ensure static/.well-known/mcp/server.json is properly served."
            )

        return recommendations


# Singleton instance
_self_ops: Optional[SelfOpsDiagnostics] = None


def get_self_ops() -> SelfOpsDiagnostics:
    """Get singleton SelfOpsDiagnostics instance."""
    global _self_ops
    if _self_ops is None:
        _self_ops = SelfOpsDiagnostics()
    return _self_ops


async def self_diagnose(request: Optional[Request] = None) -> JSONResponse:
    """
    MCP tool: self_diagnose

    Runs full self-operations diagnostic and returns health report.
    This is the operational layer, not constitutional governance.
    """
    ops = get_self_ops()
    report = await ops.run_full_diagnostic()

    return JSONResponse(report.to_dict())
