# app/main.py
from fastapi import FastAPI, Query
from app.query import query_chroma

app = FastAPI(title="Local Search Agent (Free LLM & Embeddings)")

@app.get("/")
def home():
    return {"status": "Local Search Agent running with free LLM & embeddings"}

@app.get("/search")
def search(q: str = Query(..., description="Search query")):
    result = query_chroma(q)
    return {"query": q, "result": result}
