#!/bin/bash

echo "🧪 Testing Azure Container Registry: nawoar.azurecr.io"
echo "This script will help you test your registry before full deployment"

echo ""
echo "📋 STEP 1: Manual Registry Test (Run these commands in Azure Cloud Shell)"
echo "========================================================================="
echo "az acr login --name nawoar"
echo "docker pull hello-world"
echo "docker tag hello-world nawoar.azurecr.io/test:v1"
echo "docker push nawoar.azurecr.io/test:v1"
echo ""

echo "📋 STEP 2: Test with Azure Container Apps"
echo "========================================="
echo "az containerapp create \\"
echo "  --name test-app \\"
echo "  --resource-group MDC \\"
echo "  --environment-name volvo-env \\"
echo "  --image nawoar.azurecr.io/test:v1 \\"
echo "  --target-port 80 \\"
echo "  --ingress external"
echo ""

echo "📋 STEP 3: GitHub Actions Test (Automatic)"
echo "==========================================="
echo "We can trigger the GitHub Actions workflow to test the registry"
echo "The workflow will build and push your VOLVO DMC app automatically"
echo ""

echo "✅ Once Step 1 works, we know your registry is properly configured!"
echo "💡 Then we can proceed with your full VOLVO DMC application deployment"
