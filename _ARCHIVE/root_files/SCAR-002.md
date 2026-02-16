# SCAR-002: FastMCP v2 API Drift (2026-02-14)

## Wound
FastMCP v2 FunctionTool objects not callable programmatically.
Decorators use `annotations` parameter yang v1 tak support.

## Impact
- Integration broken (Hostinger ↔ Railway)
- Ω₀ elevated to 0.20
- Cannot verify distributed deployment

## Fix
Temporary downgrade to FastMCP v1.0.
Updated decorators dari `annotations=` ke `name=, description=`.

## Revert Condition
When Option B (wrapper layer) implemented dalam v65.1.

## Responsible
888 Judge override untuk unblock deployment.

---

*DITEMPA DARI KEGAGALAN API* 🔥
