#!/usr/bin/env python3
"""
Passenger WSGI file for cPanel deployment
This file is required by most cPanel hosts to run Flask applications
"""

import sys
import os

# Add your project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import your Flask application
from app import app

# This is what Passenger will use
application = app

if __name__ == "__main__":
    application.run()
