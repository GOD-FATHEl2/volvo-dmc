# 🚀 Azure Docker Deployment Guide

## Overview
Your VOLVO DMC Generator is now configured for Docker deployment to Azure App Service. This approach ensures all system dependencies (libdmtx, libzbar) are properly installed and available.

## 🐳 Docker Configuration

### Current Setup
- **Dockerfile**: Production-ready with all system dependencies
- **Base Image**: `python:3.11-slim`
- **System Dependencies**: libdmtx, libzbar, gcc, g++
- **Application Server**: Gunicorn (production-ready)
- **Port**: 8000

## 📋 Deployment Options

### Option 1: GitHub Container Registry (Recommended)
**Workflow**: `.github/workflows/azure-deploy.yml`

**Prerequisites**:
1. Azure Web App with Container support
2. GitHub Secrets configured:
   - `AZUREAPPSERVICE_PUBLISHPROFILE`

**Steps**:
1. Go to your GitHub repository
2. Navigate to "Actions" tab
3. Select "Deploy to Azure Web App (Docker)"
4. Click "Run workflow"

### Option 2: Docker Hub + Azure
**Workflow**: `.github/workflows/docker-deploy.yml`

**Prerequisites**:
1. Docker Hub account
2. Azure Web App with Container support
3. GitHub Secrets configured:
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_TOKEN`
   - `AZUREAPPSERVICE_PUBLISHPROFILE`

**Steps**:
1. Go to your GitHub repository
2. Navigate to "Actions" tab
3. Select "Deploy Docker to Azure"
4. Choose "dockerhub" as registry
5. Enter your Azure App Service name
6. Click "Run workflow"

## 🏗️ Azure App Service Setup

### Step 1: Create Azure Web App
```bash
# Using Azure CLI
az webapp create \
  --resource-group your-resource-group \
  --plan your-app-service-plan \
  --name volvo-dmc-generator \
  --deployment-container-image-name ghcr.io/god-fathel2/volvo-dmc-generator/volvo-dmc-generator:latest
```

### Step 2: Configure Container Settings
1. Go to Azure Portal
2. Navigate to your App Service
3. Go to "Deployment Center"
4. Choose "Container Registry"
5. Configure:
   - **Registry**: GitHub Container Registry or Docker Hub
   - **Image**: `ghcr.io/god-fathel2/volvo-dmc-generator/volvo-dmc-generator:latest`
   - **Port**: `8000`

### Step 3: Configure Application Settings
Add these environment variables in Azure Portal:
- `WEBSITES_PORT`: `8000`
- `FLASK_ENV`: `production`
- `FLASK_DEBUG`: `false`

## 🔐 GitHub Secrets Configuration

### Required Secrets
1. **AZUREAPPSERVICE_PUBLISHPROFILE**
   - Download from Azure Portal → App Service → Get publish profile
   - Add entire XML content as secret

2. **DOCKERHUB_USERNAME** (if using Docker Hub)
   - Your Docker Hub username

3. **DOCKERHUB_TOKEN** (if using Docker Hub)
   - Create access token in Docker Hub settings

## 🚀 Manual Docker Deployment

### Build and Push to Docker Hub
```bash
# Build image
docker build -t your-username/volvo-dmc-generator .

# Push to Docker Hub
docker push your-username/volvo-dmc-generator:latest
```

### Deploy to Azure
```bash
# Configure Azure Web App to use your Docker image
az webapp config container set \
  --name volvo-dmc-generator \
  --resource-group your-resource-group \
  --docker-custom-image-name your-username/volvo-dmc-generator:latest
```

## ✅ Verification

### Check Deployment Status
1. Go to Azure Portal
2. Navigate to your App Service
3. Check "Log stream" for deployment logs
4. Visit your app URL

### Expected Logs
```
Container started successfully
Gunicorn starting with 4 workers
Application available on port 8000
```

## 🔧 Troubleshooting

### Common Issues

1. **Port Configuration**
   - Ensure `WEBSITES_PORT` is set to `8000`
   - Check Dockerfile exposes port 8000

2. **Container Registry Access**
   - Verify registry credentials
   - Check image name and tag

3. **Application Startup**
   - Review container logs in Azure Portal
   - Check application dependencies

### Debug Commands
```bash
# Test locally
docker run -p 8000:8000 your-image-name

# Check Azure logs
az webapp log tail --name volvo-dmc-generator --resource-group your-resource-group
```

## 📊 Benefits of Docker Deployment

✅ **Consistent Environment**: Same container runs locally and in Azure
✅ **System Dependencies**: libdmtx and libzbar pre-installed
✅ **Scalability**: Easy to scale with Azure Container Instances
✅ **Version Control**: Tagged images for rollback capability
✅ **Security**: Minimal attack surface with slim base image

## 🎯 Next Steps

1. **Set up Azure Web App** with Container support
2. **Configure GitHub Secrets** for automated deployment
3. **Run the workflow** to deploy your application
4. **Monitor and scale** as needed

Your VOLVO DMC Generator is now ready for production deployment with Docker! 🎉
