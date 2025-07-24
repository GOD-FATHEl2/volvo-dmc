#!/usr/bin/env python3
"""
VOLVO DMC Generator - Main Entry Point
Direct Flask application entry point for local development

© 2025 VOLVO Cars. All rights reserved. Made by: Nawoar Ekkou
"""
import os
import sys

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Import Flask app from backend main module (avoid circular import)
import backend.main
app = backend.main.app

if __name__ == "__main__":
    print("🚀 Starting VOLVO DMC Generator (main.py)...")
    port = int(os.environ.get('PORT', 8000))
    print(f"📍 Server will be available on port: {port}")
    print("🔧 Local development mode")
    print("© 2025 VOLVO Cars. All rights reserved. Made by: Nawoar Ekkou")
    print("=" * 50)
    
    # Run the Flask app in debug mode for local development
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
