# 📘 Local ChatGPT – Multi-Agent with OpenWebUI, Celery, and Ollama

This project sets up a **powerful local AI environment** using:

- **OpenWebUI** as the interface
- **Celery + Redis** as the task orchestration backend
- **Ollama** as the local LLM server (supports LLaMA3, LLaVA, etc.)
- **Extensions** for OCR, Graph Rendering, Research Fetcher, Smart Router, Logging, TeX Export, and more

---

## ✅ 1. Project Structure

local_chatgpt/
├── docker-compose.yaml
├── Dockerfile.openwebui
├── entrypoint.sh # Ollama model auto-puller
├── Makefile # Automation commands
├── extensions/
│ ├── init.py
│ ├── celery_config.py
│ ├── worker_tasks.py # Celery task definitions
│ ├── smart_router.py # Dynamic task routing
│ ├── sql_logger.py # Project chat logging
│ ├── sqlite_logger.py # Event logging
│ ├── image_ocr.py # OCR using Tesseract
│ ├── graph_renderer.py # Graph rendering with Matplotlib
│ ├── research_fetcher.py # Research paper fetcher (arXiv API)
│ ├── tex_export.py # TeX export
│ └── workers/
│ ├── init.py
│ ├── math_agent.py
│ ├── search_agent.py
│ ├── pcb_agent.py
│ └── rag_agent.py
└── data/
└── (persistent data, logs, outputs)

---

## ✅ 2. Prerequisites

- Docker & Docker Compose installed
- At least **8GB RAM** (for LLaMA3 8B) or **more** (for larger models)
- Enough disk space for models (`./models` volume)

---

## ✅ 3. Quick Start

### 🔹 Build Images

```bash
make build

🔹 Start All Services

make up

🔹 Open WebUI

http://localhost:3000

## ✅ 4. Services Overview

Service Port Purpose
OpenWebUI 3000 Web interface
Ollama 11434 LLM model serving
Redis 6379 Celery broker
Celery Worker - Executes agent tasks

## ✅ 5. Ollama Model Configuration

```
Models are auto-pulled at container startup using entrypoint.sh.

To add more models:
```

export OLLAMA_MODELS="llama3:8b-q4_K_M llama3:70b llava:13b-q4 mistral:7b"
make restart

## ✅ 6. Features

### ✅ Multi-Agent System:

```
math_agent → handles mathematical calculations

search_agent → performs web search

pcb_agent → runs KiCad PCB analysis

rag_agent → queries RAG database

ocr_agent → extracts text from images

graph_agent → renders graphs

research_agent → fetches research papers

router_agent → routes tasks dynamically

logger_agent → logs events to SQLite

tex_export_agent → exports TeX files
```

### ✅ Project-Aware Logging:

```
Logs chat context per project

Stores data in /app/logs/chat_logs.db
```

### ✅ Smart Router:

```
Dynamically dispatches tasks to correct agents
```

### ✅ Celery + Redis Backend:

```
Asynchronous task handling

Scalable worker architecture
```

## ✅ 7. Makefile Commands

Command Description
make build Build all Docker images
make up Start all services
make down Stop all services
make restart Restart the stack
make logs View logs for OpenWebUI + Celery
make logs-ui View only OpenWebUI logs
make logs-celery View only Celery worker logs
make logs-ollama View only Ollama logs
make shell-ui Enter OpenWebUI container
make shell-worker Enter Celery Worker container
make shell-ollama Enter Ollama container
make clean Prune unused Docker images/volumes
make test-math Test math agent via Celery

## ✅ 8. Testing Celery Agents

Example: Test math agent directly:

make test-math

Expected output:

🧮 Math Agent Result:
4

## ✅ 9. Logs & Project Context

```
Chat logs: /app/logs/chat_logs.db

Event logs: /app/data/events.db
```

Query logs via Celery task:

docker exec -it celery-worker celery call logger_agent.fetch_logs --args='["RMFE_Main", 5]'

## ✅ 10. Adding New Agents

```
Create a new file in extensions/workers/

Define a function that handles logic

Register it in worker_tasks.py

(Optional) Add routing in smart_router.py

Rebuild and restart:
```

make restart

🚀 You’re Ready!

With this setup:

```
✅ You have OpenAI-like multi-agent ChatGPT running locally

✅ Ollama handles model inference

✅ Celery coordinates asynchronous tasks

✅ Logs and project contexts are fully supported
```

🔥 Next Upgrade Ideas:

```
Multi-project RAG databases

Distributed workers (Raspberry Pi integration)

Auto-summary of logs per project
```
