#!/usr/bin/env python3

import requests
import json

# First login to get a token
login_data = {
    "emailOrMobile": "test@example.com",
    "password": "testpassword123"
}

login_response = requests.post("http://localhost:8000/api/auth/login/", json=login_data)
print("Login response:", login_response.status_code, login_response.json())

if login_response.status_code == 200:
    token = login_response.json()["token"]
    headers = {"Authorization": f"Token {token}"}
    
    # Test business details with sample data
    business_data = {
        "name": "Test Business",
        "type_of_provider": ["Tour Operator", "Travel Agent"],
        "gstin": "12ABCDE1234F1Z5",
        "years": 5,
        "website": "https://testbusiness.com",
        "reg_number": "REG123456",
        "address": "123 Test Street, Test City, Test State",
        "employees": 10,
        "seasonal": False,
        "annual_bookings": 1000
    }
    
    print("\nSending business details:", json.dumps(business_data, indent=2))
    
    business_response = requests.patch(
        "http://localhost:8000/api/partner/business-details/", 
        json=business_data,
        headers=headers
    )
    
    print("\nBusiness details response:", business_response.status_code)
    print("Response body:", business_response.json())
else:
    print("Login failed!")
