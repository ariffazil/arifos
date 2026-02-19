import psutil


def cost_estimator(
    action_description: str,
    estimated_cpu_percent: float = 0,
    estimated_ram_mb: float = 0,
    estimated_io_mb: float = 0,
) -> dict:
    """
    Predicts the thermodynamic resource cost of a proposed action.

    This serves as a proxy for entropy change (ΔS) and is used
    for F4 (Clarity) and F8 (Genius) floor calculations.

    Args:
        action_description (str): Description of the action.
        estimated_cpu_percent (float): Estimated usage (0-100 per core).
        estimated_ram_mb (float): RAM usage in MB.
        estimated_io_mb (float): I/O usage in MB.

    Returns:
        dict: Cost breakdown and risk band.
    """

    # WEIGHTS (Review periodically via 'aclip_cai analyze')
    WEIGHT_CPU = 0.5
    WEIGHT_RAM = 0.3
    WEIGHT_IO = 0.2

    # DYNAMIC CALIBRATION (F2 Truth)
    # We scale '100%' to the actual hardware reality.
    # psutil.cpu_count(logical=True) returns the number of threads.
    # e.g., on a 16-thread machine, Max CPU is 1600%.
    logical_cores = psutil.cpu_count(logical=True) or 1
    MAX_CPU_PERCENT = 100.0 * logical_cores

    # RAM and IO are harder to get dynamic max for without expensive calls,
    # so we keep reasonable defaults or try to get total physical memory.
    try:
        total_ram = psutil.virtual_memory().total / (1024 * 1024)  # MB
        MAX_RAM_MB = total_ram
    except Exception:
        MAX_RAM_MB = 16384.0  # Fallback to 16GB if lookup fails

    MAX_IO_MB = 1000.0  # 1GB throughput baseline

    # Normalization
    norm_cpu = min(estimated_cpu_percent / MAX_CPU_PERCENT, 1.0)
    norm_ram = min(estimated_ram_mb / MAX_RAM_MB, 1.0)
    norm_io = min(estimated_io_mb / MAX_IO_MB, 1.0)

    # Calculate weighted score (0.0 - 1.0)
    cost_score = (norm_cpu * WEIGHT_CPU) + (norm_ram * WEIGHT_RAM) + (norm_io * WEIGHT_IO)

    # Risk Banding (The "Pain Threshold")
    if cost_score > 0.8:
        risk_band = "CRITICAL"
    elif cost_score > 0.6:
        risk_band = "HIGH"
    elif cost_score > 0.3:
        risk_band = "MEDIUM"
    else:
        risk_band = "LOW"

    return {
        "action_description": action_description,
        "estimated_cost_score": round(cost_score, 4),
        "risk_band": risk_band,
        "hardware_context": {
            "cores": logical_cores,
            "max_cpu_percent": MAX_CPU_PERCENT,
            "total_ram_mb": round(MAX_RAM_MB, 0),
        },
        "details": {
            "cpu_normalized": round(norm_cpu, 4),
            "ram_normalized": round(norm_ram, 4),
            "io_normalized": round(norm_io, 4),
        },
    }
