FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Dockerfile snippet
COPY requirements.txt .
# Install required Python packages
RUN pip install --no-cache-dir \
    langchain \
    langchain-ollama \
    langchain-embeddings \
    openai \
    chromadb \
    fastapi \
    uvicorn

COPY . /app

EXPOSE 10000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
