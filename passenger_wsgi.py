#!/usr/bin/env python3
"""
Passenger WSGI file for cPanel deployment
"""

import sys
import os

# Add your project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import your Flask application
from app import app

# Initialize database for production
with app.app_context():
    from backend.extensions import db
    from backend.models import Book
    from backend.init_db import create_sample_data
    
    # Create tables
    db.create_all()
    
    # Add sample data if database is empty
    if not Book.query.first():
        create_sample_data()

# This is what Passenger will use
application = app

if __name__ == "__main__":
    application.run(debug=False)
