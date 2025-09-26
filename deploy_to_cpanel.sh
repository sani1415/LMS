#!/bin/bash
# cPanel Deployment Script for LMS

echo "🚀 Starting cPanel deployment..."

# Activate virtual environment
source /home/idarahco/virtualenv/public_html/maktabah/3.11/bin/activate

echo "📦 Installing/updating dependencies..."

# Install all requirements
pip install -r requirements.txt

echo "✅ Dependencies installed successfully!"

# Reset database completely (removes Flask-Migrate tables and creates proper ones)
echo "🗄️ Resetting database schema..."
python reset_cpanel_database.py

echo "🎉 Deployment completed successfully!"
echo "Your LMS application should now be running on cPanel!"
