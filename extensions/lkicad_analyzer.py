import os
import re
import sexpdata

KICAD_DIR = "/app/data/kicad"
os.makedirs(KICAD_DIR, exist_ok=True)

def analyze_kicad_file(file_path: str) -> str:
    """Reads KiCad 9 schematic or PCB and extracts basic info"""
    try:
        with open(file_path, "r") as f:
            data = f.read()

        # Detect if it's a schematic or PCB file
        if "(kicad_pcb" in data:
            file_type = "PCB Layout"
        elif "(schematic" in data or "(kicad_sch" in data:
            file_type = "Schematic"
        else:
            file_type = "Unknown"

        # Try parsing components and nets
        components = re.findall(r"\(comp\s+\(ref\s+([A-Za-z0-9]+)\)", data)
        nets = re.findall(r"\(net\s+\d+\s+([A-Za-z0-9_]+)\)", data)

        summary = f"📄 **KiCad {file_type} Analysis**\n"
        summary += f"- Components found: {len(components)} → {components[:10]}...\n"
        summary += f"- Nets found: {len(nets)} → {nets[:10]}...\n"
        summary += f"- File Size: {len(data)} bytes\n"

        return summary
    except Exception as e:
        return f"⚠️ Failed to analyze KiCad file: {e}"

try:
    import open_webui
    original_handle = open_webui.handle_upload

    def patched_upload(file_path, *args, **kwargs):
        if file_path.endswith(".kicad_pcb") or file_path.endswith(".kicad_sch"):
            print("🟢 Analyzing KiCad file...")
            summary = analyze_kicad_file(file_path)
            return summary
        return original_handle(file_path, *args, **kwargs)

    open_webui.handle_upload = patched_upload
    print("🔥 KiCad Analyzer Enabled")
except Exception as e:
    print(f"⚠️ Failed to enable KiCad Analyzer: {e}")
