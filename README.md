Local Research Agent (Offline AI Workflow)

Overview
Build an offline AI Research Assistant that searches local markdown/text files, retrieves the most relevant chunks using a local vector DB (Chroma), and summarizes them through a LangGraph agent orchestrated workflow using a local LLM (Ollama).

Features
- Load local documents from `data/` (`.md`, `.txt`)
- Embed and store in Chroma (local persistence)
- LangGraph workflow:
  - Node 1: Input Handler
  - Node 2: Retriever
  - Node 3: Summarizer
  - Node 4: Output Formatter
- Uses a local LLM via Ollama (`llama3` by default) — no paid APIs
- Optional CLI for interactive Q&A

Requirements
- Python 3.10+
- Ollama installed and a model pulled (e.g., `ollama pull llama3`)

Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file (optional) to override defaults:
   ```bash
   OLLAMA_MODEL=llama3
   CHROMA_DIR=.chroma
   ```

Data
- Place your source files in the `data/` directory. Supported: `.md`, `.txt`.

Usage
1. Ingest documents into Chroma:
   ```bash
   python -m src.ingest --data-dir data --persist-dir .chroma
   ```
2. Ask questions via CLI:
   ```bash
   python -m src.cli
   ```
   Or single-shot:
   ```bash
   python -m src.cli --query "Explain how diffusion models work"
   ```

Project Structure
```
src/
  __init__.py
  config.py
  ingest.py
  graph.py
  cli.py
data/
.chroma/
```

Notes
- The system uses LangChain for document IO, Chroma for vector search, and LangGraph for agent control flow.
- Replace the default `OLLAMA_MODEL` in `.env` if desired (e.g., `mistral`, `phi3`).

