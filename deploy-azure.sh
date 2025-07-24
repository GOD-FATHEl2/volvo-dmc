#!/bin/bash

# VOLVO DMC Generator - Azure Container Apps Deployment Script
# This script builds and deploys the Volvo_DMC container to Azure Container Apps

set -e

# Configuration
RESOURCE_GROUP="volvo-dmc-rg"
CONTAINER_APP_NAME="volvo-dmc-app"
CONTAINER_APP_ENV_NAME="volvo-dmc-env"
CONTAINER_REGISTRY="volvoDmcRegistry"
IMAGE_NAME="volvo_dmc"
LOCATION="eastus"

echo "🚀 Starting Volvo DMC deployment to Azure Container Apps..."

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Please install it first."
    exit 1
fi

# Login to Azure (if not already logged in)
echo "🔐 Checking Azure login status..."
if ! az account show &> /dev/null; then
    echo "Please login to Azure:"
    az login
fi

# Create resource group if it doesn't exist
echo "📦 Creating resource group: $RESOURCE_GROUP"
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create container registry if it doesn't exist
echo "🏗️ Creating container registry: $CONTAINER_REGISTRY"
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $CONTAINER_REGISTRY \
  --sku Basic \
  --admin-enabled true

# Get registry credentials
echo "🔑 Getting registry credentials..."
REGISTRY_PASSWORD=$(az acr credential show --name $CONTAINER_REGISTRY --query "passwords[0].value" --output tsv)
REGISTRY_USERNAME=$(az acr credential show --name $CONTAINER_REGISTRY --query "username" --output tsv)

# Build and push Docker image
echo "🐳 Building and pushing Docker image..."
az acr build \
  --registry $CONTAINER_REGISTRY \
  --image $IMAGE_NAME:latest \
  --image $IMAGE_NAME:$(date +%Y%m%d-%H%M%S) \
  .

# Create Container Apps environment
echo "🌍 Creating Container Apps environment: $CONTAINER_APP_ENV_NAME"
az containerapp env create \
  --name $CONTAINER_APP_ENV_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

# Create container app
echo "📱 Creating container app: $CONTAINER_APP_NAME"
az containerapp create \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINER_APP_ENV_NAME \
  --image $CONTAINER_REGISTRY.azurecr.io/$IMAGE_NAME:latest \
  --target-port 8000 \
  --ingress external \
  --registry-server $CONTAINER_REGISTRY.azurecr.io \
  --registry-username $REGISTRY_USERNAME \
  --registry-password $REGISTRY_PASSWORD \
  --cpu 0.5 \
  --memory 1Gi \
  --min-replicas 1 \
  --max-replicas 5 \
  --env-vars PORT=8000 FLASK_ENV=production

# Get the container app URL
echo "🌐 Getting container app URL..."
CONTAINER_APP_URL=$(az containerapp show \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn \
  --output tsv)

echo ""
echo "✅ Deployment completed successfully!"
echo "🌐 Your Volvo DMC Generator is available at: https://$CONTAINER_APP_URL"
echo "📊 Monitor your app in the Azure portal: https://portal.azure.com"
echo ""
echo "🔧 Useful commands:"
echo "  View logs: az containerapp logs show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP"
echo "  Update app: az containerapp update --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --image $CONTAINER_REGISTRY.azurecr.io/$IMAGE_NAME:latest"
echo "  Delete app: az containerapp delete --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP"
