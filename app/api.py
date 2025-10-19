# src/api.py
from fastapi import FastAPI
from pydantic import BaseModel
import os
from app.graph import run_query  # assumes your workflow function

app = FastAPI()

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
CHROMA_PERSIST_DIR = os.environ.get("CHROMA_PERSIST_DIR", ".chroma")

class QueryIn(BaseModel):
    q: str

@app.post("/query")
def query(payload: QueryIn):
    # call your workflow; ensure it uses OLLAMA_URL and CHROMA_PERSIST_DIR
    result = run_query(payload.q, chroma_dir=CHROMA_PERSIST_DIR, ollama_url=OLLAMA_URL)
    return {"answer": result}
