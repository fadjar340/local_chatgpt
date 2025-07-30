# Lightweight Controller – Sequential
from workers import math_agent, search_agent, pcb_agent, rag_agent

def controller(prompt: str) -> str:
    results = []
    lower = prompt.lower()

    if "calculate" in lower or any(op in lower for op in ["^", "*", "+", "="]):
        results.append(math_agent(prompt))

    if "search:" in lower:
        results.append(search_agent(prompt))

    if "pcb" in lower or ".kicad" in lower:
        results.append(pcb_agent(prompt))

    if "document" in lower or "research" in lower:
        results.append(rag_agent(prompt))

    return "\n\n".join(results) if results else "🤖 Controller: No worker triggered, using default LLM."
