# 🚀 VOLVO DMC GitHub Secrets Setup Guide

## Step 1: Add GitHub Secrets
Go to: https://github.com/GOD-FATHEl2/volvo-dmc/settings/secrets/actions

Click "New repository secret" and add these 8 secrets:

### Secret 1: ACR Login Server
- **Name**: `AZURE_ACR_LOGIN_SERVER`
- **Value**: `nawoar.azurecr.io`

### Secret 2: ACR Username  
- **Name**: `AZURE_ACR_USERNAME`  
- **Value**: `Nawoar`

### Secret 3: ACR Password
- **Name**: `AZURE_ACR_PASSWORD`
- **Value**: Get from: `az acr credential show --name nawoar --query passwords[0].value -o tsv`

### Secret 4: Repository Name
- **Name**: `AZURE_ACR_REPO_NAME`
- **Value**: `volvo-dmc`

### Secret 5: Service Principal ID
- **Name**: `AZURE_CLIENT_ID`
- **Value**: Your service principal app ID

### Secret 6: Service Principal Secret
- **Name**: `AZURE_CLIENT_SECRET`
- **Value**: Your service principal password

### Secret 7: Tenant ID
- **Name**: `AZURE_TENANT_ID`
- **Value**: Your Azure tenant ID

### Secret 8: Subscription ID
- **Name**: `AZURE_SUBSCRIPTION_ID`
- **Value**: Your Azure subscription ID

## Step 2: Get the Secret Values
Run these commands in Azure Cloud Shell to get the values:

```bash
# Get ACR password
az acr credential show --name nawoar --query passwords[0].value -o tsv

# Get Azure account info
az account show --query "{subscriptionId:id, tenantId:tenantId}" -o table

# Service principal details (if needed)
az ad sp show --id 5780d8ee-425c-4faa-9e90-0bf178b17692
```

## Step 3: Test the Workflow
After adding all secrets, push any change to trigger the workflow:

```bash
git add .
git commit -m "Test deployment"
git push origin main
```

## Step 4: Access Your App
After deployment: https://volvo-dmc-app.braveground-410ffbbc.swedencentral.azurecontainerapps.io/
Login: admin/admin

🎉 Your VOLVO DMC will be automatically deployed on every code push!
