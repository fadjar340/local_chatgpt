import re
import os
import time
import subprocess

MERMAID_DIR = "/app/data/image_analysis"
os.makedirs(MERMAID_DIR, exist_ok=True)

def extract_mermaid_code(response: str) -> str:
    """Extract Mermaid code blocks"""
    match = re.search(r"```mermaid(.*?)```", response, re.S)
    return match.group(1).strip() if match else None

def render_mermaid(code: str) -> str:
    """Render Mermaid diagram to PNG"""
    ts = int(time.time())
    input_file = os.path.join(MERMAID_DIR, f"diagram_{ts}.mmd")
    output_file = os.path.join(MERMAID_DIR, f"diagram_{ts}.png")
    
    with open(input_file, "w") as f:
        f.write(code)
    
    try:
        subprocess.run(["mmdc", "-i", input_file, "-o", output_file], check=True)
        print(f"✅ Mermaid diagram saved to {output_file}")
        return output_file
    except Exception as e:
        print(f"⚠️ Mermaid rendering failed: {e}")
        return ""

def process_response(response: str) -> str:
    code = extract_mermaid_code(response)
    if code:
        img = render_mermaid(code)
        if img:
            return f"🖼️ Mermaid diagram generated: {img}"
    return ""

try:
    import open_webui
    original_fn = open_webui.generate_response

    def patched_generate(*args, **kwargs):
        resp = original_fn(*args, **kwargs)
        note = process_response(resp)
        return resp + ("\n\n" + note if note else "")

    open_webui.generate_response = patched_generate
    print("🔥 Mermaid Renderer Enabled")
except Exception as e:
    print(f"⚠️ Failed to enable Mermaid Renderer: {e}")
