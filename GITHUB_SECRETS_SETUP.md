# 🚀 VOLVO DMC GitHub Secrets Setup Guide

## Step 1: Add GitHub Secrets
Go to: https://github.com/GOD-FATHEl2/volvo-dmc/settings/secrets/actions

Click "New repository secret" and add these 8 secrets:

### Secret 1:
- **Name**: `AZURE_ACR_LOGIN_SERVER`
- **Value**: `nawoar.azurecr.io`

### Secret 2:
- **Name**: `AZURE_ACR_USERNAME`  
- **Value**: `Nawoar`

### Secret 3:
- **Name**: `AZURE_ACR_PASSWORD`
- **Value**: `xdjMTQIoIxTqzqBKSK/NjOoULKn4PDExXgJ28WkPbS+ACRCthOAm`

### Secret 4:
- **Name**: `AZURE_ACR_REPO_NAME`
- **Value**: `volvo-dmc`

### Secret 5:
- **Name**: `AZURE_CLIENT_ID`
- **Value**: `5780d8ee-425c-4faa-9e90-0bf178b17692`

### Secret 6:
- **Name**: `AZURE_CLIENT_SECRET`
- **Value**: `qV48Q~HELQnc2Hsq8ARbSo1ZGCJR~pWZ6tNV3b69`

### Secret 7:
- **Name**: `AZURE_TENANT_ID`
- **Value**: `81fa766e-a349-4867-8bf4-ab35e250a08f`

### Secret 8:
- **Name**: `AZURE_SUBSCRIPTION_ID`
- **Value**: `57a382d9-18ec-4c9c-ab89-c7dad846eb55`

## Step 2: Push the Workflow
After adding all secrets, the workflow will automatically deploy your VOLVO DMC app!

## Step 3: Access Your App
After deployment: https://volvo-dmc-app.braveground-410ffbbc.swedencentral.azurecontainerapps.io/
Login: admin/admin

🎉 Your VOLVO DMC will be live and automatically updated on every code push!
