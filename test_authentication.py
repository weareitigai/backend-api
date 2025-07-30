#!/usr/bin/env python3
"""
Test script to verify authentication is working correctly.
This script tests the login and profile endpoints to ensure Token authentication works.
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8000/api"
# For deployed version, use: BASE_URL = "https://backend-api-vpx2.onrender.com/api"

def test_authentication():
    """Test the complete authentication flow."""
    
    print("🔐 Testing Authentication Flow")
    print("=" * 50)
    
    # Test data
    test_email = "testuser@example.com"
    test_password = "password123"
    
    # Step 1: Login
    print("\n1️⃣ Testing Login...")
    login_data = {
        "email": test_email,
        "password": test_password
    }
    
    try:
        login_response = requests.post(
            f"{BASE_URL}/auth/login/",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            if login_result.get('success'):
                token = login_result.get('token')
                print(f"✅ Login successful!")
                print(f"   Token: {token[:20]}...")
                
                # Step 2: Test Profile with Token
                print("\n2️⃣ Testing Profile with Token...")
                headers = {
                    "Authorization": f"Token {token}",
                    "Content-Type": "application/json"
                }
                
                profile_response = requests.get(
                    f"{BASE_URL}/auth/profile/",
                    headers=headers
                )
                
                if profile_response.status_code == 200:
                    profile_result = profile_response.json()
                    if profile_result.get('success'):
                        user_data = profile_result.get('user', {})
                        print(f"✅ Profile access successful!")
                        print(f"   User: {user_data.get('fullName', 'N/A')}")
                        print(f"   Email: {user_data.get('email', 'N/A')}")
                    else:
                        print(f"❌ Profile access failed: {profile_result.get('message', 'Unknown error')}")
                else:
                    print(f"❌ Profile request failed with status {profile_response.status_code}")
                    print(f"   Response: {profile_response.text}")
                
                # Step 3: Test Logout
                print("\n3️⃣ Testing Logout...")
                logout_response = requests.post(
                    f"{BASE_URL}/auth/logout/",
                    headers=headers
                )
                
                if logout_response.status_code == 200:
                    logout_result = logout_response.json()
                    if logout_result.get('success'):
                        print(f"✅ Logout successful!")
                    else:
                        print(f"❌ Logout failed: {logout_result.get('message', 'Unknown error')}")
                else:
                    print(f"❌ Logout request failed with status {logout_response.status_code}")
                
                # Step 4: Test Profile after Logout (should fail)
                print("\n4️⃣ Testing Profile after Logout (should fail)...")
                profile_after_logout = requests.get(
                    f"{BASE_URL}/auth/profile/",
                    headers=headers
                )
                
                if profile_after_logout.status_code == 401:
                    print(f"✅ Profile access correctly denied after logout!")
                else:
                    print(f"⚠️  Profile access not denied after logout (status: {profile_after_logout.status_code})")
                
            else:
                print(f"❌ Login failed: {login_result.get('message', 'Unknown error')}")
        else:
            print(f"❌ Login request failed with status {login_response.status_code}")
            print(f"   Response: {login_response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection error: Make sure the server is running at {BASE_URL}")
        print("   Start the server with: python manage.py runserver")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_token_format():
    """Test different token formats to ensure correct format is used."""
    
    print("\n🔍 Testing Token Format")
    print("=" * 50)
    
    # Test data
    test_token = "test_token_123"
    
    # Test different formats
    formats = [
        ("Token", f"Token {test_token}"),
        ("Bearer", f"Bearer {test_token}"),
        ("No prefix", test_token)
    ]
    
    for format_name, header_value in formats:
        print(f"\nTesting format: {format_name}")
        headers = {
            "Authorization": header_value,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(
                f"{BASE_URL}/auth/profile/",
                headers=headers
            )
            
            if response.status_code == 401:
                print(f"   ✅ Correctly rejected invalid token")
            else:
                print(f"   ⚠️  Unexpected response: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Authentication Tests")
    print("=" * 50)
    
    # Test the main authentication flow
    test_authentication()
    
    # Test token format validation
    test_token_format()
    
    print("\n" + "=" * 50)
    print("🏁 Authentication tests completed!")
    print("\n📝 Summary:")
    print("   - Use 'Token <your_token>' format for authentication")
    print("   - Frontend automatically handles token storage and injection")
    print("   - Swagger UI is configured for Token authentication")
    print("   - Postman collection uses correct Token format") 