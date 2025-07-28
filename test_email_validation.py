#!/usr/bin/env python3
"""
Test script for enhanced email validation
"""

import requests
import json

# API base URL - adjust as needed
BASE_URL = "http://localhost:8000/api/auth"

def test_email_validation():
    """Test email format and domain validation"""
    print("Testing enhanced email validation...")
    
    # Test cases
    test_cases = [
        {
            "email": "test@gmail.com",
            "expected": "valid",
            "description": "Valid email with real domain"
        },
        {
            "email": "user@example.com",
            "expected": "valid",
            "description": "Valid email with example domain"
        },
        {
            "email": "invalid-email",
            "expected": "invalid",
            "description": "Invalid email format (no @ symbol)"
        },
        {
            "email": "test@nonexistentdomain12345.com",
            "expected": "invalid",
            "description": "Invalid domain (doesn't exist)"
        },
        {
            "email": "test@.com",
            "expected": "invalid",
            "description": "Invalid email format (no domain)"
        },
        {
            "email": "@gmail.com",
            "expected": "invalid",
            "description": "Invalid email format (no username)"
        },
        {
            "email": "a" * 101 + "@gmail.com",
            "expected": "invalid",
            "description": "Email too long (>100 chars)"
        },
        {
            "email": "test..test@gmail.com",
            "expected": "invalid",
            "description": "Invalid email format (double dots)"
        },
        {
            "email": "test@test@test.com",
            "expected": "invalid",
            "description": "Invalid email format (multiple @ symbols)"
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\nTest {i+1}: {test_case['description']}")
        print(f"Email: {test_case['email']}")
        
        data = {"email": test_case["email"]}
        response = requests.post(f"{BASE_URL}/send-email-otp/", json=data)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if test_case["expected"] == "valid" and response.status_code == 200:
            print("✅ PASS")
        elif test_case["expected"] == "invalid" and response.status_code == 400:
            print("✅ PASS")
        else:
            print("❌ FAIL")

def test_real_email_domains():
    """Test with real email domains"""
    print("\nTesting with real email domains...")
    
    real_domains = [
        "gmail.com",
        "yahoo.com", 
        "hotmail.com",
        "outlook.com",
        "icloud.com"
    ]
    
    for domain in real_domains:
        email = f"test@{domain}"
        print(f"\nTesting: {email}")
        
        data = {"email": email}
        response = requests.post(f"{BASE_URL}/send-email-otp/", json=data)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ PASS - Valid domain")
        elif response.status_code == 400:
            print("❌ FAIL - Invalid domain")
        else:
            print("❓ UNEXPECTED")

def test_invalid_domains():
    """Test with invalid domains"""
    print("\nTesting with invalid domains...")
    
    invalid_domains = [
        "nonexistentdomain12345.com",
        "invalid-domain-that-does-not-exist.com",
        "fake-domain-12345.com"
    ]
    
    for domain in invalid_domains:
        email = f"test@{domain}"
        print(f"\nTesting: {email}")
        
        data = {"email": email}
        response = requests.post(f"{BASE_URL}/send-email-otp/", json=data)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 400:
            print("✅ PASS - Correctly rejected invalid domain")
        else:
            print("❌ FAIL - Should have rejected invalid domain")

if __name__ == "__main__":
    print("Starting enhanced email validation tests...")
    
    # Make sure the server is running first
    try:
        response = requests.get(f"{BASE_URL}/profile/")
        print("✅ Server is running")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start the Django server first.")
        exit(1)
    
    test_email_validation()
    test_real_email_domains()
    test_invalid_domains()
    
    print("\n🎉 All email validation tests completed!") 