"""
aclip_cai/console_tools.py
==========================

The 9-Sense Nervous System — Console Intelligence Implementation.

All tools are:
- Console-only (no ethics/ASI layer)
- Read-only (except forge_guard gating decisions)
- Fast (< 100ms response time target)
- Structured JSON output
- Fail-closed with explicit error envelopes

Design Principles:
------------------
1. No constitutional floors (these are infrastructure tools)
2. No emotional/empathy processing
3. Pure data retrieval and system inspection
4. Forge_guard is the only exception: it makes gating decisions
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import shutil
import subprocess
import time
from collections import defaultdict, deque
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# =============================================================================
# Shared Types and Utilities
# =============================================================================


@dataclass
class ToolResponse:
    """Standard response envelope for all ACLIP_CAI tools."""

    tool: str
    status: str  # "ok" | "error" | "warning"
    timestamp: str
    data: dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    latency_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _now() -> str:
    """ISO 8601 timestamp in UTC."""
    return datetime.now(timezone.utc).isoformat()


def _run_cmd(cmd: list[str], timeout: float = 5.0) -> tuple[str, str, int]:
    """Execute shell command with timeout. Returns (stdout, stderr, returncode)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", f"Command timed out after {timeout}s", 124
    except Exception as e:
        return "", str(e), 1


def _parse_size(size_str: str) -> int:
    """Parse human-readable size to bytes."""
    units = {"B": 1, "K": 1024, "M": 1024**2, "G": 1024**3, "T": 1024**4}
    size_str = size_str.strip().upper()
    for suffix, multiplier in units.items():
        if size_str.endswith(suffix):
            try:
                return int(float(size_str[:-1]) * multiplier)
            except ValueError:
                return 0
    try:
        return int(size_str)
    except ValueError:
        return 0


# =============================================================================
# Tool 1: system_health — System Resource Metrics
# =============================================================================


async def system_health(
    include_swap: bool = True,
    include_io: bool = False,
    include_temp: bool = False,
) -> ToolResponse:
    """
    Retrieve comprehensive system health metrics using psutil.
    """
    start = time.perf_counter()
    data: dict[str, Any] = {}

    try:
        import psutil

        # CPU Load
        cpu_cores = psutil.cpu_count() or 1
        # psutil.getloadavg() is not available on Windows
        if hasattr(psutil, "getloadavg"):
            load_avg = [x / cpu_cores * 100 for x in psutil.getloadavg()]
            data["cpu"] = {
                "load_1m": round(load_avg[0], 2),
                "load_5m": round(load_avg[1], 2),
                "load_15m": round(load_avg[2], 2),
            }
        else:
            data["cpu"] = {}

        data["cpu"]["usage_percent"] = psutil.cpu_percent(interval=1)
        data["cpu"]["cores"] = cpu_cores

        # Memory
        mem = psutil.virtual_memory()
        data["memory"] = {
            "total_bytes": mem.total,
            "available_bytes": mem.available,
            "used_bytes": mem.used,
            "usage_percent": mem.percent,
        }

        if include_swap:
            swap = psutil.swap_memory()
            data["memory"]["swap"] = {
                "total_bytes": swap.total,
                "free_bytes": swap.free,
                "used_bytes": swap.used,
                "usage_percent": swap.percent,
            }

        # Disk Usage
        data["disk"] = {}
        try:
            total_size = psutil.disk_usage("/")
            data["disk"]["root"] = {
                "total_bytes": total_size.total,
                "used_bytes": total_size.used,
                "free_bytes": total_size.free,
                "usage_percent": total_size.percent,
            }
        except FileNotFoundError:
            data["disk"]["root"] = {"error": "Root directory '/' not found."}

        if include_io:
            io = psutil.disk_io_counters()
            if io:
                data["disk"]["io_stats"] = {
                    "read_count": io.read_count,
                    "write_count": io.write_count,
                    "read_bytes": io.read_bytes,
                    "write_bytes": io.write_bytes,
                }

        if include_temp:
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    data["thermal"] = {
                        key: [
                            {
                                "label": s.label,
                                "current": s.current,
                                "high": s.high,
                                "critical": s.critical,
                            }
                            for s in sensors
                        ]
                        for key, sensors in temps.items()
                    }
            else:
                data["thermal"] = {"error": "sensors_temperatures not available on this platform"}

        # Uptime
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        data["uptime_seconds"] = round(uptime_seconds, 2)

        latency = (time.perf_counter() - start) * 1000
        return ToolResponse(
            tool="system_health",
            status="ok",
            timestamp=_now(),
            data=data,
            latency_ms=round(latency, 2),
        )

    except ImportError:
        return ToolResponse(
            tool="system_health",
            status="error",
            timestamp=_now(),
            error="psutil is not installed. Please install it with 'pip install psutil'",
            latency_ms=(time.perf_counter() - start) * 1000,
        )
    except Exception as e:
        latency = (time.perf_counter() - start) * 1000
        return ToolResponse(
            tool="system_health",
            status="error",
            timestamp=_now(),
            data={},
            error=str(e),
            latency_ms=round(latency, 2),
        )


