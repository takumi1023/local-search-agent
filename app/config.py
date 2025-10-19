import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3")
    chroma_dir: str = os.getenv("CHROMA_DIR", ".chroma")
    data_dir: str = os.getenv("DATA_DIR", "data")
    collection_name: str = os.getenv("COLLECTION_NAME", "local-research-agent")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "150"))

    CHROMA_PERSIST_DIR = os.environ.get("CHROMA_PERSIST_DIR", "/data/.chroma")
    OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://<OLLAMA_HOST>:11434")  # replace with your Ollama endpoint

settings = Settings()

