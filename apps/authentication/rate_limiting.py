import time
from django.core.cache import cache
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response


def check_rate_limit(key, max_requests, window_seconds):
    """
    Check if the rate limit has been exceeded for a given key.
    
    Args:
        key (str): Unique identifier for the rate limit (e.g., email or IP)
        max_requests (int): Maximum number of requests allowed
        window_seconds (int): Time window in seconds
    
    Returns:
        tuple: (is_allowed, remaining_requests, reset_time)
    """
    cache_key = f"rate_limit:{key}"
    current_time = int(time.time())
    
    # Get existing requests from cache
    requests_data = cache.get(cache_key, {'count': 0, 'reset_time': current_time + window_seconds})
    
    # Check if window has expired
    if current_time > requests_data['reset_time']:
        # Reset the counter
        requests_data = {'count': 0, 'reset_time': current_time + window_seconds}
    
    # Check if limit exceeded
    if requests_data['count'] >= max_requests:
        return False, 0, requests_data['reset_time']
    
    # Increment counter
    requests_data['count'] += 1
    cache.set(cache_key, requests_data, window_seconds)
    
    remaining = max_requests - requests_data['count']
    return True, remaining, requests_data['reset_time']


def rate_limit_otp_request(email_or_mobile, request_type='email'):
    """
    Rate limit OTP requests for email or mobile.
    
    Args:
        email_or_mobile (str): Email or mobile number
        request_type (str): Type of request ('email' or 'mobile')
    
    Returns:
        tuple: (is_allowed, response_data, status_code)
    """
    max_requests = getattr(settings, 'RATE_LIMIT_OTP_REQUESTS', 3)
    window_seconds = getattr(settings, 'RATE_LIMIT_OTP_WINDOW', 3600)
    
    # Create unique key for rate limiting
    key = f"otp_{request_type}:{email_or_mobile}"
    
    is_allowed, remaining, reset_time = check_rate_limit(key, max_requests, window_seconds)
    
    if not is_allowed:
        # Calculate time until reset
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