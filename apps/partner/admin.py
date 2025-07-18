from django.contrib import admin
from .models import Partner, BusinessDetails, LocationCoverage, ToursServices, LegalBanking


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']


@admin.register(BusinessDetails)
class BusinessDetailsAdmin(admin.ModelAdmin):
    list_display = ['partner', 'name', 'years', 'employees', 'seasonal']
    list_filter = ['seasonal', 'created_at']
    search_fields = ['name', 'partner__user__email']


@admin.register(LocationCoverage)
class LocationCoverageAdmin(admin.ModelAdmin):
    list_display = ['partner', 'primary_location', 'pan_india', 'timezone']
    list_filter = ['pan_india', 'timezone', 'created_at']
    search_fields = ['primary_location', 'partner__user__email']


@admin.register(ToursServices)
class ToursServicesAdmin(admin.ModelAdmin):
    list_display = ['partner', 'number_of_tours', 'min_price', 'group_size_min', 'group_size_max']
    list_filter = ['offers_custom_tours', 'created_at']
    search_fields = ['partner__user__email']


@admin.register(LegalBanking)
class LegalBankingAdmin(admin.ModelAdmin):
    list_display = ['partner', 'company_type', 'terms_accepted', 'emergency_contact']
    list_filter = ['company_type', 'terms_accepted', 'created_at']
    search_fields = ['partner__user__email', 'pan_or_aadhaar']
