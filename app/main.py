from fastapi import FastAPI, Query
from app.query import query_chroma

app = FastAPI(title="Local Search Agent (Render Free)")

@app.get("/")
def home():
    return {"status": "Local Search Agent on Render (Free Plan)"}

@app.get("/search")
def search(q: str = Query(..., description="Search query")):
    return {"query": q, "result": query_chroma(q)}