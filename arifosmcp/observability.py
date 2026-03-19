"""
OpenTelemetry Observability for arifOS FORGE-2
Provides distributed tracing, metrics, and logging for constitutional floors.

Features:
- Automatic instrumentation of all MCP tools
- 13 constitutional floor metrics (F1-F13 scores)
- Latency histograms for each pipeline stage
- Prometheus metrics endpoint
- Jaeger/Zipkin distributed tracing

Environment Variables:
- OTEL_EXPORTER_OTLP_ENDPOINT: OTLP collector endpoint
- OTEL_SERVICE_NAME: arifos-mcp (default)
- OTEL_TRACES_SAMPLER: always_on, always_off, traceidratio
- PROMETHEUS_PORT: 9090 (default)

Usage:
    from aaa_mcp.observability import instrument_app, floor_metrics

    app = Starlette()
    instrument_app(app)

    # Record floor score
    floor_metrics.record_floor_score("F2", 0.95)
"""

import os
import time
from dataclasses import dataclass
from typing import Any

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response

try:
    from opentelemetry import metrics, trace
    from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.exporter.prometheus import PrometheusMetricReader
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
    from opentelemetry.instrumentation.starlette import StarletteInstrumentor
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False
    trace = metrics = None


@dataclass
class FloorMetrics:
    """Metrics for constitutional floor scores."""

    floor_scores: dict[str, float]
    floor_violations: dict[str, int]
    tool_latency: dict[str, float]

    def __init__(self):
        self.floor_scores = {}
        self.floor_violations = {}
        self.tool_latency = {}


class Observability:
    """Main observability manager."""

    def __init__(self, service_name: str = "arifos-mcp"):
        self.service_name = service_name
        self.metrics = FloorMetrics()

        if not OTEL_AVAILABLE:
            print(
                "OpenTelemetry not installed. Run: pip install opentelemetry-sdk opentelemetry-exporter-otlp"
            )
            return

        # Setup tracing
        resource = Resource.create(
            {
                "service.name": service_name,
                "service.version": os.getenv("ARIFOS_VERSION", "2026.2.23-forge2"),
                "deployment.environment": os.getenv("ENVIRONMENT", "production"),
            }
        )

        # Initialize tracing
        trace.set_tracer_provider(TracerProvider(resource=resource))
        tracer_provider = trace.get_tracer_provider()

        # OTLP exporter if endpoint configured
        otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
        if otlp_endpoint:
            otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
            tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

        # Initialize metrics
        readers = []

        # Prometheus reader if port specified
        prometheus_port = os.getenv("PROMETHEUS_PORT")
        if prometheus_port:
            try:
                from opentelemetry.exporter.prometheus import PrometheusMetricReader

                reader = PrometheusMetricReader(port=int(prometheus_port))
                readers.append(reader)
            except ImportError:
                print("Prometheus exporter not available")

        # OTLP metrics exporter
        if otlp_endpoint:
            metric_exporter = OTLPMetricExporter(endpoint=otlp_endpoint)
            reader = PeriodicExportingMetricReader(
                exporter=metric_exporter, export_interval_millis=10000
            )
            readers.append(reader)

        if readers:
            metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=readers))

        self.tracer = trace.get_tracer(__name__)
        self.meter = metrics.get_meter(__name__) if readers else None

        # Create metrics instruments
        if self.meter:
            self.floor_score_gauge = self.meter.create_histogram(
                name="arifos_floor_score",
                description="Constitutional floor scores (0.0-1.0)",
                unit="1",
            )
            self.floor_violation_counter = self.meter.create_counter(
                name="arifos_floor_violations",
                description="Count of constitutional floor violations",
                unit="1",
            )
            self.tool_latency_histogram = self.meter.create_histogram(
                name="arifos_tool_latency",
                description="Tool execution latency in seconds",
                unit="s",
            )
            self.tool_call_counter = self.meter.create_counter(
                name="arifos_tool_calls", description="Count of tool calls by name", unit="1"
            )

    def record_floor_score(self, floor: str, score: float):
        """Record constitutional floor score."""
        self.metrics.floor_scores[floor] = score

        if self.meter and self.floor_score_gauge:
            attributes = {"floor": floor}
            self.floor_score_gauge.record(score, attributes=attributes)

    def record_floor_violation(self, floor: str):
        """Record constitutional floor violation."""
        self.metrics.floor_violations[floor] = self.metrics.floor_violations.get(floor, 0) + 1

        if self.meter and self.floor_violation_counter:
            attributes = {"floor": floor}
            self.floor_violation_counter.add(1, attributes=attributes)

    def record_tool_latency(self, tool_name: str, latency_seconds: float):
        """Record tool execution latency."""
        self.metrics.tool_latency[tool_name] = latency_seconds

        if self.meter and self.tool_latency_histogram:
            attributes = {"tool": tool_name}
            self.tool_latency_histogram.record(latency_seconds, attributes=attributes)

    def record_tool_call(self, tool_name: str):
        """Record tool call count."""
        if self.meter and self.tool_call_counter:
            attributes = {"tool": tool_name}
            self.tool_call_counter.add(1, attributes=attributes)

    def get_metrics_summary(self) -> dict[str, Any]:
        """Get current metrics summary."""
        return {
            "floor_scores": self.metrics.floor_scores,
            "floor_violations": self.metrics.floor_violations,
            "tool_latency": self.metrics.tool_latency,
            "service": self.service_name,
        }


