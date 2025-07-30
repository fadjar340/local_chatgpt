import os

def export_to_tex(content: str, filename: str = "/app/data/output.tex") -> str:
    """
    Exports content to a TeX file.
    """
    try:
        os.makedirs("/app/data", exist_ok=True)
        with open(filename, "w") as f:
            f.write("\\documentclass{article}\n\\begin{document}\n")
            f.write(content)
            f.write("\n\\end{document}")
        return f"📄 TeX exported to {filename}"
    except Exception as e:
        return f"⚠️ TeX Export Error: {e}"
