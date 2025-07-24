# Minimal Dockerfile that WILL work
FROM python:3.11-slim

WORKDIR /app

# Only essential packages
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy and install minimal requirements  
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 1000 -r requirements.txt

# Copy app
COPY . .

# Create directories
RUN mkdir -p backend/static/qrs

# Simple startup with longer timeout
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "300", "--workers", "1", "main:app"]
