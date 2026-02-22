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
        action_description (str): A description of the action to be estimated.
        estimated_cpu_percent (float): Estimated CPU usage percentage (0-100).
        estimated_ram_mb (float): Estimated RAM usage in megabytes.
        estimated_io_mb (float): Estimated I/O usage in megabytes.

    Returns:
        dict: A dictionary containing the cost breakdown and a final score.
    """

    # These weights are arbitrary and should be tuned based on system profiling
    # and the relative importance of each resource.
    WEIGHT_CPU = 0.5
    WEIGHT_RAM = 0.3
    WEIGHT_IO = 0.2

    # Normalize inputs to a 0-1 scale. Max values are rough estimates and
    # should be configured based on the host system's capacity.
    # For now, let's assume a "standard" dev machine.
    MAX_CPU_PERCENT = 100.0  # A single core
    MAX_RAM_MB = 2048.0  # 2GB
    MAX_IO_MB = 500.0  # 500MB for a heavy operation

    norm_cpu = min(estimated_cpu_percent / MAX_CPU_PERCENT, 1.0)
    norm_ram = min(estimated_ram_mb / MAX_RAM_MB, 1.0)
    norm_io = min(estimated_io_mb / MAX_IO_MB, 1.0)

    # Calculate the weighted cost score (0.0 to 1.0)
    cost_score = (norm_cpu * WEIGHT_CPU) + (norm_ram * WEIGHT_RAM) + (norm_io * WEIGHT_IO)

    # Determine a qualitative risk band based on the score
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
        "details": {
            "cpu_normalized": round(norm_cpu, 4),
            "ram_normalized": round(norm_ram, 4),
            "io_normalized": round(norm_io, 4),
        },
        "weights": {
            "cpu": WEIGHT_CPU,
            "ram": WEIGHT_RAM,
            "io": WEIGHT_IO,
        },
    }
