#!/bin/bash

# UNIFIED DEPLOYMENT SCRIPT - Works for both development and cPanel
# This script ensures your app works identically everywhere

set -e

echo "🚀 Starting UNIFIED deployment..."

# Check if we're on cPanel (production) or local development
if [ -d "/home" ] && [ -d "/home/idarahco" ]; then
    echo "📦 Detected cPanel environment - setting up production..."
    
    # Define your virtual environment path
    VENV_PATH="/home/idarahco/virtualenv/public_html/maktabah/3.11"
    
    # Activate virtual environment
    echo "Activating virtual environment: $VENV_PATH"
    source "$VENV_PATH/bin/activate"
    
    # Install/update dependencies
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    
    # Fix database collation issues
    echo "🔧 Fixing database collation issues..."
    python fix_cpanel_collation.py
    
    echo "✅ Dependencies installed successfully!"
    echo "🎉 cPanel deployment completed!"
    echo "Your app will automatically create database tables on startup!"
    
else
    echo "💻 Detected local development environment..."
    
    # Check if MySQL is running
    if ! pgrep -x "mysqld" > /dev/null; then
        echo "⚠️  MySQL is not running. Please start MySQL first."
        echo "   On Windows: Start MySQL service"
        echo "   On Mac: brew services start mysql"
        echo "   On Linux: sudo systemctl start mysql"
        exit 1
    fi
    
    # Install dependencies
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    
    echo "✅ Dependencies installed successfully!"
    echo "🎉 Local development setup completed!"
    echo "Run 'python app.py' to start your application!"
fi

echo ""
echo "🔧 UNIFIED CONFIGURATION:"
echo "   - Database: MySQL (same for dev and production)"
echo "   - Tables: Auto-created on startup"
echo "   - Admin user: Auto-created (admin/admin123)"
echo "   - CSV/Excel: Full support"
echo "   - No Flask-Migrate: Simplified setup"
echo ""
echo "✨ Your app now works identically everywhere!"
