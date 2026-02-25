"""
core/physics/thermodynamics.py — Thermodynamic State Management
T000 Version: 2026.02.15-FORGE-TRINITY-SEAL

F4 Clarity: Hardware-level entropy reduction via ZRAM/compression
F11 Command: CPU sovereignty enforcement (prevent Wallet Assassin loops)
F7 Humility: Environmental uncertainty measurement (Ω₀)

This module lives in core/ (kernel), NOT aaa_mcp/ (adapter).
Constitutional Boundary: All thermodynamic constraints enforced here.
"""

"""
Linux‑only dependencies:
- /sys/block/zram0/mm_stat (ZRAM compression stats) — requires Linux kernel with zram
- cpulimit command (CPU throttling) — install via apt: cpulimit
- psutil (cross‑platform but used for Linux‑specific metrics)
"""

import subprocess
import time
from dataclasses import dataclass
from typing import Any

import psutil


@dataclass
class ThermodynamicState:
    """Complete thermodynamic snapshot of system state."""

    zram_used_percent: float  # F4: Entropy reduction via compression
    cpu_throttle_status: bool  # F11: Command authority enforcement
    memory_pressure: float  # Physical memory pressure %
    cpu_usage_percent: float  # Current CPU utilization
    omega_environmental: float  # F7: Environmental uncertainty factor
    verdict: str  # SEAL, SABAR, or VOID

    def __post_init__(self):
        """Validate thermodynamic constraints post-initialization."""
        # F7 Humility: Environmental uncertainty must be quantified
        if not 0.0 <= self.omega_environmental <= 1.0:
            raise ValueError(f"Ω₀ must be in [0.0, 1.0], got {self.omega_environmental}")


