import os
import chromadb
from chromadb.utils import embedding_functions

ENABLE_RAG = os.getenv("ENABLE_RAG", "false").lower() == "true"
CHROMA_DIR = "/app/data/rag_store"

if ENABLE_RAG:
    os.makedirs(CHROMA_DIR, exist_ok=True)
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_or_create_collection(
        "knowledge_base",
        embedding_function=embedding_functions.DefaultEmbeddingFunction()
    )
    print("🧠 RAG Enabled → ChromaDB Ready")

def add_document(doc_id: str, content: str, metadata: dict = None):
    if ENABLE_RAG:
        collection.add(documents=[content], metadatas=[metadata or {}], ids=[doc_id])

def query_knowledge(query: str, n_results=3):
    if ENABLE_RAG:
        results = collection.query(query_texts=[query], n_results=n_results)
        return [doc for doc in results.get("documents", [])]
    return []
