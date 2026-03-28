"""
arifOS Environment Configuration
Handles dual-sovereignty deployment: VPS (Sovereign) vs Horizon (Public)
"""

import os
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class DeploymentMode(Enum):
    """Deployment sovereignty modes."""
    VPS_SOVEREIGN = "vps"          # Your Hostinger VPS - full sovereignty
    HORIZON_PUBLIC = "horizon"      # Prefect Horizon - public ambassador
    LOCAL_DEV = "local"             # Local development
    TEST = "test"                   # Test environment


@dataclass
class EnvironmentConfig:
    """Environment-specific configuration."""
    mode: DeploymentMode
    name: str
    base_url: str
    vault_backend: str
    memory_backend: str
    rate_limit_enabled: bool
    auth_required: bool
    thermo_budget_multiplier: float
    constitutional_floors: list[str]  # Which F1-F13 floors are enforced


# =============================================================================
# SOVEREIGN KERNEL (VPS) - Maximum constitutional enforcement
# =============================================================================
VPS_CONFIG = EnvironmentConfig(
    mode=DeploymentMode.VPS_SOVEREIGN,
    name="arifOS Sovereign Kernel",
    base_url="https://arifos.arif-fazil.com",
    vault_backend="postgresql",      # Local PostgreSQL
    memory_backend="redis",          # Local Redis
    rate_limit_enabled=True,
    auth_required=True,              # Strict auth
    thermo_budget_multiplier=1.0,    # Full thermodynamic budget
    constitutional_floors=[f"F{i}" for i in range(1, 14)],  # All F1-F13
)

# =============================================================================
# PUBLIC AMBASSADOR (Horizon) - Public access, limited scope
# =============================================================================
HORIZON_CONFIG = EnvironmentConfig(
    mode=DeploymentMode.HORIZON_PUBLIC,
    name="arifOS Public Ambassador",
    base_url="https://arifos.fastmcp.app",
    vault_backend="external",        # External DB service
    memory_backend="external",       # External Redis
    rate_limit_enabled=True,
    auth_required=False,             # Public access (tools decide)
    thermo_budget_multiplier=0.5,    # Conservative budget
    constitutional_floors=[          # Core floors only
        "F1",  # Truth
        "F2",  # Evidence
        "F3",  # Uncertainty
        "F5",  # Empathy
        "F7",  # Humility
        "F9",  # Security (basic)
        "F12", # Audit
    ],
)

# =============================================================================
# LOCAL DEVELOPMENT
# =============================================================================
LOCAL_CONFIG = EnvironmentConfig(
    mode=DeploymentMode.LOCAL_DEV,
    name="arifOS Development",
    base_url="http://localhost:8080",
    vault_backend="sqlite",          # SQLite for local
    memory_backend="memory",         # In-memory
    rate_limit_enabled=False,
    auth_required=False,
    thermo_budget_multiplier=2.0,    # Relaxed for dev
    constitutional_floors=["F1", "F2", "F3"],  # Basic only
)


def get_environment() -> EnvironmentConfig:
    """
    Detect and return the current environment configuration.
    
    Detection order:
    1. ARIFOS_DEPLOYMENT env var
    2. Horizon-specific env vars
    3. VPS-specific files/vars
    4. Default to local
    """
    deployment = os.getenv("ARIFOS_DEPLOYMENT", "").lower()
    
    # Explicit configuration
    if deployment == "horizon":
        return HORIZON_CONFIG
    elif deployment == "vps":
        return VPS_CONFIG
    elif deployment == "local":
        return LOCAL_CONFIG
    
    # Auto-detection for Horizon
    if os.getenv("HORIZON_DEPLOYMENT") or os.getenv("PREFECT_CLOUD_API_URL"):
        return HORIZON_CONFIG
    
    # Auto-detection for VPS
    if os.path.exists("/etc/arifos-vps") or os.getenv("VPS_HOSTNAME"):
        return VPS_CONFIG
    
    # Default to local
    return LOCAL_CONFIG


def is_sovereign() -> bool:
    """Check if running in sovereign (VPS) mode."""
    return get_environment().mode == DeploymentMode.VPS_SOVEREIGN


def is_public() -> bool:
    """Check if running in public (Horizon) mode."""
    return get_environment().mode == DeploymentMode.HORIZON_PUBLIC


# =============================================================================
# Tool Visibility by Environment
# =============================================================================

TOOL_VISIBILITY = {
    # Core Trinity Tools - Available everywhere
    "init_anchor": ["vps", "horizon", "local"],
    "arifOS_kernel": ["vps", "horizon", "local"],
    "apex_soul": ["vps", "horizon", "local"],
    "vault_ledger": ["vps", "local"],  # Vault only on sovereign
    "agi_mind": ["vps", "horizon", "local"],
    "asi_heart": ["vps", "horizon", "local"],
    "engineering_memory": ["vps", "local"],  # Memory tools sovereign-only
    "physics_reality": ["vps", "horizon", "local"],
    "math_estimator": ["vps", "horizon", "local"],
    "code_engine": ["vps", "local"],  # Code execution sovereign-only
    "architect_registry": ["vps", "horizon", "local"],
    
    # Intelligence Tools - VPS only (sensitive)
    "reality_grounding": ["vps", "local"],
    "reality_dossier": ["vps", "local"],
    "constitutional_rag": ["vps", "local"],
    "vector_memory": ["vps", "local"],
    
    # Public Tools - Available on Horizon
    "search_web": ["vps", "horizon", "local"],
    "fetch_url": ["vps", "horizon", "local"],
    "get_current_time": ["vps", "horizon", "local"],
}


def is_tool_available(tool_name: str) -> bool:
    """Check if a tool should be available in current environment."""
    env = get_environment().mode.value
    allowed = TOOL_VISIBILITY.get(tool_name, ["vps", "local"])
    return env in allowed


# =============================================================================
# Environment-Specific Server Configuration
# =============================================================================

def get_server_config() -> dict:
    """Get FastMCP server configuration for current environment."""
    env = get_environment()
    
    base_config = {
        "name": env.name,
        "version": os.getenv("ARIFOS_VERSION", "2026.03.25"),
    }
    
    if env.mode == DeploymentMode.VPS_SOVEREIGN:
        base_config.update({
            "strict_input_validation": True,
            "mask_error_details": False,  # Full error details for debugging
            "on_duplicate_tools": "error",
        })
    
    elif env.mode == DeploymentMode.HORIZON_PUBLIC:
        base_config.update({
            "strict_input_validation": True,
            "mask_error_details": True,   # Hide internal errors
            "on_duplicate_tools": "warn",
        })
    
    return base_config
