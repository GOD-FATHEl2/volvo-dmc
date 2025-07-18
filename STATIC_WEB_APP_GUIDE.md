# 🚀 Azure Static Web Apps Deployment Guide for VOLVO DMC Generator

## 📋 Overview
Your VOLVO DMC Generator has been restructured for Azure Static Web Apps with the following architecture:
- **Frontend**: HTML/CSS/JavaScript (Static Web App)
- **Backend**: Azure Functions (API)
- **Deployment**: GitHub Actions with existing Static Web App

## 🎯 Project Structure
```
.
├── index.html              # Main application (static frontend)
├── script.js               # Frontend JavaScript with API calls
├── style.css               # Styling
├── staticwebapp.config.json # Static Web App configuration
├── api/                    # Azure Functions API
│   ├── host.json           # Functions host configuration
│   ├── requirements.txt    # Python dependencies
│   ├── generate_dmc/       # DMC generation function
│   └── export/             # Export function
└── .github/workflows/      # GitHub Actions
    └── azure-static-web-apps-wonderful-pebble-077934d03.yml
```

## 🔧 Features Adapted for Static Web Apps

### ✅ **What Works**
- **DMC Generation**: Placeholder DMC generation (Azure Functions don't support libdmtx)
- **Batch Processing**: Multiple DMC generation with demo images
- **Export Functionality**: Excel/CSV export via Azure Functions
- **Responsive UI**: Full frontend functionality
- **Camera Integration**: Camera access for future scanning

### ⚠️ **Limitations**
- **No Real DMC Generation**: Azure Functions don't support libdmtx system dependencies
- **Placeholder Images**: Demo grid pattern instead of actual Data Matrix Codes
- **No DMC Scanning**: Would require client-side JavaScript library

## 🚀 Deployment Instructions

### Step 1: Update Your Existing Static Web App

Your existing Static Web App:
- **URL**: https://wonderful-pebble-077934d03.2.azurestaticapps.net
- **Resource Group**: rg-centralcoreservices-nonprod-001
- **Subscription**: app-7592-online-nonprod-001

### Step 2: Deploy Using GitHub Actions

1. **Go to GitHub Actions**:
   ```
   https://github.com/GOD-FATHEl2/volvo-dmc/actions
   ```

2. **Select Workflow**:
   - Choose "Azure Static Web Apps CI/CD"
   - Click "Run workflow"

3. **Monitor Deployment**:
   - Watch the build and deploy process
   - Check for any errors in the logs

### Step 3: Access Your Updated Application

After deployment, your app will be available at:
```
https://wonderful-pebble-077934d03.2.azurestaticapps.net
```

## 📊 API Endpoints

Your Azure Functions API will provide:

### 1. DMC Generation
- **Endpoint**: `/api/generate-dmc`
- **Method**: POST
- **Body**: `{ "data": "VOLVO123456789" }`
- **Response**: `{ "success": true, "image": "base64...", "data": "..." }`

### 2. Batch Generation
- **Endpoint**: `/api/generate-dmc`
- **Method**: POST
- **Body**: `{ "batch_data": ["VOLVO123", "VOLVO456"] }`
- **Response**: `{ "success": true, "batch_results": [...] }`

### 3. Export
- **Endpoint**: `/api/export`
- **Method**: POST
- **Body**: `{ "data": [...], "format": "excel" }`
- **Response**: `{ "success": true, "file": "base64...", "filename": "..." }`

## 🔧 Local Development

### Using Static Web Apps CLI

1. **Install CLI**:
   ```bash
   npm install -g @azure/static-web-apps-cli
   ```

2. **Start Development Server**:
   ```bash
   swa start
   ```

3. **Access Local App**:
   ```
   http://localhost:4280
   ```

### Using SWA CLI with Custom Settings

```bash
swa start . --api-location api --port 3000
```

## 🎨 Customization Options

### 1. **Enable Real DMC Generation**
To enable real DMC generation, you would need to:
- Use a client-side DMC library (JavaScript)
- Or deploy to Azure Container Apps/App Service instead

### 2. **Add DMC Scanning**
```javascript
// Example using ZXing library
import { BrowserMultiFormatReader } from '@zxing/browser';

const codeReader = new BrowserMultiFormatReader();
// Implementation for DMC scanning
```

### 3. **Enhance Export Features**
- Add PDF export functionality
- Include DMC images in exports
- Add custom templates

## 📈 Benefits of Static Web Apps

✅ **Cost Effective**: Free tier available
✅ **Auto-scaling**: Handles traffic spikes automatically
✅ **Global CDN**: Fast loading worldwide
✅ **Integrated API**: Azure Functions included
✅ **CI/CD Built-in**: GitHub Actions integration
✅ **Custom Domains**: Easy to add your own domain
✅ **SSL**: Automatic HTTPS

## 🔍 Troubleshooting

### Common Issues

1. **API Not Working**:
   - Check Azure Functions logs in Azure Portal
   - Verify API endpoints are correct
   - Check CORS settings

2. **Build Failures**:
   - Verify Python dependencies in api/requirements.txt
   - Check GitHub Actions logs
   - Ensure proper file structure

3. **Static Content Not Loading**:
   - Verify staticwebapp.config.json is correct
   - Check file paths in HTML/CSS
   - Ensure all static files are in root directory

### Debug Commands

```bash
# Check SWA CLI version
swa --version

# Validate configuration
swa validate

# Build locally
swa build

# Deploy to production
swa deploy --env production
```

## 🎯 Next Steps

1. **Deploy the updated code** using GitHub Actions
2. **Test all functionality** on your Static Web App
3. **Consider upgrading** to Azure App Service if you need real DMC generation
4. **Add custom domain** if needed
5. **Monitor usage** and costs

## 📞 Support

If you need real DMC generation with libdmtx support, consider:
- **Azure Container Apps**: Full Docker support
- **Azure App Service**: Container deployment
- **Azure Virtual Machines**: Full control over dependencies

Your VOLVO DMC Generator is now ready for Azure Static Web Apps deployment! 🎉
