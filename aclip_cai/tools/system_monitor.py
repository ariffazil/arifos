"""
aclip_cai/tools/system_monitor.py — System Health Sensor

ACLIP Console tool: gives AI agents clean JSON system metrics.
Replaces ad-hoc PowerShell scripts with structured, queryable output.
"""

from __future__ import annotations

import platform
import subprocess
import os
from typing import Any


def get_resource_usage() -> dict[str, Any]:
    """Return current RAM, CPU, and disk usage as structured JSON."""
    try:
        import psutil

        mem = psutil.virtual_memory()
        root_path = os.path.abspath(os.sep)
        disk = psutil.disk_usage(root_path)
        cpu_percent = psutil.cpu_percent(interval=0.5)
        net_io = psutil.net_io_counters()
        disk_io = psutil.disk_io_counters()

        # CPU load average (Not available on Windows)
        try:
            cpu_load = psutil.getloadavg()
        except AttributeError:
            cpu_load = (0, 0, 0)  # Graceful fallback for Windows

        return {
            "status": "SEAL",
            "ram": {
                "total_gb": round(mem.total / 1e9, 1),
                "used_gb": round(mem.used / 1e9, 1),
                "free_gb": round(mem.available / 1e9, 1),
                "percent": mem.percent,
            },
            "cpu": {
                "percent": cpu_percent,
                "cores": psutil.cpu_count(logical=False),
                "logical": psutil.cpu_count(logical=True),
                "load_avg_1m": cpu_load[0],
                "load_avg_5m": cpu_load[1],
                "load_avg_15m": cpu_load[2],
            },
            "disk_c": {
                "total_gb": round(disk.total / 1e9, 1),
                "used_gb": round(disk.used / 1e9, 1),
                "free_gb": round(disk.free / 1e9, 1),
                "percent": disk.percent,
            },
            "io": {
                "network": {
                    "bytes_sent_gb": round(net_io.bytes_sent / 1e9, 2),
                    "bytes_recv_gb": round(net_io.bytes_recv / 1e9, 2),
                    "packets_sent_m": round(net_io.packets_sent / 1e6, 1),
                    "packets_recv_m": round(net_io.packets_recv / 1e6, 1),
                },
                "disk": {
                    "read_count_m": round(disk_io.read_count / 1e6, 1),
                    "write_count_m": round(disk_io.write_count / 1e6, 1),
                    "read_gb": round(disk_io.read_bytes / 1e9, 2),
                    "write_gb": round(disk_io.write_bytes / 1e9, 2),
                },
            },
            "platform": platform.system(),
        }
    except ImportError:
        return _fallback_wmi_usage()


