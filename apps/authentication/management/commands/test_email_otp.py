from django.core.management.base import BaseCommand
from django.conf import settings
from apps.authentication.utils import send_email_otp
import sys

class Command(BaseCommand):
    help = 'Test email OTP functionality with SendGrid integration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to send test OTP to',
            default='test@example.com'
        )
        parser.add_argument(
            '--otp',
            type=str,
            help='OTP code to send',
            default='123456'
        )
        parser.add_argument(
            '--check-config',
            action='store_true',
            help='Only check configuration without sending email'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('\n🧪 Email OTP Test Command')
        )
        self.stdout.write('=' * 50)

        # Check configuration
        self.stdout.write('\n📋 Configuration Check:')
        
        email_backend = getattr(settings, 'EMAIL_BACKEND_TYPE', 'Not set')
        sendgrid_api_key = getattr(settings, 'SENDGRID_API_KEY', '')
        default_from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not set')
        from_name = getattr(settings, 'FROM_NAME', 'Not set')
        
        self.stdout.write(f'   EMAIL_BACKEND_TYPE: {email_backend}')
        self.stdout.write(f'   SENDGRID_API_KEY: {"✅ Set" if sendgrid_api_key else "❌ Not set"}')
        self.stdout.write(f'   DEFAULT_FROM_EMAIL: {default_from_email}')
        self.stdout.write(f'   FROM_NAME: {from_name}')
        
        # Validate configuration
        config_valid = True
        if email_backend == 'sendgrid':
            if not sendgrid_api_key:
                self.stdout.write(
                    self.style.ERROR('❌ SENDGRID_API_KEY is required when using sendgrid backend')
                )
                config_valid = False
            
            if default_from_email in ['your-email@example.com', 'Not set']:
                self.stdout.write(
                    self.style.WARNING('⚠️  DEFAULT_FROM_EMAIL should be a verified email address')
                )
        
        if options['check_config']:
            if config_valid:
                self.stdout.write(
                    self.style.SUCCESS('\n✅ Configuration looks good!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('\n❌ Configuration issues found. Please check your .env file.')
                )
            return

        # Send test email
        test_email = options['email']
        test_otp = options['otp']
        
        self.stdout.write(f'\n📧 Sending test email to: {test_email}')
        self.stdout.write(f'   OTP Code: {test_otp}')
        
        try:
            success = send_email_otp(test_email, test_otp)
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS('\n✅ Email OTP sent successfully!')
                )
                
                if email_backend == 'sendgrid':
                    self.stdout.write('\n📝 Next steps:')
                    self.stdout.write('   1. Check the target email inbox')
                    self.stdout.write('   2. Look for HTML formatted email')
                    self.stdout.write('   3. Check SendGrid dashboard for delivery stats')
                elif email_backend == 'console':
                    self.stdout.write('\n📝 Check the console output above for the email content')
                    
            else:
                self.stdout.write(
                    self.style.ERROR('\n❌ Failed to send email OTP')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n❌ Error: {e}')
            )
            
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(
            self.style.SUCCESS('🏁 Test completed!')
        )
