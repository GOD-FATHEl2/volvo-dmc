#!/usr/bin/env python3
"""
Azure Web App Entry Point for VOLVO DMC Generator
This file serves as the entry point for Azure Web App deployment.
"""

import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Add backend directory to path
backend_dir = os.path.join(project_root, 'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    # Try to import the main Flask app from backend
    from backend.main import app
    print("✅ Successfully imported VOLVO DMC Generator backend")
    
except ImportError as e:
    print(f"❌ Failed to import backend: {e}")
    
    # Fallback Flask app
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def fallback():
        return '''
        <html>
        <head><title>VOLVO DMC Generator</title></head>
        <body>
            <h1>VOLVO DMC Generator</h1>
            <p>Backend loading error. Please check deployment.</p>
            <p>Error: Failed to import backend modules</p>
            <p>Please contact administrator.</p>
        </body>
        </html>
        '''

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
