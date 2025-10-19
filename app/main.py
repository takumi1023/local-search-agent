from fastapi import FastAPI, Query
from app.chroma_wrapper import get_answer

app = FastAPI(title="Local Search Agent (Render Free)")

@app.get("/")
def home():
    return {"status": "Local Search Agent on Render (Free Plan)"}

@app.get("/search")
def search(q: str = Query(..., description="Search query")):
    return {"query": q, "result": get_answer(q)}
