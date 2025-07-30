#!/usr/bin/env python3
"""
Simple Tour API Testing Script
Run with: python test_tour_api.py
"""

import requests
import json
import os
import random
import string

# Configuration - will be loaded from file or generated
BASE_URL = "http://localhost:8000"

def load_credentials():
    """Load credentials from file or create new user"""
    if os.path.exists('test_credentials.txt'):
        # Load from file
        credentials = {}
        with open('test_credentials.txt', 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    credentials[key] = value
        
        if all(key in credentials for key in ['EMAIL', 'PASSWORD', 'USER_ID']):
            print("📋 Using existing credentials from test_credentials.txt")
            return {
                'email': credentials['EMAIL'],
                'password': credentials['PASSWORD'],
                'user_id': int(credentials['USER_ID'])
            }
    
    # Create new user if file doesn't exist
    print("🔄 No credentials found. Creating new random user...")
    return create_random_user()

def create_random_user():
    """Create a random user for testing"""
    # Generate random credentials
    random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    email = f"testuser{random_id}@example.com"
    password = f"pass{random_id}123"
    user_id = random.randint(100, 999)  # Random user ID
    
    # Save credentials to file
    with open('test_credentials.txt', 'w') as f:
        f.write(f"EMAIL={email}\n")
        f.write(f"PASSWORD={password}\n")
        f.write(f"USER_ID={user_id}\n")
    
    print(f"✅ Created new test user:")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(f"   User ID: {user_id}")
    
    return {
        'email': email,
        'password': password,
        'user_id': user_id
    }

def create_user_in_django():
    """Create user in Django database"""
    import os
    import django
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    from django.contrib.auth import get_user_model
    from apps.partner.models import Partner
    
    User = get_user_model()
    
    # Read credentials
    credentials = load_credentials()
    
    try:
        # Create user
        user = User.objects.create_user(
            username=credentials['email'],
            email=credentials['email'],
            password=credentials['password'],
            first_name=f"Test{credentials['user_id']}",
            last_name=f"User{credentials['user_id']}"
        )
        
        # Create partner
        partner = Partner.objects.create(user=user, is_verified=True)
        
        print(f"✅ User created in database:")
        print(f"   User ID: {user.id}")
        print(f"   Partner Verified: {partner.is_verified}")
        
        # Update credentials file with actual user ID
        with open('test_credentials.txt', 'w') as f:
            f.write(f"EMAIL={credentials['email']}\n")
            f.write(f"PASSWORD={credentials['password']}\n")
            f.write(f"USER_ID={user.id}\n")
        
        return {
            'email': credentials['email'],
            'password': credentials['password'],
            'user_id': user.id
        }
        
    except Exception as e:
        print(f"❌ Error creating user in database: {str(e)}")
        return None

def login(credentials):
    """Login and get token"""
    url = f"{BASE_URL}/api/auth/login/"
    data = {
        "email": credentials['email'],
        "password": credentials['password']
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        token = response.json()['data']['token']
        print("✅ Login successful!")
        return token
    else:
        print(f"❌ Login failed: {response.text}")
        return None

def create_tour(token, user_id):
    """Create a test tour"""
    url = f"{BASE_URL}/api/partner/user/{user_id}/tours/create/"
    headers = {"Authorization": f"Bearer {token}"}
    
    tour_data = {
        "tourLink": "https://makemytrip.com/bali-package",
        "title": "Bali Honeymoon Escape – 6N/5D",
        "destinations": ["Bali", "Indonesia"],
        "durationDays": 6,
        "durationNights": 5,
        "tourType": "FIT",
        "providerName": "MakeMyTrip",
        "contactLink": "https://wa.me/1234567890",
        "categories": ["Honeymoon", "Beach", "Adventure"],
        "tags": ["romantic", "beach", "honeymoon"],
        "summary": "Experience the perfect romantic getaway in Bali",
        "highlights": ["Private Villa", "Romantic Dinner", "Beach Access"],
        "startingPrice": 48999.00,
        "priceType": "Starting From",
        "departureCities": ["Delhi", "Mumbai"],
        "tourStartLocation": "Delhi Airport",
        "tourDropLocation": "Bali Hotel",
        "departureMonths": ["January", "February", "March"],
        "tourStatus": "Draft",
        "includesFlights": True,
        "includesHotels": True,
        "includesMeals": True,
        "includesTransfers": True,
        "visaSupport": False,
        "offersType": ["Early Bird Offer", "Group Discount"],
        "discountDetails": "Flat 20% off, Buy 2 Get 1 Free",
        "promotionalTagline": "Limited-time July Sale"
    }
    
    response = requests.post(url, json=tour_data, headers=headers)
    if response.status_code == 201:
        tour = response.json()['data']
        print(f"✅ Tour created successfully!")
        print(f"   Tour ID: {tour['id']}")
        print(f"   Title: {tour['title']}")
        print(f"   Price: ₹{tour['startingPrice']}")
        return tour['id']
    else:
        print(f"❌ Tour creation failed: {response.text}")
        return None

def get_all_tours(token, user_id):
    """Get all tours"""
    url = f"{BASE_URL}/api/partner/user/{user_id}/tours/"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        tours = data['data']
        print(f"✅ Found {len(tours)} tours:")
        for tour in tours:
            print(f"   - {tour['title']} (ID: {tour['id']}) - ₹{tour['startingPrice']}")
        return tours
    else:
        print(f"❌ Failed to get tours: {response.text}")
        return []

def get_tour_details(token, user_id, tour_id):
    """Get specific tour details"""
    url = f"{BASE_URL}/api/partner/user/{user_id}/tours/{tour_id}/"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tour = response.json()['data']
        print(f"✅ Tour details:")
        print(f"   Title: {tour['title']}")
        print(f"   Destinations: {', '.join(tour['destinations'])}")
        print(f"   Duration: {tour['durationDays']} days, {tour['durationNights']} nights")
        print(f"   Price: ₹{tour['startingPrice']}")
        print(f"   Status: {tour['tourStatus']}")
        print(f"   Visibility Score: {tour['visibilityScore']}")
        return tour
    else:
        print(f"❌ Failed to get tour details: {response.text}")
        return None

def update_tour(token, user_id, tour_id):
    """Update a tour"""
    url = f"{BASE_URL}/api/partner/user/{user_id}/tours/{tour_id}/update/"
    headers = {"Authorization": f"Bearer {token}"}
    
    update_data = {
        "title": "Updated Bali Honeymoon Package",
        "startingPrice": 52999.00,
        "tourStatus": "Live",
        "promotionalTagline": "New Year Special Offer"
    }
    
    response = requests.patch(url, json=update_data, headers=headers)
    if response.status_code == 200:
        tour = response.json()['data']
        print(f"✅ Tour updated successfully!")
        print(f"   New title: {tour['title']}")
        print(f"   New price: ₹{tour['startingPrice']}")
        print(f"   New status: {tour['tourStatus']}")
        return tour
    else:
        print(f"❌ Tour update failed: {response.text}")
        return None

def test_filtering(token, user_id):
    """Test filtering tours"""
    url = f"{BASE_URL}/api/partner/user/{user_id}/tours/"
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test status filter
    response = requests.get(f"{url}?status=Live", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Live tours: {len(data['data'])} found")
    
    # Test tour type filter
    response = requests.get(f"{url}?tour_type=FIT", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ FIT tours: {len(data['data'])} found")

def main():
    """Main testing function"""
    print("🚀 Starting Tour API Testing...")
    print("=" * 50)
    
    # Step 1: Create user in database
    credentials = create_user_in_django()
    if not credentials:
        print("❌ Failed to create user. Exiting...")
        return
    
    print("\n" + "=" * 50)
    
    # Step 2: Login
    token = login(credentials)
    if not token:
        print("❌ Failed to login. Exiting...")
        return
    
    print("\n" + "=" * 50)
    
    # Step 3: Create tour
    tour_id = create_tour(token, credentials['user_id'])
    if not tour_id:
        print("❌ Failed to create tour. Exiting...")
        return
    
    print("\n" + "=" * 50)
    
    # Step 4: Get all tours
    get_all_tours(token, credentials['user_id'])
    
    print("\n" + "=" * 50)
    
    # Step 5: Get tour details
    get_tour_details(token, credentials['user_id'], tour_id)
    
    print("\n" + "=" * 50)
    
    # Step 6: Update tour
    update_tour(token, credentials['user_id'], tour_id)
    
    print("\n" + "=" * 50)
    
    # Step 7: Test filtering
    test_filtering(token, credentials['user_id'])
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")
    print(f"📝 Credentials saved in: test_credentials.txt")

if __name__ == "__main__":
    main() 