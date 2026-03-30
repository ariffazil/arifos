"""
arifOS Autoresearch Benchmark Suite
Measures constitutional compliance and performance metrics.

Usage:
    python benchmark.py --duration 300 --output results.json
"""

import argparse
import asyncio
import json
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional
import statistics


@dataclass
class BenchmarkResult:
    """Single request benchmark result."""
    timestamp: float
    latency_ms: float
    verdict: str
    delta_s: float
    omega: float
    W_cube: float
    floors_violated: List[str]


@dataclass
class AggregateMetrics:
    """Aggregated benchmark metrics."""
    # Performance
    throughput_rps: float
    avg_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    
    # Constitutional
    violation_rate: float
    floor_violation_counts: Dict[str, int]
    avg_omega: float
    omega_std: float
    omega_in_range_pct: float
    avg_W_cube: float
    
    # Score
    composite_score: float


class arifOSBenchmark:
    """
    Benchmark harness for arifOS autoresearch.
    Simulates load and measures constitutional compliance.
    """
    
    def __init__(
        self,
        target_url: str = "https://arifosmcp.arif-fazil.com/mcp",
        omega_range: tuple = (0.03, 0.05),
        w3_threshold: float = 0.95
    ):
        self.target_url = target_url
        self.omega_range = omega_range
        self.w3_threshold = w3_threshold
        self.results: List[BenchmarkResult] = []
    
    async def run_benchmark(
        self,
        duration_seconds: int = 300,
        concurrency: int = 10,
        request_rate: Optional[float] = None
    ) -> AggregateMetrics:
        """
        Run benchmark for specified duration.
        
        Args:
            duration_seconds: How long to run (default 5 min)
            concurrency: Number of concurrent requests
            request_rate: Target requests per second (None = max)
        """
        print(f"Starting benchmark: {duration_seconds}s, {concurrency} concurrent")
        
        start_time = time.time()
        tasks = []
        
        # Spawn workers
        for i in range(concurrency):
            task = asyncio.create_task(
                self._worker(i, start_time, duration_seconds, request_rate)
            )
            tasks.append(task)
        
        # Wait for completion
        await asyncio.gather(*tasks)
        
        # Calculate aggregates
        return self._calculate_metrics(start_time)
    
    async def _worker(
        self,
        worker_id: int,
        start_time: float,
        duration: int,
        request_rate: Optional[float]
    ):
        """Worker that sends requests until time expires."""
        while time.time() - start_time < duration:
            request_start = time.time()
            
            # Simulate request (replace with actual MCP call)
            result = await self._simulate_request()
            
            latency = (time.time() - request_start) * 1000  # ms
            result.latency_ms = latency
            self.results.append(result)
            
            # Rate limiting
            if request_rate:
                await asyncio.sleep(1.0 / request_rate)
    
    async def _simulate_request(self) -> BenchmarkResult:
        """
        Simulate an arifOS request.
        In production, this calls the actual MCP server.
        """
        # TODO: Replace with actual MCP call
        # For now, simulate realistic values
        import random
        
        # Simulate constitutional processing
        delta_s = random.uniform(-0.3, 0.1)  # Usually clarity gain
        omega = random.gauss(0.04, 0.005)    # Centered on GOLDILOCKS
        W_cube = random.gauss(0.97, 0.02)    # High consensus
        
        # Occasional violation (baseline ~5%)
        floors_violated = []
        if random.random() < 0.05:
            floors_violated = [random.choice(["F4", "F7", "F8"])]
        
        verdict = "VOID" if floors_violated else "SEAL"
        
        return BenchmarkResult(
            timestamp=time.time(),
            latency_ms=0,  # Filled by worker
            verdict=verdict,
            delta_s=delta_s,
            omega=max(0.0, min(1.0, omega)),
            W_cube=max(0.0, min(1.0, W_cube)),
            floors_violated=floors_violated
        )
    
    def _calculate_metrics(self, start_time: float) -> AggregateMetrics:
        """Calculate aggregate metrics from results."""
        if not self.results:
            raise ValueError("No results collected")
        
        duration = time.time() - start_time
        
        # Performance metrics
        latencies = [r.latency_ms for r in self.results]
        throughput = len(self.results) / duration
        
        # Constitutional metrics
        violations = sum(1 for r in self.results if r.floors_violated)
        violation_rate = violations / len(self.results)
        
        omegas = [r.omega for r in self.results]
        omega_in_range = sum(
            1 for o in omegas 
            if self.omega_range[0] <= o <= self.omega_range[1]
        )
        
        # Floor violation counts
        floor_counts = {}
        for r in self.results:
            for f in r.floors_violated:
                floor_counts[f] = floor_counts.get(f, 0) + 1
        
        # Composite score
        # score = (throughput / 100) * (1 - violation_rate) * omega_penalty
        throughput_factor = min(1.0, throughput / 100)
        violation_factor = 1 - violation_rate
        omega_drift = abs(statistics.mean(omegas) - 0.04)
        omega_penalty = max(0, 1 - (omega_drift * 50))  # Steep penalty for drift
        
        score = throughput_factor * violation_factor * omega_penalty
        
        return AggregateMetrics(
            throughput_rps=round(throughput, 2),
            avg_latency_ms=round(statistics.mean(latencies), 2),
            p95_latency_ms=round(sorted(latencies)[int(len(latencies) * 0.95)], 2),
            p99_latency_ms=round(sorted(latencies)[int(len(latencies) * 0.99)], 2),
            violation_rate=round(violation_rate, 4),
            floor_violation_counts=floor_counts,
            avg_omega=round(statistics.mean(omegas), 4),
            omega_std=round(statistics.stdev(omegas), 4) if len(omegas) > 1 else 0,
            omega_in_range_pct=round(omega_in_range / len(omegas), 4),
            avg_W_cube=round(statistics.mean([r.W_cube for r in self.results]), 4),
            composite_score=round(score, 4)
        )


