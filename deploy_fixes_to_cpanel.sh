#!/bin/bash

# Deploy Fixes to cPanel Script
# This script helps deploy the fixed files to cPanel

echo "🚀 Deploying fixes to cPanel..."
echo "=================================="

# Files to deploy (add your cPanel details here)
CPANEL_HOST="your-cpanel-host.com"
CPANEL_USER="your-username"
CPANEL_PATH="/home/your-username/public_html/maktabah"

echo "📁 Files to deploy:"
echo "- backend/routes.py (CSV export fix)"
echo "- js/app.js (Category addition fix)"
echo "- fix_cpanel_database.py (Database schema fix)"
echo ""

echo "🔧 Manual deployment steps:"
echo "1. Upload these files to your cPanel:"
echo "   - backend/routes.py"
echo "   - js/app.js" 
echo "   - fix_cpanel_database.py"
echo ""
echo "2. Run the database fix script on cPanel:"
echo "   python fix_cpanel_database.py"
echo ""
echo "3. Restart your application on cPanel"
echo ""

echo "📋 Alternative: Use File Manager in cPanel"
echo "1. Go to cPanel → File Manager"
echo "2. Navigate to public_html/maktabah/"
echo "3. Upload the fixed files"
echo "4. Run the database fix script via Terminal"
echo ""

echo "✅ Deployment instructions ready!"
echo "After deployment, your application should work without errors."
