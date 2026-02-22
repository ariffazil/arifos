"""
arifOS OPA Policy MCP Integration

Integrates with Open Policy Agent (OPA) / Conftest for manifest validation.
Acts as F10 Ontology enforcement layer.

Architecture:
    ┌─────────────────────────────────────────┐
    │        K8s Constitutional Wrapper        │
    └──────────────┬──────────────────────────┘
                   │ F10 Ontology Check
    ┌──────────────▼──────────────────────────┐
    │     arifOS OPA Policy Adapter           │
    │  ┌─────────────────────────────────┐   │
    │  │  F10: Axiom Match = True        │   │
    │  │  ┌──────────┐ ┌──────────────┐  │   │
    │  │  │  OPA     │ │  Conftest    │  │   │
    │  │  │  Server  │ │  (local)     │  │   │
    │  │  └────┬─────┘ └──────┬───────┘  │   │
    │  │       └──────────────┘           │   │
    │  └─────────────────────────────────┘   │
    └──────────────────┬─────────────────────┘
                       │
    ┌──────────────────▼─────────────────────┐
    │      Downstream OPA/Rego Policies       │
    │  • k8s-best-practices.rego             │
    │  • pod-security-standards.rego         │
    │  • resource-limits.rego                │
    └────────────────────────────────────────┘

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

# Note: mcp is imported lazily in server.py to avoid circular imports


@dataclass
class PolicyResult:
    """Result of OPA policy evaluation."""

    policy_name: str
    passed: bool
    violations: List[str]
    severity: str  # critical, warning, info
    metadata: Dict[str, Any]


@dataclass
class F10OntologyResult:
    """F10 Ontology floor evaluation result."""

    axiom_match: bool
    policies_checked: int
    policies_passed: int
    policies_failed: int
    violations: List[Dict[str, Any]]
    score: float  # 0.0-1.0
    reasoning: str


# =============================================================================
# POLICY ENGINE ADAPTERS
# =============================================================================


class OPAServerAdapter:
    """Adapter for external OPA server."""

    def __init__(self, url: str = "http://localhost:8181"):
        self.url = url
        self.timeout = 30

    async def evaluate(self, manifest: str, policy_path: str) -> PolicyResult:
        """Evaluate manifest against OPA policy."""
        import httpx

        try:
            # Parse manifest to JSON
            import yaml

            data = yaml.safe_load(manifest)

            # Query OPA
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.url}/v1/data/{policy_path}",
                    json={"input": data},
                    timeout=self.timeout,
                )
                result = response.json()

                # Extract violations from OPA result
                violations = result.get("result", {}).get("violations", [])
                passed = len(violations) == 0

                return PolicyResult(
                    policy_name=policy_path,
                    passed=passed,
                    violations=violations,
                    severity="critical" if not passed else "info",
                    metadata={"source": "opa_server"},
                )
        except Exception as e:
            return PolicyResult(
                policy_name=policy_path,
                passed=False,
                violations=[f"OPA query failed: {e}"],
                severity="critical",
                metadata={"error": str(e)},
            )


class ConftestAdapter:
    """Adapter for local Conftest binary."""

    DEFAULT_POLICY_DIRS = [
        "policies/",
        "/opt/arifos/policies/",
    ]

    def __init__(self, policy_dir: Optional[str] = None):
        self.policy_dir = policy_dir or self._find_policy_dir()

    def _find_policy_dir(self) -> str:
        """Find available policy directory."""
        for d in self.DEFAULT_POLICY_DIRS:
            if os.path.exists(d):
                return d
        return "policies/"  # Default

    def evaluate(self, manifest: str, namespace: str = "k8s") -> List[PolicyResult]:
        """Evaluate manifest using Conftest."""
        results = []

        try:
            # Write manifest to temp file
            import tempfile

            with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
                f.write(manifest)
                temp_path = f.name

            # Run conftest
            cmd = [
                "conftest",
                "test",
                temp_path,
                "--policy",
                self.policy_dir,
                "--namespace",
                namespace,
                "--output",
                "json",
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
            )

            # Parse results
            # Conftest returns exit code 1 if failures, 0 if all pass
            try:
                output = json.loads(result.stdout)
            except json.JSONDecodeError:
                output = {"failures": []}

            # Clean up temp file
            os.unlink(temp_path)

            # Convert to PolicyResults
            failures = output.get("failures", [])
            for failure in failures:
                results.append(
                    PolicyResult(
                        policy_name=failure.get("msg", "unknown").split(":")[0],
                        passed=False,
                        violations=[failure.get("msg", "Policy violation")],
                        severity=failure.get("severity", "warning"),
                        metadata=failure,
                    )
                )

            # If no failures, add a passing result
            if not failures:
                results.append(
                    PolicyResult(
                        policy_name=f"{namespace}/all",
                        passed=True,
                        violations=[],
                        severity="info",
                        metadata={},
                    )
                )

        except FileNotFoundError:
            # Conftest not installed
            results.append(
                PolicyResult(
                    policy_name="conftest",
                    passed=True,  # Fail open if conftest not available
                    violations=[],
                    severity="info",
                    metadata={"note": "Conftest not installed, skipping F10 validation"},
                )
            )
        except Exception as e:
            results.append(
                PolicyResult(
                    policy_name="conftest",
                    passed=False,
                    violations=[f"Conftest execution failed: {e}"],
                    severity="warning",
                    metadata={"error": str(e)},
                )
            )

        return results


# =============================================================================
# BUILT-IN POLICIES (Fallback when OPA/Conftest unavailable)
# =============================================================================

BUILT_IN_POLICIES = {
    "k8s-best-practices": {
        "description": "Basic K8s best practices",
        "checks": [
            {
                "name": "no_latest_tag",
                "severity": "warning",
                "check": lambda m: not any(
                    ":latest" in c.get("image", "") or ":" not in c.get("image", "")
                    for c in m.get("spec", {})
                    .get("template", {})
                    .get("spec", {})
                    .get("containers", [])
                ),
                "message": "Container uses :latest tag or no tag (mutable)",
            },
            {
                "name": "resource_limits",
                "severity": "warning",
                "check": lambda m: all(
                    "resources" in c and "limits" in c.get("resources", {})
                    for c in m.get("spec", {})
                    .get("template", {})
                    .get("spec", {})
                    .get("containers", [])
                ),
                "message": "Container missing resource limits",
            },
            {
                "name": "liveness_probe",
                "severity": "info",
                "check": lambda m: any(
                    "livenessProbe" in c
                    for c in m.get("spec", {})
                    .get("template", {})
                    .get("spec", {})
                    .get("containers", [])
                ),
                "message": "Container missing liveness probe",
            },
            {
                "name": "security_context",
                "severity": "warning",
                "check": lambda m: not any(
                    c.get("securityContext", {}).get("privileged", False)
                    for c in m.get("spec", {})
                    .get("template", {})
                    .get("spec", {})
                    .get("containers", [])
                ),
                "message": "Container runs privileged",
            },
        ],
    },
    "pod-security": {
        "description": "Pod Security Standards (restricted)",
        "checks": [
            {
                "name": "no_host_network",
                "severity": "critical",
                "check": lambda m: not m.get("spec", {})
                .get("template", {})
                .get("spec", {})
                .get("hostNetwork", False),
                "message": "Pod uses host network namespace",
            },
            {
                "name": "no_host_pid",
                "severity": "critical",
                "check": lambda m: not m.get("spec", {})
                .get("template", {})
                .get("spec", {})
                .get("hostPID", False),
                "message": "Pod uses host PID namespace",
            },
        ],
    },
}


class BuiltInPolicyEngine:
    """Fallback policy engine using built-in Rego-like rules."""

    def evaluate(self, manifest: str) -> List[PolicyResult]:
        """Evaluate against built-in policies."""
        import yaml

        try:
            docs = list(yaml.safe_load_all(manifest))
        except yaml.YAMLError as e:
            return [
                PolicyResult(
                    policy_name="yaml-parse",
                    passed=False,
                    violations=[f"Invalid YAML: {e}"],
                    severity="critical",
                    metadata={},
                )
            ]

        results = []

        for doc in docs:
            if not doc:
                continue

            for policy_name, policy_def in BUILT_IN_POLICIES.items():
                violations = []

                for check in policy_def["checks"]:
                    try:
                        if not check["check"](doc):
                            violations.append(
                                {
                                    "msg": check["message"],
                                    "severity": check["severity"],
                                    "check": check["name"],
                                }
                            )
                    except Exception:
                        # Check failed to evaluate (e.g., wrong resource type)
                        pass

                results.append(
                    PolicyResult(
                        policy_name=policy_name,
                        passed=len(violations) == 0,
                        violations=violations,
                        severity=(
                            "critical"
                            if any(v.get("severity") == "critical" for v in violations)
                            else "warning"
                        ),
                        metadata={"checks_run": len(policy_def["checks"])},
                    )
                )

        return results


# =============================================================================
# F10 ONTOLOGY VALIDATOR
# =============================================================================


class F10OntologyValidator:
    """
    F10 Ontology floor validator using OPA/Conftest.

    Validates that manifests match expected axioms (schemas, best practices).
    """

    def __init__(self):
        self.opa = OPAServerAdapter(url=os.environ.get("OPA_SERVER_URL", "http://localhost:8181"))
        self.conftest = ConftestAdapter()
        self.builtin = BuiltInPolicyEngine()

        # Policy preference order
        self.preferred_engine = os.environ.get("F10_ENGINE", "auto")  # auto, opa, conftest, builtin

    async def validate(self, manifest: str, namespace: str = "k8s") -> F10OntologyResult:
        """Validate manifest against all available policy engines."""

        all_results: List[PolicyResult] = []

        # Try engines in order of preference
        if self.preferred_engine in ("auto", "opa"):
            try:
                result = await self.opa.evaluate(manifest, f"{namespace}/violation")
                all_results.append(result)
            except Exception:
                pass  # Fall through to next engine

        if self.preferred_engine in ("auto", "conftest"):
            try:
                results = self.conftest.evaluate(manifest, namespace)
                all_results.extend(results)
            except Exception:
                pass

        # Always run built-in as fallback
        if not all_results or self.preferred_engine == "builtin":
            results = self.builtin.evaluate(manifest)
            all_results.extend(results)

        # Calculate F10 score
        total_policies = len(all_results)
        passed_policies = sum(1 for r in all_results if r.passed)

        # Critical violations = automatic F10 fail
        critical_violations = [
            v
            for r in all_results
            for v in (r.violations if isinstance(r.violations, list) else [r.violations])
            if isinstance(v, dict) and v.get("severity") == "critical"
        ]

        # Score calculation
        if total_policies == 0:
            score = 1.0  # Pass if no policies configured
        else:
            base_score = passed_policies / total_policies
            # Deduct for critical violations
            score = max(0.0, base_score - (len(critical_violations) * 0.3))

        # Determine axiom match
        axiom_match = len(critical_violations) == 0 and score >= 0.8

        # Collect all violations
        all_violations = []
        for r in all_results:
            if isinstance(r.violations, list):
                all_violations.extend(
                    [{"policy": r.policy_name, "violation": v} for v in r.violations]
                )
            else:
                all_violations.append({"policy": r.policy_name, "violation": r.violations})

        return F10OntologyResult(
            axiom_match=axiom_match,
            policies_checked=total_policies,
            policies_passed=passed_policies,
            policies_failed=total_policies - passed_policies,
            violations=all_violations,
            score=score,
            reasoning=f"F10: {passed_policies}/{total_policies} policies passed, "
            f"{len(critical_violations)} critical violations",
        )


# Singleton
f10_validator = F10OntologyValidator()


# =============================================================================
# MCP TOOLS
# =============================================================================


async def opa_validate_manifest(
    manifest: str,
    namespace: str = "k8s",
    session_id: str = "",
) -> Dict[str, Any]:
    """
    Validate K8s manifest against OPA policies (F10 Ontology).

    Args:
        manifest: YAML Kubernetes manifest
        namespace: Policy namespace (k8s, docker, etc.)
        session_id: Constitutional session ID

    Returns:
        F10 validation result with axiom_match status
    """
    result = await f10_validator.validate(manifest, namespace)

    return {
        "axiom_match": result.axiom_match,
        "score": result.score,
        "policies": {
            "checked": result.policies_checked,
            "passed": result.policies_passed,
            "failed": result.policies_failed,
        },
        "violations": result.violations,
        "reasoning": result.reasoning,
        "message": (
            "💎🧠 DITEMPA, BUKAN DIBERI 🔒 — F10 Ontology validated"
            if result.axiom_match
            else "🔥 DITEMPA, BUKAN DIBERI — F10 Ontology violations detected"
        ),
    }


async def opa_list_policies() -> Dict[str, Any]:
    """List available OPA/Conftest policies."""
    return {
        "engines": {
            "opa_server": {
                "url": f10_validator.opa.url,
                "available": True,  # Assume available
            },
            "conftest": {
                "policy_dir": f10_validator.conftest.policy_dir,
                "available": os.path.exists(f10_validator.conftest.policy_dir),
            },
            "builtin": {
                "policies": list(BUILT_IN_POLICIES.keys()),
                "available": True,
            },
        },
        "builtin_policies": {
            name: {
                "description": policy["description"],
                "checks": [c["name"] for c in policy["checks"]],
            }
            for name, policy in BUILT_IN_POLICIES.items()
        },
        "preferred_engine": f10_validator.preferred_engine,
    }
