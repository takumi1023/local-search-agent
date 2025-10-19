import sys
from pathlib import Path

# Add project root to import path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from .query import query_chroma  # adapt to your actual query function

def get_answer(question: str):
    try:
        return query_chroma(question)
    except Exception as e:
        return {"error": str(e)}
