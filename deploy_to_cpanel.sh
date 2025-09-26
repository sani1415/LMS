#!/bin/bash
# cPanel Deployment Script for LMS

echo "🚀 Starting cPanel deployment..."

# Activate virtual environment
source /home/idarahco/virtualenv/public_html/maktabah/3.11/bin/activate

echo "📦 Installing/updating dependencies..."

# Install all requirements
pip install -r requirements.txt

echo "✅ Dependencies installed successfully!"

# Fix database schema
echo "🗄️ Fixing database schema..."
python fix_cpanel_database.py

echo "🎉 Deployment completed successfully!"
echo "Your LMS application should now be running on cPanel!"
