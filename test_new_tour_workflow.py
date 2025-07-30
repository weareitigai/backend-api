#!/usr/bin/env python3
"""
Test script for the new streamlined tour creation workflow.
This demonstrates the new automatic tour creation from URL scraping.
"""

import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
TOKEN = None  # Will be set after login

def login_and_get_token():
    """Login and get authentication token."""
    global TOKEN
    
    login_data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    
    if response.status_code == 200:
        data = response.json()
        TOKEN = data.get('token')
        print(f"✅ Login successful! Token: {TOKEN[:20]}...")
        return True
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(response.text)
        return False

def test_scrape_tour_details():
    """Test the scraping workflow - Step 1."""
    
    if not TOKEN:
        print("❌ No authentication token available. Please login first.")
        return
    
    # Test URL (you can change this to any tour URL)
    test_url = "https://example.com/sample-tour"
    
    headers = {
        "Authorization": f"Token {TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "url": test_url
    }
    
    print(f"\n🚀 Testing tour scraping (Step 1)...")
    print(f"URL: {test_url}")
    
    response = requests.post(
        f"{BASE_URL}/partner/scrape-tour-details/",
        headers=headers,
        json=data
    )
    
    print(f"\n📊 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Tour data scraped successfully!")
        print(f"📝 Message: {result.get('message')}")
        
        # Show scraped data
        scraped_data = result.get('data', {})
        print(f"\n📋 Scraped Tour Data:")
        print(f"   Title: {scraped_data.get('title')}")
        print(f"   Destinations: {scraped_data.get('destinations')}")
        print(f"   Duration: {scraped_data.get('durationDays')} days, {scraped_data.get('durationNights')} nights")
        print(f"   Price: ₹{scraped_data.get('startingPrice')} ({scraped_data.get('priceType')})")
        print(f"   Provider: {scraped_data.get('providerName')}")
        print(f"   Status: {scraped_data.get('tourStatus')}")
        
        # Show request data
        request_data = result.get('request_data', {})
        print(f"\n🔍 Request Data:")
        print(f"   Original URL: {request_data.get('url')}")
        
        return scraped_data  # Return for Step 2
        
    elif response.status_code == 400:
        result = response.json()
        print("❌ Bad Request:")
        print(f"   Message: {result.get('message')}")
        if 'errors' in result:
            print(f"   Errors: {json.dumps(result['errors'], indent=2)}")
    
    elif response.status_code == 401:
        print("❌ Unauthorized - Please check your authentication token")
    
    elif response.status_code == 403:
        print("❌ Forbidden - Partner not found or not verified")
    
    else:
        print(f"❌ Unexpected error: {response.status_code}")
        print(response.text)
    
    return None

def test_create_tour_with_edited_data(scraped_data):
    """Test creating tour with edited scraped data - Step 2."""
    
    if not TOKEN:
        print("❌ No authentication token available. Please login first.")
        return
    
    if not scraped_data:
        print("❌ No scraped data available. Please run scraping first.")
        return
    
    headers = {
        "Authorization": f"Token {TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Edit the scraped data (simulate user editing)
    edited_data = scraped_data.copy()
    edited_data['title'] = f"{edited_data.get('title', 'Tour')} (Edited)"
    edited_data['summary'] = "This tour was edited after scraping"
    edited_data['tourStatus'] = 'Draft'
    
    print(f"\n🔧 Testing tour creation with edited data (Step 2)...")
    print(f"Original Title: {scraped_data.get('title')}")
    print(f"Edited Title: {edited_data.get('title')}")
    
    response = requests.post(
        f"{BASE_URL}/partner/user/1/tours/create/",
        headers=headers,
        json=edited_data
    )
    
    print(f"\n📊 Response Status: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print("✅ Tour created successfully with edited data!")
        print(f"📝 Message: {result.get('message')}")
        
        tour_data = result.get('data', {})
        print(f"\n📋 Created Tour Details:")
        print(f"   ID: {tour_data.get('id')}")
        print(f"   Title: {tour_data.get('title')}")
        print(f"   Status: {tour_data.get('tourStatus')}")
        print(f"   Summary: {tour_data.get('summary')}")
        
        # Show request data
        request_data = result.get('request_data', {})
        print(f"\n🔍 Request Data Keys: {list(request_data.keys())}")
        
    else:
        print(f"❌ Tour creation failed: {response.status_code}")
        print(response.text)

def test_manual_tour_creation():
    """Test the manual tour creation workflow."""
    
    if not TOKEN:
        print("❌ No authentication token available. Please login first.")
        return
    
    headers = {
        "Authorization": f"Token {TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Sample tour data
    tour_data = {
        "tourLink": "https://example.com/manual-tour",
        "title": "Manual Test Tour",
        "destinations": ["Mumbai", "Goa"],
        "durationDays": 5,
        "durationNights": 4,
        "tourType": "FIT",
        "providerName": "Test Travel Agency",
        "startingPrice": 15000.00,
        "priceType": "Starting From",
        "departureCities": ["Delhi", "Mumbai"],
        "tourStartLocation": "Delhi",
        "tourDropLocation": "Mumbai",
        "departureMonths": ["January", "February", "March"],
        "tourStatus": "Draft",
        "categories": ["Adventure", "Beach"],
        "tags": ["adventure", "beach", "vacation"],
        "summary": "Test tour created manually",
        "highlights": ["Beach activities", "Water sports"],
        "includesFlights": True,
        "includesHotels": True,
        "includesMeals": True,
        "includesTransfers": True,
        "visaSupport": False,
        "offersType": ["Early Bird"],
        "discountDetails": "10% off for early booking",
        "promotionalTagline": "Book now and save!"
    }
    
    print(f"\n🔧 Testing manual tour creation...")
    
    response = requests.post(
        f"{BASE_URL}/partner/user/1/tours/create/",
        headers=headers,
        json=tour_data
    )
    
    print(f"\n📊 Response Status: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print("✅ Manual tour created successfully!")
        print(f"📝 Message: {result.get('message')}")
        
        tour_data = result.get('data', {})
        print(f"\n📋 Created Tour Details:")
        print(f"   ID: {tour_data.get('id')}")
        print(f"   Title: {tour_data.get('title')}")
        print(f"   Status: {tour_data.get('tourStatus')}")
        
        # Show request data
        request_data = result.get('request_data', {})
        print(f"\n🔍 Request Data Keys: {list(request_data.keys())}")
        
    else:
        print(f"❌ Manual tour creation failed: {response.status_code}")
        print(response.text)

def main():
    """Main test function."""
    print("🧪 Testing Two-Step Tour Creation Workflow")
    print("=" * 50)
    
    # Step 1: Login
    if not login_and_get_token():
        print("❌ Cannot proceed without authentication")
        return
    
    # Step 2: Test scraping (Step 1 of workflow)
    scraped_data = test_scrape_tour_details()
    
    # Step 3: Test creating tour with edited data (Step 2 of workflow)
    if scraped_data:
        test_create_tour_with_edited_data(scraped_data)
    
    # Step 4: Test manual tour creation (alternative)
    test_manual_tour_creation()
    
    print("\n🎉 Testing completed!")

if __name__ == "__main__":
    main() 