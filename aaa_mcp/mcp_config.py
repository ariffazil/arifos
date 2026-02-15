"""
arifOS MCP Server Integration Configuration
Maps 9 external MCP servers to constitutional governance layer
"""
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class TrinityComponent(Enum):
    AGI = "Δ"  # Mind/Logic
    ASI = "Ω"  # Heart/Care  
    APEX = "Ψ"  # Crown/Law

@dataclass
class MCPServerConfig:
    """Configuration for an MCP server with constitutional mapping"""
    name: str
    description: str
    trinity: TrinityComponent
    floors: List[str]
    atomic_action: str
    omega_threshold: float  # Ω₀ uncertainty limit
    reversible: bool  # F1 Amanah compliance
    package_name: Optional[str] = None
    
# arifOS MCP Server Registry
MCP_SERVERS = {
    "filesystem": MCPServerConfig(
        name="MCP Filesystem Server",
        description="Secure file operations with configurable access controls",
        trinity=TrinityComponent.APEX,
        floors=["F1", "F3"],
        atomic_action="VAULT999",
        omega_threshold=0.04,
        reversible=True,
        package_name="@modelcontextprotocol/server-filesystem"
    ),
    
    "memory": MCPServerConfig(
        name="MCP Memory Server",
        description="Knowledge graph-based persistent memory",
        trinity=TrinityComponent.ASI,
        floors=["F2", "F7"],
        atomic_action="Memory Weaver (#9)",
        omega_threshold=0.05,
        reversible=True,
        package_name="@modelcontextprotocol/server-memory"
    ),
    
    "fetch": MCPServerConfig(
        name="MCP Fetch Server",
        description="Web content fetching with safety filtering",
        trinity=TrinityComponent.AGI,
        floors=["F2", "F4"],
        atomic_action="Geo-Radar (#4)",
        omega_threshold=0.06,
        reversible=False,  # External data fetch
        package_name="@modelcontextprotocol/server-fetch"
    ),
    
    "everything": MCPServerConfig(
        name="MCP Everything Server",
        description="Reference/test server for validation",
        trinity=TrinityComponent.APEX,
        floors=["F3", "F8"],
        atomic_action="Peace² Auditor (#2)",
        omega_threshold=0.03,
        reversible=True,
        package_name="@modelcontextprotocol/server-everything"
    ),
    
    "git": MCPServerConfig(
        name="MCP Git Server",
        description="Git repository tools with version control",
        trinity=TrinityComponent.AGI,
        floors=["F1", "F2", "F3"],
        atomic_action="PyPI Sentinel (#3)",
        omega_threshold=0.04,
        reversible=True,
        package_name="@modelcontextprotocol/server-git"
    ),
    
    "time": MCPServerConfig(
        name="MCP Time Server",
        description="Time and timezone conversion",
        trinity=TrinityComponent.ASI,
        floors=["F6", "F4"],
        atomic_action="Meeting Metabolizer (#6)",
        omega_threshold=0.02,
        reversible=True,
        package_name="@modelcontextprotocol/server-time"
    ),
    
    "sequential-thinking": MCPServerConfig(
        name="MCP Sequential Thinking Server",
        description="Dynamic reflective problem-solving",
        trinity=TrinityComponent.ASI,
        floors=["F5", "F7", "F9"],
        atomic_action="ASI Align/Reason",
        omega_threshold=0.05,
        reversible=True,
        package_name="@modelcontextprotocol/server-sequential-thinking"
    ),

    "brave-search": MCPServerConfig(
        name="MCP Brave Search Server",
        description="Privacy-focused web search",
        trinity=TrinityComponent.AGI,
        floors=["F2", "F8"],
        atomic_action="Reality Search",
        omega_threshold=0.06,
        reversible=False,
        package_name="@modelcontextprotocol/server-brave-search"
    ),
}

def get_server_config(name: str) -> Optional[MCPServerConfig]:
    """Get MCP server configuration by name"""
    return MCP_SERVERS.get(name)

def list_servers_by_trinity(component: TrinityComponent) -> List[MCPServerConfig]:
    """List all MCP servers mapped to a Trinity component"""
    return [s for s in MCP_SERVERS.values() if s.trinity == component]

def validate_constitutional_compliance(server_name: str, omega: float) -> bool:
    """Check if operation meets constitutional Ω₀ threshold"""
    config = get_server_config(server_name)
    if not config:
        return False
    return omega <= config.omega_threshold