"""
Test reporters for arifOS MCP test suite.

Provides JSON output and rich terminal formatting for CI/CD and human readability.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class TestReporter:
    """Aggregates test results and generates reports."""

    def __init__(self):
        self.results: List[Dict[str, Any]] = []
        self.start_time = time.time()

    def add_result(self, test_name: str, validation_result: Dict[str, Any], passed: bool = True):
        """Add a test result to the report."""
        self.results.append(
            {
                "test_name": test_name,
                "passed": passed,
                "verdict": validation_result.get("verdict", "UNKNOWN"),
                "audit_verdict": validation_result.get("audit_verdict", "UNKNOWN"),
                "genius": validation_result.get("genius", 0.0),
                "delta_s": validation_result.get("delta_s", 0.0),
                "elapsed_ms": validation_result.get("elapsed_ms", 0.0),
                "floors_passed": validation_result.get("floors_passed", []),
            }
        )

    def compute_summary(self) -> Dict[str, Any]:
        """Compute aggregate statistics."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])
        failed = total - passed

        avg_genius = sum(r["genius"] for r in self.results) / total if total > 0 else 0.0
        total_delta_s = sum(r["delta_s"] for r in self.results)
        avg_latency = sum(r["elapsed_ms"] for r in self.results) / total if total > 0 else 0.0

        return {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": (passed / total * 100) if total > 0 else 0.0,
            "avg_genius": avg_genius,
            "total_delta_s": total_delta_s,
            "avg_latency_ms": avg_latency,
            "total_duration_s": time.time() - self.start_time,
        }

    def write_json(self, output_path: str = "test-results.json"):
        """Write results to JSON file for CI/CD."""
        summary = self.compute_summary()
        report = {
            "summary": summary,
            "results": self.results,
            "timestamp": time.time(),
        }

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)

        console.print(f"[green]✓[/green] JSON report written to {output_path}")

    def print_rich_summary(self):
        """Print a beautiful terminal summary using rich."""
        summary = self.compute_summary()

        # Create summary table
        table = Table(
            title="🔥 arifOS MCP Test Results", show_header=True, header_style="bold magenta"
        )
        table.add_column("Metric", style="cyan", width=25)
        table.add_column("Value", style="yellow", width=20)

        table.add_row("Total Tests", str(summary["total_tests"]))
        table.add_row("Passed", f"[green]{summary['passed']}[/green]")
        table.add_row("Failed", f"[red]{summary['failed']}[/red]")
        table.add_row("Pass Rate", f"{summary['pass_rate']:.1f}%")
        table.add_row("─" * 25, "─" * 20)
        table.add_row("Avg Genius Score", f"{summary['avg_genius']:.3f}")
        table.add_row("Total ΔS (Entropy)", f"{summary['total_delta_s']:.2f}")
        table.add_row("Avg Latency", f"{summary['avg_latency_ms']:.2f}ms")
        table.add_row("Total Duration", f"{summary['total_duration_s']:.2f}s")

        console.print()
        console.print(table)
        console.print()

        # Print individual test results
        if summary["failed"] > 0:
            console.print(Panel("[red]Failed Tests:[/red]", style="red"))
            for r in self.results:
                if not r["passed"]:
                    console.print(f"  ❌ {r['test_name']} - {r['verdict']}")

        # Constitutional health check
        if summary["avg_genius"] >= 0.90:
            genius_status = "[green]EXCELLENT[/green] 🌟"
        elif summary["avg_genius"] >= 0.80:
            genius_status = "[yellow]GOOD[/yellow] ✓"
        else:
            genius_status = "[red]NEEDS ATTENTION[/red] ⚠️"

        console.print(
            Panel(
                f"Constitutional Health: {genius_status}\n"
                f"Genius Score: {summary['avg_genius']:.3f}\n"
                f"Pass Rate: {summary['pass_rate']:.1f}%",
                title="📊 Overall Assessment",
                border_style="green" if summary["pass_rate"] == 100.0 else "yellow",
            )
        )

        console.print("\n[bold]Ditempa Bukan Diberi 🔥[/bold]\n")


# Global reporter instance
_reporter = TestReporter()


def get_reporter() -> TestReporter:
    """Get the global test reporter instance."""
    return _reporter
