#!/bin/bash

# Azure Web App startup script for VOLVO DMC Generator
# This script ensures the Flask app starts correctly on Azure Web App

# Set environment variables
export FLASK_APP=backend/app.py
export FLASK_ENV=production
export PYTHONPATH=/home/site/wwwroot/backend:/home/site/wwwroot

# Navigate to the application directory
cd /home/site/wwwroot

# Install any missing dependencies (backup safety)
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Start the Flask application with Gunicorn
echo "Starting VOLVO DMC Generator on Azure Web App..."
cd backend
gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 app:app
