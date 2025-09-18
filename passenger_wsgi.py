#!/usr/bin/env python3
"""
Passenger WSGI file for cPanel deployment
With stderr/stdout logging enabled
"""

import sys
import os

# Define path for logs inside your app folder
log_path = os.path.join(os.path.dirname(__file__), "stderr.log")

# Redirect stderr and stdout to the log file
sys.stderr = open(log_path, "a")
sys.stdout = open(log_path, "a")

# Add project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Set environment for production
os.environ['FLASK_ENV'] = 'production'

try:
    # Import Flask application
    from app import app
    application = app
    print("✅ Flask app loaded successfully", flush=True)

except Exception as e:
    print(f"❌ Error importing Flask app: {e}", flush=True)

    # Simple fallback WSGI app
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [f"Error importing Flask app: {str(e)}".encode()]
