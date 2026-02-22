from aclip_cai.tools.system_monitor import get_system_health


def forge_guard(
    check_system_health: bool = True,
    cost_score_threshold: float = 0.8,
    cost_score_to_check: float = 0.0,
) -> dict:
    """
    Acts as a local safety relay or circuit breaker before an action.

    This tool provides a recommendation based on the current system state
    and a proposed cost score for an action. It does not make a final
    constitutional verdict, but signals whether it's safe to proceed locally.

    Args:
        check_system_health (bool): Whether to evaluate current system health.
        cost_score_threshold (float): The threshold above which the guard will
                                      recommend SABAR or VOID. (0.0 to 1.0)
        cost_score_to_check (float): The estimated cost score of the action
                                     to be performed.

    Returns:
        dict: A dictionary containing the verdict (OK, SABAR, VOID_LOCAL)
              and the reasons for it.
    """
    verdict = "OK"
    reasons = []

    # 1. Check the estimated cost of the upcoming action
    if cost_score_to_check >= cost_score_threshold:
        verdict = "SABAR"
        reasons.append(
            f"Action cost score ({cost_score_to_check}) exceeds threshold ({cost_score_threshold}). "
            "Recommend delaying or running in a low-activity window."
        )

    # 2. Check the current system health
    if check_system_health:
        health = get_system_health()

        # Check for any critical warnings from the system monitor
        if health.get("warnings"):
            for warning in health["warnings"]:
                if "CRITICAL" in warning:
                    # If health is already critical, any action is risky.
                    verdict = "VOID_LOCAL"
                    reasons.append(f"System health is CRITICAL: {warning}")
                elif "HIGH" in warning and verdict != "VOID_LOCAL":
                    verdict = "SABAR"
                    reasons.append(f"System health is under HIGH pressure: {warning}")

    if not reasons:
        reasons.append("System health is nominal and action cost is within acceptable limits.")

    return {
        "verdict": verdict,
        "reasons": reasons,
    }
