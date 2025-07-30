#!/bin/sh
set -e

# ✅ Models to pull: from ENV or default list
MODELS="${OLLAMA_MODELS:-llama3:8b-q4_K_M llama3:70b llava:13b-q4}"

echo "🔥 Starting Ollama Model Loader"
echo "📦 Models to check: $MODELS"

for model in $MODELS; do
    echo "🔍 Checking $model..."
    if ollama list | grep -q "$model"; then
        echo "✔️ $model already installed, skipping pull."
    else
        echo "⬇️ Pulling $model ..."
        if ollama pull "$model"; then
            echo "✅ Successfully pulled $model"
        else
            echo "⚠️ Failed to pull $model (continuing...)"
        fi
    fi
done

echo "🚀 Starting Ollama Server..."
exec /bin/ollama serve
