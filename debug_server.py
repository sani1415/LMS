#!/usr/bin/env python3
"""
Debug script to troubleshoot Flask server connection issues
Run this to check if your server is working correctly
"""

import requests
import time
import sys

def test_server_connection():
    """Test if the Flask server is running and accessible"""
    base_url = "http://localhost:5001"
    
    print("🔍 Testing Flask Server Connection...")
    print("=" * 50)
    
    # Test 1: Basic connection
    print("\n1️⃣ Testing basic server connection...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and accessible!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Server responded with status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Server is not running.")
        print("   Make sure to run: python app.py")
        return False
    except requests.exceptions.Timeout:
        print("❌ Connection timeout! Server might be slow to respond.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    # Test 2: Dashboard endpoint
    print("\n2️⃣ Testing dashboard endpoint...")
    try:
        response = requests.get(f"{base_url}/api/dashboard", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Dashboard endpoint working!")
            print(f"   Total Books: {data.get('total_books', 0)}")
            print(f"   Total Members: {data.get('total_authors', 0)}")
        else:
            print(f"❌ Dashboard failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Dashboard test failed: {e}")
    
    # Test 3: Books endpoint
    print("\n3️⃣ Testing books endpoint...")
    try:
        response = requests.get(f"{base_url}/api/books", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Books endpoint working!")
            print(f"   Total Books: {data.get('total', 0)}")
        else:
            print(f"❌ Books failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Books test failed: {e}")
    
    # Test 4: Test all endpoints
    print("\n4️⃣ Testing all API endpoints...")
    endpoints = [
        '/api/health',
        '/api/dashboard', 
        '/api/books',
        '/api/members',
        '/api/categories',
        '/api/publishers',
        '/api/issue-history',
        '/api/library-log'
    ]
    
    working_endpoints = 0
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {endpoint}")
                working_endpoints += 1
            else:
                print(f"   ❌ {endpoint} - Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {endpoint} - Error: {e}")
    
    print(f"\n📊 Summary: {working_endpoints}/{len(endpoints)} endpoints working")
    
    if working_endpoints == len(endpoints):
        print("🎉 All endpoints are working! Your server is ready.")
        return True
    else:
        print("⚠️  Some endpoints are not working. Check server logs.")
        return False

def check_port_availability():
    """Check if port 5001 is available"""
    print("\n🔌 Checking port 5001 availability...")
    
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 5001))
        sock.close()
        
        if result == 0:
            print("✅ Port 5001 is in use (server might be running)")
        else:
            print("❌ Port 5001 is not in use (server is not running)")
            print("   Start your server with: python app.py")
    except Exception as e:
        print(f"❌ Could not check port: {e}")

def main():
    """Main debug function"""
    print("🚀 LMS Server Debug Tool")
    print("=" * 50)
    
    # Check port availability
    check_port_availability()
    
    # Test server connection
    success = test_server_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Your Flask server is working correctly!")
        print("   You can now open your frontend files in the browser.")
    else:
        print("❌ Server connection failed!")
        print("\n🔧 Troubleshooting steps:")
        print("   1. Make sure you ran: python app.py")
        print("   2. Check if another process is using port 5001")
        print("   3. Check terminal for error messages")
        print("   4. Try running: python init_db.py first")
    
    print("\n📝 Next steps:")
    print("   - If server is working: Open test_integration.html in browser")
    print("   - If server failed: Check the error messages above")

if __name__ == "__main__":
    main()
