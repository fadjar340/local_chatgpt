import os, re

TOOLS = {
    "ocr": "image_ocr",
    "math": "math_executor",
    "graph": "graph_renderer",
    "mermaid": "mermaid_renderer",
    "kicad": "kicad_drc_bom",
    "research": "research_fetcher",
    "web": "web_search"
}

def decide_tool(prompt: str) -> str:
    prompt_lower = prompt.lower()
    if "ocr" in prompt_lower: return TOOLS["ocr"]
    if re.search(r"\d+\^|\*|=", prompt_lower): return TOOLS["math"]
    if "plot" in prompt_lower: return TOOLS["graph"]
    if "diagram" in prompt_lower: return TOOLS["mermaid"]
    if "pcb" in prompt_lower or ".kicad" in prompt_lower: return TOOLS["kicad"]
    if "latest paper" in prompt_lower: return TOOLS["research"]
    if "search:" in prompt_lower: return TOOLS["web"]
    return "llm"

try:
    import open_webui
    original_fn = open_webui.generate_response
    def orchestrator(*args, **kwargs):
        prompt = args[0]
        tool = decide_tool(prompt)
        print(f"🛠 Orchestrator: Selected Tool → {tool}")
        return original_fn(*args, **kwargs)
    open_webui.generate_response = orchestrator
except:
    print("⚠️ Tool Orchestrator failed to patch")
