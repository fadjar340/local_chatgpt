from workers import math_agent, search_agent, rag_agent, pcb_agent

MAX_DEPTH = 3  # prevent infinite loops

def call_agent(agent_func, prompt, depth=0):
    if depth >= MAX_DEPTH:
        return f"⚠️ Agent chaining stopped at depth {MAX_DEPTH}."
    result = agent_func(prompt)
    # Detect if further action is needed
    if "search:" in result.lower():
        return result + "\n" + call_agent(search_agent, result, depth + 1)
    if "calculate" in result.lower():
        return result + "\n" + call_agent(math_agent, result, depth + 1)
    if "document" in result.lower():
        return result + "\n" + call_agent(rag_agent, result, depth + 1)
    return result

def chain_controller(prompt: str) -> str:
    # Start with RAG if documents exist
    if "research" in prompt.lower():
        return call_agent(rag_agent, prompt)
    if "pcb" in prompt.lower():
        return call_agent(pcb_agent, prompt)
    # Fallback to normal controller if no chain triggered
    from controller_agent_light import controller
    return controller(prompt)
