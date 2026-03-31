import matplotlib.pyplot as plt
import numpy as np
import os
from fpdf import FPDF

def create_map_image(filename="map.png"):
    # Coordinates
    lon_start, lat_start = 116.5941468, 6.5972569  # Kota Belud
    lon_end, lat_end = 115.2082005, 7.8179921      # Offshore NW Sabah
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Simple abstract representation
    ax.set_xlim(114.5, 117.5)
    ax.set_ylim(6.0, 8.5)
    
    # Draw Coastline (Abstract)
    coast_x = [116.0, 116.5, 117.0, 117.5]
    coast_y = [6.0, 6.8, 7.5, 8.0]
    ax.fill_between(coast_x, coast_y, 6.0, color='lightgreen', alpha=0.3, label='Land (Borneo)')
    ax.fill_between(coast_x, coast_y, 8.5, color='lightblue', alpha=0.3, label='Sea (South China Sea)')
    
    # Plot line
    ax.plot([lon_start, lon_end], [lat_start, lat_end], color='red', linewidth=2, marker='o', 
            markersize=8, label='Section Line (NW-SE)')
    
    ax.text(lon_start + 0.05, lat_start - 0.05, 'Kota Belud\n[116.59, 6.60]', fontsize=10, fontweight='bold', color='black')
    ax.text(lon_end - 0.5, lat_end + 0.05, 'Offshore NW Sabah\n[115.21, 7.82]', fontsize=10, fontweight='bold', color='black')
    
    # Annotate geological belts
    ax.text(116.2, 6.8, 'Inboard Belt\n(Sabah Ridges)', fontsize=10, style='italic', color='darkblue')
    ax.text(115.5, 7.4, 'Outboard Belt\n(Prograding Wedge)', fontsize=10, style='italic', color='darkblue')
    
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Regional Map: NW Sabah Basin')
    ax.legend(loc='lower left')
    ax.grid(True, linestyle='--', alpha=0.6)
    
    plt.tight_layout()
    fig.savefig(filename, dpi=150)
    plt.close(fig)

def create_cross_section_image(filename="section.png"):
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # X axis = Distance along line (km approx)
    # Total distance is roughly ~190km. We'll use 0 to 200
    x = np.linspace(0, 200, 500)
    
    # Bathymetry (Sea Floor)
    # Starts at 0 (land), drops off quickly
    z_sea = np.zeros_like(x)
    z_sea[x > 20] = -500 - 1500 * (1 - np.exp(-(x[x > 20] - 20) / 50))
    
    # DRU (Deep Regional Unconformity)
    z_dru = -2000 - 3000 * (x/200) + 1500 * np.sin(x/15) * np.exp(-x/100)
    
    # Basement (Crocker Formation)
    ax.fill_between(x, -8000, z_dru, color='gray', alpha=0.6, label='Crocker/Wariu Fm (Basement/Melange)')
    
    # Neogene Sediments
    ax.fill_between(x, z_dru, z_sea, color='khaki', alpha=0.6, label='Neogene Stage I-IV (Clastics)')
    
    # Add fault lines (Sabah Ridges)
    fault_x = [40, 70, 100, 130]
    for fx in fault_x:
        ax.plot([fx-5, fx+5], [-6000, z_sea[int(fx/200*500)] - 200], 'k-', linewidth=1.5, alpha=0.8)
    
    # Well A (Inboard)
    well_a_x = 50
    ax.plot([well_a_x, well_a_x], [z_sea[int(well_a_x/200*500)], -3500], 'k-', linewidth=3, label='Exploration Well (Representative)')
    ax.plot(well_a_x, z_sea[int(well_a_x/200*500)], 'k^', markersize=10)
    ax.text(well_a_x+2, -1000, 'Well A (Inboard)\nTD: 3500m', fontsize=9)
    
    # Well B (Outboard)
    well_b_x = 160
    ax.plot([well_b_x, well_b_x], [z_sea[int(well_b_x/200*500)], -4000], 'k-', linewidth=3)
    ax.plot(well_b_x, z_sea[int(well_b_x/200*500)], 'k^', markersize=10)
    ax.text(well_b_x+2, -1500, 'Well B (Outboard)\nTD: 4000m\n(Stage IV)', fontsize=9)
    
    ax.plot(x, z_sea, 'b-', linewidth=2, label='Sea Floor')
    ax.fill_between(x, z_sea, 0, color='lightblue', alpha=0.3)
    
    ax.set_xlim(0, 200)
    ax.set_ylim(-7000, 500)
    ax.set_xlabel('Distance from Kota Belud NW (km)')
    ax.set_ylabel('Depth (m)')
    ax.set_title('Schematic Geological Cross-Section (NW Sabah Basin)')
    
    ax.text(30, -5500, 'Inboard Belt\n(Sabah Ridges)', fontsize=11, color='white', fontweight='bold')
    ax.text(140, -5500, 'Outboard Belt', fontsize=11, color='white', fontweight='bold')
    ax.text(10, 200, 'SE (Kota Belud)', fontsize=10, fontweight='bold')
    ax.text(170, 200, 'NW (Offshore)', fontsize=10, fontweight='bold')
    
    ax.legend(loc='lower left')
    
    plt.tight_layout()
    fig.savefig(filename, dpi=150)
    plt.close(fig)