# =============================================================================
# Tool 2: process_list — Process Inspection
# =============================================================================


async def process_list(
    filter_name: Optional[str] = None,
    filter_user: Optional[str] = None,
    min_cpu_percent: float = 0.0,
    min_memory_mb: float = 0.0,
    limit: int = 50,
    include_threads: bool = False,
) -> ToolResponse:
    """
    List and filter system processes using psutil.
    """
    start_time = time.perf_counter()
    processes = []

    try:
        import psutil

        for proc in psutil.process_iter(
            [
                "pid",
                "name",
                "username",
                "cpu_percent",
                "memory_percent",
                "memory_info",
                "status",
                "create_time",
                "cmdline",
            ]
        ):
            try:
                # Apply filters
                if filter_name and filter_name.lower() not in proc.info["name"].lower():
                    continue
                if filter_user and filter_user != proc.info["username"]:
                    continue
                if proc.info["cpu_percent"] < min_cpu_percent:
                    continue
                if (proc.info["memory_info"].rss / 1024 / 1024) < min_memory_mb:
                    continue

                proc_info = {
                    "pid": proc.info["pid"],
                    "name": proc.info["name"],
                    "command": " ".join(proc.info["cmdline"])[:200] if proc.info["cmdline"] else "",
                    "user": proc.info["username"],
                    "cpu_percent": proc.info["cpu_percent"],
                    "memory_percent": round(proc.info["memory_percent"], 2),
                    "memory_rss_mb": round(proc.info["memory_info"].rss / 1024 / 1024, 2),
                    "stat": proc.info["status"],
                    "started": datetime.fromtimestamp(proc.info["create_time"]).isoformat(),
                }

                if include_threads:
                    proc_info["threads"] = proc.num_threads()

                processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # Sort by CPU usage descending
        processes.sort(key=lambda p: p["cpu_percent"], reverse=True)
        processes = processes[:limit]

        latency = (time.perf_counter() - start_time) * 1000
        return ToolResponse(
            tool="process_list",
            status="ok",
            timestamp=_now(),
            data={
                "processes": processes,
                "total_count": len(processes),
                "filters_applied": {
                    "name": filter_name,
                    "user": filter_user,
                    "min_cpu_percent": min_cpu_percent,
                    "min_memory_mb": min_memory_mb,
                },
            },
            latency_ms=round(latency, 2),
        )
    except ImportError:
        return ToolResponse(
            tool="process_list",
            status="error",
            timestamp=_now(),
            error="psutil is not installed. Please install it with 'pip install psutil'",
            latency_ms=(time.perf_counter() - start_time) * 1000,
        )
    except Exception as e:
        latency = (time.perf_counter() - start_time) * 1000
        return ToolResponse(
            tool="process_list",
            status="error",
            timestamp=_now(),
            data={},
            error=str(e),
            latency_ms=round(latency, 2),
        )


# =============================================================================
# Tool 3: fs_inspect — Filesystem Inspection
# =============================================================================


async def fs_inspect(
    path: str = ".",
    depth: int = 1,
    max_depth: Optional[int] = None,
    include_hidden: bool = False,
    min_size_bytes: int = 0,
    pattern: Optional[str] = None,
    max_files: int = 100,
) -> ToolResponse:
    """
    Inspect filesystem structure and file metadata.

    Args:
        path: Root path to inspect
        depth: Maximum directory depth to traverse
        max_depth: Compatibility alias for depth
        include_hidden: Include hidden files (starting with .)
        min_size_bytes: Minimum file size to include
        pattern: Glob pattern to filter files (e.g., "*.py")
        max_files: Maximum files to return

    Returns:
        ToolResponse with file tree and metadata
    """
    start = time.perf_counter()
    files = []
    dirs = []

    try:
        root_path = Path(path).resolve()
        effective_depth = max_depth if max_depth is not None else depth

        if not root_path.exists():
            raise FileNotFoundError(f"Path not found: {path}")

        if not root_path.is_dir():
            # Single file inspection
            stat = root_path.stat()
            latency = (time.perf_counter() - start) * 1000
            return ToolResponse(
                tool="fs_inspect",
                status="ok",
                timestamp=_now(),
                data={
                    "path": str(root_path),
                    "type": "file",
                    "size_bytes": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                    "accessed": datetime.fromtimestamp(stat.st_atime, tz=timezone.utc).isoformat(),
                    "created": datetime.fromtimestamp(stat.st_ctime, tz=timezone.utc).isoformat(),
                    "permissions": oct(stat.st_mode)[-3:],
                },
                latency_ms=round(latency, 2),
            )

        # Directory traversal
        for item in root_path.rglob("*"):
            # Check depth
            try:
                rel_depth = len(item.relative_to(root_path).parts)
            except ValueError:
                continue

            if rel_depth > effective_depth:
                continue

            # Skip hidden
            if not include_hidden and any(part.startswith(".") for part in item.parts):
                continue

            # Apply pattern filter
            if pattern and not item.match(pattern):
                continue

            try:
                stat = item.stat()

                entry = {
                    "path": str(item),
                    "relative": str(item.relative_to(root_path)),
                    "depth": rel_depth,
                    "size_bytes": stat.st_size if item.is_file() else None,
                    "modified": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                    "permissions": oct(stat.st_mode)[-3:],
                }

                if item.is_dir():
                    dirs.append(entry)
                elif item.is_file():
                    if stat.st_size >= min_size_bytes:
                        files.append(entry)

                if len(files) + len(dirs) >= max_files:
                    break

            except (OSError, PermissionError):
                continue

        latency = (time.perf_counter() - start) * 1000
        return ToolResponse(
            tool="fs_inspect",
            status="ok",
            timestamp=_now(),
            data={
                "root": str(root_path),
                "directories": dirs,
                "files": files,
                "total_dirs": len(dirs),
                "total_files": len(files),
                "traversal_depth": effective_depth,
            },
            latency_ms=round(latency, 2),
        )

    except Exception as e:
        latency = (time.perf_counter() - start) * 1000
        return ToolResponse(
            tool="fs_inspect",
            status="error",
            timestamp=_now(),
            data={},
            error=str(e),
            latency_ms=round(latency, 2),
        )


