from extensions.kicad_drc_bom import analyze_pcb

def pcb_agent(file_path: str) -> str:
    """
    PCB Agent: Runs KiCad DRC/BOM analysis on a given file.
    """
    try:
        report = analyze_pcb(file_path)
        return f"📐 PCB Agent Analysis:\n{report}"
    except Exception as e:
        return f"⚠️ PCB Agent Error: {e}"
