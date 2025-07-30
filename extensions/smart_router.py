from extensions.workers import math_agent, search_agent, pcb_agent, rag_agent
from extensions import image_ocr, graph_renderer, research_fetcher, sqlite_logger, tex_export

def route_task(task_name: str, payload: dict) -> str:
    """
    Smart Router: Dynamically routes tasks to the correct agent.
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
        elif task_name == "ocr":
            return image_ocr.extract_text(payload.get("image_path", ""))
        elif task_name == "graph":
            return graph_renderer.render_graph(payload.get("data", []))
        elif task_name == "research":
            return research_fetcher.fetch_research(payload.get("query", ""))
        elif task_name == "logs":
            project = payload.get("project", "default")
            limit = payload.get("limit", 10)
            logs = sqlite_logger.fetch_project_logs(project, limit)
            return "🗄️ Project Logs:\n" + "\n".join(logs)
        elif task_name == "tex_export":
            return tex_export.export_to_tex(payload.get("content", ""), payload.get("filename", "/app/data/output.tex"))
        else:
            return f"⚠️ Unknown task: {task_name}"
    except Exception as e:
        return f"⚠️ Smart Router Error: {e}"
