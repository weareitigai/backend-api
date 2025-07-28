from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, OTPVerification
from .utils import validate_email_exists


class SendEmailOTPSerializer(serializers.Serializer):
    """Serializer for sending email OTP."""
    email = serializers.CharField(max_length=100)
    
    def validate_email(self, value):
        # Comprehensive email validation
        is_valid, error_message = validate_email_exists(value)
        if not is_valid:
            raise serializers.ValidationError(error_message)
        return value


class VerifyEmailOTPSerializer(serializers.Serializer):
    """Serializer for verifying email OTP."""
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class SendMobileOTPSerializer(serializers.Serializer):
    """Serializer for sending mobile OTP."""
    mobile = serializers.CharField(max_length=15)


class VerifyMobileOTPSerializer(serializers.Serializer):
    """Serializer for verifying mobile OTP."""
    mobile = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)


class UserSignupSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    firstName = serializers.CharField(source='first_name', max_length=30)
    lastName = serializers.CharField(source='last_name', max_length=30)
    companyName = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['firstName', 'lastName', 'companyName', 'email', 'mobile', 'password']
    
    def validate_email(self, value):
        # Comprehensive email validation
        is_valid, error_message = validate_email_exists(value)
        if not is_valid:
            raise serializers.ValidationError(error_message)
        
        # Check if user already exists
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value
    
    def validate_password(self, value):
        # Password validation
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        return value
    
    def validate_mobile(self, value):
        # Allow None/empty values
        if not value:
            return None
            
        # Check for existing mobile numbers only if value is provided
        if User.objects.filter(mobile=value).exists():
            raise serializers.ValidationError("User with this mobile number already exists.")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        companyName = validated_data.pop('companyName')
        email = validated_data['email']
        
        # Create user with email as username
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            mobile=validated_data.get('mobile', None)
        )
        user.set_password(password)
        user.save()
        
        # Create partner profile only (do not auto-create business details)
        from apps.partner.models import Partner
        partner = Partner.objects.create(user=user)
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    emailOrMobile = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email_or_mobile = attrs.get('emailOrMobile')
        password = attrs.get('password')
        
        if email_or_mobile and password:
            # Try to find user by email or mobile
            user = None
            if '@' in email_or_mobile:
                try:
                    user = User.objects.get(email=email_or_mobile)
                except User.DoesNotExist:
                    pass
            else:
                try:
                    user = User.objects.get(mobile=email_or_mobile)
                except User.DoesNotExist:
                    pass
            
            if user and user.check_password(password):
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError("Invalid credentials.")
        else:
            raise serializers.ValidationError("Must include email/mobile and password.")


class ForgotPasswordSerializer(serializers.Serializer):
    """Serializer for forgot password."""
    email = serializers.EmailField()
    
    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer for password reset."""
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    newPassword = serializers.CharField(min_length=6)
    
    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')
        
        try:
            user = User.objects.get(email=email)
            otp_obj = OTPVerification.objects.get(
                email=email,
                otp_code=otp,
                otp_type='reset',
                is_verified=False
            )
            if otp_obj.is_expired():
                raise serializers.ValidationError("OTP has expired.")
            
            attrs['user'] = user
            attrs['otp_obj'] = otp_obj
        except (User.DoesNotExist, OTPVerification.DoesNotExist):
            raise serializers.ValidationError("Invalid email or OTP.")
        
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data."""
    firstName = serializers.CharField(source='first_name', read_only=True)
    lastName = serializers.CharField(source='last_name', read_only=True)
    isEmailVerified = serializers.BooleanField(source='is_email_verified', read_only=True)
    isMobileVerified = serializers.BooleanField(source='is_mobile_verified', read_only=True)
    dateJoined = serializers.DateTimeField(source='date_joined', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'firstName', 'lastName', 'email', 'mobile', 
                 'isEmailVerified', 'isMobileVerified', 'dateJoined']
        read_only_fields = ['id', 'dateJoined']


class UserAuthResponseSerializer(serializers.Serializer):
    """Serializer for successful authentication responses."""
    success = serializers.BooleanField()
    user = UserSerializer()
    token = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing user password."""
    currentPassword = serializers.CharField(write_only=True)
    newPassword = serializers.CharField(write_only=True, min_length=6)
    confirmPassword = serializers.CharField(write_only=True)
    
    def validate_currentPassword(self, value):
        """Validate that current password is correct."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value
    
    def validate(self, attrs):
        """Validate that new passwords match."""
        newPassword = attrs.get('newPassword')
        confirmPassword = attrs.get('confirmPassword')
        
        if newPassword != confirmPassword:
            raise serializers.ValidationError("New passwords do not match.")
        
        return attrs
