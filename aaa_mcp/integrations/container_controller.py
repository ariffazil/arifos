"""
Container Controller Integration for arifOS
Manages Docker containers via AAA MCP with Constitutional governance
"""

import json
import subprocess
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional



class ContainerStatus(Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"
    UNKNOWN = "unknown"


@dataclass
class ContainerInfo:
    name: str
    status: ContainerStatus
    image: str
    ports: str
    health: Optional[str]
    uptime: str


class ContainerController:
    """
    Constitutional container controller.
    All operations are logged and reversible (F1 Amanah).
    """

    # Sovereign Stack containers
    MANAGED_CONTAINERS = {
        "agentzero": {
            "container_name": "agentzero-fixed",
            "type": "docker",
            "ports": [50001],
            "volumes": ["/opt/agent-zero-data:/a0", "/var/run/docker.sock:/var/run/docker.sock"],
            "privileged": True,
        },
        "qdrant": {
            "container_name": "qdrant",
            "type": "docker",
            "ports": [6333, 6334],
            "volumes": ["/root/agent-zero_data/qdrant_storage:/qdrant/storage"],
            "privileged": False,
        },
        "openclaw": {
            "container_name": None,  # Host process
            "type": "host",
            "ports": [18789],
            "process_name": "openclaw-gateway",
            "systemd_service": "openclaw",
        },
    }

    def __init__(self):
        self.operation_log = []
        self._cache = {}
        self._cache_ttl = 5  # seconds

    def _get_cached(self, key: str) -> Optional[List[ContainerInfo]]:
        """Get cached result if still valid."""
        if key in self._cache:
            result, timestamp = self._cache[key]
            if time.time() - timestamp < self._cache_ttl:
                return result
        return None

    def _set_cached(self, key: str, value: List[ContainerInfo]):
        """Cache result with timestamp."""
        self._cache[key] = (value, time.time())

    def list_containers(self) -> List[ContainerInfo]:
        """List all sovereign stack containers with caching."""
        # Check cache first
        cached = self._get_cached("containers")
        if cached is not None:
            return cached

        containers = []
        """List all sovereign stack containers."""
        containers = []

        # Get Docker containers
        try:
            result = subprocess.run(
                ["docker", "ps", "-a", "--format", "json"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                data = json.loads(line)
                name = data.get("Names", "")
                if name in [
                    c["container_name"]
                    for c in self.MANAGED_CONTAINERS.values()
                    if c.get("container_name")
                ]:
                    containers.append(
                        ContainerInfo(
                            name=name,
                            status=(
                                ContainerStatus.RUNNING
                                if data.get("State") == "running"
                                else ContainerStatus.STOPPED
                            ),
                            image=data.get("Image", "unknown"),
                            ports=data.get("Ports", ""),
                            health=data.get("Health", "unknown"),
                            uptime=data.get("Status", ""),
                        )
                    )
        except Exception as e:
            containers.append(
                ContainerInfo(
                    name="docker_error",
                    status=ContainerStatus.ERROR,
                    image="",
                    ports="",
                    health=str(e),
                    uptime="",
                )
            )

        # Check OpenClaw host process
        try:
            result = subprocess.run(
                ["pgrep", "-f", "openclaw-gateway"], capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                containers.append(
                    ContainerInfo(
                        name="openclaw-host",
                        status=ContainerStatus.RUNNING,
                        image="openclaw-gateway",
                        ports="127.0.0.1:18789",
                        health="healthy",
                        uptime="host process",
                    )
                )
        except Exception:
            pass

        # Cache the result
        self._set_cached("containers", containers)
        return containers

    def restart_container(self, name: str) -> Dict:
        """Restart a container with F1 logging."""
        config = self.MANAGED_CONTAINERS.get(name)
        if not config:
            return {"verdict": "VOID", "error": f"Unknown container: {name}"}

        container_name = config.get("container_name", name)

        # Log operation (F1 Amanah)
        operation = {
            "action": "restart",
            "target": name,
            "container": container_name,
            "timestamp": subprocess.check_output(["date", "-Iseconds"]).decode().strip(),
        }

        try:
            if config["type"] == "docker":
                result = subprocess.run(
                    ["docker", "restart", container_name],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                success = result.returncode == 0
            else:
                # Host process - restart via systemd or direct
                result = subprocess.run(
                    ["pkill", "-f", config.get("process_name", name)],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                success = True  # OpenClaw auto-restarts via PM2/systemd

            operation["success"] = success
            self.operation_log.append(operation)

            return {
                "verdict": "SEAL" if success else "VOID",
                "operation": operation,
                "message": f"{'✅' if success else '❌'} {name} restart {'complete' if success else 'failed'}",
            }

        except Exception as e:
            operation["error"] = str(e)
            self.operation_log.append(operation)
            return {"verdict": "VOID", "operation": operation, "error": str(e)}

    def get_logs(self, name: str, tail: int = 50) -> str:
        """Get container logs."""
        config = self.MANAGED_CONTAINERS.get(name)
        if not config:
            return f"Unknown container: {name}"

        container_name = config.get("container_name", name)

        try:
            if config["type"] == "docker":
                result = subprocess.run(
                    ["docker", "logs", "--tail", str(tail), container_name],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                return result.stdout or result.stderr or "No logs"
            else:
                # Host process - use journalctl or log files
                result = subprocess.run(
                    [
                        "journalctl",
                        "-u",
                        config.get("systemd_service", name),
                        "-n",
                        str(tail),
                        "--no-pager",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                return result.stdout or "Check /root/.openclaw/logs/"
        except Exception as e:
            return f"Error getting logs: {e}"

    def health_check(self) -> Dict:
        """Full sovereign stack health check."""
        containers = self.list_containers()

        report = {
            "timestamp": subprocess.check_output(["date", "-Iseconds"]).decode().strip(),
            "overall_status": "HEALTHY",
            "containers": [],
            "verdict": "SEAL",
        }

        for c in containers:
            status = "🟢" if c.status == ContainerStatus.RUNNING else "🔴"
            report["containers"].append(
                {
                    "name": c.name,
                    "status": c.status.value,
                    "icon": status,
                    "ports": c.ports,
                    "uptime": c.uptime,
                }
            )
            if c.status != ContainerStatus.RUNNING:
                report["overall_status"] = "DEGRADED"
                report["verdict"] = "PARTIAL"

        return report


# Singleton instance
_controller = None


def get_controller() -> ContainerController:
    global _controller
    if _controller is None:
        _controller = ContainerController()
    return _controller
