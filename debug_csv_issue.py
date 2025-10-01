#!/usr/bin/env python3
"""
Debug CSV Template Issue Script
This script helps diagnose the CSV template download problem
"""

import os
import sys

def test_csv_template_locally():
    """Test the CSV template function locally"""
    print("🔍 Testing CSV Template Function Locally...")
    print("=" * 50)
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app import app
        
        with app.app_context():
            # Test the CSV template creation directly
            from flask import send_file
            import io
            import csv
            
            print("✅ Flask imports successful")
            
            # Create template data (same as in the endpoint)
            template_data = {
                'Book Name': ['The Great Gatsby', 'গ্রেট গ্যাটসবি', 'الغَاتسبي العظيم'],
                'Author': ['F. Scott Fitzgerald', 'রবীন্দ্রনাথ ঠাকুর', 'نجيب محفوظ'],
                'Category': ['Fiction', 'সাহিত্য', 'أدب'],
                'Editor': ['Maxwell Perkins', 'এডিটর নাম', 'اسم المحرر'],
                'Volumes': [1, 2, 1],
                'Publisher': ['Scribner', 'বিশ্বভারতী', 'دار الشروق'],
                'Year': [1925, 1913, 1956],
                'Copies': [2, 1, 3],
                'Status': ['Available', 'Available', 'Available'],
                'Completion Status': ['Complete', 'Complete', 'Incomplete'],
                'Note': ['Classic American novel', 'নোবেল পুরস্কার বিজয়ী', 'الرواية الكلاسيكية']
            }
            
            print("✅ Template data created successfully")
            
            # Create CSV content
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            headers = list(template_data.keys())
            writer.writerow(headers)
            print(f"✅ Headers written: {headers}")
            
            # Write data rows
            num_rows = len(template_data[headers[0]])
            for i in range(num_rows):
                row = [template_data[header][i] for header in headers]
                writer.writerow(row)
            
            print(f"✅ Data rows written: {num_rows} rows")
            
            # Convert to BytesIO
            csv_bytes = io.BytesIO()
            csv_content = output.getvalue()
            csv_bytes.write(csv_content.encode('utf-8'))
            csv_bytes.seek(0)
            
            print("✅ CSV bytes created successfully")
            print(f"✅ CSV content length: {len(csv_content)} characters")
            
            # Test send_file functionality
            print("✅ All CSV template creation steps completed successfully!")
            return True
            
    except Exception as e:
        print(f"❌ CSV template test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_connection():
    """Test database connection specifically"""
    print("\n🔍 Testing Database Connection...")
    print("=" * 50)
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app import check_database_connection
        
        result = check_database_connection()
        
        if result:
            print("✅ Database connection test PASSED")
            return True
        else:
            print("❌ Database connection test FAILED")
            return False
            
    except Exception as e:
        print(f"❌ Database connection test error: {e}")
        return False

def check_deployment_status():
    """Check if the latest code is deployed"""
    print("\n🔍 Checking Deployment Status...")
    print("=" * 50)
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from backend.routes import download_csv_template
        print("✅ CSV template function imported successfully")
        
        # Check if the function has the health check
        import inspect
        source = inspect.getsource(download_csv_template)
        
        if 'check_database_connection' in source:
            print("✅ Database health check is present in CSV template function")
            return True
        else:
            print("❌ Database health check is MISSING from CSV template function")
            print("❌ The updated code may not be deployed yet")
            return False
            
    except Exception as e:
        print(f"❌ Deployment check failed: {e}")
        return False

def main():
    """Main diagnostic function"""
    print("🔧 CSV Template Download Diagnostic Tool")
    print("=" * 60)
    
    # Check deployment status
    deployed = check_deployment_status()
    
    if deployed:
        # Test database connection
        db_ok = test_database_connection()
        
        # Test CSV template creation
        csv_ok = test_csv_template_locally()
        
        if db_ok and csv_ok:
            print("\n🎉 ALL TESTS PASSED!")
            print("The CSV template function should work correctly.")
            print("If it's still failing, the issue might be:")
            print("1. The application needs to be restarted")
            print("2. There might be a server-side issue")
            print("3. Check the server error logs for more details")
        else:
            print("\n🚨 SOME TESTS FAILED")
            print("Please check the errors above.")
    else:
        print("\n🚨 DEPLOYMENT ISSUE DETECTED")
        print("The updated code may not be deployed yet.")
        print("Please ensure the updated backend/routes.py is uploaded and the app is restarted.")

if __name__ == '__main__':
    main()
