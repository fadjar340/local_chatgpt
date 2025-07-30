import os
import time

KICAD_OUT = "/app/data/kicad"
os.makedirs(KICAD_OUT, exist_ok=True)

def save_kicad_design(text: str, filename="generated.kicad_sch") -> str:
    """Save AI-generated schematic or PCB text as a KiCad file"""
    try:
        filepath = os.path.join(KICAD_OUT, filename)
        with open(filepath, "w") as f:
            f.write(text)
        print(f"✅ KiCad file saved: {filepath}")
        return filepath
    except Exception as e:
        return f"⚠️ Failed to save KiCad file: {e}"

try:
    import open_webui
    original_generate = open_webui.generate_response

    def patched_generate(*args, **kwargs):
        resp = original_generate(*args, **kwargs)
        if "(kicad_pcb" in resp or "(kicad_sch" in resp:
            ts = int(time.time())
            filename = f"ai_generated_{ts}.kicad_pcb" if "(kicad_pcb" in resp else f"ai_generated_{ts}.kicad_sch"
            save_kicad_design(resp, filename)
            resp += f"\n\n📂 **KiCad file saved** → `/app/data/kicad/{filename}`"
        return resp

    open_webui.generate_response = patched_generate
    print("🔥 KiCad Generator Enabled")
except Exception as e:
    print(f"⚠️ Failed to enable KiCad Generator: {e}")
