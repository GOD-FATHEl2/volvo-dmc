#!/usr/bin/env python3
import os
import sys

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Change to backend directory
os.chdir(backend_path)

# Import Flask app from backend main module
from main import app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    # Run the Flask app
    app.run(host='0.0.0.0', port=port, debug=False)
