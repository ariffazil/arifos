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
import json


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
                self.metrics = self.metrics[-self.max_history:]
    
    def get_stats(self, window: int = 100) -> dict:
        """Get statistics for recent executions."""
        recent = self.metrics[-window:] if self.metrics else []
        
        if not recent:
            return {"error": "No metrics available"}
        
        latencies = [m.latency_ms for m in recent]
        verdicts = {}
        for m in recent:
            verdicts[m.verdict] = verdicts.get(m.verdict, 0) + 1
        
        return {
            "total_executions": len(recent),
            "avg_latency_ms": sum(latencies) / len(latencies),
            "min_latency_ms": min(latencies),
            "max_latency_ms": max(latencies),
            "verdict_distribution": verdicts,
            "seal_rate": verdicts.get("SEAL", 0) / len(recent),
            "void_rate": verdicts.get("VOID", 0) / len(recent),
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
            lines.append(f'arifos_latency_ms {m.latency_ms}')
        
        # Gauge for entropy
        lines.append("# HELP arifos_entropy_delta Thermodynamic clarity")
        lines.append("# TYPE arifos_entropy_delta gauge")
        
        if self.metrics:
            latest = self.metrics[-1]
            lines.append(f'arifos_entropy_delta {latest.entropy_delta}')
        
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
        try:
            from aaa_mcp.server import mcp
            tools = await mcp.get_tools()
            return len(tools) >= 10
        except Exception as e:
            print(f"[health] mcp_tools check failed: {e}")
            return False
    
    def check_memory():
        try:
            import psutil
            mem = psutil.virtual_memory()
            return mem.percent < 90
        except ImportError:
            # psutil not installed, skip memory check
            return True
    
    monitor.register("core_pipeline", check_core_pipeline)
    monitor.register("mcp_tools", check_mcp_tools)
    monitor.register("memory", check_memory)
    
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
