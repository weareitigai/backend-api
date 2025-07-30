#!/usr/bin/env python3
"""
Create Random User for Testing
Run with: python create_random_user.py
"""

import random
import string
from django.contrib.auth import get_user_model
from apps.partner.models import Partner

def generate_random_string(length=8):
    """Generate random string"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def create_random_user():
    """Create a random user for testing"""
    User = get_user_model()
    
    # Generate random credentials
    random_id = generate_random_string(6)
    email = f"testuser{random_id}@example.com"
    password = f"pass{random_id}123"
    first_name = f"Test{random_id.capitalize()}"
    last_name = f"User{random_id.capitalize()}"
    
    try:
        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create partner
        partner = Partner.objects.create(user=user, is_verified=True)
        
        print("✅ Random user created successfully!")
        print("=" * 50)
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"User ID: {user.id}")
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        print(f"Partner Verified: {partner.is_verified}")
        print("=" * 50)
        
        # Save credentials to file for easy access
        with open('test_credentials.txt', 'w') as f:
            f.write(f"EMAIL={email}\n")
            f.write(f"PASSWORD={password}\n")
            f.write(f"USER_ID={user.id}\n")
            f.write(f"FIRST_NAME={first_name}\n")
            f.write(f"LAST_NAME={last_name}\n")
        
        print("📝 Credentials saved to 'test_credentials.txt'")
        print("=" * 50)
        
        return {
            'email': email,
            'password': password,
            'user_id': user.id,
            'first_name': first_name,
            'last_name': last_name
        }
        
    except Exception as e:
        print(f"❌ Error creating user: {str(e)}")
        return None

if __name__ == "__main__":
    import os
    import django
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    # Create random user
    user_data = create_random_user()
    
    if user_data:
        print("\n🎯 Now you can use these credentials in your test script!")
        print("Update test_tour_api.py with these values:")
        print(f"EMAIL = '{user_data['email']}'")
        print(f"PASSWORD = '{user_data['password']}'")
        print(f"USER_ID = {user_data['user_id']}") 