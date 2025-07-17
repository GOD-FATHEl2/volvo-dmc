# Heroku Deployment Script
Write-Host "🚀 Deploying to Heroku..." -ForegroundColor Green

# Check if Heroku CLI is installed
try {
    heroku --version | Out-Null
    Write-Host "✅ Heroku CLI is available" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Installing Heroku CLI..." -ForegroundColor Yellow
    winget install Heroku.HerokuCLI
}

# Initialize git if not already
if (-not (Test-Path .git)) {
    Write-Host "📁 Initializing Git repository..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit for Heroku deployment"
}

# Login to Heroku
Write-Host "🔐 Logging in to Heroku..." -ForegroundColor Yellow
heroku login

# Create app with unique name
$timestamp = (Get-Date -Format "yyyyMMddHHmm")
$appName = "volvo-dmc-generator-$timestamp"
Write-Host "📦 Creating Heroku app: $appName" -ForegroundColor Yellow
heroku create $appName

# Set environment variables
Write-Host "⚙️ Setting environment variables..." -ForegroundColor Yellow
heroku config:set FLASK_ENV=production --app $appName

# Deploy to Heroku
Write-Host "🚀 Deploying to Heroku..." -ForegroundColor Green
git push heroku main

Write-Host "✅ Deployment completed!" -ForegroundColor Green
Write-Host "🌐 Your app is available at: https://$appName.herokuapp.com" -ForegroundColor Cyan
