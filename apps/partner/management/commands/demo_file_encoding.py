from django.core.management.base import BaseCommand
from apps.partner.utils import generate_sample_encoded_paths, decode_file_info, encode_file_path


class Command(BaseCommand):
    help = 'Demonstrate file path encoding functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-id',
            type=int,
            default=12345,
            help='User ID for demonstration'
        )
        parser.add_argument(
            '--filename',
            type=str,
            default='sample_document.pdf',
            help='Sample filename to encode'
        )

    def handle(self, *args, **options):
        user_id = options['user_id']
        filename = options['filename']
        
        self.stdout.write(
            self.style.SUCCESS('=== File Path Encoding Demonstration ===\n')
        )
        
        # Generate sample encoded paths
        self.stdout.write('1. Sample Encoded File Paths:')
        sample_paths = generate_sample_encoded_paths()
        
        for file_type, path in sample_paths.items():
            self.stdout.write(f'   {file_type}: {path}')
            
            # Decode and show information
            decoded_info = decode_file_info(path)
            if decoded_info:
                self.stdout.write(f'      Decoded: User ID={decoded_info["user_id"]}, '
                                f'Timestamp={decoded_info["timestamp"]}, '
                                f'Unique ID={decoded_info["unique_id"]}')
            self.stdout.write('')
        
        # Encode a custom file
        self.stdout.write('2. Custom File Encoding:')
        custom_path = encode_file_path(filename, user_id, 'custom_docs')
        self.stdout.write(f'   Original: {filename}')
        self.stdout.write(f'   Encoded:  {custom_path}')
        
        # Decode the custom file
        decoded_custom = decode_file_info(custom_path)
        if decoded_custom:
            self.stdout.write(f'   Decoded:  User ID={decoded_custom["user_id"]}, '
                            f'Timestamp={decoded_custom["timestamp"]}, '
                            f'Unique ID={decoded_custom["unique_id"]}')
        
        self.stdout.write('')
        
        # Show the encoding structure
        self.stdout.write('3. Encoding Structure:')
        self.stdout.write('   Directory: {file_type}/{year}/{month}/{user_id}/')
        self.stdout.write('   Filename:  base64_encoded_{user_id}_{timestamp}_{unique_id}_{hash}')
        self.stdout.write('')
        
        # Show security features
        self.stdout.write('4. Security Features:')
        self.stdout.write('   ✓ Base64 URL-safe encoding')
        self.stdout.write('   ✓ SHA256 hash for integrity')
        self.stdout.write('   ✓ UUID for uniqueness')
        self.stdout.write('   ✓ Timestamp for organization')
        self.stdout.write('   ✓ User ID isolation')
        self.stdout.write('   ✓ Organized directory structure')
        
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS('=== End of Demonstration ===')
        ) 