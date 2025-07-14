#!/bin/bash
# Azure Deployment Script for Volvo DMC Generator (Linux/Mac)

echo "🚀 Starting Azure deployment for Volvo DMC Generator..."

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Please install it first:"
    echo "   Download from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

echo "✅ Azure CLI is installed"

# Login to Azure
echo "🔐 Logging in to Azure..."
az login

# Variables
RESOURCE_GROUP="volvo-dmc-generator-rg"
APP_SERVICE_PLAN="volvo-dmc-generator-plan"
WEB_APP_NAME="volvo-dmc-generator"
LOCATION="West Europe"

echo "📦 Creating Azure resources..."

# Create resource group
echo "Creating resource group: $RESOURCE_GROUP"
az group create --name $RESOURCE_GROUP --location "$LOCATION"

# Create App Service Plan
echo "Creating App Service Plan: $APP_SERVICE_PLAN"
az appservice plan create --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP --sku F1 --is-linux

# Create Web App
echo "Creating Web App: $WEB_APP_NAME"
az webapp create --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --plan $APP_SERVICE_PLAN --runtime "PYTHON:3.11"

# Configure startup command
echo "Configuring startup command..."
az webapp config set --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --startup-file "gunicorn --bind 0.0.0.0:8000 --workers 4 backend.app:app"

# Set environment variables
echo "Setting environment variables..."
az webapp config appsettings set --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --settings \
    FLASK_APP=backend/app.py \
    FLASK_ENV=production \
    SCM_DO_BUILD_DURING_DEPLOYMENT=true

# Deploy the code
echo "🚀 Deploying code to Azure..."
az webapp up --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --plan $APP_SERVICE_PLAN --runtime "PYTHON:3.11" --location "$LOCATION"

echo "✅ Deployment completed!"
echo "🌐 Your app is available at: https://$WEB_APP_NAME.azurewebsites.net"
