#!/usr/bin/env python3
"""
Passenger WSGI file for cPanel deployment
"""

import sys
import os

# Add project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Set environment for production
os.environ['FLASK_ENV'] = 'production'

try:
    # Import Flask application
    from app import app
    
    # This is what Passenger will use
    application = app
    
    # Test import
    print("Flask app imported successfully")
    
except Exception as e:
    print(f"Error importing Flask app: {e}")
    # Create a simple WSGI app for debugging
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [f"Error importing Flask app: {str(e)}".encode()]

if __name__ == "__main__":
    application.run()
