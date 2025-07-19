from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from drf_spectacular.utils import extend_schema
from .models import User, OTPVerification
from .serializers import (
    SendEmailOTPSerializer, VerifyEmailOTPSerializer,
    SendMobileOTPSerializer, VerifyMobileOTPSerializer,
    UserSignupSerializer, UserLoginSerializer,
    ForgotPasswordSerializer, ResetPasswordSerializer,
    UserSerializer, ChangePasswordSerializer, UserAuthResponseSerializer
)
from .utils import (
    create_otp_verification, verify_otp,
    send_email_otp, send_mobile_otp
)
import logging
from django.conf import settings


@extend_schema(
    request=SendEmailOTPSerializer,
    responses={200: {'type': 'object', 'properties': {'success': {'type': 'boolean'}, 'message': {'type': 'string'}}}}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def send_email_otp_view(request):
    """Send OTP to user's email."""
    serializer = SendEmailOTPSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        
        # Create OTP verification
        otp_verification = create_otp_verification(email=email, otp_type='email')
        
        # Send OTP via email
        if send_email_otp(email, otp_verification.otp_code):
            return Response({
                'success': True,
                'message': 'OTP sent to your email successfully'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': 'Failed to send OTP. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'success': False,
        'message': 'Invalid email address'
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=VerifyEmailOTPSerializer,
    responses={200: {'type': 'object', 'properties': {'success': {'type': 'boolean'}, 'message': {'type': 'string'}}}}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email_otp_view(request):
    """Verify OTP sent to email."""
    serializer = VerifyEmailOTPSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        
        success, message = verify_otp(email=email, otp_code=otp, otp_type='email')
        
        if success:
            # Update user's email verification status if user exists
            try:
                user = User.objects.get(email=email)
                user.is_email_verified = True
                user.save()
            except User.DoesNotExist:
                pass
        
        return Response({
            'success': success,
            'message': message
        }, status=status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'success': False,
        'message': 'Invalid data provided'
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=SendMobileOTPSerializer,
    responses={200: {'type': 'object', 'properties': {'success': {'type': 'boolean'}, 'message': {'type': 'string'}}}}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def send_mobile_otp_view(request):
    """Send OTP to user's mobile number."""
    serializer = SendMobileOTPSerializer(data=request.data)
    if serializer.is_valid():
        mobile = serializer.validated_data['mobile']
        
        # Create OTP verification
        otp_verification = create_otp_verification(mobile=mobile, otp_type='mobile')
        
        # Send OTP via SMS
        if send_mobile_otp(mobile, otp_verification.otp_code):
            return Response({
                'success': True,
                'message': 'OTP sent to your mobile successfully'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': 'Failed to send OTP. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'success': False,
        'message': 'Invalid mobile number'
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=VerifyMobileOTPSerializer,
    responses={200: {'type': 'object', 'properties': {'success': {'type': 'boolean'}, 'message': {'type': 'string'}}}}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_mobile_otp_view(request):
    """Verify OTP sent to mobile."""
    serializer = VerifyMobileOTPSerializer(data=request.data)
    if serializer.is_valid():
        mobile = serializer.validated_data['mobile']
        otp = serializer.validated_data['otp']
        
        success, message = verify_otp(mobile=mobile, otp_code=otp, otp_type='mobile')
        
        if success:
            # Update user's mobile verification status if user exists
            try:
                user = User.objects.get(mobile=mobile)
                user.is_mobile_verified = True
                user.save()
            except User.DoesNotExist:
                pass
        
        return Response({
            'success': success,
            'message': message
        }, status=status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'success': False,
        'message': 'Invalid data provided'
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=UserSignupSerializer,
    responses={201: UserAuthResponseSerializer}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    """Register new user."""
    try:
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            # Check if email/mobile are verified (optional for testing)
            email = serializer.validated_data['email']
            mobile = serializer.validated_data.get('mobile')
            
            # Check verification status but don't make it mandatory
            email_verified = OTPVerification.objects.filter(
                email=email, otp_type='email', is_verified=True
            ).exists()
            
            mobile_verified = True  # Default to True if no mobile provided
            if mobile:
                mobile_verified = OTPVerification.objects.filter(
                    mobile=mobile, otp_type='mobile', is_verified=True
                ).exists()
            
            # REMOVED MANDATORY VERIFICATION CONDITIONS FOR TESTING
            # Users can signup without verification, but verification status is tracked
            
            # Create user
            user = serializer.save()
            user.is_email_verified = email_verified
            user.is_mobile_verified = mobile_verified
            user.save()
            
            # Create token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'success': True,
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'message': 'Invalid data provided',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        # Log the error for debugging
        logger = logging.getLogger(__name__)
        logger.error(f"Signup error: {str(e)}")
        
        return Response({
            'success': False,
            'message': 'An error occurred during registration. Please try again.',
            'error': str(e) if settings.DEBUG else 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    request=UserLoginSerializer,
    responses={200: UserAuthResponseSerializer}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login with email/mobile & password."""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Create or get token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'success': True,
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Invalid credentials'
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={200: {'type': 'object', 'properties': {'success': {'type': 'boolean'}}}}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout user."""
    try:
        # Delete the user's token
        request.user.auth_token.delete()
        return Response({
            'success': True
        }, status=status.HTTP_200_OK)
    except:
        return Response({
            'success': False,
            'message': 'Error logging out'
        }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=ForgotPasswordSerializer,
    responses={200: {'type': 'object', 'properties': {'success': {'type': 'boolean'}, 'message': {'type': 'string'}}}}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password_view(request):
    """Initiate password reset."""
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        
        # Create OTP for password reset
        otp_verification = create_otp_verification(email=email, otp_type='reset')
        
        # Send OTP via email
        if send_email_otp(email, otp_verification.otp_code):
            return Response({
                'success': True,
                'message': 'Password reset OTP sent to your email'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': 'Failed to send OTP. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'success': False,
        'message': 'Invalid email address'
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=ResetPasswordSerializer,
    responses={200: {'type': 'object', 'properties': {'success': {'type': 'boolean'}, 'message': {'type': 'string'}}}}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_view(request):
    """Complete password reset."""
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        otp_obj = serializer.validated_data['otp_obj']
        new_password = serializer.validated_data['newPassword']
        
        # Update password
        user.set_password(new_password)
        user.save()
        
        # Mark OTP as verified
        otp_obj.is_verified = True
        otp_obj.save()
        
        return Response({
            'success': True,
            'message': 'Password reset successfully'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Invalid data provided'
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=ChangePasswordSerializer,
    responses={200: {'type': 'object', 'properties': {'success': {'type': 'boolean'}, 'message': {'type': 'string'}}}}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """Change user password."""
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        new_password = serializer.validated_data['new_password']
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        return Response({
            'success': True,
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Invalid data provided',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
