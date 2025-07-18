# 🐳 Docker Containerization Guide for VOLVO DMC Generator

## Quick Start

### 1. Build the Docker Image
```bash
docker build -t volvo-dmc-generator .
```

### 2. Run the Container
```bash
docker run -p 8000:8000 volvo-dmc-generator
```

### 3. Access the Application
Open your browser and navigate to: `http://localhost:8000`

## 🔧 Advanced Docker Commands

### Build with Custom Tag
```bash
docker build -t volvo-dmc-generator:latest .
```

### Run with Environment Variables
```bash
docker run -p 8000:8000 \
  -e FLASK_ENV=production \
  -e FLASK_DEBUG=false \
  volvo-dmc-generator
```

### Run in Background (Detached Mode)
```bash
docker run -d -p 8000:8000 --name volvo-dmc volvo-dmc-generator
```

### View Container Logs
```bash
docker logs volvo-dmc
```

### Stop the Container
```bash
docker stop volvo-dmc
```

### Remove the Container
```bash
docker rm volvo-dmc
```

## 🚀 Cloud Deployment Options

### Azure Container Instances
```bash
# Build and push to Azure Container Registry
az acr build --registry <your-registry> --image volvo-dmc-generator .

# Deploy to Azure Container Instances
az container create \
  --resource-group <your-resource-group> \
  --name volvo-dmc-generator \
  --image <your-registry>.azurecr.io/volvo-dmc-generator:latest \
  --port 8000 \
  --dns-name-label volvo-dmc-generator
```

### Docker Hub
```bash
# Tag for Docker Hub
docker tag volvo-dmc-generator <your-username>/volvo-dmc-generator:latest

# Push to Docker Hub
docker push <your-username>/volvo-dmc-generator:latest
```

### Azure Container Apps
```bash
# Deploy to Azure Container Apps
az containerapp create \
  --name volvo-dmc-generator \
  --resource-group <your-resource-group> \
  --environment <your-environment> \
  --image <your-registry>.azurecr.io/volvo-dmc-generator:latest \
  --target-port 8000 \
  --ingress external
```

## 📊 Container Features

### ✅ What's Included
- **Python 3.11** runtime environment
- **System dependencies** for DMC processing (libdmtx, libzbar)
- **Flask application** with all routes
- **Gunicorn WSGI server** for production
- **Minimal dependencies** for optimized image size
- **Health checks** and proper logging

### 🔧 Container Specifications
- **Base Image**: `python:3.11-slim`
- **Port**: 8000
- **Workers**: 4 gunicorn workers
- **Environment**: Production-ready

### 📁 Application Structure in Container
```
/app/
├── backend/
│   ├── app.py (Flask application)
│   ├── static/ (CSS, JS, QR codes)
│   └── templates/ (HTML templates)
├── requirements-minimal.txt
└── Dockerfile
```

## 🛠️ Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   docker run -p 8001:8000 volvo-dmc-generator
   ```

2. **Permission denied**
   ```bash
   sudo docker build -t volvo-dmc-generator .
   ```

3. **Container won't start**
   ```bash
   docker logs <container-id>
   ```

### Health Check
```bash
# Check if the application is running
curl http://localhost:8000
```

## 🌟 Benefits of Containerization

- **Consistency**: Same environment everywhere
- **Scalability**: Easy to scale horizontally
- **Portability**: Deploy on any Docker-compatible platform
- **Isolation**: Dependencies are contained
- **Production-ready**: Optimized for production use

## 🎯 Next Steps

1. **Test locally** with Docker
2. **Push to container registry** (Azure ACR, Docker Hub)
3. **Deploy to cloud platform** (Azure Container Apps, AWS ECS, etc.)
4. **Set up CI/CD** for automated deployments
