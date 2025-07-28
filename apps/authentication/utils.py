import random
import string
import dns.resolver
import re
from django.core.mail import send_mail
from django.conf import settings
from .models import OTPVerification

# Try to import optional packages
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False

try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
    SENDGRID_AVAILABLE = True
except ImportError:
    SENDGRID_AVAILABLE = False


def generate_otp(length=6):
    """Generate a random OTP of specified length."""
    return ''.join(random.choices(string.digits, k=length))


def validate_email_format(email):
    """
    Validate email format using regex.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if email format is valid, False otherwise
    """
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_email_domain(email):
    """
    Validate that the email domain has valid MX records.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if domain has valid MX records, False otherwise
    """
    try:
        # Extract domain from email
        domain = email.split('@')[1]
        
        # Check for MX records
        mx_records = dns.resolver.resolve(domain, 'MX')
        return len(mx_records) > 0
    except (IndexError, dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout):
        return False
    except Exception:
        return False


def validate_email_exists(email):
    """
    Comprehensive email validation including format and domain check.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Check email format
    if not validate_email_format(email):
        return False, "Invalid email format"
    
    # Check email length
    if len(email) > 100:
        return False, "Email address cannot exceed 100 characters"
    
    # Check domain validity
    if not validate_email_domain(email):
        return False, "Invalid email domain or domain does not exist"
    
    return True, "Email is valid"


def send_email_otp(email, otp):
    """Send OTP via email using SendGrid or fallback to SMTP/console."""
    subject = 'Your OTP for Travel Partner Platform'
    
    # Create HTML email template
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Your OTP Code</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background-color: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
            .otp-code {{ font-size: 32px; font-weight: bold; color: #007bff; text-align: center; margin: 20px 0; letter-spacing: 5px; }}
            .note {{ background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            .footer {{ text-align: center; color: #666; margin-top: 20px; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Travel Partner Platform</h1>
                <p>Email Verification</p>
            </div>
            <div class="content">
                <h2>Hello!</h2>
                <p>You requested an OTP code for email verification. Please use the code below to complete your verification:</p>
                
                <div class="otp-code">{otp}</div>
                
                <div class="note">
                    <strong>Important:</strong> This OTP will expire in 10 minutes for security reasons.
                </div>
                
                <p>If you didn't request this OTP, please ignore this email.</p>
                
                <p>Thank you for using Travel Partner Platform!</p>
            </div>
            <div class="footer">
                <p>© 2025 Travel Partner Platform. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Plain text version
    plain_text = f"""
    Travel Partner Platform - Email Verification
    
    Hello!
    
    You requested an OTP code for email verification. Please use the code below:
    
    OTP: {otp}
    
    This OTP will expire in 10 minutes.
    
    If you didn't request this OTP, please ignore this email.
    
    Thank you for using Travel Partner Platform!
    """
    
    # Try SendGrid first if available and configured
    if (SENDGRID_AVAILABLE and 
        hasattr(settings, 'SENDGRID_API_KEY') and 
        settings.SENDGRID_API_KEY and
        hasattr(settings, 'EMAIL_BACKEND_TYPE') and
        settings.EMAIL_BACKEND_TYPE == 'sendgrid'):
        
        try:
            message = Mail(
                from_email=(settings.DEFAULT_FROM_EMAIL, getattr(settings, 'FROM_NAME', 'Travel Partner Platform')),
                to_emails=email,
                subject=subject,
                html_content=html_content,
                plain_text_content=plain_text
            )
            
            sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
            response = sg.send(message)
            
            print(f"✅ SENDGRID EMAIL OTP SENT to {email}: {otp}")
            print(f"📧 Response Status: {response.status_code}")
            return True
            
        except Exception as e:
            print(f"❌ SendGrid Error: {e}")
            print("🔄 Falling back to Django email backend...")
    
    # Fallback to Django's email backend (SMTP or console)
    try:
        from django.core.mail import EmailMultiAlternatives
        
        msg = EmailMultiAlternatives(
            subject=subject,
            body=plain_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        print(f"✅ DJANGO EMAIL OTP SENT to {email}: {otp}")
        return True
        
    except Exception as e:
        print(f"❌ Django Email Error: {e}")
        print(f"🔧 CONSOLE FALLBACK - EMAIL OTP for {email}: {otp}")
        print(f"📧 Subject: {subject}")
        print(f"📝 Message: {plain_text}")
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
