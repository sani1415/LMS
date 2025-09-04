#!/usr/bin/env python3
"""
Simple API test script for Library Management System
Run this after starting the Flask server to test basic functionality
"""

import requests
import json

BASE_URL = 'http://localhost:5001/api'

def test_health():
    """Test health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f'{BASE_URL}/health')
        print(f"Health check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_dashboard():
    """Test dashboard endpoint"""
    print("\nTesting dashboard...")
    try:
        response = requests.get(f'{BASE_URL}/dashboard')
        print(f"Dashboard: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Total books: {data.get('total_books', 0)}")
            print(f"Total authors: {data.get('total_authors', 0)}")
            print(f"Books available: {data.get('books_available', 0)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Dashboard test failed: {e}")
        return False

def test_books():
    """Test books endpoints"""
    print("\nTesting books endpoints...")
    try:
        # Get all books
        response = requests.get(f'{BASE_URL}/books')
        print(f"Get books: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data.get('books', []))} books")
        
        # Get categories
        response = requests.get(f'{BASE_URL}/categories')
        print(f"Get categories: {response.status_code}")
        
        # Get publishers
        response = requests.get(f'{BASE_URL}/publishers')
        print(f"Get publishers: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"Books test failed: {e}")
        return False

def test_members():
    """Test members endpoints"""
    print("\nTesting members endpoints...")
    try:
        response = requests.get(f'{BASE_URL}/members')
        print(f"Get members: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} members")
        return response.status_code == 200
    except Exception as e:
        print(f"Members test failed: {e}")
        return False

def test_issue_history():
    """Test issue history endpoint"""
    print("\nTesting issue history...")
    try:
        response = requests.get(f'{BASE_URL}/issue-history')
        print(f"Get issue history: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data.get('history', []))} issue records")
        return response.status_code == 200
    except Exception as e:
        print(f"Issue history test failed: {e}")
        return False

def test_library_log():
    """Test library log endpoint"""
    print("\nTesting library log...")
    try:
        response = requests.get(f'{BASE_URL}/library-log')
        print(f"Get library log: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data.get('logs', []))} log entries")
        return response.status_code == 200
    except Exception as e:
        print(f"Library log test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Library Management System API Test ===")
    print("Make sure the Flask server is running on http://localhost:5001")
    print()
    
    tests = [
        test_health,
        test_dashboard,
        test_books,
        test_members,
        test_issue_history,
        test_library_log
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All tests passed! The API is working correctly.")
    else:
        print("❌ Some tests failed. Check the server logs for details.")

if __name__ == '__main__':
    main()
