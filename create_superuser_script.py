#!/usr/bin/env python3
"""
Create Superuser Script
Run with: python create_superuser_script.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_superuser():
    """Create a superuser with proper fields"""
    User = get_user_model()
    
    try:
        # Create superuser
        superuser = User.objects.create_superuser(
            username='admin@example.com',  # Use email as username
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        
        print("✅ Superuser created successfully!")
        print("=" * 50)
        print(f"Username: admin@example.com")
        print(f"Email: admin@example.com")
        print(f"Password: admin123")
        print(f"User ID: {superuser.id}")
        print("=" * 50)
        print("🎯 You can now login to Django Admin with these credentials!")
        
        return superuser
        
    except Exception as e:
        print(f"❌ Error creating superuser: {str(e)}")
        return None

if __name__ == "__main__":
    create_superuser() 