def main():
    parser = argparse.ArgumentParser(description="arifOS Autoresearch Benchmark")
    parser.add_argument("--duration", type=int, default=300, help="Duration in seconds")
    parser.add_argument("--concurrency", type=int, default=10, help="Concurrent requests")
    parser.add_argument("--output", type=str, default="benchmark_results.json")
    args = parser.parse_args()
    
    benchmark = arifOSBenchmark()
    metrics = asyncio.run(benchmark.run_benchmark(
        duration_seconds=args.duration,
        concurrency=args.concurrency
    ))
    
    # Print results
    print("\n" + "=" * 60)
    print("BENCHMARK RESULTS")
    print("=" * 60)
    print(f"Duration: {args.duration}s")
    print(f"Requests: {len(benchmark.results)}")
    print()
    print("Performance:")
    print(f"  Throughput: {metrics.throughput_rps} req/s")
    print(f"  Latency (avg): {metrics.avg_latency_ms}ms")
    print(f"  Latency (p95): {metrics.p95_latency_ms}ms")
    print()
    print("Constitutional:")
    print(f"  Violation Rate: {metrics.violation_rate * 100:.2f}%")
    print(f"  Avg Omega: {metrics.avg_omega} (σ={metrics.omega_std})")
    print(f"  Omega in Range: {metrics.omega_in_range_pct * 100:.1f}%")
    print(f"  Avg W³: {metrics.avg_W_cube}")
    if metrics.floor_violation_counts:
        print(f"  Floor Violations: {metrics.floor_violation_counts}")
    print()
    print(f"COMPOSITE SCORE: {metrics.composite_score}")
    print("=" * 60)
    
    # Save to file
    output = {
        "timestamp": datetime.utcnow().isoformat(),
        "duration": args.duration,
        "concurrency": args.concurrency,
        "metrics": asdict(metrics)
    }
    
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to {args.output}")
    
    # Exit code based on score
    if metrics.composite_score >= 0.90:
        print("\n✅ EXCELLENT: Score >= 0.90")
        return 0
    elif metrics.composite_score >= 0.80:
        print("\n🟡 ACCEPTABLE: Score >= 0.80")
        return 0
    else:
        print("\n❌ NEEDS IMPROVEMENT: Score < 0.80")
        return 1


if __name__ == "__main__":
    exit(main())
