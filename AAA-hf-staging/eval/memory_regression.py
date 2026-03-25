"""
memory_regression.py — arifOS Constitutional Memory Regression Test Harness
============================================================================

Uses sentinel_queries.jsonl to detect constitutional drift in the memory subsystem.

Runs against the live arifosmcp endpoint OR a local Qdrant instance.
Part of the CI/CD gate: F8 Sabr (3-pass minimum) + floor threshold enforcement.

Usage:
    # Test live endpoint
    python eval/memory_regression.py --endpoint https://arifosmcp.arif-fazil.com/mcp

    # Test local Qdrant
    python eval/memory_regression.py --qdrant http://localhost:6333 --model bge-m3

    # Run against HF dataset canon embeddings
    python eval/memory_regression.py --dataset ariffazil/AAA --split train

    # Full CI mode (3 passes, fail fast)
    python eval/memory_regression.py --passes 3 --fail-fast

    # Output JSON report
    python eval/memory_regression.py --output regression_report.json

Dependencies:
    pip install datasets sentence-transformers qdrant-client tqdm rich requests

Constitutional floors: F2 (truth verify), F4 (context), F8 (3-pass gate), F12 (injection scan)
"""

import argparse
import json
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress
    RICH = True
except ImportError:
    RICH = False

console = Console() if RICH else None


# ─────────────────────────────────────────────
# Data Models
# ─────────────────────────────────────────────

@dataclass
class SentinelQuery:
    id: str
    query: str
    expected_canon_ids: list[str]
    expected_floor_refs: list[str]
    min_similarity: float
    description: str


@dataclass
class SentinelResult:
    sentinel_id: str
    query: str
    floor_refs: list[str]
    min_similarity: float
    actual_similarity: float
    passed: bool
    top_result_id: Optional[str] = None
    top_result_excerpt: Optional[str] = None
    latency_ms: float = 0.0
    error: Optional[str] = None


@dataclass
class RegressionPass:
    pass_number: int
    results: list[SentinelResult] = field(default_factory=list)
    passed: int = 0
    failed: int = 0
    errors: int = 0
    duration_seconds: float = 0.0

    @property
    def pass_rate(self) -> float:
        total = self.passed + self.failed
        return self.passed / total if total > 0 else 0.0


@dataclass
class RegressionReport:
    timestamp: str
    aaa_revision: str
    endpoint: Optional[str]
    total_passes: int
    passes: list[RegressionPass]
    overall_pass_rate: float
    sentinel_count: int
    drift_detected: bool
    drift_signals: list[str]
    f8_gate_passed: bool  # True if all 3 passes passed
    verdict: str  # SEAL | PARTIAL | 888_HOLD | VOID


# ─────────────────────────────────────────────
# Sentinel Query Loader
# ─────────────────────────────────────────────

