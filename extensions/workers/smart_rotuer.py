from extensions.workers import math_agent, search_agent, pcb_agent, rag_agent

def route_task(task_name: str, payload: dict) -> str:
    """
    Routes a task to the correct agent based on task_name.
    """
    try:
        if task_name == "math":
            return math_agent.math_agent(payload.get("prompt", ""))
        elif task_name == "search":
            return search_agent.search_agent(payload.get("prompt", ""))
        elif task_name == "pcb":
            return pcb_agent.pcb_agent(payload.get("file_path", ""))
        elif task_name == "rag":
            return rag_agent.rag_agent(payload.get("prompt", ""))
        else:
            return f"⚠️ Unknown task: {task_name}"
    except Exception as e:
        return f"⚠️ Smart Router Error: {e}"
