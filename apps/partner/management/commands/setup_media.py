import os
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Setup media directory and ensure proper permissions'

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        
        # Create media directory if it doesn't exist
        if not os.path.exists(media_root):
            os.makedirs(media_root, exist_ok=True)
            self.stdout.write(
                self.style.SUCCESS(f'Created media directory: {media_root}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Media directory already exists: {media_root}')
            )
        
        # Create subdirectories for different file types
        subdirs = [
            'pan_aadhaar_docs',
            'business_proofs', 
            'documents'
        ]
        
        for subdir in subdirs:
            subdir_path = os.path.join(media_root, subdir)
            if not os.path.exists(subdir_path):
                os.makedirs(subdir_path, exist_ok=True)
                self.stdout.write(
                    self.style.SUCCESS(f'Created subdirectory: {subdir_path}')
                )
        
        # Set proper permissions (readable by web server)
        try:
            os.chmod(media_root, 0o755)
            self.stdout.write(
                self.style.SUCCESS('Set proper permissions on media directory')
            )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Could not set permissions: {e}')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Media directory setup completed successfully!')
        ) 