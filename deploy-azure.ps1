# Azure Deployment Script for Volvo DMC Generator
# This script will help you deploy the application to Azure App Service

Write-Host "🚀 Starting Azure deployment for Volvo DMC Generator..." -ForegroundColor Green

# Check if Azure CLI is installed
try {
    az --version | Out-Null
    Write-Host "✅ Azure CLI is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI is not installed. Please install it first:" -ForegroundColor Red
    Write-Host "   Download from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
}

# Login to Azure
Write-Host "🔐 Logging in to Azure..." -ForegroundColor Yellow
az login

# Set subscription (optional - you can specify your subscription ID)
# az account set --subscription "your-subscription-id"

# Variables
$resourceGroup = "volvo-dmc-generator-rg"
$appServicePlan = "volvo-dmc-generator-plan"
$webAppName = "volvo-dmc-generator"
$location = "West Europe"

Write-Host "📦 Creating Azure resources..." -ForegroundColor Yellow

# Create resource group
Write-Host "Creating resource group: $resourceGroup"
az group create --name $resourceGroup --location $location

# Create App Service Plan (Free tier for testing, change to Basic or Standard for production)
Write-Host "Creating App Service Plan: $appServicePlan"
az appservice plan create --name $appServicePlan --resource-group $resourceGroup --sku F1 --is-linux

# Create Web App
Write-Host "Creating Web App: $webAppName"
az webapp create --name $webAppName --resource-group $resourceGroup --plan $appServicePlan --runtime "PYTHON:3.11"

# Configure startup command
Write-Host "Configuring startup command..."
az webapp config set --name $webAppName --resource-group $resourceGroup --startup-file "gunicorn --bind 0.0.0.0:8000 --workers 4 backend.app:app"

# Set environment variables
Write-Host "Setting environment variables..."
az webapp config appsettings set --name $webAppName --resource-group $resourceGroup --settings @(
    "FLASK_APP=backend/app.py",
    "FLASK_ENV=production",
    "SCM_DO_BUILD_DURING_DEPLOYMENT=true"
)

# Deploy the code
Write-Host "🚀 Deploying code to Azure..." -ForegroundColor Green
az webapp up --name $webAppName --resource-group $resourceGroup --plan $appServicePlan --runtime "PYTHON:3.11" --location $location

Write-Host "✅ Deployment completed!" -ForegroundColor Green
Write-Host "🌐 Your app is available at: https://$webAppName.azurewebsites.net" -ForegroundColor Cyan

# Get deployment credentials for GitHub Actions (optional)
Write-Host "📋 Getting deployment credentials for CI/CD..." -ForegroundColor Yellow
$publishProfile = az webapp deployment list-publishing-profiles --name $webAppName --resource-group $resourceGroup --xml
Write-Host "Publish profile saved. Add this to your GitHub Secrets as 'AZUREAPPSERVICE_PUBLISHPROFILE'" -ForegroundColor Yellow
