import re
import os
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

GRAPH_DIR = "/app/data/image_analysis"
os.makedirs(GRAPH_DIR, exist_ok=True)

def extract_python_code(response: str) -> str:
    """Extract Python code blocks from response"""
    match = re.search(r"```python(.*?)```", response, re.S)
    return match.group(1).strip() if match else None

def execute_graph_code(code: str) -> str:
    """Execute the extracted Matplotlib code and save graph as PNG"""
    filename = os.path.join(GRAPH_DIR, f"graph_{int(time.time())}.png")
    try:
        # Provide a safe namespace
        ns = {"plt": plt, "np": np, "savepath": filename}
        exec(code, ns)
        if os.path.exists(filename):
            print(f"✅ Graph saved to {filename}")
            return filename
        else:
            return "⚠️ Graph not generated"
    except Exception as e:
        return f"⚠️ Graph execution failed: {e}"

def process_response(response: str) -> str:
    code = extract_python_code(response)
    if code:
        file_path = execute_graph_code(code)
        if file_path.startswith("/app"):
            return f"🖼️ Graph generated: {file_path}"
    return ""

try:
    import open_webui
    original_fn = open_webui.generate_response

    def patched_generate(*args, **kwargs):
        resp = original_fn(*args, **kwargs)
        img_note = process_response(resp)
        return resp + ("\n\n" + img_note if img_note else "")

    open_webui.generate_response = patched_generate
    print("🔥 Graph Renderer Enabled (Matplotlib Execution Active)")
except Exception as e:
    print(f"⚠️ Failed to enable Graph Renderer: {e}")
