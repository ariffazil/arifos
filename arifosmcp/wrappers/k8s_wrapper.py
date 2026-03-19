"""
arifOS K8s Constitutional Wrapper

Wraps Kubernetes MCP servers with 13-floor governance.
Acts as admission controller before applying manifests.

Architecture:
    ┌─────────────────┐
    │   Agent/CLI     │
    └────────┬────────┘
             │
    ┌────────▼─────────────────────────────────┐
    │     arifOS MCP Gateway                    │
    │  ┌─────────────────────────────────────┐ │
    │  │   K8s Constitutional Wrapper         │ │
    │  │  ┌─────────┐ ┌─────────┐ ┌────────┐ │ │
    │  │  │   F1    │ │   F2    │ │   F6   │ │ │
    │  │  │ Amanah  │ │  Truth  │ │ Empathy│ │ │
    │  │  └────┬────┘ └────┬────┘ └───┬────┘ │ │
    │  │       └───────────┴──────────┘      │ │
    │  │              F13 Sovereign            │ │
    │  │         (888_HOLD for prod)           │ │
    │  └─────────────────┬────────────────────┘ │
    └────────────────────┼──────────────────────┘
                         │ SEAL / 888_HOLD / VOID
    ┌────────────────────▼──────────────────────┐
    │         Downstream K8s MCP Server          │
    │    (docker.io/lukemarsden/kubernetes-mcp)  │
    └───────────────────────────────────────────┘

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import Any

import yaml

from aaa_mcp.core.constitutional_decorator import constitutional_floor

# Note: mcp is imported lazily in server.py to avoid circular imports


class K8sRiskLevel(str, Enum):
    """Risk classification for K8s operations."""

    LOW = "low"  # safe: list, get, describe
    MEDIUM = "medium"  # apply, scale, rollout
    HIGH = "high"  # delete (namespace-scoped)
    CRITICAL = "critical"  # delete (cluster-scoped), prod changes


@dataclass
class ManifestAnalysis:
    """Analysis of a K8s manifest for constitutional floors."""

    # Resource metadata
    api_version: str
    kind: str
    name: str
    namespace: str
    labels: dict[str, str]
    annotations: dict[str, str]

    # Container analysis (for F2 Truth)
    images: list[str]
    uses_latest_tag: bool
    uses_digest: bool
    untrusted_registries: list[str]

    # Security analysis (for F6 Empathy)
    privileged_containers: bool
    host_network: bool
    host_pid: bool
    host_ipc: bool
    run_as_root: bool

    # Operational (for F1 Amanah, F5 Peace²)
    has_resource_limits: bool
    has_liveness_probe: bool
    has_readiness_probe: bool
    replicas: int
    strategy: str

    # Constitutional scores
    f2_truth_score: float  # Image provenance
    f6_empathy_score: float  # Security posture
    f5_peace_score: float  # Operational maturity


@dataclass
class BlastRadius:
    """Infrastructure blast radius for F6 Empathy."""

    affected_namespaces: list[str]
    affected_deployments: int
    affected_pods: int
    affected_services: int
    affected_configmaps: int
    affected_secrets: int
    critical_impact: bool
    score: float  # 0.0-1.0, higher = more dangerous
    mitigation_suggestions: list[str]


# =============================================================================
# MANIFEST PARSER
# =============================================================================


class ManifestParser:
    """Parse and analyze K8s manifests for constitutional floors."""

    TRUSTED_REGISTRIES = [
        "gcr.io",
        "registry.k8s.io",
        "docker.io/library/",  # Official images only
        "quay.io",
        "mcr.microsoft.com",
    ]

    UNTAINTED_NAMESPACES = [
        "kube-system",
        "kube-public",
        "kube-node-lease",
        "monitoring",
    ]

    def parse(self, manifest: str) -> ManifestAnalysis:
        """Parse YAML manifest into structured analysis."""
        try:
            docs = list(yaml.safe_load_all(manifest))
        except yaml.YAMLError:
            docs = [{}]

        # Use first document if multiple
        doc = docs[0] if docs else {}

        metadata = doc.get("metadata", {})
        spec = doc.get("spec", {})
        template = spec.get("template", {})
        template_spec = template.get("spec", {})
        containers = template_spec.get("containers", [])

        # Extract images
        images = [c.get("image", "") for c in containers]

        # Check image provenance
        uses_latest = any(":latest" in img or ":" not in img for img in images)
        uses_digest = any("@sha256:" in img for img in images)
        untrusted = [
            img for img in images if not any(trusted in img for trusted in self.TRUSTED_REGISTRIES)
        ]

        # Security context
        security_context = template_spec.get("securityContext", {})
        container_sc = [c.get("securityContext", {}) for c in containers]

        privileged = any(sc.get("privileged", False) for sc in container_sc)
        run_as_root = any(sc.get("runAsUser", 1000) == 0 for sc in container_sc)

        # Probes and limits
        has_limits = all(
            "resources" in c and "limits" in c.get("resources", {}) for c in containers
        )
        has_liveness = any("livenessProbe" in c for c in containers)
        has_readiness = any("readinessProbe" in c for c in containers)

        # Calculate F2 Truth score
        f2_score = self._calculate_f2_score(images, uses_digest, untrusted)

        # Calculate F6 Empathy score (security posture)
        f6_score = self._calculate_f6_score(
            privileged,
            run_as_root,
            template_spec.get("hostNetwork", False),
            template_spec.get("hostPID", False),
            has_limits,
        )

        # Calculate F5 Peace score (operational maturity)
        f5_score = self._calculate_f5_score(has_liveness, has_readiness, spec.get("strategy", {}))

        return ManifestAnalysis(
            api_version=doc.get("apiVersion", ""),
            kind=doc.get("kind", "Unknown"),
            name=metadata.get("name", ""),
            namespace=metadata.get("namespace", "default"),
            labels=metadata.get("labels", {}),
            annotations=metadata.get("annotations", {}),
            images=images,
            uses_latest_tag=uses_latest,
            uses_digest=uses_digest,
            untrusted_registries=untrusted,
            privileged_containers=privileged,
            host_network=template_spec.get("hostNetwork", False),
            host_pid=template_spec.get("hostPID", False),
            host_ipc=template_spec.get("hostIPC", False),
            run_as_root=run_as_root,
            has_resource_limits=has_limits,
            has_liveness_probe=has_liveness,
            has_readiness_probe=has_readiness,
            replicas=spec.get("replicas", 1),
            strategy=spec.get("strategy", {}).get("type", "RollingUpdate"),
            f2_truth_score=f2_score,
            f6_empathy_score=f6_score,
            f5_peace_score=f5_score,
        )

    def _calculate_f2_score(
        self, images: list[str], uses_digest: bool, untrusted: list[str]
    ) -> float:
        """Calculate F2 Truth score based on image provenance."""
        if not images:
            return 0.5  # Neutral if no images

        score = 1.0

        # Deductions
        if any(":latest" in img or ":" not in img for img in images):
            score -= 0.3  # Mutable tags
        if untrusted:
            score -= 0.2 * len(untrusted) / len(images)
        if not uses_digest:
            score -= 0.1  # No immutable reference

        return max(0.0, score)

    def _calculate_f6_score(
        self,
        privileged: bool,
        run_as_root: bool,
        host_network: bool,
        host_pid: bool,
        has_limits: bool,
    ) -> float:
        """Calculate F6 Empathy score based on security posture."""
        score = 1.0

        if privileged:
            score -= 0.4
        if run_as_root:
            score -= 0.2
        if host_network:
            score -= 0.15
        if host_pid:
            score -= 0.15
        if not has_limits:
            score -= 0.1

        return max(0.0, score)

    def _calculate_f5_score(self, has_liveness: bool, has_readiness: bool, strategy: dict) -> float:
        """Calculate F5 Peace² score based on operational maturity."""
        score = 0.5  # Base

        if has_liveness:
            score += 0.2
        if has_readiness:
            score += 0.2
        if strategy.get("type") == "RollingUpdate":
            score += 0.1

        return min(1.0, score)


# =============================================================================
# BLAST RADIUS CALCULATOR
# =============================================================================


class BlastRadiusCalculator:
    """Calculate infrastructure blast radius for F6 Empathy."""

    def calculate(
        self,
        operation: str,
        manifest: ManifestAnalysis | None,
        namespace: str,
        existing_state: dict | None = None,
    ) -> BlastRadius:
        """Calculate blast radius for an operation."""
        affected_ns = [namespace]
        deployments = 0
        pods = 0
        services = 0
        configmaps = 0
        secrets = 0
        critical = False
        mitigations = []

        # Namespace criticality
        if namespace in ["prod", "production", "kube-system"]:
            critical = True
            mitigations.append("Operation affects critical namespace — review carefully")

        # Operation type
        if "delete" in operation.lower():
            deployments = 1 if manifest else 0
            pods = manifest.replicas if manifest else 1
            mitigations.append("Ensure backup exists before deletion (F1)")
            mitigations.append("Verify no critical workloads affected")

        elif "apply" in operation.lower():
            if manifest:
                deployments = 1
                pods = manifest.replicas

                # Check for image changes (immutable tag check)
                if manifest.uses_latest_tag:
                    mitigations.append("Use digest-based image for immutable deployment")

        # Calculate score
        score = 0.0
        if critical:
            score += 0.5
        if "delete" in operation.lower():
            score += 0.3
        if pods > 10:
            score += 0.2

        score = min(1.0, score)

        return BlastRadius(
            affected_namespaces=affected_ns,
            affected_deployments=deployments,
            affected_pods=pods,
            affected_services=services,
            affected_configmaps=configmaps,
            affected_secrets=secrets,
            critical_impact=critical,
            score=score,
            mitigation_suggestions=mitigations,
        )


# =============================================================================
# K8S CONSTITUTIONAL WRAPPER
# =============================================================================


class K8sConstitutionalWrapper:
    """
    Constitutional wrapper for Kubernetes operations.

    Implements:
    - F1 Amanah: Reversibility check (rollback strategy)
    - F2 Truth: Image provenance verification
    - F5 Peace²: Deployment strategy validation
    - F6 Empathy: Blast radius calculation, security posture
    - F10 Ontology: Manifest schema validation
    - F13 Sovereign: Human override for critical operations
    """

    # Thresholds
    F2_TRUTH_THRESHOLD = 0.90
    F6_EMPATHY_THRESHOLD = 0.70  # κᵣ ≥ 0.70 for MEDIUM, ≥ 0.95 for CRITICAL

    def __init__(self):
        self.parser = ManifestParser()
        self.blast_calc = BlastRadiusCalculator()

    async def evaluate_apply(
        self,
        manifest: str,
        namespace: str,
        strategy: str,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Evaluate a kubectl apply through constitutional floors."""

        # Parse manifest
        analysis = self.parser.parse(manifest)

        # Calculate blast radius
        blast = self.blast_calc.calculate("apply", analysis, namespace)

        # Floor evaluations
        floors = []
        hard_failures = []

        # F10: Ontology (Schema validation)
        f10_pass = bool(analysis.api_version and analysis.kind)
        floors.append(
            {
                "floor": "F10",
                "name": "Ontology",
                "passed": f10_pass,
                "score": 1.0 if f10_pass else 0.0,
            }
        )
        if not f10_pass:
            hard_failures.append("F10")

        # F2: Truth (Image provenance)
        f2_pass = analysis.f2_truth_score >= self.F2_TRUTH_THRESHOLD
        floors.append(
            {
                "floor": "F2",
                "name": "Truth",
                "passed": f2_pass,
                "score": analysis.f2_truth_score,
                "detail": f"Images: {analysis.images}",
            }
        )
        if not f2_pass and namespace in ["prod", "production"]:
            hard_failures.append("F2")

        # F6: Empathy (Security posture + blast radius)
        # For production: κᵣ ≥ 0.95
        f6_threshold = 0.95 if namespace in ["prod", "production"] else self.F6_EMPATHY_THRESHOLD
        f6_pass = analysis.f6_empathy_score >= f6_threshold and blast.score < 0.5
        floors.append(
            {
                "floor": "F6",
                "name": "Empathy",
                "passed": f6_pass,
                "score": analysis.f6_empathy_score,
                "blast_radius": blast.score,
            }
        )
        if not f6_pass:
            hard_failures.append("F6")

        # F5: Peace² (Operational maturity)
        f5_pass = analysis.f5_peace_score >= 0.7
        floors.append(
            {"floor": "F5", "name": "Peace²", "passed": f5_pass, "score": analysis.f5_peace_score}
        )

        # F1: Amanah (Reversibility)
        has_strategy = strategy in ["canary", "blue-green", "rolling"]
        f1_pass = has_strategy or namespace not in ["prod", "production"]
        floors.append(
            {
                "floor": "F1",
                "name": "Amanah",
                "passed": f1_pass,
                "score": 1.0 if f1_pass else 0.0,
                "strategy": strategy,
            }
        )
        if not f1_pass:
            hard_failures.append("F1")

        # Determine verdict
        if hard_failures:
            verdict = "VOID"
            verdict_reason = f"HARD floors failed: {hard_failures}"
        elif blast.critical_impact and namespace in ["prod", "production"]:
            verdict = "888_HOLD"
            verdict_reason = (
                "Production operation with critical blast radius requires human approval"
            )
        else:
            verdict = "SEAL"
            verdict_reason = "All floors passed"

        # Generate manifest hash for audit
        manifest_hash = hashlib.sha256(manifest.encode()).hexdigest()[:16]

        return {
            "verdict": verdict,
            "reason": verdict_reason,
            "floors": floors,
            "hard_failures": hard_failures,
            "analysis": {
                "api_version": analysis.api_version,
                "kind": analysis.kind,
                "name": analysis.name,
                "namespace": analysis.namespace,
                "images": analysis.images,
                "privileged": analysis.privileged_containers,
                "replicas": analysis.replicas,
            },
            "blast_radius": {
                "score": blast.score,
                "critical": blast.critical_impact,
                "affected_pods": blast.affected_pods,
                "mitigations": blast.mitigation_suggestions,
            },
            "manifest_hash": manifest_hash,
            "dry_run": dry_run,
        }

    async def evaluate_delete(
        self,
        resource: str,
        name: str,
        namespace: str,
        backup_made: bool,
    ) -> dict[str, Any]:
        """Evaluate a kubectl delete through constitutional floors."""

        # Blast radius for delete
        blast = self.blast_calc.calculate("delete", None, namespace)

        floors = []
        hard_failures = []

        # F1: Amanah (Reversibility)
        f1_pass = backup_made
        floors.append(
            {"floor": "F1", "name": "Amanah", "passed": f1_pass, "score": 1.0 if f1_pass else 0.0}
        )
        if not f1_pass:
            hard_failures.append("F1")

        # F6: Empathy (Blast radius)
        f6_pass = blast.score < 0.5
        floors.append(
            {
                "floor": "F6",
                "name": "Empathy",
                "passed": f6_pass,
                "score": 1.0 - blast.score,
                "blast_radius": blast.score,
            }
        )
        if not f6_pass:
            hard_failures.append("F6")

        # F13: Sovereign (Human override for production deletes)
        needs_override = namespace in ["prod", "production"]

        # Determine verdict
        if hard_failures:
            verdict = "VOID"
            verdict_reason = f"HARD floors failed: {hard_failures}"
        elif needs_override:
            verdict = "888_HOLD"
            verdict_reason = "Production delete requires human override (F13)"
        else:
            verdict = "SEAL"
            verdict_reason = "All floors passed"

        return {
            "verdict": verdict,
            "reason": verdict_reason,
            "floors": floors,
            "hard_failures": hard_failures,
            "resource": f"{resource}/{name}",
            "namespace": namespace,
            "backup_made": backup_made,
            "requires_override": needs_override,
        }


