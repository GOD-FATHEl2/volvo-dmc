# Azure Deployment Guide for VOLVO DMC

This guide will help you deploy your VOLVO DMC application to Azure App Service.

## Prerequisites

1. **Azure Account**: You need an active Azure subscription
2. **Azure CLI**: Install from [here](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
3. **Git** (optional): For version control and CI/CD

## Quick Deployment (Easiest Method)

### For Windows Users:
```powershell
# Navigate to your project directory
cd "c:\Users\NEKKOU\Downloads\mdc generator\VOLVO MDC Generator"

# Run the deployment script
.\deploy-azure.ps1
```

### For Linux/Mac Users:
```bash
# Navigate to your project directory
cd "/path/to/VOLVO MDC Generator"

# Make the script executable
chmod +x deploy-azure.sh

# Run the deployment script
./deploy-azure.sh
```

## Manual Deployment Steps

If you prefer to deploy manually, follow these steps:

### 1. Install Azure CLI
Download and install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

### 2. Login to Azure
```bash
az login
```

### 3. Create Azure Resources
```bash
# Set variables
RESOURCE_GROUP="volvo-dmc-generator-rg"
APP_SERVICE_PLAN="volvo-dmc-generator-plan"
WEB_APP_NAME="volvo-dmc-generator-[YOUR-UNIQUE-ID]"  # Change this to make it unique
LOCATION="West Europe"

# Create resource group
az group create --name $RESOURCE_GROUP --location "$LOCATION"

# Create App Service Plan (Free tier)
az appservice plan create --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP --sku F1 --is-linux

# Create Web App
az webapp create --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --plan $APP_SERVICE_PLAN --runtime "PYTHON:3.11"
```

### 4. Configure the Web App
```bash
# Set startup command
az webapp config set --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --startup-file "gunicorn --bind 0.0.0.0:8000 --workers 4 backend.app:app"

# Set environment variables
az webapp config appsettings set --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --settings \
    FLASK_APP=backend/app.py \
    FLASK_ENV=production \
    SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

### 5. Deploy Your Code
```bash
# Deploy using az webapp up
az webapp up --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --plan $APP_SERVICE_PLAN --runtime "PYTHON:3.11" --location "$LOCATION"
```

## CI/CD with GitHub Actions

To set up automatic deployment when you push code to GitHub:

1. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/volvo-dmc-generator.git
   git push -u origin main
   ```

2. **Get deployment credentials**:
   ```bash
   az webapp deployment list-publishing-profiles --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --xml
   ```

3. **Add the publish profile to GitHub Secrets**:
   - Go to your GitHub repository
   - Settings > Secrets and variables > Actions
   - Add a new secret named `AZUREAPPSERVICE_PUBLISHPROFILE`
   - Paste the XML content from step 2

4. **The GitHub Actions workflow** (`.github/workflows/azure-deploy.yml`) will automatically deploy your app when you push to main branch.

## Important Notes

1. **App Name**: The web app name must be globally unique. If you get an error, try a different name.

2. **Free Tier Limitations**: 
   - The F1 (Free) tier has limitations on compute and daily usage
   - For production, consider upgrading to Basic (B1) or Standard (S1) tier

3. **Custom Domain**: You can add a custom domain in the Azure portal under your App Service > Custom domains

4. **SSL Certificate**: Azure provides free SSL certificates for custom domains

5. **Environment Variables**: All configuration is done through Azure App Service settings, not local files

## Upgrading to Production

For production deployment, consider:

```bash
# Use a better tier for production
az appservice plan create --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP --sku B1 --is-linux

# Or scale up existing plan
az appservice plan update --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP --sku B1
```

## Monitoring and Logs

- **View logs**: Azure Portal > App Service > Log stream
- **Application Insights**: Enable for detailed monitoring
- **Kudu console**: `https://YOUR-APP-NAME.scm.azurewebsites.net`

## Troubleshooting

1. **Deployment fails**: Check the deployment logs in Azure Portal
2. **App doesn't start**: Check Application logs for Python errors
3. **Static files not loading**: Ensure the frontend directory structure is correct
4. **Database persistence**: The JSON database will reset on container restart. Consider using Azure Database for persistent storage.

## Your App URL

After successful deployment, your app will be available at:
`https://[YOUR-WEB-APP-NAME].azurewebsites.net`

## Support

For issues with this deployment, contact:
- **Developer**: Nawoar Ekkou
- **Company**: Volvo Cars Torslanda
- **Year**: 2025
