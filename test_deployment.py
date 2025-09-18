#!/usr/bin/env python3
"""
Simple test file for cPanel deployment debugging
"""

import sys
import os

# Test basic Python functionality
print("Content-Type: text/html\n")
print("<html><body>")
print("<h1>cPanel Python Test</h1>")
print(f"<p>Python Version: {sys.version}</p>")
print(f"<p>Current Directory: {os.getcwd()}</p>")
print(f"<p>Python Path: {sys.path}</p>")

# Test Flask import
try:
    import flask
    print(f"<p>✅ Flask Version: {flask.__version__}</p>")
except Exception as e:
    print(f"<p>❌ Flask Import Error: {e}</p>")

# Test PyMySQL import  
try:
    import pymysql
    print(f"<p>✅ PyMySQL Version: {pymysql.__version__}</p>")
except Exception as e:
    print(f"<p>❌ PyMySQL Import Error: {e}</p>")

# Test app import
try:
    sys.path.insert(0, os.path.dirname(__file__))
    from app import app
    print("<p>✅ Flask App Imported Successfully</p>")
except Exception as e:
    print(f"<p>❌ App Import Error: {e}</p>")

print("</body></html>")
