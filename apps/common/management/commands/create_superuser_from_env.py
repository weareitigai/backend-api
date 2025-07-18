from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from decouple import config
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a Django admin superuser from environment variables'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update existing superuser with new values from environment'
        )

    def handle(self, *args, **options):
        # Get superuser credentials from environment variables
        username = config('DJANGO_SUPERUSER_USERNAME', default=None)
        email = config('DJANGO_SUPERUSER_EMAIL', default=None)
        password = config('DJANGO_SUPERUSER_PASSWORD', default=None)
        create_superuser = config('CREATE_SUPERUSER', default='false', cast=bool)

        # Check if superuser creation is enabled
        if not create_superuser:
            self.stdout.write(
                self.style.WARNING('Superuser creation disabled. Set CREATE_SUPERUSER=true in .env to enable.')
            )
            return

        # Validate required environment variables
        if not all([username, email, password]):
            missing_vars = []
            if not username:
                missing_vars.append('DJANGO_SUPERUSER_USERNAME')
            if not email:
                missing_vars.append('DJANGO_SUPERUSER_EMAIL')
            if not password:
                missing_vars.append('DJANGO_SUPERUSER_PASSWORD')
            
            self.stdout.write(
                self.style.ERROR(
                    f'Missing required environment variables: {", ".join(missing_vars)}'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    'Please set these variables in your .env file:'
                )
            )
            for var in missing_vars:
                self.stdout.write(f'  {var}=your_value_here')
            return

        # Check if superuser already exists
        try:
            user = User.objects.get(username=username)
            if user.is_superuser:
                if options['force']:
                    # Update existing superuser
                    user.email = email
                    user.set_password(password)
                    user.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Updated existing superuser: {username}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Superuser "{username}" already exists. Use --force to update.'
                        )
                    )
                return
            else:
                # User exists but is not a superuser - promote them
                user.is_staff = True
                user.is_superuser = True
                user.email = email
                user.set_password(password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Promoted existing user to superuser: {username}'
                    )
                )
                return
                
        except User.DoesNotExist:
            # Create new superuser
            try:
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created superuser: {username}'
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Admin panel: http://localhost:8000/admin/'
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Credentials: {username} / {password}'
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Failed to create superuser: {str(e)}'
                    )
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Error checking for existing user: {str(e)}'
                )
            ) 