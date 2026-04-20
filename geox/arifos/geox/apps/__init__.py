"""
GEOX Apps — Host-agnostic interactive applications.

This package contains GEOX MCP Apps with their manifests and implementations.
Each app is self-contained and portable across hosts.

DITEMPA BUKAN DIBERI
"""

from pathlib import Path
import json

from ..contracts.app_manifest import GeoXAppManifest, get_app_registry


def load_app_manifest(app_name: str) -> GeoXAppManifest:
    """
    Load an app manifest by name.
    
    Args:
        app_name: App directory name (e.g., 'seismic_viewer')
    
    Returns:
        Parsed GeoXAppManifest
    """
    manifest_path = Path(__file__).parent / app_name / "manifest.json"
    return GeoXAppManifest.parse_file(manifest_path)


def register_all_apps() -> None:
    """Register all built-in GEOX apps."""
    registry = get_app_registry()
    
    apps_dir = Path(__file__).parent
    for app_dir in apps_dir.iterdir():
        if app_dir.is_dir() and (app_dir / "manifest.json").exists():
            try:
                manifest = GeoXAppManifest.parse_file(app_dir / "manifest.json")
                registry.register(manifest)
            except Exception as e:
                print(f"[GEOX Apps] Failed to load {app_dir.name}: {e}")


# Auto-register on import
register_all_apps()
