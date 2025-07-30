import os
import time

OUTPUT_DIR = "/app/data/tex_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_response_as_tex(response: str):
    """Save any response containing LaTeX markers as a .tex file"""
    if "\\begin{document}" in response and "\\end{document}" in response:
        filename = os.path.join(OUTPUT_DIR, f"response_{int(time.time())}.tex")
        with open(filename, "w") as f:
            f.write(response)
        print(f"✅ Saved LaTeX output to {filename}")

# Monkey-patch Open WebUI after response generation
try:
    import open_webui
    original_fn = open_webui.generate_response

    def patched_generate(*args, **kwargs):
        resp = original_fn(*args, **kwargs)
        save_response_as_tex(resp)
        return resp

    open_webui.generate_response = patched_generate
    print("🔥 LaTeX Auto-Export Enabled")
except Exception as e:
    print("⚠️ Failed to patch Open WebUI for .tex export:", e)
