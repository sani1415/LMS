#
# PASTE THIS ENTIRE CODE INTO: passenger_wsgi.py
#
import sys
import os

# Add your project directory to the Python path
# This ensures that 'import app' works correctly
sys.path.insert(0, os.path.dirname(__file__))

# Set the FLASK_ENV to production if it's not already set in cPanel
# This is a safety measure to ensure the production config is loaded.
os.environ.setdefault('FLASK_ENV', 'production')

# Import your Flask application instance from your main app.py file
from app import app as application

# The 'application' variable is what the Phusion Passenger server looks for.