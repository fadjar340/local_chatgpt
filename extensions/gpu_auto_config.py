import os
import subprocess

# CPU and GPU model names
GPU_MODEL = os.getenv("GPU_MODEL", "llama3:70b")          # heavy model if GPU
CPU_MODEL = os.getenv("CPU_MODEL", "llama3:8b-q4_K_M")    # lightweight quantized model for CPU

def is_gpu_available():
    """Check if NVIDIA GPU is available using nvidia-smi."""
    try:
        result = subprocess.run(["nvidia-smi"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def select_model():
    """Return model based on hardware availability."""
    return GPU_MODEL if is_gpu_available() else CPU_MODEL

# Set default model dynamically
selected_model = select_model()
os.environ["DEFAULT_MODEL"] = selected_model
print(f"⚡ Auto-config: Using model → {selected_model}")
