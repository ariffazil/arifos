"""
GSM Figure Extraction Script — DITEMPA BUKAN DIBERI

Extracts pages from GSM-702001 PDF as high-resolution images for 
GEOX Seismic Viewer and Basin Map Explorer integration.
"""

import os
import json
import argparse
import sys

try:
    from pdf2image import convert_from_path
except ImportError:
    print("CRITICAL: pdf2image not found. Run: pip install pdf2image")
    print("Note: Poppler must also be installed on your system.")
    sys.exit(1)

def extract_figures(pdf_path, output_dir, dpi=300):
    """
    Extracts all pages from a PDF and saves them as PNGs.
    Generates a figures.json manifest for GEOX integration.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"[*] Extracting PDF: {pdf_path}")
    print(f"[*] Output directory: {output_dir}")
    print(f"[*] Resolution: {dpi} DPI")
    
    try:
        pages = convert_from_path(pdf_path, dpi=dpi)
    except Exception as e:
        print(f"[!] Extraction failed: {e}")
        return []

    figures = []
    for i, page in enumerate(pages):
        filename = f"page_{i:03d}.png"
        page_path = os.path.join(output_dir, filename)
        
        print(f"[+] Saving {filename}...")
        page.save(page_path, "PNG")

        figures.append({
            "id": f"gsm_702001_p{i:03d}",
            "page": i,
            "filename": filename,
            "path": page_path,
            "type": "unknown",         # Manual classification: [seismic, map, strat, table]
            "georeferenced": False,
            "provenance": "GSM-702001",
            "metadata": {
                "source_url": "https://gsm.org.my/wp-content/uploads/gsm_file_2/702001-101921-PDF.pdf",
                "extracted_at": "2026-04-09"
            }
        })

    manifest_path = os.path.join(output_dir, "figures.json")
    with open(manifest_path, "w") as f:
        json.dump(figures, f, indent=2)

    print(f"\n[OK] Successfully extracted {len(pages)} figures.")
    print(f"[OK] Manifest saved to: {manifest_path}")
    return figures

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract figures from GSM PDF")
    parser.add_argument("pdf", help="Path to source PDF")
    parser.add_argument("out", help="Output directory")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for extraction")
    
    args = parser.parse_args()
    
    extract_figures(args.pdf, args.out, args.dpi)
