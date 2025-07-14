# Quick Local Deployment Script
# This will run your app locally and make it accessible on your network

Write-Host "🚀 Starting Volvo DMC Generator locally..." -ForegroundColor Green

# Check if Python is available
try {
    python --version | Out-Null
    Write-Host "✅ Python is available" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Install requirements
Write-Host "📦 Installing requirements..." -ForegroundColor Yellow
python -m pip install -r requirements.txt

# Check if ngrok is available for external access
$ngrokAvailable = $false
try {
    ngrok version | Out-Null
    $ngrokAvailable = $true
    Write-Host "✅ ngrok is available for external access" -ForegroundColor Green
} catch {
    Write-Host "⚠️ ngrok not found. App will only be available locally." -ForegroundColor Yellow
    Write-Host "   To install ngrok: winget install ngrok" -ForegroundColor Yellow
}

# Start the application
Write-Host "🎯 Starting the application..." -ForegroundColor Green
Write-Host "📍 Local access: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📍 Network access: http://$(hostname):8000" -ForegroundColor Cyan

if ($ngrokAvailable) {
    Write-Host "🌐 Starting ngrok for external access..." -ForegroundColor Yellow
    
    # Start app in background
    $job = Start-Job -ScriptBlock {
        Set-Location $using:PWD
        python backend/app.py
    }
    
    # Wait a moment for app to start
    Start-Sleep -Seconds 3
    
    # Start ngrok
    Write-Host "🔗 ngrok tunnel will open in a new window..." -ForegroundColor Green
    Start-Process "ngrok" -ArgumentList "http", "8000" -WindowStyle Normal
    
    # Monitor the job
    Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Yellow
    try {
        while ($job.State -eq "Running") {
            Start-Sleep -Seconds 1
        }
    } finally {
        Stop-Job $job -ErrorAction SilentlyContinue
        Remove-Job $job -ErrorAction SilentlyContinue
    }
} else {
    # Run normally
    python backend/app.py
}

Write-Host "🛑 Application stopped" -ForegroundColor Red
