"""
core/governance/ — Constitutional Enforcement

APEX INVARIANTS: This module contains NON-LEARNABLE governance parameters.
These are constants of constitutional law, not trainable weights.

⚠️  NEVER implement learn(), fit(), train(), or update_thresholds() here.
⚠️  APEX is a calculator applying fixed law, not a student improving itself.

See: APEX_INVARIANTS.md for the complete invariant table.
"""

# APEX exports
from .apex_invariants import (
    APEX_CONSTANTS,
    validate_apex_non_learning,
)

# Notification Bridge exports
from .apex_notification import (
    APEXNotificationBridge,
    HoldEvent,
    HoldReason,
    NotificationChannel,
    apex_notification_bridge,
    emit_sovereign_hold,
)

__all__ = [
    "APEX_CONSTANTS",
    "validate_apex_non_learning",
    "APEXNotificationBridge",
    "HoldEvent",
    "HoldReason",
    "NotificationChannel",
    "apex_notification_bridge",
    "emit_sovereign_hold",
]
