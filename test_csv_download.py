#!/usr/bin/env python3
"""
Test CSV Download Script
This script tests the actual CSV template download functionality
"""

import requests
import sys

def test_csv_download():
    """Test the actual CSV template download"""
    print("🔍 Testing CSV Template Download...")
    print("=" * 50)
    
    try:
        url = "https://maktabah.idarah786.com/api/books/csv-template"
        
        print(f"Testing URL: {url}")
        
        # Make the request
        response = requests.get(url, timeout=30)
        
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        
        if response.status_code == 200:
            print("✅ CSV template download successful!")
            print(f"✅ Content length: {len(response.content)} bytes")
            print(f"✅ Content type: {response.headers.get('Content-Type')}")
            
            # Check if it's actually CSV content
            if 'text/csv' in response.headers.get('Content-Type', ''):
                print("✅ Content type is correct (CSV)")
            else:
                print("⚠️  Content type might be incorrect")
            
            # Show first 200 characters of content
            content_preview = response.text[:200] if response.text else "No text content"
            print(f"✅ Content preview: {content_preview}")
            
            return True
            
        else:
            print(f"❌ CSV template download failed!")
            print(f"❌ Status: {response.status_code}")
            print(f"❌ Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_simple_csv():
    """Test the simple CSV test endpoint"""
    print("\n🔍 Testing Simple CSV Endpoint...")
    print("=" * 50)
    
    try:
        url = "https://maktabah.idarah786.com/api/test-csv"
        
        response = requests.get(url, timeout=10)
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Simple CSV test successful!")
            print(f"✅ Message: {data.get('message')}")
            print(f"✅ CSV preview: {data.get('csv_preview')}")
            return True
        else:
            print(f"❌ Simple CSV test failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Simple CSV test error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 CSV Template Download Test")
    print("=" * 60)
    
    # Test simple CSV first
    simple_ok = test_simple_csv()
    
    if simple_ok:
        print("\n✅ Simple CSV functionality works!")
        print("Now testing actual template download...")
        
        # Test actual CSV template download
        download_ok = test_csv_download()
        
        if download_ok:
            print("\n🎉 CSV TEMPLATE DOWNLOAD TEST PASSED!")
            print("The CSV template download is working correctly.")
        else:
            print("\n🚨 CSV TEMPLATE DOWNLOAD TEST FAILED!")
            print("The template download endpoint is still having issues.")
            print("\n🔧 POSSIBLE CAUSES:")
            print("1. The updated code might not be deployed yet")
            print("2. There might be a server-side error in the template generation")
            print("3. The send_file function might be failing")
            print("4. There might be a permission issue")
    else:
        print("\n🚨 SIMPLE CSV TEST FAILED!")
        print("Basic CSV functionality is not working.")
        print("This suggests a broader application issue.")

if __name__ == '__main__':
    main()
