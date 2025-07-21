#!/usr/bin/env python3
"""
Test script to verify mobile OTP disable functionality
"""

import requests
import json

# Base URL - adjust as needed
BASE_URL = "http://localhost:8000/api/auth"

def test_mobile_otp_disabled():
    """Test that mobile OTP endpoints return proper disabled responses"""
    
    print("🧪 Testing Mobile OTP Disabled Functionality")
    print("=" * 50)
    
    # Test 1: Send Mobile OTP should return 503
    print("\n1. Testing send-mobile-otp endpoint...")
    try:
        response = requests.post(f"{BASE_URL}/send-mobile-otp/", 
                               json={"mobile": "+1234567890"})
        
        if response.status_code == 503:
            print("✅ PASS: send-mobile-otp correctly returns 503 (Service Unavailable)")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ FAIL: Expected 503, got {response.status_code}")
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ ERROR: Could not test send-mobile-otp: {e}")
    
    # Test 2: Verify Mobile OTP should return 503
    print("\n2. Testing verify-mobile-otp endpoint...")
    try:
        response = requests.post(f"{BASE_URL}/verify-mobile-otp/", 
                               json={"mobile": "+1234567890", "otp": "123456"})
        
        if response.status_code == 503:
            print("✅ PASS: verify-mobile-otp correctly returns 503 (Service Unavailable)")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ FAIL: Expected 503, got {response.status_code}")
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ ERROR: Could not test verify-mobile-otp: {e}")
    
    # Test 3: Bypass endpoint should work
    print("\n3. Testing bypass-mobile-verification endpoint...")
    try:
        response = requests.post(f"{BASE_URL}/bypass-mobile-verification/", 
                               json={"mobile": "+1234567890"})
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code in [200, 404]:  # 404 is OK if user doesn't exist
            print("✅ PASS: bypass endpoint is accessible")
        else:
            print(f"❌ FAIL: Unexpected status code {response.status_code}")
    except Exception as e:
        print(f"❌ ERROR: Could not test bypass endpoint: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")
    print("\nNote: Start your Django server first with:")
    print("   python manage.py runserver")

if __name__ == "__main__":
    test_mobile_otp_disabled()