def list_processes(filter_name: str = "", top_n: int = 15) -> dict[str, Any]:
    """Return top processes by RAM usage as structured JSON."""
    try:
        import psutil
        import time

        procs = []
        for p in psutil.process_iter(
            ["pid", "name", "memory_info", "cpu_percent", "username", "create_time"]
        ):
            try:
                info = p.info
                name = info["name"] or ""
                if filter_name and filter_name.lower() not in name.lower():
                    continue

                mem_mb = round((info["memory_info"].rss if info["memory_info"] else 0) / 1e6, 1)

                # Calculate age
                age_seconds = time.time() - info["create_time"]
                if age_seconds < 60:
                    age = f"{int(age_seconds)}s"
                elif age_seconds < 3600:
                    age = f"{int(age_seconds / 60)}m"
                else:
                    age = f"{int(age_seconds / 3600)}h"

                procs.append(
                    {
                        "pid": info["pid"],
                        "name": name,
                        "ram_mb": mem_mb,
                        "cpu_pct": round(info["cpu_percent"] or 0, 1),
                        "user": info["username"],
                        "age": age,
                    }
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        procs.sort(key=lambda x: x["ram_mb"], reverse=True)
        return {
            "status": "SEAL",
            "filter": filter_name or "(all)",
            "count": len(procs[:top_n]),
            "processes": procs[:top_n],
        }
    except ImportError:
        return {
            "status": "PARTIAL",
            "error": "psutil not installed",
            "hint": "uv pip install psutil",
        }


def get_system_health() -> dict[str, Any]:
    """Combined health report: resources + top RAM consumers + warnings."""
    usage = get_resource_usage()
    procs = list_processes(top_n=10)

    warnings = []
    if usage.get("ram", {}).get("percent", 0) > 85:
        warnings.append(f"HIGH RAM: {usage['ram']['percent']}% used")
    if usage.get("disk_c", {}).get("percent", 0) > 88:
        warnings.append(f"HIGH DISK: {usage['disk_c']['percent']}% used (C:\\)")
    if usage.get("cpu", {}).get("percent", 0) > 80:
        warnings.append(f"HIGH CPU: {usage['cpu']['percent']}%")

    # New warnings based on added metrics
    if usage.get("cpu", {}).get("load_avg_1m", 0) > psutil.cpu_count(logical=True) * 0.9:
        warnings.append(f"HIGH CPU LOAD (1m): {usage['cpu']['load_avg_1m']}")

    if usage.get("io", {}).get("network", {}).get("bytes_recv_gb", 0) > 10:  # Example threshold
        warnings.append(f"HIGH NET RX: {usage['io']['network']['bytes_recv_gb']}GB received")
    if usage.get("io", {}).get("network", {}).get("bytes_sent_gb", 0) > 10:  # Example threshold
        warnings.append(f"HIGH NET TX: {usage['io']['network']['bytes_sent_gb']}GB sent")

    if usage.get("io", {}).get("disk", {}).get("write_gb", 0) > 5:  # Example threshold
        warnings.append(f"HIGH DISK WRITE: {usage['io']['disk']['write_gb']}GB written")
    if usage.get("io", {}).get("disk", {}).get("read_gb", 0) > 5:  # Example threshold
        warnings.append(f"HIGH DISK READ: {usage['io']['disk']['read_gb']}GB read")

    return {
        "status": "SEAL" if not warnings else "PARTIAL",
        "warnings": warnings,
        "resources": usage,
        "top_processes": procs.get("processes", []),
    }


def _fallback_wmi_usage() -> dict[str, Any]:
    """PowerShell-based fallback for Windows when psutil is unavailable."""
    script = (
        "$mem = Get-WmiObject Win32_OperatingSystem; "
        "$disk = Get-WmiObject Win32_LogicalDisk -Filter \"DeviceID='C:'\"; "
        "$cpu = (Get-WmiObject Win32_Processor).LoadPercentage; "
        "Write-Output (ConvertTo-Json @{"
        "  ram_total=[math]::Round($mem.TotalVisibleMemorySize/1MB,1);"
        "  ram_free=[math]::Round($mem.FreePhysicalMemory/1MB,1);"
        "  disk_free=[math]::Round($disk.FreeSpace/1GB,1);"
        "  disk_total=[math]::Round($disk.Size/1GB,1);"
        "  cpu=$cpu"
        "})"
    )
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
            capture_output=True,
            text=True,
            timeout=10,
        )
        import json

        data = json.loads(result.stdout.strip())
        ram_total = data.get("ram_total", 0)
        ram_free = data.get("ram_free", 0)
        disk_total = data.get("disk_total", 0)
        disk_free = data.get("disk_free", 0)
        return {
            "status": "SEAL",
            "source": "wmi_fallback",
            "ram": {
                "total_gb": ram_total,
                "free_gb": ram_free,
                "used_gb": round(ram_total - ram_free, 1),
                "percent": round((ram_total - ram_free) / ram_total * 100, 1) if ram_total else 0,
            },
            "cpu": {"percent": data.get("cpu", 0)},
            "disk_c": {
                "total_gb": disk_total,
                "free_gb": disk_free,
                "used_gb": round(disk_total - disk_free, 1),
                "percent": (
                    round((disk_total - disk_free) / disk_total * 100, 1) if disk_total else 0
                ),
            },
            "platform": "Windows",
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "VOID",
            "error": "PowerShell command timed out.",
            "hint": "Check PowerShell or system responsiveness.",
        }
    except json.JSONDecodeError:
        return {
            "status": "VOID",
            "error": "Failed to parse PowerShell output JSON.",
            "hint": "PowerShell script output might be malformed.",
        }
    except Exception as e:
        return {"status": "VOID", "error": str(e), "hint": "Install psutil: uv pip install psutil"}
