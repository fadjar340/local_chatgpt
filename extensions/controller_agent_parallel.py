from worker_tasks import run_math, run_search, run_pcb, run_rag
from celery.result import AsyncResult

def controller(prompt: str) -> str:
    lower = prompt.lower()
    tasks = []

    if "calculate" in lower or any(op in lower for op in ["^", "*", "+", "="]):
        tasks.append(run_math.delay(prompt))
    if "search:" in lower:
        tasks.append(run_search.delay(prompt))
    if "pcb" in lower or ".kicad" in lower:
        tasks.append(run_pcb.delay(prompt))
    if "document" in lower or "research" in lower:
        tasks.append(run_rag.delay(prompt))

    if not tasks:
        return "🤖 Controller: No agent triggered, using default LLM."

    results = [AsyncResult(t.id).get(timeout=30) for t in tasks]
    return "\n\n".join(results)
