from extensions.rag_loader import query_rag

def rag_agent(prompt: str) -> str:
    """
    RAG Agent: Queries the RAG database for context-aware answers.
    """
    try:
        answer = query_rag(prompt)
        return f"📚 RAG Agent Answer:\n{answer}"
    except Exception as e:
        return f"⚠️ RAG Agent Error: {e}"
