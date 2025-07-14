# Azure App Service startup script
import os
import subprocess
import sys

if __name__ == "__main__":
    # Start the Flask application with gunicorn
    cmd = ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "backend.app:app"]
    subprocess.run(cmd)
