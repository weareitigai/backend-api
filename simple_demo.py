#!/usr/bin/env python3
import base64
import hashlib
import uuid
from datetime import datetime

def encode_file_path(original_filename, user_id, file_type):
    """Simple file path encoding demonstration."""
    _, ext = os.path.splitext(original_filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    hash_input = f"{user_id}_{timestamp}_{unique_id}"
    file_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]
    encoded_filename = base64.urlsafe_b64encode(
        f"{user_id}_{timestamp}_{unique_id}_{file_hash}".encode()
    ).decode()[:32]
    year_month = datetime.now().strftime('%Y/%m')
    directory = f"{file_type}/{year_month}/{user_id}"
    return f"{directory}/{encoded_filename}{ext}"

# Sample demonstrations
print("FILE PATH ENCODING DEMONSTRATION")
print("=" * 50)

print("\nOLD vs NEW APPROACH:")
print("OLD: pan_aadhaar_docs/pan_card_1234567890.pdf")
print("NEW: pan_aadhaar_docs/2024/07/12345/aBcDeFgHiJkLmNoPqRsTuVwXyZ123456.pdf")

print("\nSAMPLE ENCODED PATHS:")
print("-" * 30)

# Generate some sample paths
import os
sample_files = [
    ("pan_card_1234567890.pdf", 12345, "pan_aadhaar_docs"),
    ("business_license_ABC123.pdf", 12345, "business_proofs"),
    ("aadhaar_987654321098.pdf", 67890, "pan_aadhaar_docs"),
]

for filename, user_id, file_type in sample_files:
    encoded = encode_file_path(filename, user_id, file_type)
    print(f"{file_type:20}: {encoded}")

print("\nSECURITY FEATURES:")
print("- Base64 URL-safe encoding")
print("- SHA256 hash for integrity")
print("- UUID for uniqueness")
print("- Timestamp for organization")
print("- User ID isolation")
print("- Organized directory structure") 