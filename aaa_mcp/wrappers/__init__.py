"""
arifOS Wrappers — Constitutional Governance for External Systems

This package provides constitutional wrappers for Docker, Kubernetes, and
policy engines (OPA/Conftest), enforcing the 13 floors before operations
are executed on infrastructure.

Modules:
    k8s_wrapper: K8s Constitutional Wrapper (F1, F2, F5, F6, F10, F13)
    opa_policy: OPA/Conftest integration for F10 Ontology validation

Usage:
    from aaa_mcp.wrappers import k8s_wrapper, opa_policy

    # Validate K8s manifest
    result = await k8s_wrapper.evaluate_apply(manifest, namespace, strategy)

    # Validate against OPA policies
    result = await opa_policy.f10_validator.validate(manifest)

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from aaa_mcp.wrappers.k8s_wrapper import (
    k8s_analyze_manifest,
    k8s_constitutional_apply,
    k8s_constitutional_delete,
    k8s_wrapper,
)
from aaa_mcp.wrappers.opa_policy import (
    f10_validator,
    opa_list_policies,
    opa_validate_manifest,
)

__all__ = [
    "k8s_wrapper",
    "k8s_constitutional_apply",
    "k8s_constitutional_delete",
    "k8s_analyze_manifest",
    "f10_validator",
    "opa_validate_manifest",
    "opa_list_policies",
]
