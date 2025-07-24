# Azure Permission Request - VOLVO DMC Generator

**To:** Azure Administrator  
**From:** NEKKOU@volvocars.com  
**Subject:** Azure Container Registry Permissions Required

## Issue
I'm trying to deploy the VOLVO DMC Generator application to Azure Container Apps but getting permission errors:

```
Error: Authorization failed for roleAssignments
User: NEKKOU@volvocars.com
Missing Permission: Microsoft.Authorization/roleAssignments/write
Resource: ekkou.azurecr.io
```

## Required Permissions
Please grant the following permissions:

```bash
# Container Registry Push permission
az role assignment create \
  --assignee NEKKOU@volvocars.com \
  --role "AcrPush" \
  --scope /subscriptions/57a382d9-18ec-4c9c-ab89-c7dad846eb55/resourceGroups/rg-centralcoreservices-nonprod-001/providers/Microsoft.ContainerRegistry/registries/ekkou

# Container Apps Contributor permission
az role assignment create \
  --assignee NEKKOU@volvocars.com \
  --role "Contributor" \
  --scope /subscriptions/57a382d9-18ec-4c9c-ab89-c7dad846eb55/resourceGroups/rg-centralcoreservices-nonprod-001
```

## Alternative: Deploy for Me
If you prefer to deploy it yourself:

```bash
# Build and deploy the container app
az containerapp create \
  --name volvo-dmc-generator \
  --resource-group rg-centralcoreservices-nonprod-001 \
  --environment managedEnvironment-rgcentralcorese-ad94 \
  --image ekkou.azurecr.io/volvo-dmc:latest \
  --target-port 8000 \
  --ingress external \
  --cpu 0.5 \
  --memory 1.0Gi \
  --min-replicas 1 \
  --max-replicas 3
```

## Project Details
- **Application:** VOLVO DMC Generator (Data Matrix Code generator)
- **Repository:** https://github.com/GOD-FATHEl2/volvo-dmc-generator
- **Purpose:** Manufacturing DMC code generation and scanning

Thank you for your assistance!