# =============================================================================
# Tool 4: log_tail — Log File Monitoring
# =============================================================================


async def log_tail(
    log_file: str = "aaa_mcp.log",
    lines: int = 50,
    pattern: str = "",
    log_path: Optional[str] = None,
    follow: bool = False,
    grep_pattern: Optional[str] = None,
    since_minutes: Optional[int] = None,
) -> ToolResponse:
    """
    Tail and search log files.

    Args:
        log_file: Path to log file
        lines: Number of lines to retrieve
        pattern: Substring/regex filter for lines (compat with server API)
        log_path: Compatibility alias for log_file
        follow: Stream mode (not implemented for MCP, returns last N lines)
        grep_pattern: Filter lines matching pattern
        since_minutes: Only return lines from last N minutes

    Returns:
        ToolResponse with log entries
    """
    start = time.perf_counter()

    try:
        selected_path = log_path or log_file
        selected_pattern = grep_pattern if grep_pattern is not None else pattern
        path = Path(selected_path)
        if not path.exists():
            raise FileNotFoundError(f"Log file not found: {selected_path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {selected_path}")

        # Use tail command for efficiency
        cmd = ["tail", "-n", str(lines), str(path)]
        stdout, _, rc = _run_cmd(cmd, timeout=5.0)
        if rc == 0:
            log_lines = stdout.strip().split("\n") if stdout.strip() else []
        else:
            with path.open("r", encoding="utf-8", errors="ignore") as handle:
                log_lines = [line.rstrip("\n") for line in deque(handle, maxlen=lines)]

        # Apply grep filter
        if selected_pattern:
            try:
                regex = re.compile(selected_pattern, re.IGNORECASE)
                log_lines = [line for line in log_lines if regex.search(line)]
            except re.error as e:
                raise ValueError(f"Invalid regex pattern: {e}")

        # Parse log entries (common formats)
        parsed_entries = []
        for line in log_lines:
            entry = {
                "raw": line,
                "timestamp": None,
                "level": None,
                "message": line,
            }

            # Try to extract timestamp and log level
            # ISO format: 2026-02-13T09:30:00Z or 2026-02-13 09:30:00
            ts_match = re.search(
                r"(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)", line
            )
            if ts_match:
                entry["timestamp"] = ts_match.group(1)

            # Log level detection
            level_match = re.search(
                r"\b(DEBUG|INFO|WARNING|WARN|ERROR|CRITICAL|FATAL)\b", line, re.IGNORECASE
            )
            if level_match:
                entry["level"] = level_match.group(1).upper()

            parsed_entries.append(entry)

        # Time-window filter: keep entries with parseable timestamps within window.
        if since_minutes is not None:
            if since_minutes < 0:
                raise ValueError("since_minutes must be >= 0")

            cutoff_ts = datetime.now(timezone.utc).timestamp() - (since_minutes * 60)
            filtered_entries: list[dict[str, Any]] = []
            for entry in parsed_entries:
                ts_raw = entry.get("timestamp")
                if not ts_raw:
                    continue
                try:
                    normalized = ts_raw.replace("Z", "+00:00")
                    entry_ts = datetime.fromisoformat(normalized).timestamp()
                    if entry_ts >= cutoff_ts:
                        filtered_entries.append(entry)
                except ValueError:
                    continue
            parsed_entries = filtered_entries

        latency = (time.perf_counter() - start) * 1000
        return ToolResponse(
            tool="log_tail",
            status="ok",
            timestamp=_now(),
            data={
                "log_path": str(path),
                "lines_requested": lines,
                "lines_returned": len(parsed_entries),
                "entries": parsed_entries,
                "filters": {
                    "grep_pattern": selected_pattern,
                    "since_minutes": since_minutes,
                },
            },
            latency_ms=round(latency, 2),
        )

    except Exception as e:
        latency = (time.perf_counter() - start) * 1000
        return ToolResponse(
            tool="log_tail",
            status="error",
            timestamp=_now(),
            data={},
            error=str(e),
            latency_ms=round(latency, 2),
        )


