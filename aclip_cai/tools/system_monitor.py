"""
aclip_cai/tools/system_monitor.py — System Health Sensor

ACLIP Console tool: gives AI agents clean JSON system metrics.
Replaces ad-hoc PowerShell scripts with structured, queryable output.
"""

from __future__ import annotations

import platform
import subprocess
from typing import Any


def get_resource_usage() -> dict[str, Any]:
    """Return current RAM, CPU, and disk usage as structured JSON."""
    try:
        import psutil

        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("C:\\")
        cpu = psutil.cpu_percent(interval=0.5)

        return {
            "status": "SEAL",
            "ram": {
                "total_gb": round(mem.total / 1e9, 1),
                "used_gb": round(mem.used / 1e9, 1),
                "free_gb": round(mem.available / 1e9, 1),
                "percent": mem.percent,
            },
            "cpu": {
                "percent": cpu,
                "cores": psutil.cpu_count(logical=False),
                "logical": psutil.cpu_count(logical=True),
            },
            "disk_c": {
                "total_gb": round(disk.total / 1e9, 1),
                "used_gb": round(disk.used / 1e9, 1),
                "free_gb": round(disk.free / 1e9, 1),
                "percent": disk.percent,
            },
            "platform": platform.system(),
        }
    except ImportError:
        return _fallback_wmi_usage()


def list_processes(filter_name: str = "", top_n: int = 15) -> dict[str, Any]:
    """Return top processes by RAM usage as structured JSON."""
    try:
        import psutil

        procs = []
        for p in psutil.process_iter(["pid", "name", "memory_info", "cpu_percent"]):
            try:
                info = p.info
                name = info["name"] or ""
                if filter_name and filter_name.lower() not in name.lower():
                    continue
                mem_mb = round((info["memory_info"].rss if info["memory_info"] else 0) / 1e6, 1)
                procs.append({
                    "pid": info["pid"],
                    "name": name,
                    "ram_mb": mem_mb,
                    "cpu_pct": round(info["cpu_percent"] or 0, 1),
                })
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
        return {"status": "PARTIAL", "error": "psutil not installed", "hint": "uv pip install psutil"}


def get_system_health() -> dict[str, Any]:
    """Combined health report: resources + top RAM consumers + warnings."""
    usage = get_resource_usage()
    procs = list_processes(top_n=10)

    warnings = []
    if usage.get("ram", {}).get("percent", 0) > 85:
        warnings.append(f"HIGH RAM: {usage['ram']['percent']}% used")
    if usage.get("disk_c", {}).get("percent", 0) > 88:
        warnings.append(f"HIGH DISK: {usage['disk_c']['percent']}% used")
    if usage.get("cpu", {}).get("percent", 0) > 80:
        warnings.append(f"HIGH CPU: {usage['cpu']['percent']}%")

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
            capture_output=True, text=True, timeout=10
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
                "percent": round((disk_total - disk_free) / disk_total * 100, 1) if disk_total else 0,
            },
            "platform": "Windows",
        }
    except Exception as e:
        return {"status": "VOID", "error": str(e), "hint": "Install psutil: uv pip install psutil"}
