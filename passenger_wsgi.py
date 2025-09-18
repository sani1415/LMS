#!/usr/bin/env python3
"""
Passenger WSGI file for cPanel deployment
"""

import sys
import os

# Add your project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set environment for production
os.environ.setdefault('FLASK_ENV', 'production')

# Import your Flask application
from app import app

# This is what Passenger will use
application = app

if __name__ == "__main__":
    application.run(debug=False)
