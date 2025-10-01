#!/usr/bin/env python3
"""
CSV Template Issue Diagnostic Script
This script helps diagnose the CSV template download issue
"""

import requests
import sys

def test_csv_endpoints():
    """Test CSV-related endpoints"""
    base_url = "https://maktabah.idarah786.com"
    
    print("🔍 Testing CSV Template Endpoints...")
    print("=" * 50)
    
    # Test 1: Simple CSV test endpoint
    print("1. Testing simple CSV test endpoint...")
    try:
        response = requests.get(f"{base_url}/api/test-csv", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ CSV test passed: {data.get('message')}")
            print(f"   ✅ CSV preview: {data.get('csv_preview')}")
        else:
            print(f"   ❌ CSV test failed: {response.text}")
    except Exception as e:
        print(f"   ❌ CSV test error: {e}")
    
    print()
    
    # Test 2: CSV template info endpoint
    print("2. Testing CSV template info endpoint...")
    try:
        response = requests.get(f"{base_url}/api/books/csv-template-info", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Template info: {data.get('message')}")
        else:
            print(f"   ❌ Template info failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Template info error: {e}")
    
    print()
    
    # Test 3: CSV template download endpoint
    print("3. Testing CSV template download endpoint...")
    try:
        response = requests.get(f"{base_url}/api/books/csv-template", timeout=15)
        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type')}")
        print(f"   Content-Length: {response.headers.get('Content-Length')}")
        
        if response.status_code == 200:
            print("   ✅ CSV template download successful!")
            print(f"   ✅ Content length: {len(response.content)} bytes")
            # Show first 100 characters
            content_preview = response.text[:100] if response.text else "No text content"
            print(f"   ✅ Content preview: {content_preview}")
        else:
            print(f"   ❌ CSV template download failed: {response.text}")
    except Exception as e:
        print(f"   ❌ CSV template download error: {e}")
    
    print()
    
    # Test 4: Health endpoint
    print("4. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health check: {data.get('status')} - {data.get('message')}")
            print(f"   ✅ Database: {data.get('database')}")
        else:
            print(f"   ❌ Health check failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Health check error: {e}")

def main():
    """Main diagnostic function"""
    print("🔧 CSV Template Download Diagnostic Tool")
    print("=" * 60)
    print("Testing endpoints on: https://maktabah.idarah786.com")
    print()
    
    test_csv_endpoints()
    
    print()
    print("📋 DIAGNOSIS SUMMARY:")
    print("=" * 30)
    print("If the simple CSV test (test 1) works but the template download (test 3) fails:")
    print("  → The issue is with the template download endpoint specifically")
    print()
    print("If all tests fail:")
    print("  → The issue is with the application deployment or server")
    print()
    print("If tests 1 and 2 work but test 3 fails:")
    print("  → The issue is with the send_file function or file generation")
    print()
    print("🔧 NEXT STEPS:")
    print("1. Check the server logs after running test 3")
    print("2. Verify the updated backend/routes.py is deployed")
    print("3. Restart the Python application in cPanel")

if __name__ == '__main__':
    main()
