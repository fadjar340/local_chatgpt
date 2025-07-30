import os
import subprocess
import time
import pandas as pd

KICAD_DIR = "/app/data/kicad"
os.makedirs(KICAD_DIR, exist_ok=True)

def run_drc(pcb_file: str) -> str:
    """Run KiCad DRC on a PCB file and return summary"""
    try:
        drc_report = os.path.join(KICAD_DIR, f"drc_report_{int(time.time())}.rpt")
        cmd = ["kicad-cli", "pcb", "check", pcb_file, "--report", drc_report]
        subprocess.run(cmd, check=True)
        with open(drc_report, "r") as f:
            report = f.read()
        return f"✅ **DRC Completed**\n```\n{report[:1000]}\n```"  # Limit output
    except Exception as e:
        return f"⚠️ DRC failed: {e}"

def extract_bom(sch_file: str) -> str:
    """Extract BOM from schematic file"""
    try:
        bom_csv = os.path.join(KICAD_DIR, f"bom_{int(time.time())}.csv")
        cmd = ["kicad-cli", "sch", "export", "bom", sch_file, "--output", bom_csv]
        subprocess.run(cmd, check=True)

        df = pd.read_csv(bom_csv)
        preview = df.head(10).to_string(index=False)
        return f"📦 **BOM Extracted** (First 10 Rows)\n```\n{preview}\n```"
    except Exception as e:
        return f"⚠️ BOM extraction failed: {e}"

try:
    import open_webui
    original_upload = open_webui.handle_upload

    def patched_upload(file_path, *args, **kwargs):
        result = original_upload(file_path, *args, **kwargs)
        if file_path.endswith(".kicad_pcb"):
            result += "\n\n" + run_drc(file_path)
        elif file_path.endswith(".kicad_sch"):
            result += "\n\n" + extract_bom(file_path)
        return result

    open_webui.handle_upload = patched_upload
    print("🔥 KiCad DRC + BOM Module Enabled")
except Exception as e:
    print(f"⚠️ Failed to enable KiCad DRC/BOM: {e}")
