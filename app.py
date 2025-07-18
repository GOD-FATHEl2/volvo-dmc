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

# Change working directory to backend for proper file access
os.chdir(backend_dir)

# Import Flask app from backend
import backend.app as backend_app
app = backend_app.app

if __name__ == "__main__":
    print("🚀 Starting VOLVO DMC Generator...")
    print("📍 Server will be available at: http://localhost:5000")
    print("🔧 Development mode enabled")
    print("© 2025 VOLVO Cars. All rights reserved. Made by: Nawoar Ekkou")
    print("=" * 50)
    
    # Run in development mode
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000,
        threaded=True
    )
