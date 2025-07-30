import re
import os
import time
import numpy as np
import sympy as sp
import mpmath
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULT_DIR = "/app/data/image_analysis"
os.makedirs(RESULT_DIR, exist_ok=True)

def extract_code(response: str):
    """Detect code blocks (Python or SymPy)"""
    match = re.search(r"```python(.*?)```", response, re.S)
    return match.group(1).strip() if match else None

def execute_symbolic(code: str):
    """Try symbolic computation with SymPy"""
    try:
        x = sp.symbols("x")
        safe_ns = {"sp": sp, "x": x}
        exec_globals = {}
        exec(code, safe_ns, exec_globals)
        return str(exec_globals.get("result", "✅ Symbolic computation executed."))
    except Exception as e:
        return f"⚠️ Symbolic execution failed: {e}"

def execute_numeric(code: str):
    """Execute numeric computations with NumPy/SciPy"""
    try:
        safe_ns = {"np": np, "mp": mpmath}
        exec_globals = {}
        exec(code, safe_ns, exec_globals)
        return str(exec_globals.get("result", "✅ Numeric computation executed."))
    except Exception as e:
        return f"⚠️ Numeric execution failed: {e}"

def execute_plotting(code: str):
    """Detect and execute plotting code, saving a PNG"""
    ts = int(time.time())
    filename = os.path.join(RESULT_DIR, f"math_plot_{ts}.png")
    try:
        safe_ns = {"plt": plt, "np": np, "savepath": filename}
        exec(code, safe_ns)
        if os.path.exists(filename):
            return f"🖼️ Plot generated: {filename}"
        return "⚠️ No plot generated."
    except Exception as e:
        return f"⚠️ Plot execution failed: {e}"

def process_math(response: str) -> str:
    code = extract_code(response)
    if not code:
        return ""

    # Decision Logic
    if "sp." in code or "sympy" in code:
        output = execute_symbolic(code)
    elif "plt." in code:
        output = execute_plotting(code)
    else:
        output = execute_numeric(code)

    return f"🧮 Math Assistant Result:\n```\n{output}\n```"

try:
    import open_webui
    original_fn = open_webui.generate_response

    def patched_generate(*args, **kwargs):
        resp = original_fn(*args, **kwargs)
        result = process_math(resp)
        return resp + ("\n\n" + result if result else "")

    open_webui.generate_response = patched_generate
    print("🔥 Full Math Assistant Mode Enabled")
except Exception as e:
    print(f"⚠️ Failed to enable Full Math Assistant Mode: {e}")