def load_sentinels(jsonl_path: str) -> list[SentinelQuery]:
    """Load sentinel queries from JSONL file."""
    sentinels = []
    with open(jsonl_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            sentinels.append(SentinelQuery(
                id=record["id"],
                query=record["query"],
                expected_canon_ids=record.get("expected_canon_ids", []),
                expected_floor_refs=record.get("expected_floor_refs", []),
                min_similarity=record.get("min_similarity", 0.75),
                description=record.get("description", ""),
            ))
    return sentinels


# ─────────────────────────────────────────────
# Embedding Backend
# ─────────────────────────────────────────────

class EmbeddingBackend:
    """Local BGE-M3 embedding backend."""

    def __init__(self, model_name: str = "BAAI/bge-m3"):
        self.model_name = model_name
        self._model = None

    def _get_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                print(f"Loading embedding model: {self.model_name}")
                self._model = SentenceTransformer(self.model_name)
            except ImportError:
                raise RuntimeError(
                    "sentence_transformers not installed. "
                    "Run: pip install sentence-transformers"
                )
        return self._model

    def embed(self, text: str) -> list[float]:
        """Embed text to 1024-dimensional vector."""
        model = self._get_model()
        vector = model.encode(text, normalize_embeddings=True).tolist()
        return vector


# ─────────────────────────────────────────────
# Qdrant Backend
# ─────────────────────────────────────────────

class QdrantBackend:
    """Query Qdrant directly for sentinel testing."""

    def __init__(self, url: str, collection: str = "aaa_canons"):
        self.url = url
        self.collection = collection
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from qdrant_client import QdrantClient
                self._client = QdrantClient(url=self.url)
            except ImportError:
                raise RuntimeError(
                    "qdrant-client not installed. "
                    "Run: pip install qdrant-client"
                )
        return self._client

    def search(self, vector: list[float], k: int = 5) -> list[dict]:
        """Search Qdrant collection."""
        client = self._get_client()
        results = client.search(
            collection_name=self.collection,
            query_vector=vector,
            limit=k,
            with_payload=True,
        )
        return [
            {
                "id": str(r.id),
                "score": r.score,
                "payload": r.payload or {},
            }
            for r in results
        ]


# ─────────────────────────────────────────────
# HF Dataset Backend (offline testing)
# ─────────────────────────────────────────────

class HFDatasetBackend:
    """Search AAA canons from HF dataset using local embedding."""

    def __init__(self, dataset_id: str = "ariffazil/AAA", split: str = "train"):
        self.dataset_id = dataset_id
        self.split = split
        self._texts = None
        self._embeddings = None

    def _load(self, embedding_backend: EmbeddingBackend):
        if self._embeddings is not None:
            return
        try:
            from datasets import load_dataset
            import numpy as np
        except ImportError:
            raise RuntimeError("Install: pip install datasets numpy")

        print(f"Loading {self.dataset_id} / {self.split}...")
        dataset = load_dataset(self.dataset_id, split=self.split)
        self._texts = [
            {"id": r["id"], "text": r["text"], "source": r.get("source", "")}
            for r in dataset
        ]

        print(f"Embedding {len(self._texts)} canon records...")
        import numpy as np
        self._embeddings = np.array([
            embedding_backend.embed(t["text"])
            for t in self._texts
        ])

    def search(self, vector: list[float], embedding_backend: EmbeddingBackend, k: int = 5) -> list[dict]:
        """Search canons by cosine similarity."""
        import numpy as np
        self._load(embedding_backend)

        q = np.array(vector)
        scores = self._embeddings @ q
        top_indices = scores.argsort()[-k:][::-1]

        return [
            {
                "id": self._texts[i]["id"],
                "score": float(scores[i]),
                "payload": {
                    "text": self._texts[i]["text"][:200],
                    "source": self._texts[i]["source"],
                },
            }
            for i in top_indices
        ]


# ─────────────────────────────────────────────
# MCP Endpoint Backend
# ─────────────────────────────────────────────

class MCPBackend:
    """Query live arifosmcp endpoint."""

    def __init__(self, endpoint: str):
        self.endpoint = endpoint.rstrip("/")

    def query(self, query: str, k: int = 5) -> list[dict]:
        """Call engineering_memory vector_query on the live MCP."""
        try:
            import requests
        except ImportError:
            raise RuntimeError("Install: pip install requests")

        payload = {
            "method": "tools/call",
            "params": {
                "name": "engineering_memory",
                "arguments": {
                    "mode": "vector_query",
                    "payload": {
                        "query": query,
                        "k": k,
                        "project_id": "aaa_canons",
                    }
                }
            }
        }

        try:
            resp = requests.post(
                f"{self.endpoint}",
                json=payload,
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            results = data.get("result", {}).get("content", [{}])[0].get("text", "[]")
            if isinstance(results, str):
                results = json.loads(results)
            return results if isinstance(results, list) else []
        except Exception as e:
            return [{"error": str(e)}]


# ─────────────────────────────────────────────
# Regression Runner
# ─────────────────────────────────────────────

def run_pass(
    pass_number: int,
    sentinels: list[SentinelQuery],
    embedding_backend: Optional[EmbeddingBackend] = None,
    qdrant_backend: Optional[QdrantBackend] = None,
    hf_backend: Optional[HFDatasetBackend] = None,
    mcp_backend: Optional[MCPBackend] = None,
    verbose: bool = False,
) -> RegressionPass:
    """Run one regression pass over all sentinel queries."""
    
    regression_pass = RegressionPass(pass_number=pass_number)
    start = time.time()

    for sentinel in sentinels:
        result_start = time.time()
        result = SentinelResult(
            sentinel_id=sentinel.id,
            query=sentinel.query,
            floor_refs=sentinel.expected_floor_refs,
            min_similarity=sentinel.min_similarity,
            actual_similarity=0.0,
            passed=False,
        )

        try:
            # Choose backend
            if mcp_backend:
                raw_results = mcp_backend.query(sentinel.query, k=5)
                if raw_results and isinstance(raw_results[0], dict) and "error" not in raw_results[0]:
                    top = raw_results[0]
                    result.actual_similarity = top.get("score", 0.0)
                    result.top_result_id = top.get("id") or top.get("memory_id")
                    content = top.get("content", top.get("text", ""))
                    result.top_result_excerpt = content[:100] if content else None
                elif raw_results and "error" in raw_results[0]:
                    result.error = raw_results[0]["error"]

            elif embedding_backend and qdrant_backend:
                vector = embedding_backend.embed(sentinel.query)
                raw_results = qdrant_backend.search(vector, k=5)
                if raw_results:
                    top = raw_results[0]
                    result.actual_similarity = top["score"]
                    result.top_result_id = top["id"]
                    content = top.get("payload", {}).get("text", "")
                    result.top_result_excerpt = content[:100] if content else None

            elif embedding_backend and hf_backend:
                vector = embedding_backend.embed(sentinel.query)
                raw_results = hf_backend.search(vector, embedding_backend, k=5)
                if raw_results:
                    top = raw_results[0]
                    result.actual_similarity = top["score"]
                    result.top_result_id = top["id"]
                    content = top.get("payload", {}).get("text", "")
                    result.top_result_excerpt = content[:100] if content else None

            else:
                result.error = "No backend configured"

        except Exception as e:
            result.error = str(e)
            result.actual_similarity = 0.0

        result.latency_ms = (time.time() - result_start) * 1000
        result.passed = (
            result.error is None and
            result.actual_similarity >= sentinel.min_similarity
        )

        if result.passed:
            regression_pass.passed += 1
        elif result.error:
            regression_pass.errors += 1
        else:
            regression_pass.failed += 1

        regression_pass.results.append(result)

        if verbose:
            status = "PASS" if result.passed else ("ERROR" if result.error else "FAIL")
            print(f"  [{status}] {sentinel.id}: similarity={result.actual_similarity:.3f} (min={sentinel.min_similarity}) | {sentinel.description[:50]}")

    regression_pass.duration_seconds = time.time() - start
    return regression_pass


def build_report(
    passes: list[RegressionPass],
    sentinels: list[SentinelQuery],
    aaa_revision: str = "unknown",
    endpoint: Optional[str] = None,
) -> RegressionReport:
    """Build final regression report."""
    
    total_passed = sum(p.passed for p in passes)
    total_queries = sum(p.passed + p.failed + p.errors for p in passes)
    overall_pass_rate = total_passed / total_queries if total_queries > 0 else 0.0

    # Drift detection: any sentinel that fails in ALL passes
    drift_signals = []
    for sentinel in sentinels:
        all_failed = all(
            not any(r.sentinel_id == sentinel.id and r.passed for r in p.results)
            for p in passes
        )
        if all_failed:
            avg_sim = 0.0
            count = 0
            for p in passes:
                for r in p.results:
                    if r.sentinel_id == sentinel.id:
                        avg_sim += r.actual_similarity
                        count += 1
            avg_sim = avg_sim / count if count > 0 else 0.0
            drift_signals.append(
                f"{sentinel.id} ({sentinel.description[:40]}): "
                f"avg_similarity={avg_sim:.3f} < min={sentinel.min_similarity}"
            )

    drift_detected = len(drift_signals) > 0

    # F8 Sabr: all passes must pass (pass_rate >= 0.8 per pass, minimum)
    f8_gate_passed = all(p.pass_rate >= 0.80 for p in passes) and len(passes) >= 1

    # Final verdict
    if drift_detected and any(p.pass_rate < 0.5 for p in passes):
        verdict = "VOID"
    elif drift_detected or any(p.pass_rate < 0.8 for p in passes):
        verdict = "888_HOLD"
    elif f8_gate_passed and overall_pass_rate >= 0.95:
        verdict = "SEAL"
    else:
        verdict = "PARTIAL"

    return RegressionReport(
        timestamp=datetime.now(timezone.utc).isoformat(),
        aaa_revision=aaa_revision,
        endpoint=endpoint,
        total_passes=len(passes),
        passes=passes,
        overall_pass_rate=overall_pass_rate,
        sentinel_count=len(sentinels),
        drift_detected=drift_detected,
        drift_signals=drift_signals,
        f8_gate_passed=f8_gate_passed,
        verdict=verdict,
    )


def print_report(report: RegressionReport):
    """Print regression report to console."""
    
    sep = "═" * 60
    print(f"\n{sep}")
    print(f"  AAA MEMORY REGRESSION REPORT")
    print(f"  {report.timestamp}")
    print(f"  AAA Revision: {report.aaa_revision}")
    if report.endpoint:
        print(f"  Endpoint: {report.endpoint}")
    print(sep)
    print()

    for p in report.passes:
        print(f"  Pass {p.pass_number}: {p.passed}/{p.passed+p.failed+p.errors} passed "
              f"({p.pass_rate*100:.1f}%) | {p.duration_seconds:.1f}s")

    print()
    print(f"  Overall Pass Rate: {report.overall_pass_rate*100:.1f}%")
    print(f"  Sentinel Count:    {report.sentinel_count}")
    print(f"  Drift Detected:    {'YES — CONSTITUTIONAL DRIFT' if report.drift_detected else 'No'}")
    print(f"  F8 Gate:           {'PASSED' if report.f8_gate_passed else 'FAILED'}")
    print()
    print(f"  VERDICT: {report.verdict}")

    if report.drift_signals:
        print()
        print("  Drift Signals:")
        for signal in report.drift_signals:
            print(f"    ⚠ {signal}")

    print()
    print(sep)


def main():
    parser = argparse.ArgumentParser(
        description="arifOS Constitutional Memory Regression Test Harness"
    )
    parser.add_argument("--sentinels", default="memory/sentinel_queries.jsonl",
                        help="Path to sentinel_queries.jsonl")
    parser.add_argument("--endpoint", default=None,
                        help="Live MCP endpoint URL")
    parser.add_argument("--qdrant", default=None,
                        help="Qdrant URL (e.g., http://localhost:6333)")
    parser.add_argument("--collection", default="aaa_canons",
                        help="Qdrant collection name")
    parser.add_argument("--dataset", default=None,
                        help="HF dataset ID (e.g., ariffazil/AAA)")
    parser.add_argument("--split", default="train",
                        help="HF dataset split")
    parser.add_argument("--model", default="BAAI/bge-m3",
                        help="Embedding model")
    parser.add_argument("--passes", type=int, default=1,
                        help="Number of regression passes (F8: minimum 3 for CI gate)")
    parser.add_argument("--fail-fast", action="store_true",
                        help="Stop after first failing pass")
    parser.add_argument("--verbose", action="store_true",
                        help="Print per-sentinel results")
    parser.add_argument("--output", default=None,
                        help="Output JSON report path")
    parser.add_argument("--aaa-revision", default="unknown",
                        help="AAA dataset revision being tested")

    args = parser.parse_args()

    # Load sentinels
    sentinels_path = Path(args.sentinels)
    if not sentinels_path.exists():
        # Try to find relative to this script
        script_dir = Path(__file__).parent.parent
        sentinels_path = script_dir / "memory" / "sentinel_queries.jsonl"

    if not sentinels_path.exists():
        print(f"ERROR: Sentinel queries not found at {sentinels_path}")
        sys.exit(1)

    sentinels = load_sentinels(str(sentinels_path))
    print(f"Loaded {len(sentinels)} sentinel queries")

    # Configure backends
    embedding_backend = None
    qdrant_backend = None
    hf_backend = None
    mcp_backend = None

    if args.endpoint:
        mcp_backend = MCPBackend(args.endpoint)
        print(f"Backend: MCP endpoint ({args.endpoint})")
    elif args.qdrant:
        embedding_backend = EmbeddingBackend(args.model)
        qdrant_backend = QdrantBackend(args.qdrant, args.collection)
        print(f"Backend: Qdrant ({args.qdrant}) + {args.model}")
    elif args.dataset:
        embedding_backend = EmbeddingBackend(args.model)
        hf_backend = HFDatasetBackend(args.dataset, args.split)
        print(f"Backend: HF Dataset ({args.dataset}/{args.split}) + {args.model}")
    else:
        print("ERROR: Specify --endpoint, --qdrant, or --dataset")
        sys.exit(1)

    # Run passes
    all_passes = []
    for pass_num in range(1, args.passes + 1):
        print(f"\nRunning regression pass {pass_num}/{args.passes}...")
        regression_pass = run_pass(
            pass_number=pass_num,
            sentinels=sentinels,
            embedding_backend=embedding_backend,
            qdrant_backend=qdrant_backend,
            hf_backend=hf_backend,
            mcp_backend=mcp_backend,
            verbose=args.verbose,
        )
        all_passes.append(regression_pass)

        pass_ok = regression_pass.pass_rate >= 0.80
        print(f"Pass {pass_num}: {regression_pass.passed}/{len(sentinels)} passed "
              f"({regression_pass.pass_rate*100:.1f}%) | {'PASS' if pass_ok else 'FAIL'}")

        if args.fail_fast and not pass_ok:
            print("Fail-fast: stopping after failing pass.")
            break

    # Build and print report
    report = build_report(
        passes=all_passes,
        sentinels=sentinels,
        aaa_revision=args.aaa_revision,
        endpoint=args.endpoint,
    )

    print_report(report)

    # Save JSON output
    if args.output:
        output_data = asdict(report)
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)
        print(f"\nReport saved to: {args.output}")

    # Exit code
    if report.verdict in ("VOID", "888_HOLD"):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
