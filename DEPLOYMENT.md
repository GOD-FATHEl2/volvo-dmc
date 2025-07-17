# VOLVO MDC - Deployment Guide

## 🚀 Quick Deployment to GitHub

### Prerequisites
- Git installed on your system
- GitHub account
- Python 3.8+ (for local testing)

### Step 1: Initialize Git Repository
```bash
cd "VOLVO MDC Generator - Copy"
git init
git add .
git commit -m "Initial commit: VOLVO MDC v2.0 with DMC reading functionality"
```

### Step 2: Create GitHub Repository
1. Go to [GitHub.com](https://github.com)
2. Click "New Repository"
3. Repository name: `volvo-dmc-generator`
4. Description: "VOLVO MDC - Data Matrix Code Generator & Reader for Industrial Use"
5. Choose Public or Private
6. **Don't** initialize with README (we already have one)
7. Click "Create Repository"

### Step 3: Connect and Push
```bash
git remote add origin https://github.com/YOUR_USERNAME/volvo-dmc-generator.git
git branch -M main
git push -u origin main
```

### Step 4: Configure Repository Settings
1. Go to repository Settings
2. Set description and topics:
   - **Topics**: `volvo`, `dmc`, `datamatrix`, `manufacturing`, `python`, `flask`, `industrial`
3. Enable Issues and Wiki if desired

## 🌐 Deployment Options

### Option 1: Local Development
```bash
cd backend
pip install -r ../requirements.txt
python app.py
```
Access: http://localhost:5000

### Option 2: Heroku Deployment
1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: cd backend && python app.py
   ```
3. Deploy:
   ```bash
   heroku create volvo-mdc-app
   git push heroku main
   ```

### Option 3: Railway Deployment
1. Connect GitHub repository to Railway
2. Set start command: `cd backend && python app.py`
3. Add environment variables if needed

### Option 4: DigitalOcean App Platform
1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set run command: `cd backend && python app.py`

### Option 5: Render Deployment
1. Connect GitHub repository
2. Build command: `pip install -r requirements.txt`
3. Start command: `cd backend && python app.py`

## 🔧 Environment Configuration

### Environment Variables
```bash
# Optional configurations
PORT=5000
FLASK_ENV=production
FLASK_DEBUG=False
```

### Production Considerations
1. **Security**: Change default login credentials
2. **Database**: Consider migrating from JSON to PostgreSQL for high volume
3. **Storage**: Use cloud storage for generated files
4. **Monitoring**: Implement logging and error tracking
5. **SSL**: Enable HTTPS for production

## 📱 Mobile Access

### QR Code for Easy Access
Once deployed, create a QR code pointing to your deployment URL for easy mobile access in the factory.

### PWA Installation
The app can be installed as a Progressive Web App on mobile devices for offline access.

## 🔍 Testing Deployment

### Verify Functionality
1. ✅ Login functionality
2. ✅ DMC code generation
3. ✅ DMC code reading
4. ✅ PDF export
5. ✅ Excel export
6. ✅ Print functionality
7. ✅ Mobile responsiveness

### Performance Testing
- Test with multiple concurrent users
- Verify file upload limits
- Check memory usage with large batches

## 🆘 Troubleshooting

### Common Issues
1. **pylibdmtx installation**: Install system dependencies
2. **File permissions**: Ensure write access to static folder
3. **Memory issues**: Monitor for large file uploads
4. **CORS errors**: Configure CORS for production domain

### Logs and Monitoring
```bash
# View application logs
tail -f app.log

# Monitor system resources
htop
```

## 📞 Support

**Developer**: Nawoar Ekkou  
**Organization**: VOLVO Cars Torslanda  
**Department**: Manufacturing Technology

---

© 2025 VOLVO Cars. All rights reserved.
