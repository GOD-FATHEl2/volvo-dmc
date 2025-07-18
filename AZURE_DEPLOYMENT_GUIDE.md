# 🚀 Azure App Service Docker Deployment Guide for VOLVO DMC Generator

## 📋 Current Status
- **Repository**: https://github.com/GOD-FATHEl2/volvo-dmc
- **Current Azure Resource**: Azure Static Web App (wonderful-pebble-077934d03.2.azurestaticapps.net)
- **Subscription**: app-7592-online-nonprod-001 (68aae588-09f5-43cf-b974-42c4cc5f7a94)
- **Resource Group**: rg-centralcoreservices-nonprod-001

## 🎯 Deployment Strategy

### Option 1: Use Azure Developer CLI (Recommended)
This will create new resources specifically for Docker deployment:

```bash
# Install Azure Developer CLI if not already installed
# Visit: https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd

# Login to Azure
azd auth login

# Initialize the project
azd init

# Deploy the infrastructure and app
azd up
```

### Option 2: Manual Azure CLI Deployment
Create Azure App Service with container support:

```bash
# Login to Azure
az login

# Set your subscription
az account set --subscription "68aae588-09f5-43cf-b974-42c4cc5f7a94"

# Create resource group (or use existing)
az group create --name rg-volvo-dmc-generator --location "East US"

# Deploy the Bicep template
az deployment group create \
  --resource-group rg-volvo-dmc-generator \
  --template-file infra/main.bicep \
  --parameters @infra/main.parameters.json
```

### Option 3: Use Existing Resource Group
If you want to deploy to your existing resource group:

```bash
# Update the parameters file to use your existing resource group
# Edit infra/main.parameters.json and change:
{
  "resourceGroupName": {
    "value": "rg-centralcoreservices-nonprod-001"
  }
}

# Then deploy
az deployment group create \
  --resource-group rg-centralcoreservices-nonprod-001 \
  --template-file infra/app-service.bicep \
  --parameters appServiceName=volvo-dmc-generator
```

## 🔐 GitHub Actions Setup

### Step 1: Get Azure Service Principal
```bash
# Create service principal for GitHub Actions
az ad sp create-for-rbac \
  --name "volvo-dmc-generator-github" \
  --role contributor \
  --scopes /subscriptions/68aae588-09f5-43cf-b974-42c4cc5f7a94/resourceGroups/rg-volvo-dmc-generator \
  --sdk-auth
```

### Step 2: Configure GitHub Secrets
Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

1. **AZURE_CREDENTIALS**: The JSON output from the service principal creation
2. **AZURE_SUBSCRIPTION_ID**: `68aae588-09f5-43cf-b974-42c4cc5f7a94`
3. **AZURE_RESOURCE_GROUP**: `rg-volvo-dmc-generator` (or your chosen resource group)

### Step 3: Update Workflow
The workflow is now configured to:
- Build Docker image with GitHub Container Registry
- Deploy to Azure App Service with container support
- Handle all libdmtx dependencies in the container

## 🚀 Deployment Steps

### 1. Deploy Infrastructure First
```bash
# Option A: Using AZD (Recommended)
azd up

# Option B: Using Azure CLI
az deployment group create \
  --resource-group rg-volvo-dmc-generator \
  --template-file infra/main.bicep \
  --parameters @infra/main.parameters.json
```

### 2. Run GitHub Actions
1. Go to: https://github.com/GOD-FATHEl2/volvo-dmc/actions
2. Select "Deploy to Azure Web App (Docker)"
3. Click "Run workflow"

### 3. Access Your Application
After deployment, your app will be available at:
- `https://volvo-dmc-generator.azurewebsites.net`

## 🔧 Configuration Details

### Docker Image
- **Registry**: GitHub Container Registry (ghcr.io)
- **Image**: `ghcr.io/god-fathel2/volvo-dmc-generator/volvo-dmc-generator:latest`
- **Port**: 8000
- **Dependencies**: All libdmtx and libzbar dependencies included

### Azure App Service Settings
- **OS**: Linux
- **Container**: Docker
- **Plan**: B1 (Basic, can be upgraded)
- **Always On**: Enabled
- **CORS**: Enabled for all origins

## 🎯 Benefits of This Approach

✅ **Solves libdmtx Issues**: Container includes all system dependencies
✅ **Scalable**: Can upgrade to higher SKUs as needed
✅ **Cost Effective**: B1 plan is suitable for production workloads
✅ **Automated**: GitHub Actions handles build and deployment
✅ **Secure**: Uses managed identity and secure container registry

## 📊 Next Steps

1. **Choose deployment option** (AZD recommended)
2. **Run infrastructure deployment**
3. **Configure GitHub secrets**
4. **Trigger GitHub Actions workflow**
5. **Test your deployed application**

## 🔍 Troubleshooting

### Common Issues
- **Authentication**: Ensure service principal has proper permissions
- **Resource Names**: App Service names must be globally unique
- **Container Startup**: Check Application Insights logs for startup issues

### Useful Commands
```bash
# Check deployment status
az webapp show --name volvo-dmc-generator --resource-group rg-volvo-dmc-generator

# View logs
az webapp log tail --name volvo-dmc-generator --resource-group rg-volvo-dmc-generator

# Test container locally
docker run -p 8000:8000 ghcr.io/god-fathel2/volvo-dmc-generator/volvo-dmc-generator:latest
```

Your VOLVO DMC Generator is now ready for professional Azure deployment! 🎉
