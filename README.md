# VOLVO DMC Generator

> **Advanced Data Matrix Code (DMC) Generator and Scanner**  
> Professional tool for generating, scanning, and managing Data Matrix Codes

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Online-brightgreen)](https://volvo-dmc-app.braveground-410ffbbc.swedencentral.azurecontainerapps.io/)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.1-lightgrey)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Live Application

**Access the live application**: [volvo-dmc-app.braveground-410ffbbc.swedencentral.azurecontainerapps.io](https://volvo-dmc-app.braveground-410ffbbc.swedencentral.azurecontainerapps.io/)

**Login Credentials:**
- Username: `admin`
- Password: `admin`

## ✨ Features

### 🔢 DMC Generation
- **Custom Data Matrix Codes**: Generate DMC codes with custom text/numbers
- **Bulk Generation**: Create multiple codes with automatic incrementing
- **Download Options**: Save as PNG images
- **Preview**: Real-time preview of generated codes

### 📷 DMC Scanning
- **Camera Scanning**: Real-time DMC detection using device camera
- **File Upload**: Upload images to scan for DMC codes
- **Multi-Detection**: Detect multiple DMC codes in single image
- **Result Export**: Download scan results

### 💾 Data Management
- **Database Storage**: Persistent storage of generated codes
- **Search History**: Find previously generated codes
- **Export Data**: JSON export functionality
- **Code Validation**: Verify DMC code integrity

## 🏗️ Project Structure

```
volvo-dmc-generator/
├── 📁 backend/                 # Core Flask application
│   ├── main.py                # Main Flask app with routes
│   ├── generate_qr.py         # DMC generation module
│   ├── read_dmc.py            # DMC scanning module
│   ├── dmc_detection_hybrid.py # Advanced detection algorithms
│   ├── database.json          # Data storage
│   ├── static/                # CSS, JS, images
│   └── templates/             # HTML templates
├── 📁 .github/workflows/      # CI/CD automation
│   └── working-deployment.yml # Azure Container Apps deployment
├── 📁 docs/                   # Documentation
│   ├── CHANGELOG.md
│   ├── CONTRIBUTING.md
│   └── SECURITY.md
├── app.py                     # Azure Web App entry point
├── main.py                    # Local development entry point
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container configuration
├── docker-compose.yml         # Local container setup
└── README.md                  # This file
```

## 🛠️ Installation & Setup

### Option 1: Local Development

```bash
# Clone repository
git clone https://github.com/GOD-FATHEl2/volvo-dmc-generator.git
cd volvo-dmc-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

Visit `http://localhost:5000` in your browser.

### Option 2: Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t volvo-dmc-generator .
docker run -p 5000:5000 volvo-dmc-generator
```

## 🔧 Configuration

### Environment Variables
- `PORT`: Application port (default: 5000)
- `FLASK_ENV`: Development/Production mode
- `DEBUG`: Enable debug mode (development only)

### Dependencies
- **Flask 3.1.1**: Web framework
- **Pillow**: Image processing
- **qrcode**: DMC generation
- **Flask-CORS**: Cross-origin requests
- **gunicorn**: Production WSGI server

## 🌐 Deployment

### Azure Container Apps (Current)
The application is deployed using GitHub Actions to Azure Container Apps:
- **URL**: https://volvo-dmc-app.braveground-410ffbbc.swedencentral.azurecontainerapps.io/
- **Auto-scaling**: Handles multiple concurrent users
- **CI/CD**: Automatic deployment on code push

### Local Deployment
```bash
# Production mode with gunicorn
gunicorn --bind 0.0.0.0:8000 app:app
```

## 🔐 Security

- **Authentication**: Admin login required
- **Input Validation**: Secure file upload handling
- **CORS Protection**: Configured cross-origin policies
- **Error Handling**: Graceful error management

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed guidelines.

## 📋 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard |
| `/login` | POST | User authentication |
| `/generate` | POST | Generate DMC codes |
| `/read_dmc` | POST | Scan uploaded images |
| `/download/<filename>` | GET | Download generated files |
| `/database` | GET | View stored data |

## 🐛 Troubleshooting

### Common Issues

**1. Camera not working**
- Ensure HTTPS connection (required for camera access)
- Check browser permissions

**2. Import errors**
- Verify Python path configuration
- Check virtual environment activation

**3. File upload issues**
- Supported formats: PNG, JPG, JPEG
- Maximum file size: 16MB

## 📈 Performance

- **Multi-user Support**: Handles concurrent users
- **Scalable Architecture**: Container-based deployment
- **Optimized Images**: Efficient DMC generation
- **Response Time**: < 200ms for generation

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/GOD-FATHEl2/volvo-dmc-generator/issues)
- **Documentation**: [docs/](docs/)
- **Live Demo**: [Try Online](https://volvo-dmc-app.braveground-410ffbbc.swedencentral.azurecontainerapps.io/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Live Application**: https://volvo-dmc-app.braveground-410ffbbc.swedencentral.azurecontainerapps.io/
- **GitHub Repository**: https://github.com/GOD-FATHEl2/volvo-dmc-generator
- **Docker Hub**: Available on request

---

**Made with ❤️ for VOLVO Cars**  
*Professional DMC solutions for modern manufacturing*
