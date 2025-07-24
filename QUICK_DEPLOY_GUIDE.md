# Quick Deployment Guide - Docker Hub Alternative

## 🚨 Azure Permission Issue Workaround

Since you're getting ACR permission errors, here's a quick solution using Docker Hub:

### Option 1: Use Pre-built Image (Fastest)

For now, you can use a publicly available Python Flask image and deploy immediately:

**Azure Container App Settings:**
```
Registry: docker.io
Image: python:3.11-slim
Tag: latest
```

**Startup Command:**
```bash
pip install flask flask-cors qrcode pillow && python -c "
from flask import Flask, jsonify, render_template_string
app = Flask(__name__)
@app.route('/')
def home():
    return '''<!DOCTYPE html>
<html><head><title>VOLVO DMC Generator</title></head>
<body style=\"font-family: Arial; text-align: center; padding: 50px;\">
<h1>🚀 VOLVO DMC Generator</h1>
<p>Container deployed successfully!</p>
<p>Login: admin / admin</p>
<div style=\"background: #f0f0f0; padding: 20px; border-radius: 10px; margin: 20px;\">
<h3>✅ Deployment Status: SUCCESS</h3>
<p>Azure Container App is running correctly</p>
</div>
</body></html>'''
@app.route('/login', methods=['POST'])
def login():
    return jsonify({'success': True})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
" & sleep infinity
```

### Option 2: Contact Azure Admin

Send this message to your Azure administrator:

**Subject:** Urgent: ACR Permission Required for VOLVO DMC Generator

**Body:**
```
Hi,

I need permission to deploy the VOLVO DMC Generator to Azure Container Apps. 
I'm getting this error:

Error: Authorization failed for roleAssignments
User: NEKKOU@volvocars.com  
Resource: ekkou.azurecr.io

Please grant me "AcrPush" role:

az role assignment create \
  --assignee NEKKOU@volvocars.com \
  --role "AcrPush" \
  --scope /subscriptions/57a382d9-18ec-4c9c-ab89-c7dad846eb55/resourceGroups/dmc-web-app/providers/Microsoft.ContainerRegistry/registries/ekkou

This is for the VOLVO DMC Generator manufacturing application.

Thanks!
```

### Option 3: Deploy with GitHub Actions (Once permissions are fixed)

The GitHub Actions workflow I created will automatically build and deploy once you have ACR permissions.

## 🎯 Quick Test Deploy

**Try Option 1 first** - use the Python Flask image above to get your Container App running immediately. This proves the Container App configuration works, then we can update the image later.
