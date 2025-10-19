# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies (corrected)
RUN pip install --no-cache-dir \
    langchain \
    langchain-ollama \
    langchain-community \
    chromadb \
    fastapi \
    uvicorn[standard] \
    openai

# Expose the port Render uses
EXPOSE 10000

# Start the FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