# =============================================================================
# Tool 5: net_status — Network Diagnostics
# =============================================================================


async def net_status(
    check_ports: bool = True,
    check_connections: bool = True,
    check_interfaces: bool = True,
    check_routing: bool = True,
    target_host: Optional[str] = None,
) -> ToolResponse:
    """
    Network connectivity and interface status.

    Args:
        check_ports: Include listening/open ports
        check_connections: Include active socket connections
        check_interfaces: Include network interface status
        check_connections: Include active connections
        check_routing: Include routing table
        target_host: Optional host to ping test

    Returns:
        ToolResponse with network status
    """
    start = time.perf_counter()
    data = {}

    try:
        # Network interfaces
        if check_interfaces:
            interfaces = {}
            net_dev_path = Path("/proc/net/dev")
            if net_dev_path.exists():
                with open(net_dev_path, "r") as f:
                    for line in f:
                        if ":" in line and not line.strip().startswith("Inter"):
                            parts = line.strip().split(":")
                            iface = parts[0].strip()
                            stats = parts[1].split()
                            if len(stats) >= 9:
                                interfaces[iface] = {
                                    "rx_bytes": int(stats[0]),
                                    "rx_packets": int(stats[1]),
                                    "rx_errors": int(stats[2]),
                                    "tx_bytes": int(stats[8]),
                                    "tx_packets": int(stats[9]),
                                    "tx_errors": int(stats[10]) if len(stats) > 10 else 0,
                                }
            data["interfaces"] = interfaces

        # Open/listening ports
        if check_ports:
            stdout, _, rc = _run_cmd(["ss", "-tuln"], timeout=3.0)
            if rc != 0:
                stdout, _, rc = _run_cmd(["netstat", "-an"], timeout=3.0)
            if rc == 0:
                ports = []
                lines = stdout.strip().split("\n")
                for line in lines[1:]:
                    parts = line.split()
                    if len(parts) >= 4:
                        local_addr = (
                            parts[4]
                            if parts[0].startswith("tcp")
                            else parts[3] if len(parts) > 3 else ""
                        )
                        ports.append(
                            {
                                "protocol": parts[0],
                                "state": parts[1] if len(parts) > 1 else None,
                                "local": local_addr,
                            }
                        )
                data["ports"] = ports[:50]

        # Active connections
        if check_connections:
            stdout, _, rc = _run_cmd(["ss", "-tan"], timeout=3.0)
            if rc != 0:
                stdout, _, rc = _run_cmd(["netstat", "-an"], timeout=3.0)
            if rc == 0:
                connections = []
                for line in stdout.strip().split("\n")[1:]:  # Skip header
                    parts = line.split()
                    if len(parts) >= 4:
                        connections.append(
                            {
                                "protocol": parts[0],
                                "state": parts[1] if len(parts) > 1 else None,
                                "recv_q": parts[2] if len(parts) > 2 else None,
                                "send_q": parts[3] if len(parts) > 3 else None,
                                "local": parts[4] if len(parts) > 4 else None,
                                "peer": parts[5] if len(parts) > 5 else None,
                            }
                        )
                data["connections"] = connections[:20]  # Limit output

        # Routing table
        if check_routing:
            stdout, _, rc = _run_cmd(["ip", "route"], timeout=2.0)
            if rc != 0:
                stdout, _, rc = _run_cmd(["route", "print"], timeout=2.0)
            if rc == 0:
                routes = []
                for line in stdout.strip().split("\n"):
                    parts = line.split()
                    if "via" in parts:
                        idx = parts.index("via")
                        routes.append(
                            {
                                "destination": parts[0],
                                "gateway": parts[idx + 1] if idx + 1 < len(parts) else None,
                                "dev": parts[parts.index("dev") + 1] if "dev" in parts else None,
                            }
                        )
                data["routing"] = routes

        # Ping test
        if target_host:
            stdout, _, rc = _run_cmd(["ping", "-c", "3", "-W", "2", target_host], timeout=8.0)
            if rc != 0:
                stdout, _, rc = _run_cmd(["ping", "-n", "3", target_host], timeout=8.0)
            data["ping_test"] = {
                "target": target_host,
                "success": rc == 0,
                "output": stdout[-500:] if stdout else None,  # Last 500 chars
            }

        data["summary"] = {
            "ports_count": len(data.get("ports", [])),
            "connections_count": len(data.get("connections", [])),
            "interfaces_count": len(data.get("interfaces", {})),
            "routing_count": len(data.get("routing", [])),
        }

        latency = (time.perf_counter() - start) * 1000
        return ToolResponse(
            tool="net_status",
            status="ok",
            timestamp=_now(),
            data=data,
            latency_ms=round(latency, 2),
        )

    except Exception as e:
        latency = (time.perf_counter() - start) * 1000
        return ToolResponse(
            tool="net_status",
            status="error",
            timestamp=_now(),
            data={},
            error=str(e),
            latency_ms=round(latency, 2),
        )


