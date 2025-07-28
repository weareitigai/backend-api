#!/usr/bin/env python3
"""
Script to create a test user for performance testing.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/home/yash/office/apiproject')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.authentication.models import User
from apps.partner.models import Partner

def create_test_user():
    """Create a test user for performance testing."""
    
    email = "test@example.com"
    password = "testpass123"
    
    # Check if user already exists
    if User.objects.filter(email=email).exists():
        print(f"User {email} already exists.")
        return
    
    # Create user
    user = User.objects.create_user(
        email=email,
        password=password,
        first_name="Test",
        last_name="User"
    )
    
    # Create partner
    partner = Partner.objects.create(user=user)
    
    print(f"Created test user:")
    print(f"  Email: {email}")
    print(f"  Password: {password}")
    print(f"  Partner ID: {partner.id}")
    
    return user

if __name__ == "__main__":
    create_test_user() 