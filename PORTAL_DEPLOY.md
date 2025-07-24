# 🎯 AZURE PORTAL DEPLOYMENT (No CLI needed)

## Steps:
1. Go to: https://portal.azure.com/#create/Microsoft.ContainerApp
2. Fill in:
   - **Subscription**: Your current subscription
   - **Resource Group**: `MDC`
   - **Container App Name**: `volvo-dmc-app`
   - **Region**: `Sweden Central`

3. **Container Settings**:
   - **Use quickstart image**: No
   - **Image source**: Azure Container Registry
   - **Registry**: `nawoar.azurecr.io`
   - **Image**: `volvo-dmc`
   - **Tag**: `latest`

4. **Ingress**:
   - **Ingress**: Enabled
   - **Ingress traffic**: Accepting traffic from anywhere
   - **Ingress type**: HTTP
   - **Target port**: `8000`

5. **Click**: Review + Create → Create

## Alternative: Use existing app
If you have `dmc-web-app`, just update the image:
- Go to your existing `dmc-web-app` 
- Click **Containers** → **Edit and deploy**
- Change image to: `nawoar.azurecr.io/volvo-dmc:latest`
- Click **Create**
