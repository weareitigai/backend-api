#!/usr/bin/env python3
"""
Script to check Django admin image display functionality.
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

from apps.partner.models import LegalBanking, Partner
from apps.authentication.models import User

def check_admin_image_display():
    """Check if images are properly configured for admin display."""
    
    print("Checking Django admin image display configuration...")
    
    # Check if media files are properly configured
    print(f"\n1. Media configuration:")
    print(f"   MEDIA_URL: {settings.MEDIA_URL}")
    print(f"   MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"   Media root exists: {os.path.exists(settings.MEDIA_ROOT)}")
    
    # Check if there are any LegalBanking records with files
    print(f"\n2. LegalBanking records with files:")
    legal_banking_records = LegalBanking.objects.filter(
        models.Q(pan_or_aadhaar_file__isnull=False) | 
        models.Q(business_proof_file__isnull=False)
    )
    
    print(f"   Total records with files: {legal_banking_records.count()}")
    
    for record in legal_banking_records:
        print(f"\n   Record ID: {record.id}")
        print(f"   Partner: {record.partner.user.email}")
        
        if record.pan_or_aadhaar_file:
            print(f"   PAN/Aadhaar file: {record.pan_or_aadhaar_file.name}")
            print(f"   File exists: {os.path.exists(record.pan_or_aadhaar_file.path)}")
            print(f"   File size: {record.pan_or_aadhaar_file.size} bytes")
            print(f"   File URL: {record.pan_or_aadhaar_file.url}")
        
        if record.business_proof_file:
            print(f"   Business proof file: {record.business_proof_file.name}")
            print(f"   File exists: {os.path.exists(record.business_proof_file.path)}")
            print(f"   File size: {record.business_proof_file.size} bytes")
            print(f"   File URL: {record.business_proof_file.url}")
    
    # Check admin configuration
    print(f"\n3. Admin configuration:")
    from apps.partner.admin import LegalBankingAdmin
    
    admin_instance = LegalBankingAdmin(LegalBanking, None)
    print(f"   List display includes file preview: {'get_file_preview' in admin_instance.list_display}")
    print(f"   Readonly fields includes file preview: {'get_file_preview' in admin_instance.readonly_fields}")
    
    # Test file preview method
    if legal_banking_records.exists():
        test_record = legal_banking_records.first()
        try:
            preview = admin_instance.get_file_preview(test_record)
            print(f"   File preview method works: {preview is not None}")
        except Exception as e:
            print(f"   File preview method error: {str(e)}")
    
    print(f"\n4. Recommendations:")
    print(f"   - Ensure media files are served in development")
    print(f"   - Check that file permissions are correct")
    print(f"   - Verify that the admin template includes proper styling")
    print(f"   - Test the admin interface manually at /admin/")

if __name__ == "__main__":
    check_admin_image_display() 