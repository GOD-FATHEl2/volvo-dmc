#!/usr/bin/env python3
"""
VOLVO DMC Generator - Development Server
© 2025 VOLVO Cars. All rights reserved.
Made by: Nawoar Ekkou

Local development server for the VOLVO DMC Generator application.
Production deployment: https://dmc-ggbxhgeaajb8ffed.swedencentral-01.azurewebsites.net
"""

import os
import sys

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Import the Flask app from backend
from app import app

if __name__ == "__main__":
    print("🚀 Starting VOLVO DMC Generator...")
    print("📍 Server will be available at: http://localhost:5000")
    print("🔧 Development mode enabled")
    print("=" * 50)
    
    # Run in development mode
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000,
        threaded=True
    )