# =============================================================================
# Tool 6: config_flags — Configuration Inspection
# =============================================================================


async def config_flags(
    config_path: Optional[str] = None,
    env_prefix: Optional[str] = "ARIFOS",
    include_secrets: bool = False,
) -> ToolResponse:
    """
    Inspect configuration files and environment variables.

    Args:
        config_path: Path to config file (.json, .yaml, .env)
        env_prefix: Filter environment variables by prefix
        include_secrets: Mask secrets if False (recommended)

    Returns:
        ToolResponse with configuration data
    """
    start = time.perf_counter()
    data: dict[str, Any] = {"files": {}, "environment": {}}

    try:

        def _is_sensitive_key(key: str) -> bool:
            lowered = key.lower()
            return any(s in lowered for s in ["key", "secret", "pass", "token", "pwd"])

        def _masked_value(key: str, value: str) -> str:
            if include_secrets or not _is_sensitive_key(key):
                return value
            return "***masked***"

        def _detect_repo_root() -> Path:
            env_root = os.environ.get("ARIFOS_ROOT")
            if env_root:
                return Path(env_root).resolve()
            cwd = Path.cwd().resolve()
            for candidate in [cwd] + list(cwd.parents):
                if (candidate / "pyproject.toml").exists():
                    return candidate
            return cwd

        # Parse config file
        if config_path:
            path = Path(config_path)
            if path.exists():
                content = path.read_text(encoding="utf-8", errors="ignore")
                suffix = path.suffix.lower()

                if suffix == ".json":
                    data["files"][str(path)] = json.loads(content)
                elif suffix in (".yaml", ".yml"):
                    try:
                        import yaml

                        data["files"][str(path)] = yaml.safe_load(content)
                    except ImportError:
                        data["files"][str(path)] = {"raw": content[:2000]}
                elif suffix == ".env":
                    env_vars = {}
                    for line in content.split("\n"):
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, _, value = line.partition("=")
                            env_vars[key] = _masked_value(key, value)
                    data["files"][str(path)] = env_vars
                elif suffix == ".toml":
                    try:
                        import tomllib

                        data["files"][str(path)] = tomllib.loads(content)
                    except Exception:
                        data["files"][str(path)] = {
                            "note": "TOML parse failed",
                            "size_bytes": len(content.encode("utf-8")),
                        }
                else:
                    # Never expose raw contents for unknown file types by default.
                    data["files"][str(path)] = {
                        "note": "unsupported file type",
                        "suffix": suffix or None,
                        "size_bytes": len(content.encode("utf-8")),
                    }
            else:
                data["files"][str(path)] = {"error": "file_not_found"}

        # Environment variables
        if env_prefix:
            for key, value in os.environ.items():
                if key.startswith(env_prefix):
                    data["environment"][key] = _masked_value(key, value)

        # Check for common config files in arifOS/root
        arifos_root = _detect_repo_root()
        common_configs = [
            "pyproject.toml",
            ".env",
            "requirements.txt",
            "railway.toml",
        ]
        detected: list[str] = []
        for cfg in common_configs:
            cfg_path = arifos_root / cfg
            if cfg_path.exists() and str(cfg_path) != str(config_path or ""):
                detected.append(str(cfg_path))
        data["files"]["detected"] = detected

        mode = (
            os.environ.get("ARIFOS_MODE")
            or os.environ.get("ARIFOS_GOVERNANCE_MODE")
            or (
                "LAB"
                if os.environ.get("ARIFOS_LAB_MODE", "").lower() in {"1", "true", "yes"}
                else "HARD"
            )
        )
        feature_flags = {
            key: _masked_value(key, value)
            for key, value in os.environ.items()
            if key.startswith("ARIFOS_FEATURE_")
        }
        data["governance"] = {
            "mode": mode,
            "mode_source": "env",
            "feature_flags": feature_flags,
            "repo_root": str(arifos_root),
        }

        latency = (time.perf_counter() - start) * 1000
        return ToolResponse(
            tool="config_flags",
            status="ok",
            timestamp=_now(),
            data=data,
            latency_ms=round(latency, 2),
        )

    except Exception as e:
        latency = (time.perf_counter() - start) * 1000
        return ToolResponse(
            tool="config_flags",
            status="error",
            timestamp=_now(),
            data={},
            error=str(e),
            latency_ms=round(latency, 2),
        )


# =============================================================================
# Tool 7: chroma_query — Vector Database Search
# =============================================================================


