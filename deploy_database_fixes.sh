#!/bin/bash

# Database Connection Fixes Deployment Script
# This script deploys the database connection stability improvements

set -e

echo "🔧 Deploying Database Connection Fixes..."
echo "========================================"

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
    
    echo "✅ Database connection fixes deployed successfully!"
    echo ""
    echo "🎉 IMPROVEMENTS DEPLOYED:"
    echo "   ✅ Optimized connection pool settings for cPanel"
    echo "   ✅ Enhanced error handling and recovery"
    echo "   ✅ Added connection health checks"
    echo "   ✅ Improved error messages for users"
    echo "   ✅ Better environment variable validation"
    echo ""
    echo "🚀 Your application should now handle database connection issues gracefully!"
    
else
    echo "💻 Detected local development environment..."
    echo "✅ Database connection fixes are ready for local testing!"
    echo "Run 'python app.py' to test the improvements locally."
fi

echo ""
echo "📋 WHAT WAS FIXED:"
echo "   • MySQL connection timeouts and 'gone away' errors"
echo "   • Connection pool settings optimized for shared hosting"
echo "   • Automatic connection recovery and health checks"
echo "   • Better error handling with 503 status codes"
echo "   • Enhanced logging for debugging"
echo ""
echo "🔍 TESTING:"
echo "   • Visit /api/health to check system status"
echo "   • Monitor logs for connection recovery messages"
echo "   • All API endpoints now have connection health checks"
echo ""
echo "✨ Your Library Management System is now more stable and resilient!"
