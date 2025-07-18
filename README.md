# VOLVO MDC (Matrix Data Code Generator & Reader)

<div align="center">

![VOLVO](https://img.shields.io/badge/VOLVO-Cars-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-green?style=for-the-badge&logo=flask)
![Status](https://img.shields.io/badge/Status-Production-success?style=for-the-badge)

**A modern, mobile-friendly web application for generating and reading Data Matrix Codes (DMC) for industrial use at VOLVO Cars Torslanda.**

</div>

---

## � Quick Deployment Status

| Deployment Type | Status | URL | Notes |
|----------------|--------|-----|-------|
| **Azure App Service** | ✅ Ready | *Configure in Azure* | Full Flask app with all features |
| **Docker Container** | ✅ Ready | *Deploy anywhere* | Portable containerized version |
| **Local Development** | ✅ Ready | `http://localhost:5000` | Run with `python backend/app.py` |
| **Azure Static Web Apps** | ⚠️ Disabled | *Requires reconfiguration* | Resource unavailable |

> **Recommended**: Use Azure App Service for production deployment with complete functionality.

---

## �📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [API Endpoints](#-api-endpoints)
- [File Structure](#-file-structure)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [About](#-about)

---

## 🎯 Overview

VOLVO MDC is a comprehensive industrial tool designed specifically for VOLVO Cars manufacturing operations. The application provides a complete solution for Data Matrix Code management, supporting both code generation and reading capabilities with an intuitive, Apple-inspired user interface.

### Key Capabilities:
- **Generate** unique DMC codes with custom prefixes
- **Read and decode** DMC codes from uploaded images
- **Export** codes to PDF and Excel formats
- **Track history** of all operations
- **Print-optimized** layouts for industrial use
- **Mobile-responsive** design for factory floor usage

---

## ✨ Features

### � **Authentication System**
- Secure login with username/password authentication
- Default credentials: `admin` / `admin`
- Session management for secure access

### 🏭 **DMC Code Generation**
- **Prefix Selection**: Choose from letters (A-Z) or numbers (0-9)
- **Automatic Code Format**: `{prefix}{month}{day}{year_last_digit}{hour}{second}`
- **Batch Generation**: Creates 30 codes automatically in 5x6 grid layout
- **Unique Identification**: Each code includes timestamp and sequence number
- **Example Output**: `A7725640` (A + July 17, 2025 + time components)

### 📖 **DMC Code Reading**
- **Image Upload**: Support for PNG, JPG, JPEG, GIF, BMP, TIFF formats
- **Automatic Decoding**: Real-time DMC code recognition
- **Error Handling**: Comprehensive feedback for failed reads
- **Source Tracking**: Records original filename and timestamp

### 📄 **Export & Print Functions**
- **PDF Export**: Professional layout with VOLVO branding
- **Excel Export**: Structured data in 5-column format
- **Print Optimization**: Clean, ink-efficient printing layout
- **Batch Selection**: Choose specific codes for export

### 📊 **History & Tracking**
- **Complete Audit Trail**: All generated and read operations logged
- **Operation Types**: Visual distinction between generated (🏭) and read (📖) codes
- **Timestamps**: Precise tracking of all activities
- **JSON Storage**: Lightweight, file-based database

### 🎨 **User Interface**
- **Apple-Inspired Design**: Clean, minimalist aesthetic
- **Mobile-First**: Responsive design for tablets and phones
- **Professional Color Scheme**: White, gray, and dark gray palette
- **Accessibility**: Clear typography and intuitive navigation

---

## 🛠 Technology Stack

### Backend
- **Framework**: Python Flask 2.0+
- **DMC Processing**: pylibdmtx (generation & reading)
- **PDF Generation**: FPDF
- **Excel Export**: openpyxl
- **Image Processing**: Pillow (PIL)
- **CORS Support**: flask-cors

### Frontend
- **Languages**: HTML5, CSS3, JavaScript (ES6+)
- **Design System**: Custom Apple-inspired CSS framework
- **Responsive**: Mobile-first responsive design
- **Icons**: Unicode emoji for industrial clarity

### Data Storage
- **Database**: JSON file-based storage
- **File Management**: Secure file handling with werkzeug
- **Static Assets**: Organized directory structure

---

## � Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Modern web browser

### Step 1: Clone or Download
```bash
git clone <repository-url>
cd "VOLVO MDC Generator"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Required packages:**
```txt
flask
qrcode
pillow
fpdf
pandas
openpyxl
Pillow
pylibdmtx
numpy
setuptools
flask-cors
```

### Step 3: Start the Application
```bash
cd backend
python app.py
```

### Step 4: Access the Application
- **Local**: http://localhost:5000
- **Network**: http://[your-ip]:5000
- **Production**: Configure with ngrok or deployment platform

---

## 📚 Usage Guide

### Getting Started

1. **Launch Application**
   - Start the Flask server
   - Open web browser to application URL
   - Login with credentials (admin/admin)

2. **Generate DMC Codes**
   - Select a prefix from the dropdown (A-Z or 0-9)
   - Click "Generate 30 DMC Codes"
   - Codes appear in a 5x6 grid layout
   - All codes are automatically selected for export

3. **Read DMC Codes**
   - Navigate to "📖 Read DMC Codes" section
   - Click file input to select image
   - Supported formats: PNG, JPG, JPEG, GIF, BMP, TIFF
   - View decoded results instantly

4. **Export Operations**
   - **PDF Export**: Select codes → Click "Download PDF"
   - **Excel Export**: Select codes → Click "Download Excel"
   - **Print**: Click "Print" for optimized layout

5. **History Management**
   - View all operations in chronological order
   - Distinguish between generated (🏭) and read (📖) operations
   - Track timestamps and source information

### Advanced Features

#### Batch Operations
- Generate multiple sets of codes
- Select specific codes for export
- Bulk delete unwanted codes

#### Quality Control
- Verify code readability by uploading generated images
- Cross-reference codes with production records
- Maintain audit trail for compliance

#### Mobile Usage
- Full functionality on tablets and smartphones
- Touch-optimized interface
- Offline viewing of generated codes

---

## 🔌 API Endpoints

### Authentication
```http
POST /login
Content-Type: application/json
{
  "username": "admin",
  "password": "admin"
}
```

### Generate DMC Codes
```http
POST /generate
Content-Type: multipart/form-data
prefix: A
count: 30
```

### Read DMC Code
```http
POST /read_dmc
Content-Type: multipart/form-data
file: [image file]
```

### Export Functions
```http
POST /download_pdf
Content-Type: application/json
{
  "files": ["dmc_0_timestamp.png", "dmc_1_timestamp.png"]
}
```

```http
POST /download_excel
Content-Type: application/json
{
  "files": ["dmc_0_timestamp.png", "dmc_1_timestamp.png"]
}
```

### History & Assets
```http
GET /history
GET /qrs/<filename>
```

---

## 📁 File Structure

```
VOLVO MDC/
│
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── generate_qr.py         # DMC generation module
│   ├── read_dmc.py           # DMC reading module
│   ├── database.json         # Operations history
│   ├── static/
│   │   ├── script.js         # Frontend JavaScript
│   │   ├── style.css         # CSS styling
│   │   ├── qrs/              # Generated DMC images
│   │   └── *.pdf             # Exported PDF files
│   └── templates/
│       └── index.html        # Main UI template
│
├── frontend/                 # Standalone frontend (optional)
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── requirements.txt          # Python dependencies
├── startup.txt              # Deployment configuration
├── structure.txt            # Project documentation
└── README.md               # This file
```

---

## ⚙️ Configuration

### Environment Variables
```bash
# Optional: Set custom port
export FLASK_PORT=5000

# Optional: Enable debug mode
export FLASK_DEBUG=True
```

### Application Settings
```python
# app.py configuration
app.config['UPLOAD_FOLDER'] = 'static/qrs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
```

### NGrok Setup (for remote access)
```bash
# Install ngrok
pip install pyngrok

# Start tunnel
ngrok http 5000

# Update BASE URL in script.js
let BASE = "https://your-ngrok-url.ngrok-free.app";
```

---

## � Troubleshooting

### Common Issues

**Installation Problems**
```bash
# If pylibdmtx fails to install
# Windows: Install Visual C++ Build Tools
# macOS: brew install libdmtx
# Linux: apt-get install libdmtx-dev
```

**File Upload Issues**
- Verify image format is supported
- Check file size (max 16MB)
- Ensure image contains visible DMC code

**Code Reading Failures**
- Use high-contrast images
- Ensure DMC code is clearly visible
- Try different image formats
- Check lighting and resolution

**Export Problems**
- Verify write permissions in static folder
- Check available disk space
- Ensure no files are locked by other applications

### Performance Optimization
- Regularly clean old export files
- Monitor database.json size
- Restart application if memory usage is high

---

## 👨‍💻 About

### Project Information
**Application Name**: VOLVO MDC (Matrix Data Code Generator & Reader)  
**Version**: 2.0  
**Release Date**: July 2025  
**Environment**: Industrial Manufacturing  

### Development Team
**Lead Developer**: Nawoar Ekkou  
**Organization**: VOLVO Cars Torslanda  
**Department**: Manufacturing Technology  

### Purpose
This application was developed to streamline Data Matrix Code operations in VOLVO Cars manufacturing processes. It replaces manual code generation and reading workflows with an automated, user-friendly solution that maintains quality standards and provides comprehensive tracking capabilities.

### Technical Features
- **Production-Ready**: Tested in industrial environment
- **Scalable**: Handles high-volume code generation
- **Reliable**: Robust error handling and validation
- **Maintainable**: Clean code architecture and documentation

### Use Cases
- **Quality Control**: Track components through production
- **Inventory Management**: Label parts and assemblies
- **Compliance**: Maintain audit trails for regulations
- **Efficiency**: Reduce manual data entry errors

---

## 📄 Copyright

```
© 2025 VOLVO Cars. All rights reserved.

This software is proprietary to VOLVO Cars and is intended for 
internal use only. Unauthorized reproduction, distribution, or 
modification is strictly prohibited.

Made by: Nawoar Ekkou
VOLVO Cars Torslanda
Manufacturing Technology Division
```

---

## � Support

For technical support or feature requests:

**Internal Support**: Contact IT Manufacturing Systems  
**Developer**: Nawoar Ekkou  
**Location**: VOLVO Cars Torslanda  

---

<div align="center">

**VOLVO MDC** - *Powering Industrial Excellence*

![VOLVO Cars](https://img.shields.io/badge/VOLVO-Cars%20Torslanda-blue?style=for-the-badge)

</div>