async def chroma_query(
    query_text: str,
    collection_name: str = "default",
    n_results: int = 5,
    where_filter: Optional[dict] = None,
    include_embeddings: bool = False,
) -> ToolResponse:
    """
    Query ChromaDB vector store for semantic search.

    Args:
        query_text: Text to search for
        collection_name: ChromaDB collection name
        n_results: Number of results to return
        where_filter: Optional metadata filter (ChromaDB where clause)
        include_embeddings: Include vector embeddings in output

    Returns:
        ToolResponse with semantic search results
    """
    start = time.perf_counter()

    try:
        try:
            import chromadb
        except ImportError:
            # Fallback: simulate results for development
            return ToolResponse(
                tool="chroma_query",
                status="warning",
                timestamp=_now(),
                data={
                    "note": "ChromaDB not installed. Running in simulation mode.",
                    "query": query_text,
                    "collection": collection_name,
                    "results": [],
                },
                latency_ms=round((time.perf_counter() - start) * 1000, 2),
            )

        # Initialize ChromaDB client
        chroma_path = os.environ.get("CHROMA_PERSIST_DIR", "/root/arifOS/.chroma")
        client = chromadb.PersistentClient(path=chroma_path)

        # Get or create collection
        try:
            collection = client.get_collection(collection_name)
        except Exception:
            return ToolResponse(
                tool="chroma_query",
                status="error",
                timestamp=_now(),
                data={"query": query_text, "collection": collection_name},
                error=f"Collection '{collection_name}' not found",
                latency_ms=round((time.perf_counter() - start) * 1000, 2),
            )

        # Query
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where_filter,
            include=["metadatas", "documents", "distances"]
            + (["embeddings"] if include_embeddings else []),
        )

        # Format results
        formatted_results = []
        if results["ids"] and results["ids"][0]:
            for i, doc_id in enumerate(results["ids"][0]):
                result_item = {
                    "id": doc_id,
                    "document": results["documents"][0][i] if results["documents"] else None,
                    "distance": results["distances"][0][i] if results["distances"] else None,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else None,
                }
                if include_embeddings and results.get("embeddings"):
                    result_item["embedding"] = results["embeddings"][0][i]
                formatted_results.append(result_item)

        latency = (time.perf_counter() - start) * 1000
        return ToolResponse(
            tool="chroma_query",
            status="ok",
            timestamp=_now(),
            data={
                "query": query_text,
                "collection": collection_name,
                "results_count": len(formatted_results),
                "results": formatted_results,
            },
            latency_ms=round(latency, 2),
        )

    except Exception as e:
        latency = (time.perf_counter() - start) * 1000
        return ToolResponse(
            tool="chroma_query",
            status="error",
            timestamp=_now(),
            data={},
            error=str(e),
            latency_ms=round(latency, 2),
        )


# =============================================================================
# Tool 8: cost_estimator — Resource Cost Projection
# =============================================================================


