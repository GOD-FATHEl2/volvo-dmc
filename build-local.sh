#!/bin/bash

# VOLVO DMC Generator - Local Docker Build Script
# This script builds the Volvo_DMC container locally

set -e

IMAGE_NAME="volvo_dmc"
CONTAINER_NAME="volvo-dmc-container"

echo "🚀 Building Volvo DMC Docker container..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Build the Docker image
echo "🐳 Building Docker image: $IMAGE_NAME"
docker build -t $IMAGE_NAME:latest .

echo "✅ Docker image built successfully!"
echo ""
echo "🔧 Available commands:"
echo "  Run container: docker run -p 8000:8000 --name $CONTAINER_NAME $IMAGE_NAME:latest"
echo "  Run in background: docker run -d -p 8000:8000 --name $CONTAINER_NAME $IMAGE_NAME:latest"
echo "  View logs: docker logs $CONTAINER_NAME"
echo "  Stop container: docker stop $CONTAINER_NAME"
echo "  Remove container: docker rm $CONTAINER_NAME"
echo ""
echo "🌐 After running, access your app at: http://localhost:8000"
