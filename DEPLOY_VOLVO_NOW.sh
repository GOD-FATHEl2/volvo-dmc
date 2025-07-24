#!/bin/bash
# DIRECT VOLVO DMC DEPLOYMENT
# Run these commands in Azure Cloud Shell

echo "🎯 DEPLOYING VOLVO DMC TO nawoar.azurecr.io"
echo "============================================="

# Build your VOLVO DMC container
git clone https://github.com/GOD-FATHEl2/volvo-dmc-generator.git
cd volvo-dmc-generator

# Build and push VOLVO DMC
az acr build --registry nawoar --image volvo-dmc:latest .

# Create Container App Environment (if not exists)
az containerapp env create \
  --name volvo-env \
  --resource-group MDC \
  --location "Sweden Central"

# Deploy VOLVO DMC Container App
az containerapp create \
  --name volvo-dmc-app \
  --resource-group MDC \
  --environment volvo-env \
  --image nawoar.azurecr.io/volvo-dmc:latest \
  --target-port 8000 \
  --ingress external \
  --cpu 0.5 \
  --memory 1Gi

echo "🚀 VOLVO DMC DEPLOYED!"
echo "Check Azure Portal for your app URL"
