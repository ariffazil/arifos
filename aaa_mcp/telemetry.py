"""
aaa_mcp/telemetry.py — Hardened FastMCP Telemetry Integration

Bridges FastMCP's OpenTelemetry instrumentation with arifOS constitutional observability.
Provides unified tracing, metrics, and constitutional floor telemetry.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import functools
import time
from contextlib import contextmanager
from typing import Any, Callable

# FastMCP telemetry (protocol-level)
try:
    from fastmcp.telemetry import get_tracer
    FASTMCP_TELEMETRY_AVAILABLE = True
except ImportError:
    FASTMCP_TELEMETRY_AVAILABLE = False

# OpenTelemetry
try:
    from opentelemetry import trace
    from opentelemetry.trace import Status, StatusCode
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False

# arifOS constitutional observability
from aaa_mcp.observability import (
    get_observability,
    record_floor_score,
    record_floor_violation,
    record_tool_latency,
    record_tool_call,
)
from aaa_mcp.infrastructure.monitoring import get_metrics_collector, PipelineMetrics


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTITUTIONAL SPAN CONTEXT
# ═══════════════════════════════════════════════════════════════════════════════

class ConstitutionalSpan:
    """
    Wrapper for OpenTelemetry spans with constitutional floor awareness.
    
    Extends standard OTEL spans with:
    - Floor score attributes (F1-F13)
    - Metabolic stage tracking (000-999)
    - Verdict recording (SEAL/SABAR/VOID)
    """
    
    def __init__(self, span: Any, session_id: str | None = None):
        self._span = span
        self.session_id = session_id
        self.floor_scores: dict[str, float] = {}
        self.floor_violations: list[str] = []
        self.stage = "000_INIT"
        
    def set_floor_score(self, floor: str, score: float):
        """Record constitutional floor score as span attribute."""
        self.floor_scores[floor] = score
        if self._span:
            self._span.set_attribute(f"arifos.floor.{floor}.score", score)
        
    def set_floor_violation(self, floor: str, reason: str = ""):
        """Record constitutional floor violation."""
        self.floor_violations.append(floor)
        if self._span:
            self._span.set_attribute(f"arifos.floor.{floor}.violated", True)
            if reason:
                self._span.set_attribute(f"arifos.floor.{floor}.reason", reason)
        
    def set_stage(self, stage: str):
        """Record metabolic stage (000-999)."""
        self.stage = stage
        if self._span:
            self._span.set_attribute("arifos.metabolic_stage", stage)
        
    def set_verdict(self, verdict: str, confidence: float | None = None):
        """Record constitutional verdict."""
        if self._span:
            self._span.set_attribute("arifos.verdict", verdict)
            if confidence is not None:
                self._span.set_attribute("arifos.confidence", confidence)
            
            # Mark span status based on verdict
            if verdict == "VOID":
                self._span.set_status(Status(StatusCode.ERROR, "Constitutional VOID"))
            elif verdict == "SABAR":
                self._span.set_status(Status(StatusCode.UNSET, "SABAR - requires attention"))
            else:
                self._span.set_status(Status(StatusCode.OK))
        
    def record_metric(self, name: str, value: float, attributes: dict | None = None):
        """Record custom metric within span context."""
        if self._span:
            full_name = f"arifos.{name}"
            self._span.set_attribute(full_name, value)
            if attributes:
                for k, v in attributes.items():
                    self._span.set_attribute(f"{full_name}.{k}", v)


# ═══════════════════════════════════════════════════════════════════════════════
# FASTMCP-NATIVE TELEMETRY DECORATORS
# ═══════════════════════════════════════════════════════════════════════════════

def instrument_tool(
    tool_name: str | None = None,
    record_floors: bool = True,
    record_latency: bool = True,
) -> Callable:
    """
    Decorator to instrument MCP tools with constitutional telemetry.
    
    Usage:
        @mcp.tool
        @instrument_tool("anchor_session")
        async def anchor_session(query: str, ...):
            ...
    """
    def decorator(func: Callable) -> Callable:
        name = tool_name or func.__name__
        
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            
            # Get FastMCP tracer if available
            tracer = None
            if FASTMCP_TELEMETRY_AVAILABLE:
                try:
                    tracer = get_tracer()
                except:
                    pass
            
            # Get OTEL tracer as fallback
            if not tracer and OTEL_AVAILABLE:
                tracer = trace.get_tracer(__name__)
            
            if not tracer:
                # No telemetry available, just run function
                return await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            
            # Start span with MCP semantic conventions
            with tracer.start_as_current_span(f"tools/call {name}") as span:
                span.set_attribute("mcp.method.name", "tools/call")
                span.set_attribute("fastmcp.component.type", "tool")
                span.set_attribute("fastmcp.component.key", f"tool:{name}")
                
                # Create constitutional span wrapper
                session_id = kwargs.get("session_id", "unknown")
                const_span = ConstitutionalSpan(span, session_id)
                
                try:
                    # Record tool call
                    record_tool_call(name)
                    
                    # Execute tool
                    result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
                    
                    # Extract constitutional data from result
                    if isinstance(result, dict):
                        verdict = result.get("verdict", "UNKNOWN")
                        const_span.set_verdict(verdict)
                        
                        # Record floor scores
                        if record_floors:
                            floors = result.get("floors", {})
                            passed = floors.get("passed", [])
                            failed = floors.get("failed", [])
                            
                            for floor in passed:
                                const_span.set_floor_score(floor, 1.0)
                                record_floor_score(floor, 1.0)
                            for floor in failed:
                                const_span.set_floor_violation(floor)
                                record_floor_violation(floor)
                        
                        # Record stage
                        stage = result.get("stage", "UNKNOWN")
                        const_span.set_stage(stage)
                    
                    # Record latency
                    if record_latency:
                        latency = time.time() - start_time
                        record_tool_latency(name, latency)
                        span.set_attribute("arifos.latency_ms", latency * 1000)
                    
                    return result
                    
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    span.record_exception(e)
                    raise
        
        return wrapper
    return decorator


@contextmanager
def constitutional_span(
    name: str,
    session_id: str | None = None,
    stage: str | None = None,
    attributes: dict | None = None,
):
    """
    Context manager for constitutional spans.
    
    Usage:
        with constitutional_span("F2_truth_check", session_id, "111_SENSE") as span:
            span.set_floor_score("F2", 0.99)
            ...
    """
    tracer = None
    if FASTMCP_TELEMETRY_AVAILABLE:
        try:
            tracer = get_tracer()
        except:
            pass
    
    if not tracer and OTEL_AVAILABLE:
        tracer = trace.get_tracer(__name__)
    
    if not tracer:
        # Yield None if no telemetry
        yield None
        return
    
    with tracer.start_as_current_span(name) as otel_span:
        if attributes:
            for k, v in attributes.items():
                otel_span.set_attribute(k, v)
        
        if stage:
            otel_span.set_attribute("arifos.metabolic_stage", stage)
        
        const_span = ConstitutionalSpan(otel_span, session_id)
        yield const_span


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION WITH EXISTING OBSERVABILITY
# ═══════════════════════════════════════════════════════════════════════════════

def record_pipeline_metrics(
    session_id: str,
    query_hash: str,
    verdict: str,
    stages_executed: list[str],
    floors_checked: dict[str, bool],
    entropy_delta: float = 0.0,
    tri_witness_score: float = 0.0,
    genius_score: float = 0.0,
    start_time: float | None = None,
    end_time: float | None = None,
):
    """
    Record pipeline execution metrics to both:
    - FastMCP/OpenTelemetry tracing
    - arifOS constitutional metrics collector
    """
    # Record to arifOS collector
    collector = get_metrics_collector()
    
    metric = PipelineMetrics(
        session_id=session_id,
        query_hash=query_hash,
        start_time=start_time or time.time(),
        end_time=end_time or time.time(),
        verdict=verdict,
        stages_executed=stages_executed,
        floors_checked=floors_checked,
        entropy_delta=entropy_delta,
        tri_witness_score=tri_witness_score,
        genius_score=genius_score,
    )
    
    # Run async record in sync context
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Schedule without waiting
            asyncio.create_task(collector.record(metric))
        else:
            loop.run_until_complete(collector.record(metric))
    except:
        pass
    
    # Record to OpenTelemetry if available
    if OTEL_AVAILABLE:
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("arifos.pipeline.complete") as span:
            span.set_attribute("arifos.session_id", session_id)
            span.set_attribute("arifos.verdict", verdict)
            span.set_attribute("arifos.stages_count", len(stages_executed))
            span.set_attribute("arifos.floors_passed", sum(1 for v in floors_checked.values() if v))
            span.set_attribute("arifos.floors_failed", sum(1 for v in floors_checked.values() if not v))
            span.set_attribute("arifos.entropy_delta", entropy_delta)
            span.set_attribute("arifos.tri_witness_score", tri_witness_score)
            span.set_attribute("arifos.genius_score", genius_score)


# ═══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "ConstitutionalSpan",
    "instrument_tool",
    "constitutional_span",
    "record_pipeline_metrics",
    "FASTMCP_TELEMETRY_AVAILABLE",
    "OTEL_AVAILABLE",
]
