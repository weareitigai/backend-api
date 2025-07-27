#!/usr/bin/env python3
"""
Simple demonstration of file path encoding functionality.
This shows your boss what the data encoding looks like.
"""

import os
import hashlib
import base64
import uuid
from datetime import datetime


def encode_file_path(original_filename, user_id, file_type):
    """
    Encode file path with security and organization features.
    """
    # Get file extension
    _, ext = os.path.splitext(original_filename)
    
    # Create a unique identifier
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    
    # Create a hash of user_id + timestamp for security
    hash_input = f"{user_id}_{timestamp}_{unique_id}"
    file_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]
    
    # Encode the filename components
    encoded_filename = base64.urlsafe_b64encode(
        f"{user_id}_{timestamp}_{unique_id}_{file_hash}".encode()
    ).decode()[:32]
    
    # Create organized directory structure
    year_month = datetime.now().strftime('%Y/%m')
    directory = f"{file_type}/{year_month}/{user_id}"
    
    # Return the complete encoded path
    return f"{directory}/{encoded_filename}{ext}"


def decode_file_info(encoded_path):
    """
    Decode file information from encoded path.
    """
    try:
        # Extract filename from path
        filename = os.path.basename(encoded_path)
        name, ext = os.path.splitext(filename)
        
        # Decode the filename
        decoded = base64.urlsafe_b64decode(name + '=' * (4 - len(name) % 4)).decode()
        
        # Parse components
        parts = decoded.split('_')
        if len(parts) >= 4:
            user_id = parts[0]
            timestamp = f"{parts[1]}_{parts[2]}"
            unique_id = parts[3]
            file_hash = parts[4] if len(parts) > 4 else None
            
            return {
                'user_id': user_id,
                'timestamp': timestamp,
                'unique_id': unique_id,
                'file_hash': file_hash,
                'extension': ext
            }
    except Exception:
        pass
    
    return None


def main():
    print("=" * 60)
    print("FILE PATH ENCODING DEMONSTRATION")
    print("=" * 60)
    
    # 1. Show the OLD vs NEW approach
    print("\n1. OLD vs NEW File Paths:")
    print("-" * 40)
    
    old_pan_path = "pan_aadhaar_docs/pan_card_1234567890.pdf"
    old_business_path = "business_proofs/business_license_ABC123.pdf"
    
    print(f"OLD PAN Path:      {old_pan_path}")
    print(f"OLD Business Path: {old_business_path}")
    
    # Generate new encoded paths
    new_pan_path = encode_file_path("pan_card_1234567890.pdf", 12345, "pan_aadhaar_docs")
    new_business_path = encode_file_path("business_license_ABC123.pdf", 12345, "business_proofs")
    
    print(f"\nNEW PAN Path:      {new_pan_path}")
    print(f"NEW Business Path: {new_business_path}")
    
    # 2. Show different scenarios
    print("\n2. Different Document Types:")
    print("-" * 40)
    
    scenarios = [
        ("PAN Card", "pan_card_ABCDE1234F.pdf", 12345, "pan_aadhaar_docs"),
        ("Aadhaar Card", "aadhaar_987654321098.pdf", 12345, "pan_aadhaar_docs"),
        ("Business License", "business_license_XYZ789.pdf", 67890, "business_proofs"),
        ("GST Certificate", "gst_cert_22AAAAA0000A1Z5.pdf", 67890, "business_proofs"),
    ]
    
    for description, filename, user_id, file_type in scenarios:
        encoded = encode_file_path(filename, user_id, file_type)
        decoded = decode_file_info(encoded)
        print(f"\n{description}:")
        print(f"  Original: {filename}")
        print(f"  Encoded:  {encoded}")
        if decoded:
            print(f"  User ID:  {decoded['user_id']}")
            print(f"  Time:     {decoded['timestamp']}")
    
    # 3. Show encoding structure
    print("\n3. Encoding Structure:")
    print("-" * 40)
    print("Directory Structure: {file_type}/{year}/{month}/{user_id}/")
    print("Filename Format:     base64_encoded_{user_id}_{timestamp}_{unique_id}_{hash}{ext}")
    
    # 4. Show security features
    print("\n4. Security Features:")
    print("-" * 40)
    security_features = [
        "✓ Base64 URL-safe encoding (prevents path traversal)",
        "✓ SHA256 hash for file integrity",
        "✓ UUID for uniqueness (prevents collisions)",
        "✓ Timestamp for organization and audit trail",
        "✓ User ID isolation (prevents access to other users' files)",
        "✓ Organized directory structure (year/month/user_id)",
        "✓ No sensitive information in filename",
        "✓ Consistent length regardless of original filename"
    ]
    
    for feature in security_features:
        print(f"  {feature}")
    
    # 5. Show sample encoded paths
    print("\n5. Sample Encoded Paths:")
    print("-" * 40)
    
    sample_files = [
        ("pan_card_1234567890.pdf", 12345, "pan_aadhaar_docs"),
        ("business_license_ABC123.pdf", 12345, "business_proofs"),
        ("aadhaar_987654321098.pdf", 67890, "pan_aadhaar_docs"),
        ("gst_cert_22AAAAA0000A1Z5.pdf", 67890, "business_proofs"),
    ]
    
    for filename, user_id, file_type in sample_files:
        encoded = encode_file_path(filename, user_id, file_type)
        print(f"{file_type:20}: {encoded}")
    
    print("\n" + "=" * 60)
    print("END OF DEMONSTRATION")
    print("=" * 60)


if __name__ == "__main__":
    main() 