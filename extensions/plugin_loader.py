import os, glob, importlib.util
import project_context

PLUGINS_DIR = "/app/extensions"

def load_plugin(path):
    """Safely load a plugin from file."""
    try:
        spec = importlib.util.spec_from_file_location("plugin", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print(f"✅ Loaded Plugin: {os.path.basename(path)}")
    except Exception as e:
        print(f"⚠️ Failed to load plugin {os.path.basename(path)}: {e}")

# ✅ 1. Initialize Multi-Project Context DB
try:
    project_context.init_db()
    print("📂 Multi-Project Context Manager Initialized")
except Exception as e:
    print(f"⚠️ Failed to init project context: {e}")

# ✅ 2. Load GPU auto-config first
gpu_plugin = os.path.join(PLUGINS_DIR, "gpu_auto_config.py")
if os.path.exists(gpu_plugin):
    load_plugin(gpu_plugin)

# ✅ 3. Determine Controller: Auto-Chaining > Parallel > Light
try:
    if os.getenv("ENABLE_AUTO_CHAINING", "false").lower() == "true":
        chaining_plugin = os.path.join(PLUGINS_DIR, "agent_chaining.py")
        if os.path.exists(chaining_plugin):
            load_plugin(chaining_plugin)
            from agent_chaining import chain_controller as controller
            print("🧠 AutoGPT-Style Agent Chaining Enabled")
        else:
            print("⚠️ agent_chaining.py not found, skipping chaining.")
            if os.getenv("ENABLE_PARALLEL_AGENTS", "false").lower() == "true":
                from controller_agent_parallel import controller
                print("🛠 Parallel Multi-Agent Controller Enabled")
            else:
                from controller_agent_light import controller
                print("🛠 Lightweight Multi-Agent Controller Enabled")
    else:
        if os.getenv("ENABLE_PARALLEL_AGENTS", "false").lower() == "true":
            from controller_agent_parallel import controller
            print("🛠 Parallel Multi-Agent Controller Enabled")
        else:
            from controller_agent_light import controller
            print("🛠 Lightweight Multi-Agent Controller Enabled")
except Exception as e:
    print(f"⚠️ Failed to select controller: {e}")

# ✅ 4. Hook into OpenWebUI with Multi-Project Context
try:
    import open_webui
    orig_fn = open_webui.generate_response

    def orchestrator_with_multi_project(*args, **kwargs):
        prompt = args[0]
        project = os.getenv("PROJECT_NAME", "default")

        # Runtime project switching: "project: NAME | your question"
        if prompt.lower().startswith("project:"):
            parts = prompt.split("|", 1)
            if len(parts) == 2:
                project = parts[0].split(":", 1)[1].strip()
                prompt = parts[1].strip()

        # Load last N threads as context
        context = project_context.get_project_context(project)
        full_prompt = f"[Project: {project}]\n[Context]\n{context}\n[User Request]\n{prompt}"

        # Use controller (Auto-Chaining / Parallel / Light)
        result = controller(full_prompt)

        # Save to multi-project DB
        project_context.save_thread(project, prompt, result)
        return result

    open_webui.generate_response = orchestrator_with_multi_project
    print("🔗 Multi-Project Orchestrator Hook Installed")
except Exception as e:
    print(f"⚠️ Failed to hook orchestrator: {e}")

# ✅ 5. Load all other optional plugins (skip explicitly handled ones)
EXCLUDE = {
    "gpu_auto_config.py",
    "agent_chaining.py",
    "web_search.py",
    "tool_controller.py",
    "memory_summarizer.py"
}

for plugin in glob.glob(f"{PLUGINS_DIR}/*.py"):
    name = os.path.basename(plugin)
    if name in EXCLUDE:
        continue
    env_key = "ENABLE_" + name.replace(".py", "").upper()
    if os.getenv(env_key, "true").lower() == "true":
        load_plugin(plugin)
    else:
        print(f"⏸️ Plugin {name} disabled via {env_key}")

# ✅ 6. Explicitly load core plugins (if enabled)
for core in ["web_search.py", "tool_controller.py", "memory_summarizer.py"]:
    env_key = "ENABLE_" + core.replace(".py", "").upper()
    if os.getenv(env_key, "true").lower() == "true":
        load_plugin(os.path.join(PLUGINS_DIR, core))
    else:
        print(f"⏸️ Core Plugin {core} disabled via {env_key}")
