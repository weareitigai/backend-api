from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Partner, BusinessDetails, LocationCoverage, ToursServices, LegalBanking


@admin.register(Partner)
class PartnerAdmin(ImportExportModelAdmin):
    list_display = ['user', 'is_verified', 'status', 'created_at', 'updated_at']
    list_filter = ['is_verified', 'status', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['user']


@admin.register(BusinessDetails)
class BusinessDetailsAdmin(ImportExportModelAdmin):
    list_display = ['partner', 'name', 'years', 'employees', 'seasonal', 'created_at']
    list_filter = ['seasonal', 'created_at']
    search_fields = ['name', 'partner__user__email']
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['partner']


@admin.register(LocationCoverage)
class LocationCoverageAdmin(ImportExportModelAdmin):
    list_display = ['partner', 'primary_location', 'pan_india', 'timezone', 'created_at']
    list_filter = ['pan_india', 'timezone', 'created_at']
    search_fields = ['primary_location', 'partner__user__email']
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['partner']


@admin.register(ToursServices)
class ToursServicesAdmin(ImportExportModelAdmin):
    list_display = ['partner', 'number_of_tours', 'min_price', 'group_size_min', 'group_size_max', 'created_at']
    list_filter = ['offers_custom_tours', 'created_at']
    search_fields = ['partner__user__email']
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['partner']


@admin.register(LegalBanking)
class LegalBankingAdmin(ImportExportModelAdmin):
    list_display = ['partner', 'company_type', 'terms_accepted', 'emergency_contact', 'created_at']
    list_filter = ['company_type', 'terms_accepted', 'created_at']
    search_fields = ['partner__user__email', 'pan_or_aadhaar']
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['partner']
