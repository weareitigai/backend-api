#!/usr/bin/env python
"""
Railway Migration Script
Run this after PostgreSQL service is connected to Railway
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    """Run Django migrations for Railway deployment."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    print("🔄 Running Django migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("✅ Migrations completed successfully!")
    print("🚀 Your Django backend is ready!")

if __name__ == '__main__':
    main() 