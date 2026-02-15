"""
Safe type conversion utilities for constitutional metrics.
Prevents crashes from malformed metric values.
"""
from typing import Any, Union

def safe_float(
    value: Any, 
    default: float = 0.0, 
    min_val: float = -float('inf'),
    max_val: float = float('inf')
) -> float:
    """
    Safely convert value to float with bounds checking.
    
    Args:
        value: Value to convert (any type)
        default: Fallback if conversion fails
        min_val: Minimum allowed value (clips below)
        max_val: Maximum allowed value (clips above)
        
    Returns:
        Float value within [min_val, max_val]
        
    Examples:
        >>> safe_float("0.95")
        0.95
        >>> safe_float("invalid", default=0.0)
        0.0
        >>> safe_float(1.5, min_val=0.0, max_val=1.0)
        1.0
    """
    try:
        result = float(value)
        return max(min_val, min(result, max_val))
    except (TypeError, ValueError, AttributeError):
        return default

def safe_bool(value: Any, default: bool = False) -> bool:
    """Safely convert to boolean."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', '1', 'yes')
    try:
        return bool(value)
    except (TypeError, ValueError):
        return default
