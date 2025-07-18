#!/usr/bin/env python3
"""
Deployment preparation script for VOLVO DMC Generator
This script prepares the application for GitHub deployment
"""

import os
import shutil
import json
from pathlib import Path

def clean_deployment_files():
    """Remove unnecessary files for deployment"""
    print("🧹 Cleaning deployment files...")
    
    # Files and directories to remove
    remove_items = [
        '.github/workflows/azure-static-web-apps-*.yml',
        'api/',
        'azure.yaml',
        'staticwebapp.config.json',
        'swa-cli.config.json',
        'infra/',
        'deploy-azure.*',
        '*.md',
        'frontend/',  # We'll use the backend templates
        'index.html',  # Root level, using backend templates
        'script.js',   # Root level, using backend static
        'style.css',   # Root level, using backend static
    ]
    
    for item in remove_items:
        if '*' in item:
            # Handle wildcards
            import glob
            for file in glob.glob(item):
                if os.path.exists(file):
                    if os.path.isdir(file):
                        shutil.rmtree(file)
                    else:
                        os.remove(file)
                    print(f"  ✅ Removed: {file}")
        else:
            if os.path.exists(item):
                if os.path.isdir(item):
                    shutil.rmtree(item)
                else:
                    os.remove(item)
                print(f"  ✅ Removed: {item}")

def create_deployment_structure():
    """Create the proper deployment structure"""
    print("📁 Creating deployment structure...")
    
    # Ensure required directories exist
    required_dirs = [
        'backend/static/qrs',
        'backend/templates',
        'logs'
    ]
    
    for dir_path in required_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"  ✅ Created: {dir_path}")

def create_runtime_txt():
    """Create runtime.txt for deployment platforms"""
    print("📝 Creating runtime.txt...")
    
    with open('runtime.txt', 'w') as f:
        f.write('python-3.11.9\n')
    
    print("  ✅ Created runtime.txt")

def create_procfile():
    """Create Procfile for deployment"""
    print("📝 Creating Procfile...")
    
    with open('Procfile', 'w') as f:
        f.write('web: python run_production.py\n')
    
    print("  ✅ Created Procfile")

def create_gitignore():
    """Create comprehensive .gitignore"""
    print("📝 Creating .gitignore...")
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/
env.bak/
venv.bak/

# Flask
instance/
.webassets-cache

# Database
*.db
*.sqlite3

# Logs
*.log
logs/

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Generated files
backend/static/qrs/*.png
backend/static/qrs/*.jpg
backend/static/qrs/*.jpeg
backend/static/Export_*.pdf
backend/database.json

# Deployment
.deployment
.azure/
node_modules/

# Test files
test_*.py
*_test.py
test_dmc.png
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("  ✅ Created .gitignore")

def create_readme():
    """Create a comprehensive README"""
    print("📝 Creating README.md...")
    
    readme_content = """# VOLVO DMC Generator

A professional Data Matrix Code (DMC) generator built with Flask for VOLVO manufacturing processes.

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
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
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

#### Azure App Service
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

## Support

For support, please create an issue in the GitHub repository.
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("  ✅ Created README.md")

def main():
    """Main deployment preparation function"""
    print("🚀 Preparing VOLVO DMC Generator for deployment...")
    print("=" * 60)
    
    clean_deployment_files()
    create_deployment_structure()
    create_runtime_txt()
    create_procfile()
    create_gitignore()
    create_readme()
    
    print("\n✅ Deployment preparation complete!")
    print("=" * 60)
    print("\n📋 Next steps:")
    print("1. Review the created files")
    print("2. Test the application locally: python app.py")
    print("3. Create a new GitHub repository")
    print("4. Push the code to GitHub")
    print("5. Deploy to your chosen platform")
    print("\n🎉 Ready for deployment!")

if __name__ == "__main__":
    main()
