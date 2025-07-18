#!/usr/bin/env python3
"""
API Test Script
Test all the APIs defined in the CSV specification
"""

import requests
import json
import sys
from urllib.parse import urljoin

class APITester:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.token = None
        self.headers = {"Content-Type": "application/json"}
        
    def log(self, message, status="INFO"):
        print(f"[{status}] {message}")
    
    def make_request(self, method, endpoint, data=None, params=None):
        url = urljoin(self.base_url, endpoint)
        headers = self.headers.copy()
        
        if self.token:
            headers["Authorization"] = f"Token {self.token}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=params)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == "PATCH":
                response = requests.patch(url, headers=headers, json=data)
            else:
                self.log(f"Unsupported method: {method}", "ERROR")
                return None
            
            self.log(f"{method} {endpoint} - Status: {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            self.log(f"Request failed: {e}", "ERROR")
            return None
    
    def test_authentication_apis(self):
        self.log("Testing Authentication APIs", "INFO")
        
        # Test email OTP
        email = "test@example.com"
        response = self.make_request("POST", "/api/auth/send-email-otp/", {"email": email})
        if response and response.status_code == 200:
            self.log("✅ Send Email OTP - Success")
        else:
            self.log("❌ Send Email OTP - Failed")
        
        # Test mobile OTP
        mobile = "+1234567890"
        response = self.make_request("POST", "/api/auth/send-mobile-otp/", {"mobile": mobile})
        if response and response.status_code == 200:
            self.log("✅ Send Mobile OTP - Success")
        else:
            self.log("❌ Send Mobile OTP - Failed")
        
        # Note: OTP verification and signup would require actual OTP codes
        self.log("ℹ️  OTP verification and signup require actual OTP codes")
        
        # Test login with demo credentials (if user exists)
        login_data = {"emailOrMobile": email, "password": "testpassword123"}
        response = self.make_request("POST", "/api/auth/login/", login_data)
        if response and response.status_code == 200:
            data = response.json()
            if data.get("success"):
                self.token = data.get("token")
                self.log("✅ Login - Success")
            else:
                self.log("❌ Login - Failed")
        else:
            self.log("ℹ️  Login - No demo user available")
    
    def test_partner_apis(self):
        self.log("Testing Partner APIs", "INFO")
        
        if not self.token:
            self.log("⚠️  Skipping partner tests - no authentication token", "WARN")
            return
        
        # Test business details
        business_data = {
            "name": "Test Travel Company",
            "type_of_provider": ["Tour Operator", "Travel Agent"],
            "years": 5,
            "address": "123 Test Street, Test City",
            "employees": 10,
            "seasonal": False
        }
        
        response = self.make_request("PATCH", "/api/partner/business-details/", business_data)
        if response and response.status_code == 200:
            self.log("✅ Update Business Details - Success")
        else:
            self.log("❌ Update Business Details - Failed")
        
        response = self.make_request("GET", "/api/partner/business-details/")
        if response and response.status_code == 200:
            self.log("✅ Get Business Details - Success")
        else:
            self.log("❌ Get Business Details - Failed")
        
        # Test location coverage
        location_data = {
            "primary_location": "Mumbai",
            "destinations": [1, 2, 3],
            "languages": ["English", "Hindi"],
            "regions": ["Western India"],
            "pan_india": False,
            "seasons": ["Winter", "Summer"],
            "timezone": "Asia/Kolkata"
        }
        
        response = self.make_request("PATCH", "/api/partner/location-coverage/", location_data)
        if response and response.status_code == 200:
            self.log("✅ Update Location Coverage - Success")
        else:
            self.log("❌ Update Location Coverage - Failed")
        
        response = self.make_request("GET", "/api/partner/location-coverage/")
        if response and response.status_code == 200:
            self.log("✅ Get Location Coverage - Success")
        else:
            self.log("❌ Get Location Coverage - Failed")
        
        # Test tours services
        tours_data = {
            "number_of_tours": 25,
            "types_of_tours": ["Adventure", "Cultural"],
            "min_price": 5000.00,
            "group_size_min": 2,
            "group_size_max": 20,
            "offers_custom_tours": True
        }
        
        response = self.make_request("PATCH", "/api/partner/tours-services/", tours_data)
        if response and response.status_code == 200:
            self.log("✅ Update Tours Services - Success")
        else:
            self.log("❌ Update Tours Services - Failed")
        
        response = self.make_request("GET", "/api/partner/tours-services/")
        if response and response.status_code == 200:
            self.log("✅ Get Tours Services - Success")
        else:
            self.log("❌ Get Tours Services - Failed")
        
        # Test legal banking
        legal_data = {
            "pan_or_aadhaar": "ABCDE1234F",
            "company_type": "Private Limited",
            "emergency_contact": "+1234567890",
            "terms_accepted": True
        }
        
        response = self.make_request("PATCH", "/api/partner/legal-banking/", legal_data)
        if response and response.status_code == 200:
            self.log("✅ Update Legal Banking - Success")
        else:
            self.log("❌ Update Legal Banking - Failed")
        
        response = self.make_request("GET", "/api/partner/legal-banking/")
        if response and response.status_code == 200:
            self.log("✅ Get Legal Banking - Success")
        else:
            self.log("❌ Get Legal Banking - Failed")
        
        # Test partner status
        response = self.make_request("GET", "/api/partner/status/")
        if response and response.status_code == 200:
            self.log("✅ Get Partner Status - Success")
        else:
            self.log("❌ Get Partner Status - Failed")
        
        # Test complete onboarding
        response = self.make_request("POST", "/api/partner/complete-onboarding/")
        if response and response.status_code == 200:
            self.log("✅ Complete Onboarding - Success")
        else:
            self.log("❌ Complete Onboarding - Failed")
    
    def test_common_apis(self):
        self.log("Testing Common APIs", "INFO")
        
        # Test destinations
        response = self.make_request("GET", "/api/common/destinations/")
        if response and response.status_code == 200:
            self.log("✅ Get Destinations - Success")
        else:
            self.log("❌ Get Destinations - Failed")
        
        # Test destinations with search
        response = self.make_request("GET", "/api/common/destinations/", params={"search": "Mumbai"})
        if response and response.status_code == 200:
            self.log("✅ Search Destinations - Success")
        else:
            self.log("❌ Search Destinations - Failed")
        
        # Test languages
        response = self.make_request("GET", "/api/common/languages/")
        if response and response.status_code == 200:
            self.log("✅ Get Languages - Success")
        else:
            self.log("❌ Get Languages - Failed")
        
        # Test tour types
        response = self.make_request("GET", "/api/common/tour-types/")
        if response and response.status_code == 200:
            self.log("✅ Get Tour Types - Success")
        else:
            self.log("❌ Get Tour Types - Failed")
        
        # Test timezones
        response = self.make_request("GET", "/api/common/timezones/")
        if response and response.status_code == 200:
            self.log("✅ Get Timezones - Success")
        else:
            self.log("❌ Get Timezones - Failed")
    
    def run_all_tests(self):
        self.log("Starting API Tests", "INFO")
        self.log("=" * 50)
        
        self.test_common_apis()
        self.log("-" * 30)
        
        self.test_authentication_apis()
        self.log("-" * 30)
        
        self.test_partner_apis()
        self.log("=" * 50)
        
        self.log("API Tests Completed", "INFO")

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    tester = APITester(base_url)
    tester.run_all_tests()
