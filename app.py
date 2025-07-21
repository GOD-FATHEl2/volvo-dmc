#!/usr/bin/env python3
"""
VOLVO DMC Generator - WSGI Entry Point
Entry point for Azure Web App deployment

© 2025 VOLVO Cars. All rights reserved. Made by: Nawoar Ekkou
"""

import os
import sys

# Add backend directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, 'backend')
sys.path.insert(0, backend_dir)

# Don't change working directory - keep it at root for Azure Web App
# os.chdir(backend_dir)  # Commented out to avoid path issues

# Import Flask app from backend directory
import backend.main as backend_main
app = backend_main.app

if __name__ == "__main__":
    print("🚀 Starting VOLVO DMC Generator...")
    # Get port from environment variable (Azure sets this)
    port = int(os.environ.get('PORT', 8000))
    print(f"📍 Server will be available on port: {port}")
    print("🔧 Production mode enabled for Azure")
    print("© 2025 VOLVO Cars. All rights reserved. Made by: Nawoar Ekkou")
    print("=" * 50)
    
    # Run in production mode for Azure
    app.run(
        debug=False,
        host="0.0.0.0",
        port=port,
        threaded=True
    )
