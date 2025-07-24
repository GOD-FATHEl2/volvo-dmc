#!/bin/bash

# VOLVO DMC Generator - Docker Hub Deployment Script
echo "🚀 Deploying VOLVO DMC Generator to Docker Hub..."

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not available. Using GitHub Actions instead."
    exit 1
fi

# Build the image
echo "🐳 Building Docker image..."
docker build -t volvo-dmc:latest .

# Login to Docker Hub (you'll need to enter your credentials)
echo "🔐 Login to Docker Hub..."
docker login

# Tag for Docker Hub (replace 'yourusername' with your Docker Hub username)
read -p "Enter your Docker Hub username: " DOCKER_USERNAME
docker tag volvo-dmc:latest $DOCKER_USERNAME/volvo-dmc:latest

# Push to Docker Hub
echo "📤 Pushing to Docker Hub..."
docker push $DOCKER_USERNAME/volvo-dmc:latest

echo "✅ Image pushed successfully!"
echo "🌐 Use this in Azure Container Apps:"
echo "   Registry: docker.io (or leave empty)"
echo "   Image: $DOCKER_USERNAME/volvo-dmc"
echo "   Tag: latest"
