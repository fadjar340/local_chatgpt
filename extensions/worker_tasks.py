from extensions.celery_config import app

# === Import all agents ===
from extensions.workers import math_agent, search_agent, pcb_agent, rag_agent
from extensions import image_ocr, graph_renderer, research_fetcher, smart_router, sqlite_logger, tex_export


# ✅ === Math Agent Task ===
@app.task(name="math_agent.run")
def run_math(prompt: str) -> str:
    return math_agent.math_agent(prompt)


# ✅ === Web Search Agent Task ===
@app.task(name="search_agent.run")
def run_search(prompt: str) -> str:
    return search_agent.search_agent(prompt)


# ✅ === PCB Agent Task ===
@app.task(name="pcb_agent.run")
def run_pcb(file_path: str) -> str:
    return pcb_agent.pcb_agent(file_path)


# ✅ === RAG Agent Task ===
@app.task(name="rag_agent.run")
def run_rag(prompt: str) -> str:
    return rag_agent.rag_agent(prompt)


# ✅ === OCR Agent Task ===
@app.task(name="ocr_agent.run")
def run_ocr(image_path: str) -> str:
    return image_ocr.extract_text(image_path)


# ✅ === Graph Renderer Agent Task ===
@app.task(name="graph_agent.run")
def run_graph(data: list) -> str:
    return graph_renderer.render_graph(data)


# ✅ === Research Fetcher Agent Task ===
@app.task(name="research_agent.run")
def run_research(query: str) -> str:
    return research_fetcher.fetch_research(query)


# ✅ === Smart Router Agent Task ===
@app.task(name="router_agent.run")
def run_router(task_name: str, payload: dict) -> str:
    return smart_router.route_task(task_name, payload)


# ✅ === SQLite Logger Task ===
@app.task(name="logger_agent.log")
def log_event_task(event_type: str, details: str) -> str:
    return sqlite_logger.log_event(event_type, details)


# ✅ === SQLite Log Fetch Task ===
@app.task(name="logger_agent.fetch_logs")
def fetch_logs_task(project: str = "default", limit: int = 10) -> str:
    try:
        logs = sqlite_logger.fetch_project_logs(project, limit)
        return "🗄️ Project Logs:\n" + "\n".join(logs)
    except Exception as e:
        return f"⚠️ Failed to fetch logs: {e}"


# ✅ === TeX Export Agent Task ===
@app.task(name="tex_export_agent.run")
def run_tex_export(content: str, filename: str = "/app/data/output.tex") -> str:
    return tex_export.export_to_tex(content, filename)