# Singleton instance
k8s_wrapper = K8sConstitutionalWrapper()


# =============================================================================
# MCP TOOLS
# =============================================================================


@constitutional_floor("F1", "F2", "F6", "F10", "F11", "F12")
async def k8s_constitutional_apply(
    manifest: str,
    namespace: str = "default",
    strategy: str = "rolling",
    session_id: str = "",
    dry_run: bool = False,
) -> dict[str, Any]:
    """
    Evaluate K8s apply through constitutional floors.

    Returns evaluation result. For actual execution, use gateway_route_tool.

    Args:
        manifest: YAML Kubernetes manifest
        namespace: Target namespace
        strategy: Deployment strategy (canary, blue-green, rolling)
        session_id: Constitutional session ID
        dry_run: If True, only evaluate without executing
    """
    result = await k8s_wrapper.evaluate_apply(manifest, namespace, strategy, dry_run)

    # Add constitutional motto
    if result["verdict"] == "SEAL":
        result["message"] = "💎🧠 DITEMPA, BUKAN DIBERI 🔒 — Manifest constitutionally approved"
    elif result["verdict"] == "VOID":
        result["message"] = "🔥 DITEMPA, BUKAN DIBERI — Manifest blocked by constitutional floors"
    elif result["verdict"] == "888_HOLD":
        result["message"] = "💎🧠 DITEMPA, BUKAN DIBERI 🔒 — Human approval required"

    return result


