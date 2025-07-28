import os
import hashlib
import base64
import uuid
import time
import logging
from datetime import datetime
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Set up logging
logger = logging.getLogger(__name__)


def log_performance_metric(operation, duration, file_size=None):
    """Log performance metrics for monitoring."""
    logger.info(f"Performance: {operation} took {duration:.2f}s" + 
                (f" for {file_size} bytes" if file_size else ""))


def optimize_file_upload(file_obj, user_id, file_type):
    """
    Optimized file upload with performance monitoring.
    
    Args:
        file_obj: Uploaded file object
        user_id (int): User ID for organization
        file_type (str): Type of file
    
    Returns:
        str: Optimized file path
    """
    start_time = time.time()
    
    try:
        # Generate secure path
        encoded_path = get_secure_upload_path(None, file_obj.name)
        
        # Use Django's default storage for efficient file handling
        file_path = default_storage.save(encoded_path, ContentFile(file_obj.read()))
        
        # Log performance
        duration = time.time() - start_time
        log_performance_metric(f"File upload ({file_type})", duration, file_obj.size)
        
        return file_path
        
    except Exception as e:
        logger.error(f"File upload error: {str(e)}")
        raise


def get_secure_upload_path(instance, filename):
    """
    Django upload_to function for secure file paths.
    
    Args:
        instance: Model instance
        filename: Original filename
    
    Returns:
        str: Secure file path
    """
    # Determine file type based on model field
    if hasattr(instance, 'pan_or_aadhaar_file') and instance.pan_or_aadhaar_file:
        file_type = 'pan_aadhaar_docs'
    elif hasattr(instance, 'business_proof_file') and instance.business_proof_file:
        file_type = 'business_proofs'
    else:
        file_type = 'documents'
    
    # Get user ID from partner
    user_id = instance.partner.user.id if instance.partner and instance.partner.user else 0
    
    return encode_file_path(filename, user_id, file_type)


def encode_file_path(original_filename, user_id, file_type):
    """
    Encode file path with security and organization features.
    
    Args:
        original_filename (str): Original filename
        user_id (int): User ID for organization
        file_type (str): Type of file (e.g., 'pan_aadhaar', 'business_proof')
    
    Returns:
        str: Encoded file path
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
    Decode file information from encoded path (for admin/debugging purposes).
    
    Args:
        encoded_path (str): Encoded file path
    
    Returns:
        dict: Decoded file information
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


def generate_sample_encoded_paths():
    """
    Generate sample encoded file paths for demonstration.
    
    Returns:
        dict: Sample encoded paths
    """
    sample_paths = {}
    
    # Sample PAN/Aadhaar document
    pan_path = encode_file_path(
        "pan_card_1234567890.pdf", 
        12345, 
        "pan_aadhaar_docs"
    )
    sample_paths['pan_aadhaar'] = pan_path
    
    # Sample business proof document
    business_path = encode_file_path(
        "business_license_ABC123.pdf", 
        12345, 
        "business_proofs"
    )
    sample_paths['business_proof'] = business_path
    
    # Sample with different user ID
    pan_path_2 = encode_file_path(
        "aadhaar_card_987654321098.pdf", 
        67890, 
        "pan_aadhaar_docs"
    )
    sample_paths['pan_aadhaar_user2'] = pan_path_2
    
    return sample_paths


def validate_encoded_path(encoded_path):
    """
    Validate if an encoded path is properly formatted.
    
    Args:
        encoded_path (str): Encoded file path
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Check if path has expected structure
        if not encoded_path or '/' not in encoded_path:
            return False
        
        # Extract filename
        filename = os.path.basename(encoded_path)
        if not filename:
            return False
        
        # Try to decode
        decoded_info = decode_file_info(encoded_path)
        return decoded_info is not None
        
    except Exception:
        return False 