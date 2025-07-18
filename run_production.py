#!/usr/bin/env python3
"""
Production startup script for VOLVO DMC Generator
This script starts the Flask application with Gunicorn for production deployment

© 2025 VOLVO Cars. All rights reserved. Made by: Nawoar Ekkou
"""

import os
import sys
import subprocess

def main():
    """Main function to start the application"""
    print("🚀 Starting VOLVO DMC Generator (Production Mode)")
    print("© 2025 VOLVO Cars. All rights reserved. Made by: Nawoar Ekkou")
    print("=" * 50)
    
    # Determine the port (for Azure App Service or local)
    port = os.environ.get('PORT', '8000')
    
    # Set working directory to backend
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
    os.chdir(backend_dir)
    
    # Gunicorn command for production
    cmd = [
        'gunicorn',
        '--bind', f'0.0.0.0:{port}',
        '--workers', '4',
        '--worker-class', 'sync',
        '--worker-connections', '1000',
        '--timeout', '30',
        '--keep-alive', '2',
        '--max-requests', '1000',
        '--max-requests-jitter', '100',
        '--log-level', 'info',
        'app:app'
    ]
    
    print(f"📍 Server starting on port {port}")
    print(f"🔧 Command: {' '.join(cmd)}")
    print("=" * 50)
    
    # Start the server
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
