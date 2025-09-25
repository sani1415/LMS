#!/bin/bash
# cPanel Deployment Script for LMS

echo "🚀 Starting cPanel deployment..."

# Activate virtual environment
source /home/idarahco/virtualenv/public_html/maktabah/3.11/bin/activate

echo "📦 Installing/updating dependencies..."

# Install all requirements
pip install -r requirements.txt

# Fix pandas/numpy compatibility issues
pip install --upgrade --force-reinstall numpy==1.24.3 pandas==2.0.3

echo "✅ Dependencies installed successfully!"

# Run database migrations
echo "🗄️ Running database migrations..."
python -m flask db upgrade

echo "🎉 Deployment completed successfully!"
echo "Your LMS application should now be running on cPanel!"
