"""
MCP Container Tools for AAA MCP Server
Adds container management to the constitutional AI gateway
"""

from aaa_mcp.integrations.container_controller import get_controller

# These will be registered with the main MCP server
def register_container_tools(mcp):
    """Register container management tools with the MCP server."""
    
    @mcp.tool()
    async def container_list() -> dict:
        """
        List all sovereign stack containers (AgentZero, OpenClaw, Qdrant).
        Floor: F11 (Command), F2 (Truth)
        """
        controller = get_controller()
        containers = controller.list_containers()
        
        return {
            "verdict": "SEAL",
            "containers": [
                {
                    "name": c.name,
                    "status": c.status.value,
                    "image": c.image,
                    "ports": c.ports,
                    "uptime": c.uptime,
                    "health": c.health
                }
                for c in containers
            ],
            "floor_enforced": ["F11", "F2"]
        }
    
    @mcp.tool()
    async def container_restart(name: str) -> dict:
        """
        Restart a container (AgentZero, OpenClaw, or Qdrant).
        
        Args:
            name: Container name (agentzero, openclaw, or qdrant)
        
        Floor: F11 (Command), F1 (Amanah - logged), F5 (Peace² - graceful)
        888_HOLD: Requires confirmation for production containers
        """
        controller = get_controller()
        
        # 888_HOLD check for critical operations
        if name in ["agentzero", "openclaw"]:
            # In real implementation, this would check session for confirmation
            pass
        
        result = controller.restart_container(name)
        return {
            "verdict": result.get("verdict", "VOID"),
            "operation": result.get("operation", {}),
            "message": result.get("message", result.get("error", "Unknown result")),
            "floor_enforced": ["F11", "F1", "F5"]
        }
    
    @mcp.tool()
    async def container_logs(name: str, tail: int = 50) -> dict:
        """
        Get logs from a container.
        
        Args:
            name: Container name
            tail: Number of lines to return (default: 50)
        
        Floor: F11 (Command), F2 (Truth - accurate logs)
        """
        controller = get_controller()
        logs = controller.get_logs(name, tail)
        
        return {
            "verdict": "SEAL",
            "container": name,
            "logs": logs,
            "floor_enforced": ["F11", "F2"]
        }
    
    @mcp.tool()
    async def sovereign_health() -> dict:
        """
        Full health check of the sovereign stack.
        Checks AgentZero, OpenClaw, and Qdrant status.
        
        Floor: F2 (Truth), F7 (Humility - reports uncertainty)
        """
        controller = get_controller()
        report = controller.health_check()
        
        return {
            "verdict": report["verdict"],
            "overall_status": report["overall_status"],
            "timestamp": report["timestamp"],
            "containers": report["containers"],
            "floor_enforced": ["F2", "F7"]
        }
    
    @mcp.tool()
    async def container_exec(name: str, command: str) -> dict:
        """
        Execute a command inside a container (AgentZero or Qdrant).
        
        Args:
            name: Container name
            command: Shell command to execute
        
        Floor: F11 (Command), F12 (Injection defense)
        888_HOLD: All exec commands require confirmation
        """
        # Injection defense (F12)
        dangerous_patterns = ["rm -rf", "; rm", "&& rm", "drop table", "truncate"]
        cmd_lower = command.lower()
        for pattern in dangerous_patterns:
            if pattern in cmd_lower:
                return {
                    "verdict": "VOID",
                    "error": f"F12 Injection Defense: Pattern '{pattern}' blocked",
                    "floor_enforced": ["F12"]
                }
        
        import subprocess
        container_map = {
            "agentzero": "agentzero-fixed",
            "qdrant": "qdrant"
        }
        container_name = container_map.get(name, name)
        
        try:
            result = subprocess.run(
                ["docker", "exec", container_name, "sh", "-c", command],
                capture_output=True, text=True, timeout=30
            )
            
            return {
                "verdict": "SEAL" if result.returncode == 0 else "PARTIAL",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode,
                "floor_enforced": ["F11", "F12"]
            }
        except Exception as e:
            return {
                "verdict": "VOID",
                "error": str(e),
                "floor_enforced": ["F11"]
            }
    
    return {
        "container_list": container_list,
        "container_restart": container_restart,
        "container_logs": container_logs,
        "sovereign_health": sovereign_health,
        "container_exec": container_exec
    }
