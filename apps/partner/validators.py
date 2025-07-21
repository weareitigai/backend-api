import os
from django.core.exceptions import ValidationError


def validate_document_file(value):
    """Validate that the uploaded file is a PDF or image."""
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif']
    
    if ext not in valid_extensions:
        raise ValidationError('Only PDF and image files are allowed.')
    
    # Check file size (max 10MB)
    if value.size > 10 * 1024 * 1024:
        raise ValidationError('File size must be less than 10MB.')
