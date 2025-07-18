# VOLVO DMC Generator

A professional Data Matrix Code (DMC) generator built with Flask for VOLVO manufacturing processes.

**© VOLVO Cars. All rights reserved.**  
**Made by: Nawoar Ekkou**

## Live Demo

🌐 **Azure Deployment**: [https://dmc-ggbxhgeaajb8ffed.swedencentral-01.azurewebsites.net](https://dmc-ggbxhgeaajb8ffed.swedencentral-01.azurewebsites.net)

### Azure App Service Details
- **Resource Group**: rg-centralcoreservices-nonprod-001
- **Location**: Sweden Central
- **Runtime**: Python 3.11 on Linux
- **Plan**: App Service Plan (Free F1)
- **Status**: Running ✅

## Features

- Industrial-grade DMC Generation: Generate Data Matrix codes with pylibdmtx
- Batch Processing: Generate multiple codes with sequential numbering
- Responsive Interface: Modern web interface with mobile support
- Multiple Export Options: Download individual codes or batch export to PDF/Excel
- QR Code Reading: Upload and decode existing DMC codes
- Secure Access: Login system with admin controls
- History Tracking: Complete audit trail of generated codes

## Quick Start

### Local Development

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd volvo-dmc-generator
   ```

2. **Set up Python environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements-production.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open in browser**: http://localhost:5000

### Production Deployment

#### Azure App Service (Current Deployment)
- **Live URL**: https://dmc-ggbxhgeaajb8ffed.swedencentral-01.azurewebsites.net
- **Resource Group**: rg-centralcoreservices-nonprod-001
- **Location**: Sweden Central
- **Subscription**: app-7592-online-nonprod-001
- **Runtime**: Python 3.11 on Linux
- **Plan**: ASP-rgcentralcoreservicesnonprod001-bbb0 (Free F1)
- **Virtual IP**: 51.12.31.11

**Deployment Steps**:
1. Create an Azure App Service (Python 3.11)
2. Configure deployment from GitHub
3. Set startup command: `python run_production.py`
4. Deploy from main branch

#### Alternative Deployment Options
1. Fork this repository
2. Create an Azure App Service (Python 3.11)
3. Configure deployment from GitHub
4. Set startup command: `python run_production.py`

#### Heroku
1. Install Heroku CLI
2. Login and create app:
   ```bash
   heroku login
   heroku create your-app-name
   ```
3. Deploy:
   ```bash
   git push heroku main
   ```

#### Railway
1. Connect your GitHub repository
2. Railway will automatically detect and deploy

## Usage

### Default Login
- **Username**: admin
- **Password**: admin

### Generating DMC Codes

1. **Login** with admin credentials
2. **Enter prefix** (single letter: A-Z)
3. **Set count** (number of codes to generate)
4. **Click Generate** to create codes
5. **Download** individual codes or export batch

### Reading DMC Codes

1. Go to **"Read DMC"** tab
2. **Upload image** containing DMC code
3. **View decoded** data

## Technical Details

### Dependencies

- **Flask 3.1.1**: Web framework
- **pylibdmtx 0.1.10**: DMC code generation
- **Pillow 11.3.0**: Image processing
- **openpyxl 3.1.5**: Excel export
- **fpdf 1.7.2**: PDF generation

### Architecture

```
volvo-dmc-generator/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── generate_qr.py      # DMC generation logic
│   ├── read_dmc.py         # DMC reading logic
│   ├── static/             # CSS, JS, images
│   └── templates/          # HTML templates
├── app.py                  # Development server
├── run_production.py       # Production server
└── requirements-production.txt
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Copyright

**© 2025 VOLVO Cars. All rights reserved.**

This application is developed for VOLVO manufacturing processes and is proprietary to VOLVO Cars.

**Developer**: Nawoar Ekkou  
**Company**: VOLVO Cars  
**Purpose**: Data Matrix Code generation for manufacturing processes  

## Support

For support, please create an issue in the GitHub repository or contact the development team.
