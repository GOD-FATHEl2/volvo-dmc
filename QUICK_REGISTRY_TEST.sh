#!/bin/bash
# FASTEST VOLVO DMC DEPLOYMENT - Azure Cloud Shell Ready

echo "🚀 VOLVO DMC DEPLOYMENT - nawoar.azurecr.io"
echo "=========================================="

# Step 1: Build directly from GitHub (no Docker daemon needed)
echo "Building VOLVO DMC from GitHub..."
az acr build --registry nawoar \
  --image volvo-dmc:latest \
  --source https://github.com/GOD-FATHEl2/volvo-dmc.git

echo "✅ VOLVO DMC built and pushed to nawoar.azurecr.io!"
echo "🎯 Image: nawoar.azurecr.io/volvo-dmc:latest"

# Step 2: Create Container App Environment (if needed)
echo "Creating container environment..."
az containerapp env create \
  --name volvo-env \
  --resource-group MDC \
  --location "Sweden Central" || echo "Environment may already exist"

# Step 3: Deploy VOLVO DMC Container App
echo "Deploying VOLVO DMC Container App..."
az containerapp create \
  --name volvo-dmc-app \
  --resource-group MDC \
  --environment volvo-env \
  --image nawoar.azurecr.io/volvo-dmc:latest \
  --target-port 8000 \
  --ingress external \
  --cpu 0.5 \
  --memory 1Gi

echo "� VOLVO DMC DEPLOYED!"
echo "Check Azure Portal → Container Apps → volvo-dmc-app for URL"
