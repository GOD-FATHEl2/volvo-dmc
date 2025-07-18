#!/usr/bin/env python3
"""
Simplified Azure App Service startup script
© 2025 VOLVO Cars. All rights reserved. Made by: Nawoar Ekkou
"""

import os
import sys

# Set the working directory to the backend folder
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

# Import and run the Flask app
from app import app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
