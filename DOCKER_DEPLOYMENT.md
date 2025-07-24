# VOLVO DMC Generator - Container Deployment Guide

## 🐳 Docker Container: `volvo_dmc`

This guide explains how to build and deploy the VOLVO DMC Generator as a Docker container named `volvo_dmc` to various platforms.

## 📋 Prerequisites

- Docker installed and running
- Azure CLI (for Azure deployment)
- Git (for GitHub integration)

## 🏗️ Building the Container Locally

### Option 1: Using the build script
```bash
./build-local.sh
```

### Option 2: Manual build
```bash
docker build -t volvo_dmc:latest .
```

### Running the container locally
```bash
# Run interactively
docker run -p 8000:8000 --name volvo-dmc-container volvo_dmc:latest

# Run in background
docker run -d -p 8000:8000 --name volvo-dmc-container volvo_dmc:latest

# Access the application
open http://localhost:8000
```

## 🚀 Deploying to Azure Container Apps

### Option 1: Using the deployment script
```bash
./deploy-azure.sh
```

### Option 2: Manual deployment

1. **Create Azure resources:**
```bash
# Create resource group
az group create --name volvo-dmc-rg --location eastus

# Create container registry
az acr create --resource-group volvo-dmc-rg --name volvoDmcRegistry --sku Basic

# Create container apps environment
az containerapp env create --name volvo-dmc-env --resource-group volvo-dmc-rg --location eastus
```

2. **Build and push image:**
```bash
az acr build --registry volvoDmcRegistry --image volvo_dmc:latest .
```

3. **Deploy container app:**
```bash
az containerapp create \
  --name volvo-dmc-app \
  --resource-group volvo-dmc-rg \
  --environment volvo-dmc-env \
  --image volvoDmcRegistry.azurecr.io/volvo_dmc:latest \
  --target-port 8000 \
  --ingress external \
  --registry-server volvoDmcRegistry.azurecr.io
```

## 📱 GitHub Actions CI/CD

The repository includes a GitHub Actions workflow that automatically:

1. **Builds** the Docker image on every push
2. **Pushes** to Azure Container Registry  
3. **Deploys** to Azure Container Apps

### Setup GitHub Secrets

Add these secrets to your GitHub repository:

- `AZURE_CREDENTIALS`: Azure service principal credentials
- `AZURE_CLIENT_ID`: Azure client ID
- `AZURE_CLIENT_SECRET`: Azure client secret

### Trigger deployment
```bash
git add .
git commit -m "Deploy Volvo DMC container"
git push origin main
```

## 🔧 Container Configuration

### Environment Variables
- `PORT`: Application port (default: 8000)
- `FLASK_ENV`: Flask environment (production/development)
- `PYTHONPATH`: Python path configuration

### Resource Requirements
- **CPU**: 0.5 cores
- **Memory**: 1GB
- **Storage**: Ephemeral (container filesystem)

### Ports
- **Container Port**: 8000
- **External Port**: 80/443 (via load balancer)

## 📊 Monitoring and Logs

### View container logs
```bash
# Local Docker
docker logs volvo-dmc-container

# Azure Container Apps
az containerapp logs show --name volvo-dmc-app --resource-group volvo-dmc-rg
```

### Health Check
The container includes a health check endpoint at `/` that returns HTTP 200 when healthy.

## 🛠️ Troubleshooting

### Common Issues

1. **Container won't start**
   - Check logs: `docker logs volvo-dmc-container`
   - Verify port 8000 is available
   - Ensure all dependencies are installed

2. **Azure deployment fails**
   - Verify Azure CLI login: `az account show`
   - Check resource group exists
   - Ensure sufficient Azure credits/permissions

3. **GitHub Actions fails**
   - Check repository secrets are configured
   - Verify Azure service principal has proper permissions
   - Review workflow logs in GitHub Actions tab

### Getting Help

- Check application logs for specific error messages
- Verify all required files are present in the container
- Test locally before deploying to Azure

## 🔄 Updating the Deployment

### Local updates
```bash
# Rebuild image
docker build -t volvo_dmc:latest .

# Stop and remove old container
docker stop volvo-dmc-container
docker rm volvo-dmc-container

# Run new container
docker run -d -p 8000:8000 --name volvo-dmc-container volvo_dmc:latest
```

### Azure updates
```bash
# Update via Azure CLI
az containerapp update \
  --name volvo-dmc-app \
  --resource-group volvo-dmc-rg \
  --image volvoDmcRegistry.azurecr.io/volvo_dmc:latest
```

## 📝 Application Features

The containerized VOLVO DMC Generator includes:

- ✅ **DMC Code Generation**: Generate Data Matrix Codes with custom prefixes
- ✅ **QR Code Reading**: Upload images to decode DMC/QR codes  
- ✅ **Live Camera Scanning**: Real-time camera-based code detection
- ✅ **Export Functions**: Download codes as PDF or Excel
- ✅ **Print Support**: Direct printing of generated codes
- ✅ **History Tracking**: Keep track of generated and scanned codes
- ✅ **Responsive Design**: Works on desktop and mobile devices

## 🔐 Security

- Container runs as non-root user
- No sensitive data stored in container
- HTTPS enabled in production deployments
- Regular security updates via base image updates
