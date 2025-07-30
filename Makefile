PROJECT_NAME = local_chatgpt

# Default docker-compose command
DC = docker compose

# ===============================
# 🚀 Main Targets
# ===============================

# 🔹 Build all images without cache
build:
	@echo "🔨 Building all containers..."
	$(DC) build --no-cache

# 🔹 Start all services
up:
	@echo "🚀 Starting $(PROJECT_NAME)..."
	$(DC) up -d

# 🔹 Stop all services
down:
	@echo "🛑 Stopping $(PROJECT_NAME)..."
	$(DC) down

# 🔹 Restart services
restart: down up

# 🔹 Show logs (follow mode)
logs:
	@echo "📜 Showing logs for OpenWebUI and Celery..."
	$(DC) logs -f openwebui celery-worker

# 🔹 Show logs only for Celery
logs-celery:
	$(DC) logs -f celery-worker

# 🔹 Show logs only for OpenWebUI
logs-ui:
	$(DC) logs -f openwebui

# 🔹 Show logs only for Ollama
logs-ollama:
	$(DC) logs -f ollama

# 🔹 Clean unused Docker images/volumes
clean:
	@echo "🧹 Cleaning up unused Docker images and volumes..."
	docker system prune -f
	docker volume prune -f

# ===============================
# 🔍 Debugging Targets
# ===============================

# 🔹 Exec into OpenWebUI container
shell-ui:
	$(DC) exec openwebui /bin/bash

# 🔹 Exec into Celery Worker container
shell-worker:
	$(DC) exec celery-worker /bin/bash

# 🔹 Exec into Ollama container
shell-ollama:
	$(DC) exec ollama /bin/sh

# 🔹 Test Celery Tasks
test-math:
	$(DC) exec celery-worker celery call math_agent.run --args='["2+2"]'

# 🔹 Show Running Containers
ps:
	$(DC) ps
