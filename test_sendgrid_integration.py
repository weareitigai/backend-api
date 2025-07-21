#!/usr/bin/env python3
"""
Test script to verify SendGrid email OTP functionality
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.authentication.utils import send_email_otp
from django.conf import settings

def test_sendgrid_email():
    """Test SendGrid email OTP functionality"""
    
    print("🧪 Testing SendGrid Email OTP Integration")
    print("=" * 50)
    
    # Configuration check
    print("\n📋 Configuration Check:")
    print(f"   EMAIL_BACKEND_TYPE: {getattr(settings, 'EMAIL_BACKEND_TYPE', 'Not set')}")
    print(f"   SENDGRID_API_KEY: {'✅ Set' if getattr(settings, 'SENDGRID_API_KEY', '') else '❌ Not set'}")
    print(f"   DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not set')}")
    print(f"   FROM_NAME: {getattr(settings, 'FROM_NAME', 'Not set')}")
    
    # Test email sending
    test_email = "test@example.com"  # Change this to your test email
    test_otp = "123456"
    
    print(f"\n📧 Testing email send to: {test_email}")
    print(f"   OTP Code: {test_otp}")
    
    try:
        success = send_email_otp(test_email, test_otp)
        
        if success:
            print("✅ Email OTP function completed successfully!")
            print("\n📝 Next steps:")
            print("   1. Check your email inbox (including spam folder)")
            print("   2. Look for the OTP email from Travel Partner Platform")
            print("   3. Verify the email contains the HTML template")
            
            if getattr(settings, 'EMAIL_BACKEND_TYPE', '') == 'sendgrid':
                print("   4. Check SendGrid dashboard for delivery statistics")
            
        else:
            print("❌ Email OTP function failed!")
            
    except Exception as e:
        print(f"❌ Error during email test: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("🏁 SendGrid Integration Test Completed!")
    
    print("\n💡 Troubleshooting Tips:")
    print("   - Ensure SENDGRID_API_KEY is correctly set in .env")
    print("   - Verify your SendGrid account has sending permissions")
    print("   - Check that DEFAULT_FROM_EMAIL is verified in SendGrid")
    print("   - For testing, you can temporarily change EMAIL_BACKEND to 'console'")

if __name__ == "__main__":
    test_sendgrid_email()
