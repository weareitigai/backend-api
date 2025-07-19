#!/usr/bin/env python3

import requests
import json

# First login to get a token
login_data = {
    "emailOrMobile": "test@example.com",
    "password": "testpassword123"
}

login_response = requests.post("http://localhost:8000/api/auth/login/", json=login_data)
print("Login response:", login_response.status_code)

if login_response.status_code == 200:
    token = login_response.json()["token"]
    headers = {"Authorization": f"Token {token}"}
    
    # Test 1: Business Details
    print("\n1. Testing Business Details...")
    business_data = {
        "name": "Test Business",
        "type_of_provider": ["Tour Operator"],
        "years": 5,
        "address": "123 Test Street",
        "employees": 10,
        "seasonal": False
    }
    
    business_response = requests.patch(
        "http://localhost:8000/api/partner/business-details/", 
        json=business_data,
        headers=headers
    )
    print(f"Business Details: {business_response.status_code}")
    
    # Test 2: Location Coverage
    print("\n2. Testing Location Coverage...")
    location_data = {
        "primary_location": "Mumbai",
        "destinations": ["Mumbai", "Delhi", "Goa"],
        "languages": ["English", "Hindi"],
        "regions": ["Western India"],
        "pan_india": False,
        "seasons": ["All Year"],
        "timezone": "Asia/Kolkata"
    }
    
    location_response = requests.patch(
        "http://localhost:8000/api/partner/location-coverage/", 
        json=location_data,
        headers=headers
    )
    print(f"Location Coverage: {location_response.status_code}")
    
    # Test 3: Tours Services
    print("\n3. Testing Tours Services...")
    tours_data = {
        "number_of_tours": 10,
        "types_of_tours": ["Adventure Tours", "Cultural Tours"],
        "min_price": 2500.00,
        "group_size_min": 2,
        "group_size_max": 20,
        "preference": "Quality over Quantity",
        "offers_custom_tours": True
    }
    
    tours_response = requests.patch(
        "http://localhost:8000/api/partner/tours-services/", 
        json=tours_data,
        headers=headers
    )
    print(f"Tours Services: {tours_response.status_code}")
    
    # Test 4: Legal Banking (without file upload for now)
    print("\n4. Testing Legal Banking...")
    legal_data = {
        "pan_or_aadhaar": "ABCDE1234F",
        "company_type": "Private Limited",
        "emergency_contact": "+9876543210",
        "terms_accepted": True
    }
    
    legal_response = requests.patch(
        "http://localhost:8000/api/partner/legal-banking/", 
        json=legal_data,
        headers=headers
    )
    print(f"Legal Banking: {legal_response.status_code}")
    
    print("\nAll onboarding steps tested!")
    
else:
    print("Login failed!")
