#!/usr/bin/env python3
"""
Test CSV Template Endpoint Script
This script tests the CSV template endpoint directly
"""

import os
import sys
import requests

def test_csv_endpoint():
    """Test the CSV template endpoint directly"""
    print("🔍 Testing CSV Template Endpoint...")
    print("=" * 50)
    
    try:
        # Test the endpoint
        url = "https://maktabah.idarah786.com/api/books/csv-template"
        
        print(f"Testing URL: {url}")
        
        response = requests.get(url, timeout=30)
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ CSV template download successful!")
            print(f"✅ Content-Type: {response.headers.get('Content-Type')}")
            print(f"✅ Content-Length: {response.headers.get('Content-Length')}")
            return True
        else:
            print(f"❌ CSV template download failed with status: {response.status_code}")
            print(f"❌ Response content: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_health_endpoint():
    """Test the health endpoint to see if the app is running"""
    print("\n🔍 Testing Health Endpoint...")
    print("=" * 50)
    
    try:
        url = "https://maktabah.idarah786.com/api/health"
        
        response = requests.get(url, timeout=10)
        
        print(f"Health endpoint status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"✅ Response: {response.json()}")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            print(f"❌ Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 CSV Template Endpoint Test")
    print("=" * 60)
    
    # Test health endpoint first
    health_ok = test_health_endpoint()
    
    if health_ok:
        # Test CSV template endpoint
        csv_ok = test_csv_endpoint()
        
        if csv_ok:
            print("\n🎉 CSV TEMPLATE ENDPOINT TEST PASSED!")
            print("The endpoint is working correctly.")
        else:
            print("\n🚨 CSV TEMPLATE ENDPOINT TEST FAILED")
            print("The endpoint is still returning errors.")
            print("Please check:")
            print("1. Is the updated backend/routes.py deployed?")
            print("2. Has the Python application been restarted?")
            print("3. Are there any server-side errors in the logs?")
    else:
        print("\n🚨 APPLICATION HEALTH CHECK FAILED")
        print("The application may not be running properly.")

if __name__ == '__main__':
    main()
