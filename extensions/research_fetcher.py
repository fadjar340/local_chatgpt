import os
import requests
import arxiv
from semanticscholar import SemanticScholar

PAPER_DIR = "/app/data/research_papers"
os.makedirs(PAPER_DIR, exist_ok=True)

def fetch_arxiv(query="plasma confinement", max_results=5):
    """Fetch latest papers from arXiv"""
    papers = []
    search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.SubmittedDate)
    for result in search.results():
        papers.append({
            "title": result.title,
            "authors": [a.name for a in result.authors],
            "published": str(result.published.date()),
            "pdf": result.pdf_url
        })
    return papers

def download_pdf(url, filename):
    """Download open-access PDF"""
    filepath = os.path.join(PAPER_DIR, filename)
    try:
        r = requests.get(url, timeout=15)
        with open(filepath, "wb") as f:
            f.write(r.content)
        return filepath
    except Exception as e:
        return f"⚠️ PDF download failed: {e}"

def fetch_semantic(query="plasma confinement", max_results=5):
    """Fetch papers from Semantic Scholar"""
    sch = SemanticScholar()
    results = sch.search_paper(query, limit=max_results)
    papers = []
    for r in results["data"]:
        papers.append({
            "title": r.get("title", ""),
            "authors": [a.get("name") for a in r.get("authors", [])],
            "year": r.get("year"),
            "url": r.get("url")
        })
    return papers

def summarize_papers(papers):
    """Return a Markdown summary"""
    md = "📚 **Latest Research Papers**\n"
    for i, p in enumerate(papers, 1):
        md += f"\n{i}. **{p['title']}**\n   - Authors: {', '.join(p['authors'])}\n   - Published: {p.get('published', p.get('year', 'N/A'))}\n   - [PDF]({p.get('pdf', p.get('url', '#'))})"
    return md

try:
    import open_webui
    original_generate = open_webui.generate_response

    def patched_generate(*args, **kwargs):
        prompt = args[0] if args else ""
        if "latest paper" in prompt.lower() or "research on" in prompt.lower():
            topic = prompt.replace("latest paper", "").replace("research on", "").strip()
            papers = fetch_arxiv(topic, max_results=3)
            return summarize_papers(papers)
        return original_generate(*args, **kwargs)

    open_webui.generate_response = patched_generate
    print("🔥 Research Fetcher Enabled (arXiv + Semantic Scholar)")
except Exception as e:
    print(f"⚠️ Failed to enable Research Fetcher: {e}")
