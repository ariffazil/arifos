async def well_agi() -> dict:
    return {
        "uri": "organ://well/agi",
        "organ": "WELL",
        "maps_to": "AGI",
        "purpose": "Biological substrate, operator readiness, stability",
        "status": "available",
    }


async def wealth_asi() -> dict:
    return {
        "uri": "organ://wealth/asi",
        "organ": "WEALTH",
        "maps_to": "ASI",
        "purpose": "Capital engine, resource allocation, operational economics",
        "status": "available",
    }


async def geox_apex() -> dict:
    return {
        "uri": "organ://geox/apex",
        "organ": "GEOX",
        "maps_to": "APEX",
        "purpose": "Earth intelligence, spatial and subsurface witness context",
        "status": "available",
    }


RESOURCES = {
    "organ://well/agi": well_agi,
    "organ://wealth/asi": wealth_asi,
    "organ://geox/apex": geox_apex,
}

__all__ = ["RESOURCES", "geox_apex", "wealth_asi", "well_agi"]