# Global observability instance
_observability: Observability | None = None


def get_observability() -> Observability:
    """Get or create global observability instance."""
    global _observability
    if _observability is None:
        _observability = Observability()
    return _observability


def instrument_app(app: Starlette):
    """Instrument Starlette/FastAPI application with OpenTelemetry."""
    if not OTEL_AVAILABLE:
        return app

    try:
        StarletteInstrumentor().instrument_app(app)
        HTTPXClientInstrumentor().instrument()
    except Exception as e:
        print(f"Failed to instrument app: {e}")

    # Add metrics endpoint
    @app.route("/metrics", methods=["GET"])
    async def metrics_endpoint(request: Request) -> Response:
        """Prometheus metrics endpoint."""
        if OTEL_AVAILABLE:
            # Try to get OpenTelemetry metrics
            try:
                return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
            except:
                pass

        # Fallback to simple JSON metrics
        obs = get_observability()
        return Response(
            content=json.dumps(obs.get_metrics_summary()), media_type="application/json"
        )

    # Add tracing middleware
    @app.middleware("http")
    async def trace_requests(request: Request, call_next):
        obs = get_observability()
        tracer = obs.tracer if OTEL_AVAILABLE else None

        if tracer:
            with tracer.start_as_current_span(f"http.{request.method}.{request.url.path}") as span:
                span.set_attribute("http.method", request.method)
                span.set_attribute("http.url", str(request.url))
                span.set_attribute("http.route", request.url.path)

                start_time = time.time()
                response = await call_next(request)
                latency = time.time() - start_time

                span.set_attribute("http.status_code", response.status_code)
                span.set_attribute("http.latency", latency)

                # Record tool latency if this is a tool call
                if request.url.path.startswith("/tools/"):
                    tool_name = request.url.path.split("/")[-1]
                    obs.record_tool_latency(tool_name, latency)
                    obs.record_tool_call(tool_name)

                return response
        else:
            return await call_next(request)

    return app


def floor_metrics_middleware():
    """Middleware to record constitutional floor metrics."""

    async def middleware(request: Request, call_next):
        obs = get_observability()

        # Check for floor score headers in response
        response = await call_next(request)

        # Extract floor scores from response headers
        floor_scores_header = response.headers.get("X-Floor-Scores")
        if floor_scores_header:
            try:
                import json

                scores = json.loads(floor_scores_header)
                for floor, score in scores.items():
                    obs.record_floor_score(floor, float(score))
            except:
                pass

        # Extract floor violations
        violations_header = response.headers.get("X-Floor-Violations")
        if violations_header:
            try:
                violations = violations_header.split(",")
                for violation in violations:
                    if violation.strip():
                        obs.record_floor_violation(violation.strip())
            except:
                pass

        return response

    return middleware


# Convenience functions for recording metrics
def record_floor_score(floor: str, score: float):
    get_observability().record_floor_score(floor, score)


def record_floor_violation(floor: str):
    get_observability().record_floor_violation(floor)


def record_tool_latency(tool_name: str, latency_seconds: float):
    get_observability().record_tool_latency(tool_name, latency_seconds)


def record_tool_call(tool_name: str):
    get_observability().record_tool_call(tool_name)


# Simple metrics endpoint for backward compatibility
async def metrics_handler(request: Request) -> Response:
    """Legacy metrics endpoint."""
    obs = get_observability()
    import json

    return Response(content=json.dumps(obs.get_metrics_summary()), media_type="application/json")
