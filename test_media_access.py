#!/usr/bin/env python3
"""
Test script to check media file accessibility and configuration.
"""

import os
import sys
import django
from django.conf import settings
from django.db import models

# Add the project directory to Python path
sys.path.append('/home/yash/office/apiproject')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.partner.models import LegalBanking

def test_media_configuration():
    """Test media file configuration and accessibility."""
    
    print("=== Media File Configuration Test ===\n")
    
    # Check settings
    print("1. Django Settings:")
    print(f"   MEDIA_URL: {settings.MEDIA_URL}")
    print(f"   MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"   DEBUG: {settings.DEBUG}")
    print(f"   Media root exists: {os.path.exists(settings.MEDIA_ROOT)}")
    
    # Check if media directory exists and has files
    if os.path.exists(settings.MEDIA_ROOT):
        print(f"\n2. Media Directory Contents:")
        for root, dirs, files in os.walk(settings.MEDIA_ROOT):
            level = root.replace(str(settings.MEDIA_ROOT), '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files[:5]:  # Show first 5 files
                print(f"{subindent}{file}")
            if len(files) > 5:
                print(f"{subindent}... and {len(files) - 5} more files")
    
    # Check LegalBanking records with files
    print(f"\n3. LegalBanking Records with Files:")
    legal_banking_records = LegalBanking.objects.filter(
        models.Q(pan_or_aadhaar_file__isnull=False) | 
        models.Q(business_proof_file__isnull=False)
    )
    
    print(f"   Total records with files: {legal_banking_records.count()}")
    
    for record in legal_banking_records[:3]:  # Check first 3 records
        print(f"\n   Record ID: {record.id}")
        print(f"   Partner: {record.partner.user.email}")
        
        if record.pan_or_aadhaar_file:
            print(f"   PAN/Aadhaar file: {record.pan_or_aadhaar_file.name}")
            print(f"   File exists: {os.path.exists(record.pan_or_aadhaar_file.path)}")
            print(f"   File size: {record.pan_or_aadhaar_file.size} bytes")
            print(f"   File URL: {record.pan_or_aadhaar_file.url}")
            
            # Test if file is accessible
            try:
                with open(record.pan_or_aadhaar_file.path, 'rb') as f:
                    content = f.read(100)  # Read first 100 bytes
                    print(f"   File readable: ✅ ({len(content)} bytes read)")
            except Exception as e:
                print(f"   File readable: ❌ ({str(e)})")
        
        if record.business_proof_file:
            print(f"   Business proof file: {record.business_proof_file.name}")
            print(f"   File exists: {os.path.exists(record.business_proof_file.path)}")
            print(f"   File size: {record.business_proof_file.size} bytes")
            print(f"   File URL: {record.business_proof_file.url}")
            
            # Test if file is accessible
            try:
                with open(record.business_proof_file.path, 'rb') as f:
                    content = f.read(100)  # Read first 100 bytes
                    print(f"   File readable: ✅ ({len(content)} bytes read)")
            except Exception as e:
                print(f"   File readable: ❌ ({str(e)})")
    
    # Test URL generation
    print(f"\n4. URL Generation Test:")
    if legal_banking_records.exists():
        test_record = legal_banking_records.first()
        
        if test_record.pan_or_aadhaar_file:
            url = test_record.pan_or_aadhaar_file.url
            print(f"   Sample URL: {url}")
            print(f"   URL starts with /media/: {url.startswith('/media/')}")
        
        if test_record.business_proof_file:
            url = test_record.business_proof_file.url
            print(f"   Sample URL: {url}")
            print(f"   URL starts with /media/: {url.startswith('/media/')}")
    
    print(f"\n5. Recommendations:")
    if not settings.DEBUG:
        print("   ⚠️  DEBUG is False - media files may not be served in production")
        print("   💡 Consider using a CDN or static file server for production")
    else:
        print("   ✅ DEBUG is True - media files should be served in development")
    
    print("   💡 Check that your web server is configured to serve /media/ URLs")
    print("   💡 Ensure file permissions allow web server to read media files")

if __name__ == "__main__":
    test_media_configuration() 