def create_pdf(output_pdf="NW_Sabah_Geological_Synthesis.pdf"):
    create_map_image("temp_map.png")
    create_cross_section_image("temp_section.png")
    
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "Geological Synthesis Report: NW Sabah Basin", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("helvetica", "I", 10)
    pdf.cell(0, 10, "Transect: Kota Belud [116.594, 6.597] to Offshore [115.208, 7.818]", new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.ln(5)
    
    # Section 1: Regional Map
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "1. Structural Map & Coordinate Trajectory", new_x="LMARGIN", new_y="NEXT")
    pdf.image("temp_map.png", w=160, x=25)
    
    pdf.set_font("helvetica", "", 10)
    pdf.multi_cell(0, 5, "The section line begins onshore near Kota Belud, situated within the Northern Inboard Belt. It traverses northwestwards across the continental shelf, crossing the Bunbury-St. Joseph Fault Zone, and terminates in the deepwater Outboard Belt towards the NW Sabah Trough. This area marks the critical structural pivot known as the 'Kota Belud Bend', where regional strike shifts from NE-SW to NW-SE.")
    
    pdf.add_page()
    
    # Section 2: Subsurface Cross-Section
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "2. Synthesized Seismic/Geological Cross-Section", new_x="LMARGIN", new_y="NEXT")
    pdf.image("temp_section.png", w=190, x=10)
    
    pdf.set_font("helvetica", "", 10)
    pdf.multi_cell(0, 5, "The schematic cross-section above illustrates the primary tectono-stratigraphic domains along the transect:\n\n"
                         "- Inboard Belt (SE): Characterized by intense compressional tectonics, forming the 'Sabah Ridges'. Deep-seated wrench faulting uplifts the Crocker Formation basement. Neogene sediments are relatively thin and highly deformed.\n"
                         "- Outboard Belt (NW): A massive, prograding wedge of Neogene clastics (Stage IV). Characterized by extensional growth faults and a thicker, less deformed sedimentary section, typical of primary reservoir targets.\n"
                         "- Stratigraphy: The Deep Regional Unconformity (DRU) separates the highly deformed Paleogene basement from the younger Neogene basin fill.")
    
    pdf.ln(5)
    
    # Section 3: Exploration Well Synthesis
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "3. Regional Exploration Well Data", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    pdf.multi_cell(0, 5, "Detailed well data for specific offshore blocks is proprietary to PETRONAS/PSC contractors. However, regional exploration trends along this transect indicate:\n\n"
                         "Well A (Representative Inboard Well - e.g., near South Furious/Barton trends):\n"
                         "  - Status: Mostly drilled on crests of 'Sabah Ridges' (tight anticlines).\n"
                         "  - Targets: Shallow marine sands (Stage IV A-C).\n"
                         "  - Basement: Often encounters the underlying Crocker or Wariu Formation melange at shallower depths.\n\n"
                         "Well B (Representative Outboard Well - Deepwater):\n"
                         "  - Status: Drilled in block settings targeting stratigraphic traps or growth-fault rollovers.\n"
                         "  - Targets: Thick, prograding deltaic to deep-marine fan sands (Stage IV C-F).\n"
                         "  - Depth: Requires significant TD (>3000m) to reach target horizons due to thick sedimentary loading.")
                         
    pdf.ln(5)
    pdf.set_font("helvetica", "I", 8)
    pdf.multi_cell(0, 5, "Data synthesized via arifOS GeoRAG tools utilizing published geological models (e.g., Hazebroek & Tan 1993, Tongkul 1994). Proprietary well logs and seismic SEGY files are secured under national frameworks and not rendered directly.")
    
    pdf.output(output_pdf)
    
    # Cleanup
    os.remove("temp_map.png")
    os.remove("temp_section.png")

if __name__ == "__main__":
    create_pdf()
    print("PDF generated successfully.")