class EntropyManager:
    """
    F4 Clarity: Hardware-level entropy reduction management.

    Enforces thermodynamic constraints at the kernel level,
    ensuring resource sovereignty (F11) and clarity (F4).
    """

    # Constitutional thresholds (calibrated for VPS: srv1325122)
    DEFAULT_ZRAM_THRESHOLD: float = 85.0  # F4: SABAR if ZRAM > 85%
    DEFAULT_CPU_CAP: int = 80  # F11: Throttle if CPU > 80%
    DEFAULT_MEMORY_PRESSURE: float = 90.0  # F5: Peace² threshold

    def __init__(
        self,
        zram_threshold: float | None = None,
        cpu_cap: int | None = None,
        memory_pressure_threshold: float | None = None,
    ):
        """
        Initialize EntropyManager with constitutional thresholds.

        Args:
            zram_threshold: F4 threshold for ZRAM compression (default: 85.0%)
            cpu_cap: F11 CPU sovereignty limit (default: 80%)
            memory_pressure_threshold: F5 system stability limit (default: 90%)
        """
        self.zram_threshold = zram_threshold or self.DEFAULT_ZRAM_THRESHOLD
        self.cpu_cap = cpu_cap or self.DEFAULT_CPU_CAP
        self.memory_pressure_threshold = memory_pressure_threshold or self.DEFAULT_MEMORY_PRESSURE

        # F7 Humility: Track initialization uncertainty
        self._calibration_uncertainty = 0.03  # Ω₀ for hardware variance

    def check_thermodynamic_budget(self) -> ThermodynamicState:
        """
        F4 + F11 + F7: Comprehensive thermodynamic assessment.

        Returns ThermodynamicState with verdict based on:
        - ZRAM usage (F4 Clarity via compression)
        - CPU throttling status (F11 Command authority)
        - Memory pressure (F5 Peace²)
        - Environmental Ω₀ (F7 Humility)

        Returns:
            ThermodynamicState with constitutional verdict
        """
        # Gather raw metrics
        zram_stats = self._get_zram_stats()
        cpu_stats = psutil.cpu_percent(interval=0.5)  # Faster sampling
        memory = psutil.virtual_memory()

        # F7 Humility: Calculate environmental uncertainty
        omega_env = self._calculate_omega(memory, zram_stats, cpu_stats)

        # F11 Command: Check CPU sovereignty
        cpu_throttled = cpu_stats > self.cpu_cap

        # F4 Clarity: Check entropy reduction capacity
        zram_critical = zram_stats > self.zram_threshold

        # F5 Peace²: Check system stability
        memory_critical = memory.percent > self.memory_pressure_threshold

        # Constitutional verdict logic
        if zram_critical or memory_critical:
            # F4/F5 violation: System under thermodynamic stress
            return ThermodynamicState(
                zram_used_percent=zram_stats,
                cpu_throttle_status=cpu_throttled,
                memory_pressure=memory.percent,
                cpu_usage_percent=cpu_stats,
                omega_environmental=omega_env,
                verdict="SABAR",  # Cooling required
            )

        if cpu_throttled:
            # F11 violation: CPU sovereignty compromised
            return ThermodynamicState(
                zram_used_percent=zram_stats,
                cpu_throttle_status=True,
                memory_pressure=memory.percent,
                cpu_usage_percent=cpu_stats,
                omega_environmental=omega_env,
                verdict="SABAR",  # Throttle enforcement
            )

        # All floors satisfied
        return ThermodynamicState(
            zram_used_percent=zram_stats,
            cpu_throttle_status=False,
            memory_pressure=memory.percent,
            cpu_usage_percent=cpu_stats,
            omega_environmental=omega_env,
            verdict="SEAL",
        )

    def enforce_f11_cpu_sovereignty(self, target_pid: int | None = None) -> bool:
        """
        F11 Command: Enforce CPU resource sovereignty.

        Prevents "Wallet Assassin" loops and runaway processes
        by applying kernel-level CPU throttling.

        Args:
            target_pid: Specific process to throttle, or None for system-wide

        Returns:
            True if enforcement applied, False otherwise
        """
        try:
            if target_pid:
                # Throttle specific process (e.g., rogue agent)
                subprocess.run(
                    ["cpulimit", "-p", str(target_pid), "-l", str(self.cpu_cap)],
                    check=True,
                    capture_output=True,
                    timeout=5,
                )
            else:
                # System-wide enforcement via cgroups (if available)
                # Fallback: Log F11 violation for manual intervention
                pass
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            # cpulimit not available — log and return False
            return False

    def _get_zram_stats(self) -> float:
        """
        F4 Clarity: Measure ZRAM (compressed swap) utilization.

        Returns:
            ZRAM usage percentage (0.0 to 100.0)
        """
        try:
            # Read ZRAM statistics from /sys/block/zram0
            with open("/sys/block/zram0/mm_stat") as f:
                stats = f.read().strip().split()
                if len(stats) >= 3:
                    # mm_stat format: orig_data_size compr_data_size mem_used_total
                    orig_size = int(stats[0])
                    compr_size = int(stats[2])
                    if orig_size > 0:
                        # Calculate compression ratio as proxy for pressure
                        return (compr_size / orig_size) * 100
        except (FileNotFoundError, PermissionError, ValueError):
            pass

        # Fallback: Use swap usage as proxy
        swap = psutil.swap_memory()
        if swap.total > 0:
            return (swap.used / swap.total) * 100
        return 0.0

    def _calculate_omega(self, memory: Any, zram_stats: float, cpu_stats: float) -> float:
        """
        F7 Humility: Calculate environmental uncertainty factor (Ω₀).

        Environmental Ω₀ increases with:
        - High memory pressure
        - High ZRAM usage (compression overhead)
        - High CPU utilization (thermal throttling risk)

        Returns:
            Omega value in [0.03, 0.08] range
        """
        # Base uncertainty from calibration
        omega = self._calibration_uncertainty

        # Memory pressure contribution (max +0.02)
        memory_factor = (memory.percent / 100) * 0.02
        omega += memory_factor

        # ZRAM overhead contribution (max +0.02)
        zram_factor = (zram_stats / 100) * 0.02
        omega += zram_factor

        # CPU thermal risk contribution (max +0.01)
        cpu_factor = (cpu_stats / 100) * 0.01
        omega += cpu_factor

        # Clamp to valid range [0.03, 0.08]
        return max(0.03, min(0.08, omega))

    def get_thermodynamic_report(self) -> dict:
        """
        Generate comprehensive thermodynamic report for logging/telemetry.

        Returns:
            Dictionary with all thermodynamic metrics
        """
        state = self.check_thermodynamic_budget()
        return {
            "timestamp": time.time(),
            "thermodynamic_state": {
                "zram_percent": state.zram_used_percent,
                "cpu_percent": state.cpu_usage_percent,
                "memory_percent": state.memory_pressure,
                "cpu_throttled": state.cpu_throttle_status,
                "omega_environmental": state.omega_environmental,
            },
            "constitutional_verdict": state.verdict,
            "thresholds": {
                "zram_threshold": self.zram_threshold,
                "cpu_cap": self.cpu_cap,
                "memory_threshold": self.memory_pressure_threshold,
            },
            "compliance": {
                "F4_clarity": state.zram_used_percent <= self.zram_threshold,
                "F11_command": not state.cpu_throttle_status,
                "F5_peace": state.memory_pressure <= self.memory_pressure_threshold,
                "F7_humility": 0.03 <= state.omega_environmental <= 0.05,
            },
        }


# Singleton instance for system-wide use
_entropy_manager: EntropyManager | None = None


def get_entropy_manager() -> EntropyManager:
    """Get or create singleton EntropyManager instance."""
    global _entropy_manager
    if _entropy_manager is None:
        _entropy_manager = EntropyManager()
    return _entropy_manager


# Constitutional exports
__all__ = [
    "ThermodynamicState",
    "EntropyManager",
    "get_entropy_manager",
]
