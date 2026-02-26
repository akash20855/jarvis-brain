# Jarvis Brain - Docker Container
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt .
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user for security
RUN useradd -m -u 1000 jarvis && \
    chown -R jarvis:jarvis /app

USER jarvis

# Expose dashboard port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')" || exit 1

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV JARVIS_MODE=docker

# Start Jarvis
CMD ["python", "-m", "core.main"]
