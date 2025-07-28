#!/usr/bin/env python3
"""
Test script for signup validation features
"""

import requests
import json

# API base URL - adjust as needed
BASE_URL = "http://localhost:8000/api/auth"

def test_email_validation():
    """Test email format and length validation"""
    print("Testing email validation...")
    
    # Test cases
    test_cases = [
        {
            "email": "test@example.com",
            "expected": "valid",
            "description": "Valid email"
        },
        {
            "email": "a" * 101 + "@example.com",  # 101 characters + domain
            "expected": "invalid",
            "description": "Email too long (>100 chars)"
        },
        {
            "email": "invalid-email",
            "expected": "invalid", 
            "description": "Invalid email format"
        },
        {
            "email": "test@example.com",
            "expected": "exists",
            "description": "Email already exists (after first request)"
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\nTest {i+1}: {test_case['description']}")
        
        data = {"email": test_case["email"]}
        response = requests.post(f"{BASE_URL}/send-email-otp/", json=data)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if test_case["expected"] == "valid" and response.status_code == 200:
            print("✅ PASS")
        elif test_case["expected"] == "invalid" and response.status_code == 400:
            print("✅ PASS")
        elif test_case["expected"] == "exists" and response.status_code == 400:
            print("✅ PASS")
        else:
            print("❌ FAIL")

def test_password_validation():
    """Test password length validation"""
    print("\nTesting password validation...")
    
    test_cases = [
        {
            "password": "123456",
            "expected": "valid",
            "description": "Valid password (6 chars)"
        },
        {
            "password": "12345",
            "expected": "invalid",
            "description": "Password too short (5 chars)"
        },
        {
            "password": "strongpassword123",
            "expected": "valid",
            "description": "Strong password (>6 chars)"
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\nTest {i+1}: {test_case['description']}")
        
        data = {
            "firstName": "Test",
            "lastName": "User", 
            "companyName": "Test Company",
            "email": f"test{i}@example.com",
            "password": test_case["password"]
        }
        
        response = requests.post(f"{BASE_URL}/signup/", json=data)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if test_case["expected"] == "valid" and response.status_code in [200, 201]:
            print("✅ PASS")
        elif test_case["expected"] == "invalid" and response.status_code == 400:
            print("✅ PASS")
        else:
            print("❌ FAIL")

def test_rate_limiting():
    """Test rate limiting for OTP requests"""
    print("\nTesting rate limiting...")
    
    email = "ratelimit@example.com"
    
    print(f"Making multiple OTP requests for {email}...")
    
    for i in range(5):  # Try 5 requests (limit is 3)
        data = {"email": email}
        response = requests.post(f"{BASE_URL}/send-email-otp/", json=data)
        
        print(f"Request {i+1}: Status {response.status_code}")
        print(f"Response: {response.json()}")
        
        if i < 2:  # First 3 should succeed
            if response.status_code == 200:
                print("✅ PASS")
            else:
                print("❌ FAIL")
        else:  # Requests 4+ should be rate limited
            if response.status_code == 429:
                print("✅ PASS (Rate limited)")
            else:
                print("❌ FAIL")

if __name__ == "__main__":
    print("Starting signup validation tests...")
    
    # Make sure the server is running first
    try:
        response = requests.get(f"{BASE_URL}/profile/")
        print("✅ Server is running")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start the Django server first.")
        exit(1)
    
    test_email_validation()
    test_password_validation()
    test_rate_limiting()
    
    print("\n🎉 All tests completed!") 