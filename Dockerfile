# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install system dependencies (including build tools for hnswlib)
RUN apt-get update && apt-get install -y \
    wget \
    git \
    build-essential \
    cmake \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to latest version for better dependency resolution
RUN pip install --upgrade pip

# Install Python dependencies
# Also allow pip to resolve dependency conflicts automatically
RUN pip install --use-feature=truststore --use-deprecated=legacy-resolver --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Create models folder
RUN mkdir -p /app/models

# Download GPT4All model during build
RUN wget -O /app/models/gpt4all-lora-quantized.bin https://the-eye.eu/public/AI/models/nomic-ai/gpt4all/gpt4all-lora-quantized.bin

# Expose port
EXPOSE 8000

# Start the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
