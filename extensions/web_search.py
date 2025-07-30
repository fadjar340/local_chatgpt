import os, requests

ENABLE_WEB_SEARCH = os.getenv("ENABLE_WEB_SEARCH", "true").lower() == "true"

def search_web(query: str) -> str:
    if not ENABLE_WEB_SEARCH:
        return "🌐 Web search is disabled."
    try:
        url = f"https://duckduckgo.com/html/?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        results = []
        for line in r.text.split("\n"):
            if "<a rel=\"nofollow\"" in line:
                link = line.split("href=\"")[1].split("\"")[0]
                text = line.split(">")[1].split("<")[0]
                results.append(f"- [{text}]({link})")
                if len(results) >= 5: break
        return "🌐 **Web Search Results:**\n" + "\n".join(results)
    except Exception as e:
        return f"⚠️ Web search failed: {e}"

# Hook into OpenWebUI
try:
    import open_webui
    orig_fn = open_webui.generate_response
    def patched_generate(*args, **kwargs):
        prompt = args[0]
        if "search:" in prompt.lower():
            query = prompt.split("search:",1)[1].strip()
            return search_web(query)
        return orig_fn(*args, **kwargs)
    open_webui.generate_response = patched_generate
    print("🌐 Web Search Plugin Enabled")
except:
    print("⚠️ Web search hook failed")
