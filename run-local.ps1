# Quick Local Development Script
# This will run your app locally for development and testing

Write-Host "🚀 Starting Volvo DMC Generator locally..." -ForegroundColor Green

# Check if Python is available
try {
    python --version | Out-Null
    Write-Host "✅ Python is available" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Check if virtual environment is activated
if ($env:VIRTUAL_ENV) {
    Write-Host "✅ Virtual environment is active: $env:VIRTUAL_ENV" -ForegroundColor Green
} else {
    Write-Host "⚠️ No virtual environment detected. Recommended to activate venv first." -ForegroundColor Yellow
}

# Install requirements if needed
Write-Host "📦 Checking requirements..." -ForegroundColor Yellow
python -m pip install -r requirements-minimal.txt --quiet

# Start the application
Write-Host "🎯 Starting the application..." -ForegroundColor Green
Write-Host "📍 Local access: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📍 Network access: http://$(hostname):8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Yellow
Write-Host "===========================================" -ForegroundColor Green

# Run the Flask application
python backend/app.py
