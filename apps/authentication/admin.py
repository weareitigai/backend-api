from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import User, OTPVerification


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'mobile', 'is_email_verified', 'is_mobile_verified', 'is_active', 'date_joined']
    list_filter = ['is_email_verified', 'is_mobile_verified', 'is_active', 'date_joined', 'last_login']
    search_fields = ['email', 'first_name', 'last_name', 'mobile']
    ordering = ['-date_joined']
    list_per_page = 25
    date_hierarchy = 'date_joined'
    readonly_fields = ['date_joined', 'last_login']


@admin.register(OTPVerification)
class OTPVerificationAdmin(ImportExportModelAdmin):
    list_display = ['email', 'mobile', 'otp_type', 'otp_code', 'is_verified', 'created_at', 'expires_at']
    list_filter = ['otp_type', 'is_verified', 'created_at']
    search_fields = ['email', 'mobile', 'otp_code']
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'expires_at']
