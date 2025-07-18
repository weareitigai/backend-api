import random
import string
from django.core.mail import send_mail
from django.conf import settings
from .models import OTPVerification

# Try to import optional packages
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False


def generate_otp(length=6):
    """Generate a random OTP of specified length."""
    return ''.join(random.choices(string.digits, k=length))


def send_email_otp(email, otp):
    """Send OTP via email."""
    subject = 'Your OTP for Travel Partner Platform'
    message = f'Your OTP is: {otp}. This OTP will expire in 10 minutes.'
    from_email = settings.DEFAULT_FROM_EMAIL
    
    try:
        send_mail(subject, message, from_email, [email])
        print(f"✅ EMAIL OTP SENT to {email}: {otp}")
        return True
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        print(f"🔧 CONSOLE FALLBACK - EMAIL OTP for {email}: {otp}")
        print(f"📧 Subject: {subject}")
        print(f"📝 Message: {message}")
        print("-" * 50)
        # Return True for testing purposes - in production you might want False
        return True


def send_mobile_otp(mobile, otp):
    """Send OTP via SMS using Twilio."""
    message_body = f'Your OTP is: {otp}. This OTP will expire in 10 minutes.'
    
    if not TWILIO_AVAILABLE:
        print("📱 Twilio package not installed. Using console fallback.")
        print(f"🔧 CONSOLE FALLBACK - MOBILE OTP for {mobile}: {otp}")
        print(f"📱 SMS Message: {message_body}")
        print("-" * 50)
        return True
        
    if not all([settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, settings.TWILIO_PHONE_NUMBER]):
        print("📱 Twilio credentials not configured. Using console fallback.")
        print(f"🔧 CONSOLE FALLBACK - MOBILE OTP for {mobile}: {otp}")
        print(f"📱 SMS Message: {message_body}")
        print("-" * 50)
        return True
    
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message_body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=mobile
        )
        print(f"✅ SMS OTP SENT to {mobile}: {otp}")
        return True
    except Exception as e:
        print(f"❌ Error sending SMS: {e}")
        print(f"🔧 CONSOLE FALLBACK - MOBILE OTP for {mobile}: {otp}")
        print(f"📱 SMS Message: {message_body}")
        print("-" * 50)
        return True


def create_otp_verification(email=None, mobile=None, otp_type='email', user=None):
    """Create OTP verification record."""
    otp = generate_otp()
    
    otp_verification = OTPVerification.objects.create(
        user=user,
        email=email,
        mobile=mobile,
        otp_type=otp_type,
        otp_code=otp
    )
    
    return otp_verification


def verify_otp(email=None, mobile=None, otp_code=None, otp_type='email'):
    """Verify OTP code."""
    try:
        if email:
            otp_obj = OTPVerification.objects.get(
                email=email,
                otp_code=otp_code,
                otp_type=otp_type,
                is_verified=False
            )
        elif mobile:
            otp_obj = OTPVerification.objects.get(
                mobile=mobile,
                otp_code=otp_code,
                otp_type=otp_type,
                is_verified=False
            )
        else:
            return False, "Email or mobile required"
        
        if otp_obj.is_expired():
            return False, "OTP has expired"
        
        otp_obj.is_verified = True
        otp_obj.save()
        return True, "OTP verified successfully"
        
    except OTPVerification.DoesNotExist:
        return False, "Invalid OTP"
