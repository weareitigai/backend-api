#!/usr/bin/env python
"""
Render Deployment Verification Script
Test this after deploying to Render
"""
import sys
import requests
import json

def test_render_deployment(base_url):
    """Test Render deployment endpoints."""
    
    if not base_url.startswith('http'):
        base_url = f"https://{base_url}"
    
    print(f"🔍 Testing Render deployment: {base_url}")
    print("=" * 50)
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/health/", timeout=30)
        if response.status_code == 200:
            print("✅ Health check: PASSED")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Health check: ERROR - {e}")
        return False
    
    # Test API documentation
    try:
        response = requests.get(f"{base_url}/api/docs/", timeout=30)
        if response.status_code == 200:
            print("✅ API Documentation: ACCESSIBLE")
        else:
            print(f"⚠️  API Documentation: {response.status_code}")
    except Exception as e:
        print(f"⚠️  API Documentation: ERROR - {e}")
    
    # Test common APIs
    endpoints = [
        "/api/common/languages/",
        "/api/common/tour-types/",
        "/api/common/destinations/",
        "/api/common/timezones/"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=30)
            if response.status_code == 200:
                print(f"✅ {endpoint}: WORKING")
            else:
                print(f"❌ {endpoint}: FAILED ({response.status_code})")
        except Exception as e:
            print(f"❌ {endpoint}: ERROR - {e}")
    
    # Test authentication signup
    try:
        signup_data = {
            "first_name": "Render",
            "last_name": "Test",
            "email": "render-test@example.com",
            "password": "rendertest123"
        }
        response = requests.post(
            f"{base_url}/api/auth/signup/",
            json=signup_data,
            timeout=30
        )
        if response.status_code == 201:
            print("✅ Authentication signup: WORKING")
            data = response.json()
            if 'token' in data:
                print("✅ Token generation: WORKING")
        else:
            print(f"⚠️  Authentication signup: {response.status_code}")
            if response.status_code == 400:
                error_data = response.json()
                if "already exists" in str(error_data):
                    print("   (User already exists - signup working)")
    except Exception as e:
        print(f"❌ Authentication signup: ERROR - {e}")
    
    print("\n🚀 Render deployment test completed!")
    print(f"📡 Your API: {base_url}")
    print(f"📚 API Docs: {base_url}/api/docs/")
    print(f"🏠 Health: {base_url}/health/")
    
    return True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python check_render_deployment.py <your-app-url.onrender.com>")
        print("Example: python check_render_deployment.py django-travel-api.onrender.com")
        sys.exit(1)
    
    url = sys.argv[1]
    test_render_deployment(url) 