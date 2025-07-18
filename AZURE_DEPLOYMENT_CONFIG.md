# Azure App Service Deployment Configuration

## Application Details
- **App Name**: DMC
- **Domain**: dmc-ggbxhgeaajb8ffed.swedencentral-01.azurewebsites.net
- **Resource Group**: rg-centralcoreservices-nonprod-001
- **Location**: Sweden Central
- **Runtime**: Python 3.11
- **OS**: Linux
- **Plan**: ASP-rgcentralcoreservicesnonprod001-bbb0 (F1: Free tier)

## Deployment Settings

### Startup Command
```
python run_production.py
```

### Application Settings (Environment Variables)
```
SCM_DO_BUILD_DURING_DEPLOYMENT=true
WEBSITES_ENABLE_APP_SERVICE_STORAGE=false
```

### Required Files
- ✅ `run_production.py` - Production startup script
- ✅ `requirements-production.txt` - Dependencies
- ✅ `runtime.txt` - Python version (python-3.11.9)

### Deployment Steps
1. Connect GitHub repository to Azure App Service
2. Configure deployment center with GitHub
3. Set startup command: `python run_production.py`
4. Deploy from main branch

### Health Check
- Endpoint: `/` (home page)
- Expected: HTTP 200 response
- Health check URL: https://dmc-ggbxhgeaajb8ffed.swedencentral-01.azurewebsites.net

### File Structure for Azure
```
/
├── backend/
│   ├── app.py
│   ├── generate_qr.py
│   ├── read_dmc.py
│   ├── static/
│   └── templates/
├── run_production.py
├── requirements-production.txt
├── runtime.txt
└── README.md
```

### Copyright Information
© 2025 VOLVO Cars. All rights reserved. Made by: Nawoar Ekkou
