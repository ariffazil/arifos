"""
arifOS Configuration Constants
Centralized thresholds and magic numbers for maintainability
"""


class ConstitutionalThresholds:
    """13 Constitutional Floor Thresholds"""

    # Uncertainty and Truth
    OMEGA_CRITICAL = 0.08  # F7 Humility - blocks if uncertainty > this
    OMEGA_DISPLAY_MIN = 0.03  # Minimum display omega
    OMEGA_DISPLAY_MAX = 0.05  # Maximum display omega
    TRUTH_SCORE_MINIMUM = 0.5  # F2 Truth - VOID if below

    # Empathy and Safety
    EMPATHY_KAPPA_R = 0.95  # Default empathy score
    EMPATHY_THRESHOLD = 0.7  # F6 Empathy - SABAR if below

    # Injection Defense
    INJECTION_RISK_HIGH = 0.9  # Flagged as adversarial
    INJECTION_RISK_BLOCK = 0.85  # F12 Defense - VOID if above

    # Witness and Judgment
    TRI_WITNESS_SCORE = 0.98  # F3 Tri-Witness default
    APEX_CONFIDENCE = 0.98  # Final verdict confidence

    # Irreversibility (L7 Action Gate)
    IRREVERSIBILITY_HOLD = 0.8  # Triggers 888_HOLD


class ToolDefaults:
    """Default values for tool outputs"""

    # Reason tool
    TRUTH_SCORE_PLACEHOLDER = 0.85  # TODO: Replace with real calculation
    CLARITY_DELTA = -0.2
    HYPOTHESES_DEFAULT = 3

    # Validate tool
    SAFE_DEFAULT = True

    # Align tool
    ANTI_HANTU = True

    # Forge tool
    ARTIFACT_READY = True


class SessionConfig:
    """Session initialization defaults"""

    MODE_DEFAULT = "conscience"
    ACTOR_ID_DEFAULT = "user"


class PerformanceLimits:
    """Performance and resource limits"""

    MAX_HYPOTHESES = 10
    MAX_EVIDENCE_ITEMS = 100
    MAX_STAKEHOLDERS = 50
    MAX_TOKENS_DEFAULT = 8192
