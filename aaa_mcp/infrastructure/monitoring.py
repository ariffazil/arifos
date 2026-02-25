"""
arifOS Production Monitoring
============================

Metrics, health checks, and alerting for civilization deployment.

DITEMPA BUKAN DIBERI
"""

import asyncio
import inspect
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class PipelineMetrics:
    """Metrics for constitutional pipeline execution."""

    session_id: str
    query_hash: str
    start_time: float
    end_time: float = 0.0
    verdict: str = ""
    stages_executed: list[str] = field(default_factory=list)
    floors_checked: dict[str, bool] = field(default_factory=dict)
    entropy_delta: float = 0.0
    landauer_risk: float = 0.0
    vault_lag_ms: float = 0.0
    energy_eff: float = 0.0
    tri_witness_score: float = 0.0
    genius_score: float = 0.0

    @property
    def latency_ms(self) -> float:
        if self.end_time > 0:
            return (self.end_time - self.start_time) * 1000
        return 0.0

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "query_hash": self.query_hash,
            "latency_ms": self.latency_ms,
            "verdict": self.verdict,
            "stages_executed": self.stages_executed,
            "floors_passed": sum(1 for v in self.floors_checked.values() if v),
            "floors_failed": sum(1 for v in self.floors_checked.values() if not v),
            "entropy_delta": self.entropy_delta,
            "landauer_risk": self.landauer_risk,
            "vault_lag_ms": self.vault_lag_ms,
            "energy_eff": self.energy_eff,
            "tri_witness_score": self.tri_witness_score,
            "genius_score": self.genius_score,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


class MetricsCollector:
    """Collects and exports constitutional metrics."""

    def __init__(self):
        self.metrics: list[PipelineMetrics] = []
        self.max_history = 1000
        self._lock = asyncio.Lock()

    async def record(self, metric: PipelineMetrics):
        """Record a pipeline execution metric."""
        async with self._lock:
            self.metrics.append(metric)
            if len(self.metrics) > self.max_history:
                self.metrics = self.metrics[-self.max_history :]

    def get_stats(self, window: int = 100) -> dict:
        """Get statistics for recent executions."""
        recent = self.metrics[-window:] if self.metrics else []

        if not recent:
            return {
                "total_executions": 0,
                "avg_latency_ms": 0.0,
                "avg_genius_g": 0.0,
                "avg_entropy_delta": 0.0,
                "avg_tri_witness_score": 0.0,
                "avg_landauer_risk": 0.0,
                "avg_vault_lag_ms": 0.0,
                "avg_energy_eff": 0.0,
                "verdicts": {},
            }

        latencies = [m.latency_ms for m in recent]
        verdicts = {}
        for m in recent:
            verdicts[m.verdict] = verdicts.get(m.verdict, 0) + 1

        genius_scores = [m.genius_score for m in recent]
        entropy_deltas = [m.entropy_delta for m in recent]
        tri_witness_scores = [m.tri_witness_score for m in recent]
        landauer_risks = [m.landauer_risk for m in recent]
        vault_lags = [m.vault_lag_ms for m in recent]
        energy_effs = [m.energy_eff for m in recent]

        avg_genius = sum(genius_scores) / len(genius_scores) if genius_scores else 0.0
        avg_entropy_delta = sum(entropy_deltas) / len(entropy_deltas) if entropy_deltas else 0.0
        avg_tri_witness = (
            sum(tri_witness_scores) / len(tri_witness_scores) if tri_witness_scores else 0.0
        )
        avg_landauer = sum(landauer_risks) / len(landauer_risks) if landauer_risks else 0.0
        avg_vault_lag = sum(vault_lags) / len(vault_lags) if vault_lags else 0.0
        avg_energy_eff = sum(energy_effs) / len(energy_effs) if energy_effs else 0.0

        return {
            "total_executions": len(recent),
            "avg_latency_ms": sum(latencies) / len(latencies),
            "min_latency_ms": min(latencies),
            "max_latency_ms": max(latencies),
            "verdict_distribution": verdicts,
            "seal_rate": verdicts.get("SEAL", 0) / len(recent),
            "void_rate": verdicts.get("VOID", 0) / len(recent),
            "avg_genius_g": avg_genius,
            "avg_entropy_delta": avg_entropy_delta,
            "avg_tri_witness_score": avg_tri_witness,
            "avg_landauer_risk": avg_landauer,
            "avg_vault_lag_ms": avg_vault_lag,
            "avg_energy_eff": avg_energy_eff,
        }

    def export_prometheus(self) -> str:
        """Export metrics in Prometheus format."""
        lines = []

        # Counter for executions
        lines.append("# HELP arifos_executions_total Total constitutional executions")
        lines.append("# TYPE arifos_executions_total counter")

        verdict_counts = {}
        for m in self.metrics:
            verdict_counts[m.verdict] = verdict_counts.get(m.verdict, 0) + 1

        for verdict, count in verdict_counts.items():
            lines.append(f'arifos_executions_total{{verdict="{verdict}"}} {count}')

        # Histogram for latency
        lines.append("# HELP arifos_latency_ms Pipeline latency")
        lines.append("# TYPE arifos_latency_ms histogram")

        for m in self.metrics[-100:]:
            lines.append(f"arifos_latency_ms {m.latency_ms}")

        # Gauge for entropy
        lines.append("# HELP arifos_entropy_delta Thermodynamic clarity")
        lines.append("# TYPE arifos_entropy_delta gauge")

        if self.metrics:
            latest = self.metrics[-1]
            lines.append(f"arifos_entropy_delta {latest.entropy_delta}")

        return "\n".join(lines)


