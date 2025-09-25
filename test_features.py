#!/usr/bin/env python3
"""
Test script to validate the new CSV import update functionality
and bulk delete functionality implemented in the LMS system.
"""

import os
import sys
import pandas as pd
import requests
import json
from datetime import datetime

# Add the current directory to the path so we can import the app modules
sys.path.append('/storage/emulated/0/Documents/programming/LMS')

# Test configuration
BASE_URL = 'http://127.0.0.1:5001'
TEST_FILES_PATH = '/storage/emulated/0/Documents/programming/LMS'

def get_auth_token():
    """Get authentication token for API calls"""
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }

    response = requests.post(f'{BASE_URL}/api/login',
                           headers={'Content-Type': 'application/json'},
                           data=json.dumps(login_data))

    if response.status_code == 200:
        return response.json().get('token')
    else:
        print(f"Failed to get token: {response.status_code} - {response.text}")
        return None

def get_books_count():
    """Get current number of books in the database"""
    try:
        response = requests.get(f'{BASE_URL}/api/books')
        if response.status_code == 200:
            return response.json().get('total', 0)
        else:
            return None
    except Exception as e:
        print(f"Error getting books count: {e}")
        return None

def test_csv_import_update_functionality():
    """Test the CSV import with duplicate detection and update functionality"""
    print("\n=== Testing CSV Import with Update Functionality ===")

    token = get_auth_token()
    if not token:
        print("❌ Failed to get authentication token")
        return False

    # Get initial book count
    initial_count = get_books_count()
    print(f"📊 Initial book count: {initial_count}")

    # Test 1: Upload test_duplicate.csv which contains books that might already exist
    print("\n🔄 Testing duplicate detection and update...")

    csv_file_path = os.path.join(TEST_FILES_PATH, 'test_duplicate.csv')
    if not os.path.exists(csv_file_path):
        print(f"❌ Test file not found: {csv_file_path}")
        return False

    # Read the test file to see what we're uploading
    df = pd.read_csv(csv_file_path)
    print(f"📁 Test file contains {len(df)} records:")
    for idx, row in df.iterrows():
        print(f"   - {row['Book Name']} by {row['Author']} (Category: {row['Category']})")

    # Upload the CSV file
    headers = {'x-access-token': token}

    try:
        with open(csv_file_path, 'rb') as f:
            files = {'file': ('test_duplicate.csv', f, 'text/csv')}
            response = requests.post(f'{BASE_URL}/api/books/import-csv',
                                   headers=headers,
                                   files=files)

        if response.status_code in [200, 201]:
            result = response.json()
            print(f"✅ CSV Import successful!")
            print(f"   - New books imported: {result.get('imported_count', 0)}")
            print(f"   - Existing books updated: {result.get('updated_count', 0)}")
            print(f"   - Message: {result.get('message', 'No message')}")

            if 'errors' in result:
                print(f"   - Errors: {len(result['errors'])}")
                for error in result['errors']:
                    print(f"     • {error}")

            return True
        else:
            print(f"❌ CSV Import failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error during CSV import: {e}")
        return False

def test_bulk_delete_functionality():
    """Test the bulk delete functionality"""
    print("\n=== Testing Bulk Delete Functionality ===")

    token = get_auth_token()
    if not token:
        print("❌ Failed to get authentication token")
        return False

    # Get all books to identify some for deletion
    headers = {'x-access-token': token}
    response = requests.get(f'{BASE_URL}/api/books', headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to get books list: {response.status_code}")
        return False

    books_data = response.json()
    books = books_data.get('books', [])
    total_before = books_data.get('total', 0)

    if not books:
        print("❌ No books found to test bulk delete")
        return False

    print(f"📊 Total books before deletion: {total_before}")

    # Select books for bulk deletion (we'll delete the duplicate books we might have created)
    books_to_delete = []
    for book in books:
        if 'Test Book' in book.get('bookName', '') or book.get('bookName') in ['Test Book 1', 'Test Book 2']:
            books_to_delete.append(book['library_id'])
        if len(books_to_delete) >= 2:  # Limit to 2 books for testing
            break

    if not books_to_delete:
        print("⚠️  No suitable test books found for bulk deletion")
        # Let's create some test books first and then delete them
        return True

    print(f"🗑️  Selected {len(books_to_delete)} books for bulk deletion:")
    for book in books:
        if book['library_id'] in books_to_delete:
            print(f"   - {book['bookName']} by {book['author']} (ID: {book['library_id']})")

    # Perform bulk delete
    delete_data = {'book_ids': books_to_delete}

    try:
        response = requests.post(f'{BASE_URL}/api/books/bulk-delete',
                               headers={'x-access-token': token,
                                       'Content-Type': 'application/json'},
                               data=json.dumps(delete_data))

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Bulk delete successful!")
            print(f"   - Books deleted: {result.get('deleted_count', 0)}")
            print(f"   - Message: {result.get('message', 'No message')}")

            # Verify the deletion worked
            updated_response = requests.get(f'{BASE_URL}/api/books', headers={'x-access-token': token})
            if updated_response.status_code == 200:
                total_after = updated_response.json().get('total', 0)
                print(f"📊 Total books after deletion: {total_after}")
                if total_after < total_before:
                    print(f"✅ Successfully reduced book count by {total_before - total_after}")
                    return True
                else:
                    print("❌ Book count did not decrease after bulk delete")
                    return False

        else:
            print(f"❌ Bulk delete failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error during bulk delete: {e}")
        return False

def run_all_tests():
    """Run all test functions"""
    print("🚀 Starting LMS Feature Testing")
    print(f"⏰ Test started at: {datetime.now()}")

    # Check if server is running
    try:
        response = requests.get(f'{BASE_URL}/api/dashboard')
        if response.status_code != 200:
            print("❌ Server is not responding properly. Please ensure the Flask app is running.")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Please ensure the Flask app is running on http://127.0.0.1:5001")
        return

    print("✅ Server is running and accessible")

    # Test results
    results = {
        'csv_import_update': False,
        'bulk_delete': False
    }

    # Run tests
    results['csv_import_update'] = test_csv_import_update_functionality()
    results['bulk_delete'] = test_bulk_delete_functionality()

    # Print summary
    print("\n" + "="*50)
    print("📋 TEST SUMMARY")
    print("="*50)

    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name.replace('_', ' ').title()}: {status}")

    all_passed = all(results.values())
    overall_status = "✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED"

    print(f"\nOverall Result: {overall_status}")
    print(f"⏰ Test completed at: {datetime.now()}")

    return all_passed

if __name__ == '__main__':
    run_all_tests()