"""
Sandbox Runner — F1 Amanah Containerized Execution

Executes shell commands in disposable, restricted containers.
Prevents host VPS compromise even if malicious commands execute.

Usage:
    runner = SandboxRunner()
    exit_code, stdout, stderr = await runner.execute(
        command="ls -la",
        workspace=Path("/usr/src/app/docs"),
    )

DITEMPA BUKAN DIBERI | F1 Amanah | F12 Defense
"""

from __future__ import annotations

import asyncio
import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class SandboxResult:
    """Result from sandbox execution."""

    exit_code: int
    stdout: str
    stderr: str
    command: str
    workspace: Path
    duration_ms: float
    sandbox_id: str | None = None


class SandboxRunner:
    """
    F1 Amanah: Execute commands in disposable sandbox containers.

    All filesystem mutations are contained within the sandbox.
    Even CRITICAL commands can only damage the sandbox, not the host VPS.
    """

    DEFAULT_IMAGE = "alpine:3.19"
    DEFAULT_MEMORY = "256m"
    DEFAULT_CPUS = "0.5"
    DEFAULT_TIMEOUT = 60
    DEFAULT_PIDS_LIMIT = 64

    def __init__(
        self,
        image: str | None = None,
        memory_limit: str | None = None,
        cpu_limit: str | None = None,
        pids_limit: int | None = None,
        timeout: int | None = None,
        network_mode: str = "none",
    ):
        self.image = image or self.DEFAULT_IMAGE
        self.memory_limit = memory_limit or self.DEFAULT_MEMORY
        self.cpu_limit = cpu_limit or self.DEFAULT_CPUS
        self.pids_limit = pids_limit or self.DEFAULT_PIDS_LIMIT
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.network_mode = network_mode

        # Validate Docker is available
        self._docker_available = self._check_docker()

    def _check_docker(self) -> bool:
        """Check if Docker is available for sandbox execution."""
        try:
            result = subprocess.run(
                ["docker", "version", "--format", "{{.Server.Version}}"],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            logger.warning("Docker not available, sandbox execution disabled")
            return False

    async def execute(
        self,
        command: str,
        workspace: Path,
        env_vars: dict[str, str] | None = None,
        timeout: int | None = None,
    ) -> SandboxResult:
        """
        Execute command in disposable sandbox container.

        Args:
            command: Shell command to execute
            workspace: Host directory to mount into sandbox
            env_vars: Environment variables for sandbox
            timeout: Execution timeout (seconds)

        Returns:
            SandboxResult with exit code, stdout, stderr

        Raises:
            SandboxError: If sandbox execution fails
            TimeoutError: If command exceeds timeout
        """
        import time

        start_time = time.time()
        timeout = timeout or self.timeout

        if not self._docker_available:
            raise SandboxError(
                "Docker not available. " "Install Docker or set use_sandbox=False in eureka_forge"
            )

        # Validate workspace exists
        workspace = Path(workspace).resolve()
        if not workspace.exists():
            raise SandboxError(f"Workspace does not exist: {workspace}")

        # Build docker run command with security restrictions
        docker_cmd = [
            "docker",
            "run",
            "--rm",
            # Network isolation (F12 Defense)
            "--network",
            self.network_mode,
            # Privilege restriction (F1 Amanah)
            "--cap-drop=ALL",
            # Read-only root filesystem
            "--read-only",
            # Resource limits (F7 Humility)
            f"--memory={self.memory_limit}",
            f"--cpus={self.cpu_limit}",
            f"--pids-limit={self.pids_limit}",
            # Prevent privilege escalation
            "--security-opt=no-new-privileges:true",
            # Mount workspace
            "-v",
            f"{workspace}:/workspace:rw",
            "-w",
            "/workspace",
        ]

        # Add environment variables if provided
        if env_vars:
            for key, value in env_vars.items():
                docker_cmd.extend(["-e", f"{key}={value}"])

        # Add image and command
        docker_cmd.extend([self.image, "sh", "-c", command])

        logger.info(f"Sandbox execution: {command[:100]}...")

        try:
            # Execute with asyncio for non-blocking
            proc = await asyncio.create_subprocess_exec(
                *docker_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            # Wait with timeout
            try:
                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(),
                    timeout=timeout,
                )
            except asyncio.TimeoutError:
                proc.kill()
                raise TimeoutError(f"Sandbox execution timed out after {timeout}s")

            duration_ms = (time.time() - start_time) * 1000

            return SandboxResult(
                exit_code=proc.returncode or 0,
                stdout=stdout.decode("utf-8", errors="replace"),
                stderr=stderr.decode("utf-8", errors="replace"),
                command=command,
                workspace=workspace,
                duration_ms=duration_ms,
            )

        except asyncio.TimeoutError:
            logger.error(f"Sandbox timeout: {command[:100]}...")
            raise
        except Exception as e:
            logger.error(f"Sandbox execution failed: {e}")
            raise SandboxError(f"Sandbox execution failed: {e}")

    async def execute_direct(
        self,
        command: str,
        working_dir: Path,
        timeout: int | None = None,
    ) -> SandboxResult:
        """
        Execute command directly (fallback, no sandbox).

        ⚠️ Only use this when sandbox is explicitly disabled.
        ⚠️ This bypasses F1 Amanah container isolation.
        """
        import time

        start_time = time.time()
        timeout = timeout or self.timeout

        logger.warning(f"DIRECT execution (no sandbox): {command[:100]}...")

        try:
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(working_dir),
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(),
                    timeout=timeout,
                )
            except asyncio.TimeoutError:
                proc.kill()
                raise TimeoutError(f"Direct execution timed out after {timeout}s")

            duration_ms = (time.time() - start_time) * 1000

            return SandboxResult(
                exit_code=proc.returncode or 0,
                stdout=stdout.decode("utf-8", errors="replace"),
                stderr=stderr.decode("utf-8", errors="replace"),
                command=command,
                workspace=Path(working_dir),
                duration_ms=duration_ms,
            )

        except Exception as e:
            logger.error(f"Direct execution failed: {e}")
            raise SandboxError(f"Direct execution failed: {e}")


class SandboxError(Exception):
    """Error during sandbox execution."""

    pass


# Global runner instance
_sandbox_runner: SandboxRunner | None = None


def get_sandbox_runner() -> SandboxRunner:
    """Get or create global sandbox runner instance."""
    global _sandbox_runner
    if _sandbox_runner is None:
        _sandbox_runner = SandboxRunner()
    return _sandbox_runner


async def execute_in_sandbox(
    command: str,
    workspace: Path | str,
    **kwargs,
) -> SandboxResult:
    """Convenience function for one-off sandbox execution."""
    runner = get_sandbox_runner()
    return await runner.execute(
        command=command,
        workspace=Path(workspace),
        **kwargs,
    )
