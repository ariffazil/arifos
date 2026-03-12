import os
import subprocess
import shutil

def forge_office_document(file_path):
    base_name = os.path.basename(file_path)
    processing_path = os.path.join("/watch/processing", base_name)
    outbox_base = os.path.join("/watch/outbox", os.path.splitext(base_name)[0])
    
    print(f"FORGE: Processing {file_path}...")
    shutil.move(file_path, processing_path)

    try:
        # PPTX
        pptx_out = outbox_base + ".pptx"
        subprocess.run(["marp", processing_path, "-o", pptx_out, "--no-sandbox"], check=True)
        # PDF
        pdf_out = outbox_base + ".pdf"
        subprocess.run(["marp", processing_path, "-o", pdf_out, "--no-sandbox"], check=True)
        print(f"FORGE: Success")
        os.remove(processing_path)
        return True
    except Exception as e:
        print(f"FORGE ERROR: {e}")
        return False
