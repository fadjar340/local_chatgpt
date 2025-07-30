from extensions.web_search import perform_web_search

def search_agent(prompt: str) -> str:
    """
    Search Agent: Performs a web search and returns results.
    """
    try:
        results = perform_web_search(prompt)
        if not results:
            return "🔍 No results found."
        return "🔍 Web Search Results:\n" + "\n".join(results)
    except Exception as e:
        return f"⚠️ Search Agent Error: {e}"
