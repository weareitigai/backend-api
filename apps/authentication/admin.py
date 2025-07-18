from django.contrib import admin
from .models import User, OTPVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'mobile', 'is_email_verified', 'is_mobile_verified', 'is_active']
    list_filter = ['is_email_verified', 'is_mobile_verified', 'is_active', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name', 'mobile']


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ['email', 'mobile', 'otp_type', 'otp_code', 'is_verified', 'created_at', 'expires_at']
    list_filter = ['otp_type', 'is_verified', 'created_at']
    search_fields = ['email', 'mobile', 'otp_code']
