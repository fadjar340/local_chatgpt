import os
import sqlite3
from datetime import datetime

# ✅ Use ENV for DB path (default: /app/logs/chat_logs.db)
DB_PATH = os.getenv("SQLITE_LOG_DB", "/app/logs/chat_logs.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# ✅ Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project TEXT,
        timestamp TEXT,
        user_input TEXT,
        model_response TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# ✅ Log interaction with optional project name
def log_interaction(user_input: str, response: str, project: str = "default"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (project, timestamp, user_input, model_response) VALUES (?, ?, ?, ?)",
                   (project, datetime.now().isoformat(), user_input, response))
    conn.commit()
    conn.close()
    print(f"💾 Conversation logged to SQLite [{project}]")

# ✅ Fetch last N logs for a project
def fetch_project_logs(project: str = "default", limit: int = 10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, user_input, model_response FROM logs WHERE project=? ORDER BY id DESC LIMIT ?", (project, limit))
    rows = cursor.fetchall()
    conn.close()
    return [f"{ts} | Q: {ui[:80]} → A: {mr[:120]}..." for ts, ui, mr in rows]

# ✅ Hook into OpenWebUI
try:
    import open_webui
    from extensions import project_context  # Optional: integrate project context
    original_fn = open_webui.generate_response

    def patched_generate(*args, **kwargs):
        user_input = args[0]
        project = os.getenv("PROJECT_NAME", "default")
        context = project_context.get_project_context(project) if "project_context" in globals() else ""
        final_prompt = f"[Project: {project}]\n{context}\n{user_input}"
        resp = original_fn(final_prompt, **kwargs)
        log_interaction(user_input, resp, project)
        return resp

    open_webui.generate_response = patched_generate
    print("✅ SQLite Logger with Project Context Enabled")
except Exception as e:
    print(f"⚠️ SQLite Logger failed to initialize: {e}")