# Global collector instance
_collector: MetricsCollector | None = None


def get_metrics_collector() -> MetricsCollector:
    """Get or create global metrics collector."""
    global _collector
    if _collector is None:
        _collector = MetricsCollector()
    return _collector


class HealthMonitor:
    """Monitors system health for civilization deployment."""

    def __init__(self):
        self.checks: dict[str, Callable] = {}
        self.status: dict[str, bool] = {}
        self.last_check: dict[str, float] = {}

    def register(self, name: str, check_fn: Callable):
        """Register a health check."""
        self.checks[name] = check_fn

    async def check_all(self) -> dict[str, Any]:
        """Run all health checks."""
        results = {}

        for name, check_fn in self.checks.items():
            try:
                start = time.time()
                result = await check_fn() if asyncio.iscoroutinefunction(check_fn) else check_fn()
                latency = (time.time() - start) * 1000

                # Base result object
                check_data = {
                    "status": "healthy" if result else "unhealthy",
                    "latency_ms": latency,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }

                # If check returned a dict, merge it (but don't overwrite base keys unless intentional)
                if isinstance(result, dict):
                    check_data.update(result)
                    # Ensure status is string "healthy"/"unhealthy" even if dict had boolean
                    if "status" in result:
                        if isinstance(result["status"], bool):
                            check_data["status"] = "healthy" if result["status"] else "unhealthy"
                            self.status[name] = result["status"]
                        elif isinstance(result["status"], str):
                            # Trust string status (connected/healthy/etc) as True unless it's "unhealthy"/"error"
                            self.status[name] = result["status"] not in (
                                "unhealthy",
                                "error",
                                "failed",
                                "disconnected",
                            )
                    else:
                        # Dict without status key -> assume True (data return)
                        self.status[name] = True
                else:
                    self.status[name] = bool(result)

                results[name] = check_data
                self.last_check[name] = time.time()

            except Exception as e:
                results[name] = {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                self.status[name] = False

        return results

    def is_healthy(self) -> bool:
        """Check if all systems are healthy."""
        return all(self.status.values()) if self.status else False


# Global health monitor
_health_monitor: HealthMonitor | None = None


def get_health_monitor() -> HealthMonitor:
    """Get or create global health monitor."""
    global _health_monitor
    if _health_monitor is None:
        _health_monitor = HealthMonitor()
    return _health_monitor


async def init_monitoring():
    """Initialize monitoring for production."""
    monitor = get_health_monitor()

    # Register core health checks
    async def check_core_pipeline():
        try:
            from core.pipeline import forge

            result = await forge("health check", actor_id="monitor")
            return {
                "status": result.verdict in ("SEAL", "PARTIAL", "VOID", "888_HOLD"),
                "verdict": result.verdict,
                "session_id": result.session_id,
            }
        except Exception as e:
            return {"status": False, "error": str(e)}

    async def check_mcp_tools():
        """Test MCP tools are registered and report any issues."""
        from aaa_mcp.server import mcp

        try:
            tool_names = set()

            # FastMCP API differs across versions. Prefer get_tools() when available,
            # otherwise fall back to known canonical exports from aaa_mcp.server.
            get_tools_fn = getattr(mcp, "get_tools", None)
            if callable(get_tools_fn):
                tools = get_tools_fn()
                if inspect.isawaitable(tools):
                    tools = await tools
                if isinstance(tools, dict):
                    tool_names.update(str(k) for k in tools.keys())
                elif isinstance(tools, (list, tuple, set)):
                    for t in tools:
                        name = getattr(t, "name", None) or str(t)
                        tool_names.add(name)
                elif tools is not None:
                    # Last-resort fallback for unknown tool container types
                    tool_names.add(str(tools))
            else:
                from aaa_mcp import server as server_mod

                candidates = [
                    "init_session",
                    "agi_cognition",
                    "asi_empathy",
                    "apex_verdict",
                    "vault_seal",
                    "search",
                    "fetch",
                    "anchor",
                    "reason",
                    "integrate",
                    "respond",
                    "validate",
                    "align",
                    "forge",
                    "audit",
                    "seal",
                ]
                for name in candidates:
                    if hasattr(server_mod, name):
                        tool_names.add(name)

            tool_count = len(tool_names)

            # Check critical tools (MCP verbs)
            critical_tools = [
                "anchor",
                "reason",
                "integrate",
                "respond",
                "validate",
                "align",
                "forge",
                "audit",
                "seal",
            ]
            missing = [t for t in critical_tools if t not in tool_names]

            if missing:
                print(f"[health] mcp_tools: UNHEALTHY - missing: {', '.join(missing)}")
                return {"status": False, "tool_count": tool_count, "missing": missing}

            if tool_count < 10:
                print(f"[health] mcp_tools: UNHEALTHY - only {tool_count} tools (need 10+)")
                return {"status": False, "tool_count": tool_count, "missing": []}

            print(f"[health] mcp_tools: HEALTHY - {tool_count} tools registered")
            return {"status": True, "tool_count": tool_count}

        except Exception as e:
            err_type = type(e).__name__
            print(f"[health] mcp_tools: ERROR - {err_type}: {e}")
            return {"status": False, "error": f"{err_type}: {e}"}

    def check_memory():
        try:
            import psutil

            mem = psutil.virtual_memory()
            return {"status": mem.percent < 90, "percent": mem.percent, "available": mem.available}
        except ImportError:
            # psutil not installed, skip memory check
            return True

    async def check_postgres():
        try:
            from aaa_mcp.sessions.session_ledger import get_ledger

            ledger = await get_ledger()
            if not ledger.is_postgres_available:
                return False
            # Try a simple query to verify connection and calculate vault lag
            if ledger._pool:
                async with ledger._pool.acquire() as conn:
                    row = await conn.fetchrow("""
                        SELECT EXTRACT(EPOCH FROM (created_at - timestamp)) * 1000 as lag_ms
                        FROM vault999
                        ORDER BY id DESC
                        LIMIT 1
                    """)
                    lag = row["lag_ms"] if row else 0.0
                    return {"status": "connected", "lag_ms": lag}
            return False
        except Exception:
            return False

    async def check_redis():
        try:
            from aaa_mcp.services.redis_client import get_mind_vault

            vault = get_mind_vault()
            health = vault.health_check()
            # Pass through the full health dict (keys, memory, etc.)
            return health
        except Exception:
            return False

    monitor.register("core_pipeline", check_core_pipeline)
    monitor.register("mcp_tools", check_mcp_tools)
    monitor.register("memory", check_memory)
    monitor.register("postgres", check_postgres)
    monitor.register("redis", check_redis)

    return monitor


# Startup monitoring
async def startup_health_check() -> dict:
    """Run health checks on startup."""
    monitor = await init_monitoring()
    results = await monitor.check_all()

    return {
        "status": "healthy" if monitor.is_healthy() else "degraded",
        "checks": results,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
