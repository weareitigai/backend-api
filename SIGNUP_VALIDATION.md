# Signup Validation Features

This document outlines the validation features implemented for the signup process.

## Email Validation

### Format & Length
- **Maximum length**: 100 characters
- **Format validation**: Must be a valid email format (e.g., user@domain.com)
- **Domain validation**: Checks if the email domain has valid MX records
- **Duplicate check**: Prevents signup with existing email addresses

### Validation Rules
```python
# Email field in UserSignupSerializer
email = serializers.EmailField(max_length=100)

# Comprehensive validation method
def validate_email(self, value):
    # Comprehensive email validation
    is_valid, error_message = validate_email_exists(value)
    if not is_valid:
        raise serializers.ValidationError(error_message)
    
    # Check if user already exists
    if User.objects.filter(email=value).exists():
        raise serializers.ValidationError("User with this email already exists.")
    return value
```

### Email Validation Functions
```python
def validate_email_format(email):
    """Validate email format using regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_email_domain(email):
    """Validate that the email domain has valid MX records."""
    try:
        domain = email.split('@')[1]
        mx_records = dns.resolver.resolve(domain, 'MX')
        return len(mx_records) > 0
    except Exception:
        return False

def validate_email_exists(email):
    """Comprehensive email validation including format and domain check."""
    if not validate_email_format(email):
        return False, "Invalid email format"
    
    if len(email) > 100:
        return False, "Email address cannot exceed 100 characters"
    
    if not validate_email_domain(email):
        return False, "Invalid email domain or domain does not exist"
    
    return True, "Email is valid"
```

## Password Security

### Requirements
- **Minimum length**: 6 characters
- **Hashing**: Passwords are automatically hashed using Django's built-in password hashing (bcrypt-like)

### Validation Rules
```python
# Password field in UserSignupSerializer
password = serializers.CharField(write_only=True, min_length=6)

# Validation method
def validate_password(self, value):
    if len(value) < 6:
        raise serializers.ValidationError("Password must be at least 6 characters long.")
    return value
```

## Rate Limiting / Throttling

### OTP Request Limits
- **Maximum requests**: 3 per hour per email/mobile
- **Time window**: 1 hour (3600 seconds)
- **Storage**: Uses Django's cache backend

### Configuration
```python
# Settings configuration
RATE_LIMIT_OTP_REQUESTS = 3  # Maximum OTP requests per hour
RATE_LIMIT_OTP_WINDOW = 3600  # Time window in seconds (1 hour)

# Cache configuration for rate limiting
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```

### Rate Limiting Implementation
```python
def rate_limit_otp_request(email_or_mobile, request_type='email'):
    """
    Rate limit OTP requests for email or mobile.
    
    Returns:
        tuple: (is_allowed, response_data, status_code)
    """
    max_requests = getattr(settings, 'RATE_LIMIT_OTP_REQUESTS', 3)
    window_seconds = getattr(settings, 'RATE_LIMIT_OTP_WINDOW', 3600)
    
    key = f"otp_{request_type}:{email_or_mobile}"
    is_allowed, remaining, reset_time = check_rate_limit(key, max_requests, window_seconds)
    
    if not is_allowed:
        time_until_reset = reset_time - int(time.time())
        hours = time_until_reset // 3600
        minutes = (time_until_reset % 3600) // 60
        
        if hours > 0:
            time_message = f"{hours} hour{'s' if hours != 1 else ''}"
        else:
            time_message = f"{minutes} minute{'s' if minutes != 1 else ''}"
        
        return False, {
            'success': False,
            'message': f'Too many OTP requests. Please try again in {time_message}.'
        }, status.HTTP_429_TOO_MANY_REQUESTS
    
    return True, {
        'success': True,
        'remaining_requests': remaining,
        'reset_time': reset_time
    }, status.HTTP_200_OK
```

## API Endpoints Affected

### Email OTP Endpoint
- **URL**: `/api/auth/send-email-otp/`
- **Method**: POST
- **Rate limiting**: ✅ Applied
- **Email validation**: ✅ Applied

### Mobile OTP Endpoint
- **URL**: `/api/auth/send-mobile-otp/`
- **Method**: POST
- **Rate limiting**: ✅ Applied
- **Mobile validation**: ✅ Applied

### Signup Endpoint
- **URL**: `/api/auth/signup/`
- **Method**: POST
- **Email validation**: ✅ Applied
- **Password validation**: ✅ Applied

## Error Responses

### Email Validation Errors
```json
{
    "success": false,
    "message": "Invalid email format"
}
```

```json
{
    "success": false,
    "message": "Email address cannot exceed 100 characters."
}
```

```json
{
    "success": false,
    "message": "Invalid email domain or domain does not exist"
}
```

```json
{
    "success": false,
    "message": "Account with this email already exists, please sign in"
}
```

### Password Validation Errors
```json
{
    "success": false,
    "errors": {
        "password": ["Password must be at least 6 characters long."]
    }
}
```

### Rate Limiting Errors
```json
{
    "success": false,
    "message": "Too many OTP requests. Please try again in 45 minutes."
}
```

## Testing

Run the validation test script:
```bash
python test_signup_validation.py
```

This will test:
- Email format and length validation
- Password length validation
- Rate limiting functionality

## Dependencies

- `django-ratelimit==4.1.0` - For rate limiting functionality
- `dnspython==2.7.0` - For DNS resolution and domain validation
- Django's built-in cache system
- Django REST Framework serializers

## Security Considerations

1. **Password Hashing**: Django automatically hashes passwords using secure algorithms
2. **Rate Limiting**: Prevents abuse of OTP endpoints
3. **Input Validation**: All user inputs are validated before processing
4. **Duplicate Prevention**: Prevents account creation with existing emails/mobile numbers
5. **Email Domain Validation**: Ensures OTP is only sent to valid email domains with MX records
6. **Format Validation**: Comprehensive email format validation using regex patterns 