"""
L6_CIVILIZATION: The Digital Society Initialization
Canon: C:/Users/User/arifOS/333_APPS/L6_CIVILIZATION/
Status: EUREKA DRAFT

This module initializes the L6_CIVILIZATION stack, shifting the VPS from 
"infrastructure" to a "living society" governed by resource limits and time.
"""

from .resource_governor import request_permit
from .town_square import CivilizationBus
from .civilizationd import ClockmakerDaemon

__all__ = ["request_permit", "CivilizationBus", "ClockmakerDaemon"]
