"""
arifOS Production Monitoring
============================

Metrics, health checks, and alerting for civilization deployment.

DITEMPA BUKAN DIBERI
"""

import asyncio
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime, timezone


@dataclass
class PipelineMetrics:
    """Metrics for constitutional pipeline execution."""

    session_id: str
    query_hash: str
    start_time: float
    end_time: float = 0.0
    verdict: str = ""
    stages_executed: List[str] = field(default_factory=list)
    floors_checked: Dict[str, bool] = field(default_factory=dict)
    entropy_delta: float = 0.0
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
            "tri_witness_score": self.tri_witness_score,
            "genius_score": self.genius_score,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


class MetricsCollector:
    """Collects and exports constitutional metrics."""

    def __init__(self):
        self.metrics: List[PipelineMetrics] = []
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
            return {"error": "No metrics available"}

        latencies = [m.latency_ms for m in recent]
        verdicts = {}
        for m in recent:
            verdicts[m.verdict] = verdicts.get(m.verdict, 0) + 1

        genius_scores = [m.genius_score for m in recent]
        entropy_deltas = [m.entropy_delta for m in recent]
        tri_witness_scores = [m.tri_witness_score for m in recent]

        avg_genius = sum(genius_scores) / len(genius_scores) if genius_scores else 0.0
        avg_entropy_delta = sum(entropy_deltas) / len(entropy_deltas) if entropy_deltas else 0.0
        avg_tri_witness = sum(tri_witness_scores) / len(tri_witness_scores) if tri_witness_scores else 0.0

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
_collector: Optional[MetricsCollector] = None


def get_metrics_collector() -> MetricsCollector:
    """Get or create global metrics collector."""
    global _collector
    if _collector is None:
        _collector = MetricsCollector()
    return _collector


class HealthMonitor:
    """Monitors system health for civilization deployment."""

    def __init__(self):
        self.checks: Dict[str, callable] = {}
        self.status: Dict[str, bool] = {}
        self.last_check: Dict[str, float] = {}

    def register(self, name: str, check_fn: callable):
        """Register a health check."""
        self.checks[name] = check_fn

    async def check_all(self) -> Dict[str, any]:
        """Run all health checks."""
        results = {}

        for name, check_fn in self.checks.items():
            try:
                start = time.time()
                result = await check_fn() if asyncio.iscoroutinefunction(check_fn) else check_fn()
                latency = (time.time() - start) * 1000

                results[name] = {
                    "status": "healthy" if result else "unhealthy",
                    "latency_ms": latency,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                self.status[name] = result
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
_health_monitor: Optional[HealthMonitor] = None


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
            return result.verdict in ("SEAL", "PARTIAL", "VOID", "888_HOLD")
        except Exception:
            return False

    async def check_mcp_tools():
        """Test MCP tools are registered and report any issues."""
        from aaa_mcp.server import mcp

        try:
            tools = await mcp.get_tools()
            tool_count = len(tools)

            # Get tool names for verification
            tool_names = set()
            for t in tools:
                name = getattr(t, "name", None) or str(t)
                tool_names.add(name)

            # Check critical tools
            critical_tools = [
                "init_gate",
                "agi_sense",
                "agi_think",
                "agi_reason",
                "asi_empathize",
                "asi_align",
                "apex_verdict",
                "vault_seal",
                "vault_query",
                "truth_audit",
            ]
            missing = [t for t in critical_tools if t not in tool_names]

            if missing:
                print(f"[health] mcp_tools: UNHEALTHY - missing: {', '.join(missing)}")
                return False

            if tool_count < 10:
                print(f"[health] mcp_tools: UNHEALTHY - only {tool_count} tools (need 10+)")
                return False

            print(f"[health] mcp_tools: HEALTHY - {tool_count} tools registered")
            return True

        except Exception as e:
            err_type = type(e).__name__
            print(f"[health] mcp_tools: ERROR - {err_type}: {e}")
            return False

    def check_memory():
        try:
            import psutil

            mem = psutil.virtual_memory()
            return mem.percent < 90
        except ImportError:
            # psutil not installed, skip memory check
            return True

    async def check_postgres():
        try:
            from aaa_mcp.sessions.session_ledger import get_ledger
            ledger = await get_ledger()
            if not ledger.is_postgres_available:
                return False
            # Try a simple query to verify connection
            if ledger._pool:
                async with ledger._pool.acquire() as conn:
                    row = await conn.fetchrow("SELECT 1")
                    return row is not None
            return False
        except Exception:
            return False

    async def check_redis():
        try:
            from aaa_mcp.services.redis_client import get_mind_vault
            vault = get_mind_vault()
            health = vault.health_check()
            return health.get("status") == "connected"
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
