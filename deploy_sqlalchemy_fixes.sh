#!/bin/bash

# SQLAlchemy and Connection Fixes Deployment Script
# This script deploys the fixes for the specific errors found in your logs

set -e

echo "🔧 Deploying SQLAlchemy and Connection Fixes..."
echo "=============================================="

# Check if we're on cPanel (production) or local development
if [ -d "/home" ] && [ -d "/home/idarahco" ]; then
    echo "📦 Detected cPanel environment - deploying production fixes..."
    
    # Define your virtual environment path
    VENV_PATH="/home/idarahco/virtualenv/public_html/maktabah/3.11"
    
    # Activate virtual environment
    echo "Activating virtual environment: $VENV_PATH"
    source "$VENV_PATH/bin/activate"
    
    # Install/update dependencies
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    
    # Run database schema fix
    echo "🔧 Running database schema fix..."
    python fix_cpanel_database.py
    
    # Fix Flask warning (optional)
    echo "🔧 Checking Flask environment configuration..."
    python fix_flask_warning.py
    
    echo "✅ SQLAlchemy and connection fixes deployed successfully!"
    echo ""
    echo "🎉 FIXES DEPLOYED:"
    echo "   ✅ Fixed SQLAlchemy text() issue"
    echo "   ✅ Fixed connection pool disposal error"
    echo "   ✅ Enhanced error handling for connection recovery"
    echo "   ✅ Added proper null checks for connection objects"
    echo ""
    echo "🚀 Your application should now handle database connections properly!"
    
else
    echo "💻 Detected local development environment..."
    echo "✅ SQLAlchemy and connection fixes are ready for local testing!"
    echo "Run 'python app.py' to test the improvements locally."
fi

echo ""
echo "📋 WHAT WAS FIXED:"
echo "   • SQLAlchemy text() deprecation warning"
echo "   • Connection pool disposal null pointer error"
echo "   • Enhanced connection recovery with proper error handling"
echo "   • Better null checks for database session objects"
echo ""
echo "🔍 EXPECTED RESULTS:"
echo "   • No more 'Textual SQL expression' errors"
echo "   • No more 'NoneType' object errors"
echo "   • Better connection recovery logging"
echo "   • More stable database operations"
echo ""
echo "✨ Your Library Management System should now work without connection errors!"
