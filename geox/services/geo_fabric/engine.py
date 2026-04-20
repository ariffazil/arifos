import numpy as np
from pyproj import Transformer, CRS
from shapely.geometry import Point, LineString, Polygon
from typing import List, Tuple, Optional, Dict, Any
from pydantic import BaseModel

# ══════════════════════════════════════════════════════════════════════════════
# GeoFabric Engine — Sovereign Spatial Laws
# ══════════════════════════════════════════════════════════════════════════════

class GeoFabricEngine:
    """
    The spatial core of GEOX. 
    Governs CRS validation, coordinate projection, and geometric truth.
    """

    def __init__(self):
        self._transformers: Dict[str, Transformer] = {}

    def get_transformer(self, source_epsg: int, target_epsg: int) -> Transformer:
        """Cache-backed transformer acquisition."""
        key = f"{source_epsg}:{target_epsg}"
        if key not in self._transformers:
            self._transformers[key] = Transformer.from_crs(
                CRS.from_epsg(source_epsg),
                CRS.from_epsg(target_epsg),
                always_xy=True
            )
        return self._transformers[key]

    def transform_point(self, x: float, y: float, source_epsg: int, target_epsg: int) -> Tuple[float, float]:
        """Transform a single point between CRSs."""
        transformer = self.get_transformer(source_epsg, target_epsg)
        return transformer.transform(x, y)

    def transform_points(self, points: List[Tuple[float, float]], source_epsg: int, target_epsg: int) -> List[Tuple[float, float]]:
        """Batch transform points."""
        transformer = self.get_transformer(source_epsg, target_epsg)
        # Using numpy for speed if points list is large
        pts = np.array(points)
        xt, yt = transformer.transform(pts[:, 0], pts[:, 1])
        return list(zip(xt, yt))

    def project_well_trajectory(
        self, 
        head_xy: Tuple[float, float], 
        md_points: List[float], 
        incl_points: List[float], 
        azim_points: List[float],
        method: str = "minimum_curvature"
    ) -> List[Tuple[float, float, float]]:
        """
        Calculate XYZ coordinates from MD/Incl/Azim.
        Simplified implementation of Minimum Curvature or Radius of Curvature.
        """
        # TODO: Implement full minimum curvature algorithm.
        # For MVP A, we use a placeholder or simplified tangent method if complex compute is deferred.
        # But let's try a basic vector summation (Tangent method) for now to prove the loop.
        
        results = []
        x, y, z = head_xy[0], head_xy[1], 0.0 # Assumes KB at 0 for simplicity
        results.append((x, y, z))
        
        for i in range(1, len(md_points)):
            dm = md_points[i] - md_points[i-1]
            inc = np.radians(incl_points[i])
            azi = np.radians(azim_points[i])
            
            # Simple Tangent
            dz = dm * np.cos(inc)
            dhoriz = dm * np.sin(inc)
            dx = dhoriz * np.sin(azi)
            dy = dhoriz * np.cos(azi)
            
            x += dx
            y += dy
            z += dz
            results.append((x, y, z))
            
        return results

    def validate_constraint(self, point: Tuple[float, float], polygon_coords: List[Tuple[float, float]]) -> bool:
        """Check if a point violates a spatial constraint (e.g. lease boundary)."""
        poly = Polygon(polygon_coords)
        p = Point(point)
        return poly.contains(p)

    def calculate_distance_line_to_point(self, line_coords: List[Tuple[float, float]], point: Tuple[float, float]) -> float:
        """Distance from a trajectory (line) to a target (point)."""
        line = LineString(line_coords)
        p = Point(point)
        return line.distance(p)

# Global Access Instance
fabric = GeoFabricEngine()
