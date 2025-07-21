from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Toggle mobile OTP functionality on/off'

    def add_arguments(self, parser):
        parser.add_argument(
            '--enable',
            action='store_true',
            help='Enable mobile OTP',
        )
        parser.add_argument(
            '--disable',
            action='store_true',
            help='Disable mobile OTP',
        )
        parser.add_argument(
            '--status',
            action='store_true',
            help='Show current status of mobile OTP',
        )

    def handle(self, *args, **options):
        if options['status']:
            status = getattr(settings, 'MOBILE_OTP_ENABLED', False)
            self.stdout.write(
                self.style.SUCCESS(f'Mobile OTP is currently: {"ENABLED" if status else "DISABLED"}')
            )
        elif options['enable']:
            self.stdout.write(
                self.style.WARNING('To enable mobile OTP, set MOBILE_OTP_ENABLED=True in your environment variables.')
            )
            self.stdout.write('Then restart your Django server.')
        elif options['disable']:
            self.stdout.write(
                self.style.WARNING('To disable mobile OTP, set MOBILE_OTP_ENABLED=False in your environment variables.')
            )
            self.stdout.write('Then restart your Django server.')
        else:
            self.stdout.write(
                self.style.ERROR('Please specify --enable, --disable, or --status')
            )