async def cost_estimator(
    action_description: str = "",
    estimated_cpu_percent: float = 0.0,
    estimated_ram_mb: float = 0.0,
    estimated_io_mb: float = 0.0,
    operation_type: str = "compute",
    token_count: Optional[int] = None,
    compute_seconds: Optional[float] = None,
    storage_gb: Optional[float] = None,
    api_calls: Optional[int] = None,
    provider: str = "openai",
    model: str = "gpt-4",
) -> ToolResponse:
    """
    Estimate costs for AI operations and infrastructure usage.

    Args:
        action_description: Free-form action description for C7 output
        estimated_cpu_percent: Estimated CPU usage percentage
        estimated_ram_mb: Estimated RAM usage in MB
        estimated_io_mb: Estimated I/O impact in MB
        operation_type: Type of operation (llm, embedding, storage, compute)
        token_count: Number of tokens (input + output)
        compute_seconds: Compute time in seconds
        storage_gb: Storage usage in GB
        api_calls: Number of API calls
        provider: LLM provider (openai, anthropic, gemini, etc.)
        model: Model name for pricing

    Returns:
        ToolResponse with cost breakdown
    """
    start = time.perf_counter()

    # Pricing tables (USD) - updated periodically
    PRICING = {
        "openai": {
            "gpt-4": {"input_per_1k": 0.03, "output_per_1k": 0.06},
            "gpt-4-turbo": {"input_per_1k": 0.01, "output_per_1k": 0.03},
            "gpt-3.5-turbo": {"input_per_1k": 0.0005, "output_per_1k": 0.0015},
            "text-embedding-3-small": {"per_1k": 0.00002},
            "text-embedding-3-large": {"per_1k": 0.00013},
        },
        "anthropic": {
            "claude-3-opus": {"input_per_1k": 0.015, "output_per_1k": 0.075},
            "claude-3-sonnet": {"input_per_1k": 0.003, "output_per_1k": 0.015},
            "claude-3-haiku": {"input_per_1k": 0.00025, "output_per_1k": 0.00125},
        },
        "gemini": {
            "gemini-pro": {"input_per_1k": 0.0005, "output_per_1k": 0.0015},
            "gemini-ultra": {"input_per_1k": 0.001, "output_per_1k": 0.003},
        },
    }

    # Infrastructure costs (approximate)
    INFRA_COSTS = {
        "compute_per_hour": 0.05,  # $0.05/hour for modest VM
        "storage_per_gb_month": 0.02,  # $0.02/GB/month
        "egress_per_gb": 0.09,  # $0.09/GB egress
    }

    try:
        costs = {
            "llm_cost_usd": 0.0,
            "compute_cost_usd": 0.0,
            "storage_cost_usd": 0.0,
            "api_cost_usd": 0.0,
            "total_usd": 0.0,
        }

        breakdown = {}

        # LLM cost calculation
        if operation_type == "llm" and token_count:
            provider_pricing = PRICING.get(provider, {})
            model_pricing = provider_pricing.get(
                model, {"input_per_1k": 0.01, "output_per_1k": 0.03}
            )

            # Assume 70/30 input/output split
            input_tokens = int(token_count * 0.7)
            output_tokens = int(token_count * 0.3)

            input_cost = (input_tokens / 1000) * model_pricing.get("input_per_1k", 0.01)
            output_cost = (output_tokens / 1000) * model_pricing.get("output_per_1k", 0.03)

            costs["llm_cost_usd"] = round(input_cost + output_cost, 6)
            breakdown["llm"] = {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "input_cost": round(input_cost, 6),
                "output_cost": round(output_cost, 6),
            }

        # Embedding cost
        elif operation_type == "embedding" and token_count:
            provider_pricing = PRICING.get(provider, {})
            model_pricing = provider_pricing.get(model, {"per_1k": 0.00002})
            costs["llm_cost_usd"] = round(
                (token_count / 1000) * model_pricing.get("per_1k", 0.00002), 6
            )
            breakdown["embedding"] = {"tokens": token_count}

        # Compute cost
        if compute_seconds:
            hours = compute_seconds / 3600
            costs["compute_cost_usd"] = round(hours * INFRA_COSTS["compute_per_hour"], 6)
            breakdown["compute"] = {"seconds": compute_seconds, "hours": round(hours, 4)}

        # Storage cost
        if storage_gb:
            costs["storage_cost_usd"] = round(storage_gb * INFRA_COSTS["storage_per_gb_month"], 6)
            breakdown["storage"] = {"gb": storage_gb}

        # API cost (generic rate)
        if api_calls:
            costs["api_cost_usd"] = round(api_calls * 0.0001, 6)  # $0.0001 per call estimate
            breakdown["api"] = {"calls": api_calls}

        costs["total_usd"] = round(
            costs["llm_cost_usd"]
            + costs["compute_cost_usd"]
            + costs["storage_cost_usd"]
            + costs["api_cost_usd"],
            6,
        )

        # C7 thermodynamic cost proxy (0..1)
        cpu_score = max(0.0, min(1.0, estimated_cpu_percent / 100.0))
        ram_score = max(0.0, min(1.0, estimated_ram_mb / 8192.0))
        io_score = max(0.0, min(1.0, estimated_io_mb / 2048.0))
        thermo_score = round((0.5 * cpu_score) + (0.3 * ram_score) + (0.2 * io_score), 4)
        if thermo_score >= 0.8:
            risk_band = "red"
        elif thermo_score >= 0.5:
            risk_band = "amber"
        else:
            risk_band = "green"

        latency = (time.perf_counter() - start) * 1000
        return ToolResponse(
            tool="cost_estimator",
            status="ok",
            timestamp=_now(),
            data={
                "action_description": action_description,
                "operation_type": operation_type,
                "provider": provider,
                "model": model,
                "costs": costs,
                "breakdown": breakdown,
                "resource_estimate": {
                    "estimated_cpu_percent": estimated_cpu_percent,
                    "estimated_ram_mb": estimated_ram_mb,
                    "estimated_io_mb": estimated_io_mb,
                },
                "thermodynamic": {
                    "cost_score": thermo_score,
                    "risk_band": risk_band,
                },
                "note": "Estimates are approximate. Actual costs may vary.",
            },
            latency_ms=round(latency, 2),
        )

    except Exception as e:
        latency = (time.perf_counter() - start) * 1000
        return ToolResponse(
            tool="cost_estimator",
            status="error",
            timestamp=_now(),
            data={},
            error=str(e),
            latency_ms=round(latency, 2),
        )


# =============================================================================
# Tool 9: forge_guard — Gating Decisions (Write-Enabled)
# =============================================================================


