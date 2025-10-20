# import os
# from dataclasses import dataclass


# @dataclass(frozen=True)
# class Settings:
#     ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3")
#     chroma_dir: str = os.getenv("CHROMA_DIR", ".chroma")
#     data_dir: str = os.getenv("DATA_DIR", "data")
#     collection_name: str = os.getenv("COLLECTION_NAME", "local-research-agent")
#     chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))
#     chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "150"))

#     CHROMA_PERSIST_DIR = os.environ.get("CHROMA_PERSIST_DIR", "/data/.chroma")
#     OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://<OLLAMA_HOST>:11434")  # replace with your Ollama endpoint

# settings = Settings()


# app/config.py

# import os
# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     openai_api_key: str
#     ollama_model: str = "llama3" # <-- Add this line
#     collection_name: str = "local-research-agent"  # if you have one

#     class Config:
#         env_file = ".env"  # optional, for local testing

# settings = Settings()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str  # must be set as environment variable
    collection_name: str = "local-research-agent"

    class Config:
        env_file = ".env"  # optional local .env file for development
        env_file_encoding = "utf-8"

# Instantiate settings
settings = Settings()


