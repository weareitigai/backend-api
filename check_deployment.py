#!/usr/bin/env python
"""
Railway Deployment Check Script
Run this to verify your Django app is properly deployed
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    """Check Django deployment status."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    print("🔍 Checking Django deployment status...")
    
    try:
        django.setup()
        from django.conf import settings
        
        print("✅ Django settings loaded successfully")
        print(f"📍 DEBUG mode: {settings.DEBUG}")
        print(f"🔑 SECRET_KEY configured: {'Yes' if settings.SECRET_KEY else 'No'}")
        print(f"🌐 ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        
        # Check database connection
        try:
            from django.db import connection
            cursor = connection.cursor()
            print("✅ Database connection successful")
        except Exception as e:
            print(f"⚠️  Database connection failed: {e}")
            print("💡 Add PostgreSQL service in Railway and run migrations")
        
        print("🚀 Django app is ready!")
        print("📡 Health check available at: /health/")
        print("📚 API docs available at: /api/docs/")
        
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 