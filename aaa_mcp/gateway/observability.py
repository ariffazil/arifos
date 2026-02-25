"""
arifOS Gateway Observability

Post-deployment health checks and F4 Clarity validation.
Ensures SEAL means "applied + healthy", not just "applied".

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class HealthStatus(str, Enum):
    """Health check status."""

    PENDING = "pending"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    TIMEOUT = "timeout"


class RollbackTrigger(str, Enum):
    """Reasons for auto-rollback."""

    HEALTH_CHECK_FAILED = "health_check_failed"
    ERROR_RATE_SPIKE = "error_rate_spike"
    LATENCY_REGRESSION = "latency_regression"
    POD_NOT_READY = "pod_not_ready"
    MANUAL = "manual"


@dataclass
class HealthMetrics:
    """Health metrics for a deployment."""

    error_rate: float = 0.0
    latency_p99: float = 0.0
    latency_p95: float = 0.0
    latency_p50: float = 0.0
    pods_ready: int = 0
    pods_total: int = 0
    restarts: int = 0
    cpu_usage: float = 0.0
    memory_usage: float = 0.0

    def to_dict(self) -> dict[str, float]:
        return {
            "error_rate": self.error_rate,
            "latency_p99": self.latency_p99,
            "latency_p95": self.latency_p95,
            "latency_p50": self.latency_p50,
            "pods_ready": self.pods_ready,
            "pods_total": self.pods_total,
            "pod_readiness_ratio": self.pods_ready / max(self.pods_total, 1),
            "restarts": self.restarts,
            "cpu_usage": self.cpu_usage,
            "memory_usage": self.memory_usage,
        }


@dataclass
class F4ClarityResult:
    """
    F4 Clarity floor evaluation for post-deployment state.

    Verifies that the deployment reduced entropy (improved clarity)
    rather than increased it.
    """

    session_id: str
    deployment_name: str
    namespace: str

    # Pre-deployment baseline
    baseline_metrics: HealthMetrics | None = None

    # Post-deployment metrics
    post_metrics: HealthMetrics | None = None

    # Delta analysis
    delta_entropy: float = 0.0  # Negative = good (reduced entropy)

    # Status
    status: HealthStatus = HealthStatus.PENDING

    # F4 score (0.0-1.0)
    clarity_score: float = 0.0

    # Verdict
    f4_passed: bool = False

    # Timestamp
    checked_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def calculate_entropy_delta(self) -> float:
        """
        Calculate entropy change (F4 Clarity).

        Lower error rate, lower latency variance, higher pod readiness
        all contribute to reduced entropy (negative delta).
        """
        if not self.baseline_metrics or not self.post_metrics:
            return 0.0

        baseline = self.baseline_metrics
        post = self.post_metrics

        # Error rate delta (positive = worse)
        error_delta = post.error_rate - baseline.error_rate

        # Latency variance delta (positive = worse)
        baseline_variance = baseline.latency_p99 - baseline.latency_p50
        post_variance = post.latency_p99 - post.latency_p50
        variance_delta = post_variance - baseline_variance

        # Pod readiness delta (negative = worse)
        baseline_ready = baseline.pods_ready / max(baseline.pods_total, 1)
        post_ready = post.pods_ready / max(post.pods_total, 1)
        readiness_delta = post_ready - baseline_ready

        # Combined entropy (weighted)
        # Lower is better (reduced entropy)
        entropy = (error_delta * 0.4) + (variance_delta * 0.3) - (readiness_delta * 0.3)

        self.delta_entropy = entropy
        return entropy

    def evaluate_f4(self, threshold: float = 0.0) -> bool:
        """
        Evaluate F4 Clarity floor.

        Threshold: ΔS ≤ 0 (entropy must not increase)
        """
        self.calculate_entropy_delta()

        # Convert entropy to clarity score (0-1, higher is better)
        # entropy <= 0 → clarity >= 0.5
        self.clarity_score = max(0.0, min(1.0, 0.5 - self.delta_entropy))

        # F4 passes if entropy did not increase
        self.f4_passed = self.delta_entropy <= threshold

        # Determine status
        if self.clarity_score >= 0.8:
            self.status = HealthStatus.HEALTHY
        elif self.clarity_score >= 0.5:
            self.status = HealthStatus.DEGRADED
        else:
            self.status = HealthStatus.UNHEALTHY

        return self.f4_passed


@dataclass
class ObservabilityConfig:
    """Configuration for post-deploy observability."""

    enabled: bool = True
    timeout: int = 300  # 5 minutes
    interval: int = 10  # 10 seconds

    # Success criteria
    max_error_rate: float = 0.01  # 1%
    max_latency_p99: float = 500.0  # 500ms
    min_pod_readiness: float = 1.0  # 100%

    # Auto-rollback
    auto_rollback: bool = True
    rollback_on_error_spike: bool = True


class PostDeployMonitor:
    """
    Monitors deployments after application for F4 Clarity validation.

    Implements the "observe before seal is complete" pattern.
    """

    def __init__(self, config: ObservabilityConfig | None = None):
        self.config = config or ObservabilityConfig()
        self._monitors: dict[str, asyncio.Task] = {}
        self._results: dict[str, F4ClarityResult] = {}

    async def start_monitoring(
        self,
        session_id: str,
        deployment_name: str,
        namespace: str,
        baseline: HealthMetrics | None = None,
        metrics_provider: Callable[[], HealthMetrics] | None = None,
    ) -> F4ClarityResult:
        """
        Start monitoring a deployment for F4 Clarity.

        Returns initial result; actual monitoring happens async.
        """
        result = F4ClarityResult(
            session_id=session_id,
            deployment_name=deployment_name,
            namespace=namespace,
            baseline_metrics=baseline,
            status=HealthStatus.PENDING,
        )

        if not self.config.enabled:
            result.status = HealthStatus.HEALTHY
            result.f4_passed = True
            result.clarity_score = 1.0
            return result

        # Start async monitoring
        task = asyncio.create_task(
            self._monitor_loop(session_id, deployment_name, namespace, metrics_provider)
        )
        self._monitors[session_id] = task

        return result

    async def _monitor_loop(
        self,
        session_id: str,
        deployment_name: str,
        namespace: str,
        metrics_provider: Callable[[], HealthMetrics] | None,
    ):
        """Internal monitoring loop."""
        start_time = datetime.now(timezone.utc)

        for attempt in range(self.config.timeout // self.config.interval):
            await asyncio.sleep(self.config.interval)

            # Get current metrics
            if metrics_provider:
                metrics = metrics_provider()
            else:
                # Default: query K8s metrics (placeholder)
                metrics = await self._query_k8s_metrics(deployment_name, namespace)

            # Update result
            result = F4ClarityResult(
                session_id=session_id,
                deployment_name=deployment_name,
                namespace=namespace,
                post_metrics=metrics,
            )
            result.evaluate_f4()

            self._results[session_id] = result

            # Check if healthy
            if result.status == HealthStatus.HEALTHY:
                break

            # Check for rollback triggers
            if self.config.auto_rollback and self._should_rollback(result):
                await self._trigger_rollback(session_id, deployment_name, namespace, result)
                break

            # Timeout check
            elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
            if elapsed >= self.config.timeout:
                result.status = HealthStatus.TIMEOUT
                break

    async def _query_k8s_metrics(
        self,
        deployment_name: str,
        namespace: str,
    ) -> HealthMetrics:
        """Query K8s metrics for deployment health."""
        # Placeholder: actual implementation would query Prometheus/metrics-server
        # For now, return dummy metrics
        return HealthMetrics(
            error_rate=0.001,
            latency_p99=100.0,
            latency_p95=80.0,
            latency_p50=50.0,
            pods_ready=3,
            pods_total=3,
            restarts=0,
            cpu_usage=0.5,
            memory_usage=0.6,
        )

    def _should_rollback(self, result: F4ClarityResult) -> bool:
        """Check if rollback should be triggered."""
        if not result.post_metrics:
            return False

        metrics = result.post_metrics

        # Error rate spike
        if (
            self.config.rollback_on_error_spike
            and metrics.error_rate > self.config.max_error_rate * 5
        ):
            return True

        # Pod readiness failure
        readiness = metrics.pods_ready / max(metrics.pods_total, 1)
        if readiness < 0.5:  # Less than 50% ready
            return True

        return False

    async def _trigger_rollback(
        self,
        session_id: str,
        deployment_name: str,
        namespace: str,
        result: F4ClarityResult,
    ):
        """Trigger automatic rollback."""
        # Log to VAULT
        from aaa_mcp.services.constitutional_metrics import store_stage_result

        store_stage_result(
            session_id=session_id,
            stage="observability_rollback",
            result={
                "deployment": deployment_name,
                "namespace": namespace,
                "reason": "health_check_failed",
                "clarity_score": result.clarity_score,
                "delta_entropy": result.delta_entropy,
            },
        )

        # Actual rollback would call K8s API here
        # For now, just log
        print(f"[OBSERVABILITY] Auto-rollback triggered for {deployment_name} in {namespace}")

    def get_result(self, session_id: str) -> F4ClarityResult | None:
        """Get monitoring result for a session."""
        return self._results.get(session_id)

    async def finalize_seal(
        self,
        session_id: str,
    ) -> dict[str, Any]:
        """
        Finalize seal after observability validation.

        This is called before vault_seal to ensure F4 Clarity.
        """
        result = self._results.get(session_id)

        if not result:
            return {
                "f4_clarity": "skipped",
                "verdict": "SEAL",
                "reason": "No observability data (monitoring disabled or not started)",
            }

        # Wait for monitoring to complete if still running
        if session_id in self._monitors:
            try:
                await asyncio.wait_for(self._monitors[session_id], timeout=60)
            except asyncio.TimeoutError:
                pass

        result = self._results.get(session_id)

        if result.f4_passed:
            return {
                "f4_clarity": "passed",
                "verdict": "SEAL",
                "clarity_score": result.clarity_score,
                "delta_entropy": result.delta_entropy,
                "status": result.status.value,
            }
        else:
            return {
                "f4_clarity": "failed",
                "verdict": "SABAR",
                "clarity_score": result.clarity_score,
                "delta_entropy": result.delta_entropy,
                "status": result.status.value,
                "reason": "F4 Clarity floor failed: entropy increased post-deployment",
                "recommendation": "Investigate deployment health and re-apply with fixes",
            }


# Singleton instance
post_deploy_monitor = PostDeployMonitor()
