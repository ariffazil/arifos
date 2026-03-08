"""Compatibility shim — re-exports from core.rest_routes."""
from core.rest_routes import *  # noqa: F401, F403
from core.rest_routes import (  # noqa: F401
    _openapi_schema, _canonical_floor_defaults, _representative_floor_score,
    register_rest_routes,
)
