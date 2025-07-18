# 🚨 Azure App Service Troubleshooting Guide

## Application Error Diagnosis

Your application is showing: **Application Error**
URL: https://dmc-ggbxhgeaajb8ffed.swedencentral-01.azurewebsites.net/

## 🔍 Diagnostic Steps

### Step 1: Check Application Logs
1. **Azure Portal** → Your App Service (DMC)
2. **Monitoring** → **Log stream** (real-time logs)
3. **Monitoring** → **App Service logs** → Enable and check

### Step 2: Common Issues & Solutions

#### Issue 1: Startup Command Problem
**Current Setting Should Be:**
```
python run_production.py
```

**How to Fix:**
1. Azure Portal → App Service → **Configuration** → **General Settings**
2. **Startup Command**: `python run_production.py`
3. **Save** and **Restart** the app

#### Issue 2: Missing Dependencies
**Solution:**
Ensure `requirements-production.txt` contains:
```
Flask==3.1.1
flask-cors==6.0.1
Werkzeug==3.1.3
pylibdmtx==0.1.10
pillow==11.3.0
openpyxl==3.1.5
fpdf==1.7.2
gunicorn==21.2.0
requests==2.32.3
```

#### Issue 3: Build Configuration
**Application Settings to Add:**
1. Azure Portal → App Service → **Configuration** → **Application settings**
2. Add these settings:

```
SCM_DO_BUILD_DURING_DEPLOYMENT = true
WEBSITES_ENABLE_APP_SERVICE_STORAGE = false
PYTHONPATH = /home/site/wwwroot
WEBSITE_RUN_FROM_PACKAGE = 0
```

#### Issue 4: Python Runtime
**Check Runtime Stack:**
1. Azure Portal → App Service → **Configuration** → **General Settings**
2. **Runtime stack**: Python
3. **Version**: 3.11

### Step 3: Quick Fix - Alternative Startup Commands

If `python run_production.py` doesn't work, try these alternatives:

**Option 1: Direct Gunicorn**
```
cd backend && gunicorn --bind 0.0.0.0:$PORT app:app
```

**Option 2: Simple Python**
```
cd backend && python app.py
```

**Option 3: With Environment**
```
cd /home/site/wwwroot && python run_production.py
```

### Step 4: Check File Structure
Ensure your deployment has this structure:
```
/home/site/wwwroot/
├── backend/
│   ├── app.py
│   ├── generate_qr.py
│   ├── read_dmc.py
│   ├── static/
│   └── templates/
├── run_production.py
├── requirements-production.txt
└── runtime.txt
```

## 🛠️ Immediate Fix Actions

### Action 1: Update Startup Command
1. Go to Azure Portal
2. Find your App Service: **DMC**
3. **Configuration** → **General Settings**
4. **Startup Command**: `cd backend && gunicorn --bind 0.0.0.0:$PORT app:app`
5. **Save** and **Restart**

### Action 2: Enable Logging
1. **App Service logs** → **Enable**
2. **Application Logging**: On
3. **Level**: Information
4. **Save**

### Action 3: Check Build Logs
1. **Deployment Center** → **Logs**
2. Look for Python package installation errors
3. Check if pylibdmtx failed to install

## 📞 Quick Diagnostics Commands

If you have access to **Kudu Console** (Advanced Tools):

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check file structure
ls -la /home/site/wwwroot/

# Test import
cd /home/site/wwwroot/backend
python -c "import app; print('App imports successfully')"

# Check for specific library
python -c "import pylibdmtx; print('pylibdmtx works')"
```

## ⚡ Simplified Deployment Option

If the current approach fails, try this simplified startup:

### Create startup.sh
```bash
#!/bin/bash
cd /home/site/wwwroot/backend
export FLASK_APP=app.py
export FLASK_ENV=production
python -m flask run --host=0.0.0.0 --port=$PORT
```

**Startup Command**: `bash startup.sh`

## 🚨 Most Likely Solution

Based on common Azure App Service issues, try this:

1. **Change Startup Command** to:
   ```
   cd backend && python -m gunicorn --bind=0.0.0.0:$PORT app:app
   ```

2. **Add Application Setting**:
   ```
   PYTHONPATH = /home/site/wwwroot/backend
   ```

3. **Restart** the App Service

## 📋 Verification Steps

After applying fixes:
1. Wait 2-3 minutes for restart
2. Check https://dmc-ggbxhgeaajb8ffed.swedencentral-01.azurewebsites.net/
3. If still error, check **Log stream** for specific error messages
4. Look for Python import errors or missing dependencies

---

**Need immediate help?** Check the **Log stream** in Azure Portal for specific error messages!