@constitutional_floor("F1", "F6", "F11", "F12")
async def k8s_constitutional_delete(
    resource: str,
    name: str,
    namespace: str = "default",
    backup_made: bool = False,
    session_id: str = "",
) -> dict[str, Any]:
    """
    Evaluate K8s delete through constitutional floors.

    DESTRUCTIVE operation — requires F1 (backup) and F13 (override for prod).
    """
    result = await k8s_wrapper.evaluate_delete(resource, name, namespace, backup_made)

    if result["verdict"] == "SEAL":
        result["message"] = "💎🧠 DITEMPA, BUKAN DIBERI 🔒 — Delete approved"
    elif result["verdict"] == "VOID":
        result["message"] = "🔥 DITEMPA, BUKAN DIBERI — Delete blocked"
    elif result["verdict"] == "888_HOLD":
        result["message"] = (
            "💎🧠 DITEMPA, BUKAN DIBERI 🔒 — Human approval required for prod delete"
        )

    return result


async def k8s_analyze_manifest(manifest: str) -> dict[str, Any]:
    """
    Analyze a K8s manifest without constitutional enforcement.

    Returns detailed analysis of security posture, image provenance, etc.
    """
    analysis = k8s_wrapper.parser.parse(manifest)

    return {
        "resource": {
            "api_version": analysis.api_version,
            "kind": analysis.kind,
            "name": analysis.name,
            "namespace": analysis.namespace,
        },
        "images": {
            "list": analysis.images,
            "uses_latest": analysis.uses_latest_tag,
            "uses_digest": analysis.uses_digest,
            "untrusted": analysis.untrusted_registries,
        },
        "security": {
            "privileged": analysis.privileged_containers,
            "host_network": analysis.host_network,
            "host_pid": analysis.host_pid,
            "run_as_root": analysis.run_as_root,
        },
        "operational": {
            "has_resource_limits": analysis.has_resource_limits,
            "has_liveness_probe": analysis.has_liveness_probe,
            "has_readiness_probe": analysis.has_readiness_probe,
            "replicas": analysis.replicas,
            "strategy": analysis.strategy,
        },
        "constitutional_scores": {
            "f2_truth": analysis.f2_truth_score,
            "f6_empathy": analysis.f6_empathy_score,
            "f5_peace": analysis.f5_peace_score,
        },
    }
