from fastapi import FastAPI, Query
from app.chroma_wrapper import get_answer

app = FastAPI(title="Local Search Agent (Cloud Edition)")

@app.get("/")
def home():
    return {"status": "Local Search Agent on Render (Free Plan)"}

@app.get("/search")
def search(q: str = Query(..., description="Your search query")):
    result = get_answer(q)
    return {"query": q, "result": result}