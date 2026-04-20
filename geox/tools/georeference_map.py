"""
GSM Georeferencing Helper — DITEMPA BUKAN DIBERI

Assigns WGS84 (EPSG:4326) coordinates to extracted GSM maps.
Requires: rasterio, numpy, pillow
"""

import os
import argparse
from PIL import Image
import numpy as np

try:
    import rasterio
    from rasterio.transform import from_bounds
except ImportError:
    print("CRITICAL: rasterio not found. Run: pip install rasterio")
    rasterio = None

def georeference_map(input_path, output_path, bounds):
    """
    bounds: [min_lon, min_lat, max_lon, max_lat]
    Example Malay Basin: [102.0, 3.0, 107.0, 7.5]
    """
    if rasterio is None:
        return
        
    print(f"[*] Georeferencing {input_path}...")
    print(f"[*] Bounds: {bounds}")
    
    # Load image to get dimensions
    with Image.open(input_path) as img:
        width, height = img.size
        # Convert to numpy array
        data = np.array(img)
        
    # Transpose if necessary (rasterio expects [bands, height, width])
    if len(data.shape) == 3:
        data = data.transpose(2, 0, 1)
    else:
        # Grayscale
        data = data.reshape(1, height, width)

    # Create transform
    transform = from_bounds(*bounds, width, height)

    # Write GeoTIFF
    with rasterio.open(
        output_path,
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=data.shape[0],
        dtype=data.dtype,
        crs='EPSG:4326',
        transform=transform,
    ) as dst:
        dst.write(data)

    print(f"[OK] Georeferenced map saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Georeference a JPG/PNG map")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output GeoTIFF path")
    parser.add_argument("--bounds", nargs=4, type=float, required=True, 
                        help="west south east north (WGS84)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found.")
    else:
        georeference_map(args.input, args.output, args.bounds)
        
# ────────────────────────────────────────────────────────────────────
# Typical Malay Basin Bounds (Approximate)
# Longitude: 102.0 to 107.0
# Latitude:  3.0 to 7.5
# ────────────────────────────────────────────────────────────────────