async def forge_guard(
    check_system_health: bool = True,
    cost_score_threshold: float = 0.8,
    cost_score_to_check: float = 0.0,
    action: str = "",
    target: str = "",
    session_id: str = "",
    risk_level: str = "low",  # low | medium | high | critical
    justification: str = "",
    dry_run: bool = True,
    require_approval: bool = False,
) -> ToolResponse:
    """
    Forge guard — local circuit breaker for ACLIP_CAI.

    Evaluates gating decisions for actions that could modify system state.
    This is the integration point with aaa-mcp 9-law pipeline.

    Args:
        check_system_health: Include host pressure checks from C0
        cost_score_threshold: Threshold for SABAR/hold gate
        cost_score_to_check: Caller-provided C7 score
        action: Action to evaluate (deploy, modify, delete, execute)
        target: Target resource (path, service, config)
        session_id: aaa-mcp session ID for correlation
        risk_level: Assessed risk level
        justification: Reason for the action
        dry_run: If True, only evaluate without executing
        require_approval: If True, mandate human approval

    Returns:
        ToolResponse with local gate outcome (OK/SABAR/VOID_LOCAL)
    """
    start = time.perf_counter()

    try:
        gate = "OK"
        reason_code = "CLEAR"
        can_proceed = True

        # Optional host-pressure check
        host_hot = False
        host_signals: dict[str, Any] = {}
        if check_system_health:
            health = await system_health(include_swap=True, include_io=False, include_temp=False)
            if health.status == "ok":
                load_1m = float(health.data.get("cpu", {}).get("load_1m", 0))
                cores = int(health.data.get("cpu", {}).get("cores", 1)) or 1
                mem_pct = float(health.data.get("memory", {}).get("usage_percent", 0))
                host_signals = {
                    "load_1m": load_1m,
                    "cores": cores,
                    "memory_usage_percent": mem_pct,
                }
                host_hot = (load_1m / cores) > 1.5 or mem_pct > 90.0

        if host_hot:
            gate = "SABAR"
            reason_code = "HOST_HOT"
            can_proceed = False

        if cost_score_to_check >= cost_score_threshold and gate != "VOID_LOCAL":
            gate = "SABAR"
            reason_code = "COST_THRESHOLD_EXCEEDED"
            can_proceed = False

        # Risk-based gate evaluation
        GATE_THRESHOLDS = {
            "low": {"auto_approve": True, "max_scope": "single_file"},
            "medium": {"auto_approve": False, "max_scope": "directory"},
            "high": {"auto_approve": False, "max_scope": "service"},
            "critical": {"auto_approve": False, "max_scope": None},
        }

        threshold = GATE_THRESHOLDS.get(risk_level, GATE_THRESHOLDS["critical"])

        # Elevate based on explicit risk gate
        if risk_level in {"high", "critical"} or require_approval:
            if gate == "OK":
                gate = "SABAR"
                reason_code = "RISK_REVIEW_REQUIRED"
                can_proceed = False

        # Check for forbidden patterns
        forbidden_patterns = [
            r"rm\s+-rf\s+/",
            r"dd\s+if=.*\s+of=/dev/",
            r"mkfs\.",
            r">\s*/etc/passwd",
            r":(){ :|: & };:",  # Fork bomb
        ]

        # F12 Hardened Logic: Check all input surfaces
        scan_surfaces = f"{action} {target} {justification} {session_id}"

        danger_detected = False
        for pattern in forbidden_patterns:
            if re.search(pattern, scan_surfaces, re.IGNORECASE | re.VERBOSE):
                danger_detected = True
                gate = "VOID_LOCAL"
                reason_code = "FORBIDDEN_PATTERN_DETECTED"
                can_proceed = False
                break

        # F6 Empathy: Critical Target Protection
        if not danger_detected:
            critical_targets = [
                r"\.env",
                r"id_rsa",
                r"\.ssh",
                r"production",
                r"database",
                r"master\.key",
            ]
            for pattern in critical_targets:
                if re.search(pattern, target, re.IGNORECASE):
                    if risk_level not in ("high", "critical") or not require_approval:
                        gate = "SABAR"
                        reason_code = "CRITICAL_TARGET_NEEDS_APPROVAL"
                        can_proceed = False

        # Legacy alias for downstream compatibility
        verdict_alias = {
            "OK": "SEAL",
            "SABAR": "SABAR",
            "VOID_LOCAL": "VOID",
        }[gate]

        latency = (time.perf_counter() - start) * 1000
        return ToolResponse(
            tool="forge_guard",
            status="ok",
            timestamp=_now(),
            data={
                "gate": gate,
                "reason_code": reason_code,
                "action": action,
                "target": target,
                "session_id": session_id,
                "risk_level": risk_level,
                "can_proceed": can_proceed,
                "dry_run": dry_run,
                "danger_detected": danger_detected,
                "cost_score_threshold": cost_score_threshold,
                "cost_score_to_check": cost_score_to_check,
                "host_signals": host_signals,
                "approval_required": not threshold["auto_approve"] or require_approval,
                "justification": justification,
                "verdict": verdict_alias,
                "recommendations": (
                    [
                        "Review target scope before execution",
                        "Ensure backup is available",
                        "Test in non-production environment first",
                    ]
                    if risk_level in ("high", "critical")
                    else []
                ),
            },
            latency_ms=round(latency, 2),
        )

    except Exception as e:
        latency = (time.perf_counter() - start) * 1000
        return ToolResponse(
            tool="forge_guard",
            status="error",
            timestamp=_now(),
            data={},
            error=str(e),
            latency_ms=round(latency, 2),
        )
