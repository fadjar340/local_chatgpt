import requests

def fetch_research(query: str) -> str:
    """
    Fetch research papers using arXiv API.
    """
    try:
        url = f"http://export.arxiv.org/api/query?search_query={query}&start=0&max_results=3"
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return f"⚠️ Research Fetch Error: HTTP {r.status_code}"
        return f"🔬 Research Results for '{query}':\n{r.text[:1000]}..."
    except Exception as e:
        return f"⚠️ Research Fetch Error: {e}"
