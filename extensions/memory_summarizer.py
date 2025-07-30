import os, sqlite3
from datetime import datetime, timedelta

DB_PATH = "/app/data/chat_logs.db"
SUMMARY_FILE = "/app/data/memory_summary.txt"

def summarize_logs():
    if not os.path.exists(DB_PATH):
        return "⚠️ No logs to summarize."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, user_input, model_response FROM logs ORDER BY id DESC LIMIT 50")
    rows = cursor.fetchall()
    conn.close()
    
    summary = "🧠 **Conversation Memory Summary**\n"
    for ts, user, resp in reversed(rows):
        summary += f"\n[{ts}] Q: {user}\nA: {resp[:300]}...\n"
    
    with open(SUMMARY_FILE, "w") as f:
        f.write(summary)
    print("💾 Memory summarized and saved.")

try:
    import open_webui
    orig_fn = open_webui.generate_response
    def patched(*args, **kwargs):
        summarize_logs()
        return orig_fn(*args, **kwargs)
    open_webui.generate_response = patched
    print("🧠 Memory Summarizer Enabled")
except:
    print("⚠️ Failed to hook memory summarizer")
