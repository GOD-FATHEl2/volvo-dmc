# 🚀 VOLVO DMC DEPLOYMENT WITH SERVICE PRINCIPAL

## Your Service Principal Details:
- **Application ID**: `5780d8ee-425c-4faa-9e90-0bf178b17692`
- **Tenant ID**: `81fa766e-a349-4867-8bf4-ab35e250a08f`
- **Object ID**: `2a57ab69-fd60-47a4-b226-b4390b0521fe`

## Step 1: First, build your VOLVO DMC image
```bash
az acr build --registry nawoar --image volvo-dmc:latest --source https://github.com/GOD-FATHEl2/volvo-dmc.git
```

## Step 2: Register Microsoft.App provider
```bash
az provider register -n Microsoft.App --wait
```

## Step 3: Create Container App Environment
```bash
az containerapp env create \
  --name volvo-env \
  --resource-group MDC \
  --location "Sweden Central"
```

## Step 4: Deploy VOLVO DMC Container App
```bash
az containerapp create \
  --name volvo-dmc-app \
  --resource-group MDC \
  --environment volvo-env \
  --image nawoar.azurecr.io/volvo-dmc:latest \
  --target-port 8000 \
  --ingress external \
  --cpu 0.5 \
  --memory 1Gi
```

## Alternative: Portal Deployment (If CLI issues persist)
1. Go to: https://portal.azure.com/#create/Microsoft.ContainerApp
2. Use these settings:
   - **Resource Group**: MDC
   - **App Name**: volvo-dmc-app
   - **Region**: Sweden Central
   - **Container Image**: nawoar.azurecr.io/volvo-dmc:latest
   - **Target Port**: 8000
   - **Ingress**: External

## Service Principal Permissions
Your service principal might need these roles:
- Container Apps Contributor
- Azure Container Registry Reader/Contributor

To assign roles:
```bash
az role assignment create \
  --assignee 5780d8ee-425c-4faa-9e90-0bf178b17692 \
  --role "Container Apps Contributor" \
  --scope "/subscriptions/d563d8cd-37a4-4ef8-a495-cc6347ba8124/resourceGroups/MDC"
```

## 🎯 Expected Result
After successful deployment, you'll get a URL like:
`https://volvo-dmc-app.happyocean-xyz.swedencentral.azurecontainerapps.io`

Where you can access your VOLVO DMC Generator with:
- **Login**: admin/admin
- **Generate DMC codes**
- **Camera scanning**
- **File upload**
