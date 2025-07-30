from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html
from .models import Partner, BusinessDetails, LocationCoverage, ToursServices, LegalBanking, Tour


@admin.register(Partner)
class PartnerAdmin(ImportExportModelAdmin):
    list_display = ['user', 'is_verified', 'status', 'get_completed_steps', 'created_at', 'updated_at']
    list_filter = ['is_verified', 'status', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'get_completed_steps']
    raw_id_fields = ['user']
    list_editable = ['is_verified', 'status']
    
    fieldsets = (
        ('Partner Information', {
            'fields': ('user', 'is_verified', 'status')
        }),
        ('Onboarding Progress', {
            'fields': ('get_completed_steps',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_completed_steps(self, obj):
        steps = obj.completed_steps
        if steps:
            step_names = {
                1: 'Business Details',
                2: 'Location Coverage', 
                3: 'Tours Services',
                4: 'Legal Banking'
            }
            completed = [step_names.get(step, f'Step {step}') for step in steps]
            return ', '.join(completed)
        return 'No steps completed'
    get_completed_steps.short_description = 'Completed Steps'


@admin.register(BusinessDetails)
class BusinessDetailsAdmin(ImportExportModelAdmin):
    list_display = [
        'partner', 'name', 'get_type_of_provider', 'gstin', 'years', 'website', 
        'reg_number', 'city', 'state', 'country', 'employees', 'seasonal', 
        'annual_bookings', 'created_at'
    ]
    list_filter = ['seasonal', 'created_at', 'country', 'state']
    search_fields = ['name', 'partner__user__email', 'gstin', 'reg_number']
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['partner']
    list_editable = ['seasonal', 'employees', 'annual_bookings']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('partner', 'name', 'type_of_provider', 'years', 'employees')
        }),
        ('Business Details', {
            'fields': ('gstin', 'website', 'reg_number', 'seasonal', 'annual_bookings')
        }),
        ('Location', {
            'fields': ('city', 'state', 'country')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_type_of_provider(self, obj):
        if obj.type_of_provider:
            return ', '.join(obj.type_of_provider)
        return '-'
    get_type_of_provider.short_description = 'Provider Types'


@admin.register(LocationCoverage)
class LocationCoverageAdmin(ImportExportModelAdmin):
    list_display = [
        'partner', 'city', 'state', 'get_destinations', 'get_languages', 'get_regions', 
        'pan_india', 'get_seasons', 'timezone', 'created_at'
    ]
    list_filter = ['pan_india', 'created_at', 'state', 'timezone']
    search_fields = ['city', 'state', 'partner__user__email']
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['partner']
    list_editable = ['pan_india']
    
    fieldsets = (
        ('Partner Information', {
            'fields': ('partner',)
        }),
        ('Location Details', {
            'fields': ('city', 'state', 'pan_india')
        }),
        ('Coverage Information', {
            'fields': ('destinations', 'languages', 'regions', 'seasons', 'timezone')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_destinations(self, obj):
        if obj.destinations:
            return ', '.join(map(str, obj.destinations))
        return '-'
    get_destinations.short_description = 'Destinations'
    
    def get_languages(self, obj):
        if obj.languages:
            return ', '.join(obj.languages)
        return '-'
    get_languages.short_description = 'Languages'
    
    def get_regions(self, obj):
        if obj.regions:
            return ', '.join(obj.regions)
        return '-'
    get_regions.short_description = 'Regions'
    
    def get_seasons(self, obj):
        if obj.seasons:
            return ', '.join(obj.seasons)
        return '-'
    get_seasons.short_description = 'Seasons'


@admin.register(ToursServices)
class ToursServicesAdmin(ImportExportModelAdmin):
    list_display = [
        'partner', 'number_of_tours', 'get_types_of_tours', 'custom_tour_type', 
        'min_price', 'group_size_min', 'group_size_max', 'preference', 
        'offers_custom_tours', 'created_at'
    ]
    list_filter = ['offers_custom_tours', 'created_at']
    search_fields = ['partner__user__email', 'custom_tour_type', 'preference']
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['partner']
    list_editable = ['offers_custom_tours', 'min_price']
    
    fieldsets = (
        ('Partner Information', {
            'fields': ('partner',)
        }),
        ('Tour Information', {
            'fields': ('number_of_tours', 'types_of_tours', 'custom_tour_type', 'offers_custom_tours')
        }),
        ('Pricing & Groups', {
            'fields': ('min_price', 'group_size_min', 'group_size_max', 'preference')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_types_of_tours(self, obj):
        if obj.types_of_tours:
            return ', '.join(obj.types_of_tours)
        return '-'
    get_types_of_tours.short_description = 'Tour Types'


@admin.register(LegalBanking)
class LegalBankingAdmin(ImportExportModelAdmin):
    list_display = [
        'partner', 'company_type', 'pan_or_aadhaar_text', 'license_number', 
        'emergency_contact', 'terms_accepted', 'get_file_preview', 'created_at'
    ]
    list_filter = ['company_type', 'terms_accepted', 'created_at']
    search_fields = ['partner__user__email', 'pan_or_aadhaar_text', 'license_number']
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'get_file_preview', 'get_detailed_file_preview']
    raw_id_fields = ['partner']
    list_editable = ['terms_accepted']
    
    fieldsets = (
        ('Partner Information', {
            'fields': ('partner',)
        }),
        ('Company Details', {
            'fields': ('company_type', 'license_number')
        }),
        ('Documentation', {
            'fields': ('pan_or_aadhaar_file', 'pan_or_aadhaar_text', 'business_proof_file', 'get_detailed_file_preview')
        }),
        ('Contact Information', {
            'fields': ('emergency_contact', 'terms_accepted')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_file_preview(self, obj):
        """Display compact file preview in list view."""
        preview_html = []
        
        if obj.pan_or_aadhaar_file:
            file_name = obj.pan_or_aadhaar_file.name.split('/')[-1]
            file_ext = file_name.split('.')[-1].lower()
            
            if file_ext in ['jpg', 'jpeg', 'png', 'gif']:
                preview_html.append(
                    f'<div style="margin: 5px 0;"><strong>PAN:</strong> '
                    f'<img src="{obj.pan_or_aadhaar_file.url}" style="max-width: 50px; max-height: 40px; border: 1px solid #ddd;" />'
                    f'<br><small>{file_name[:20]}...</small></div>'
                )
            else:
                preview_html.append(
                    f'<div style="margin: 5px 0;"><strong>PAN:</strong> '
                    f'<a href="{obj.pan_or_aadhaar_file.url}" target="_blank">📄 {file_name[:20]}...</a></div>'
                )
        
        if obj.business_proof_file:
            file_name = obj.business_proof_file.name.split('/')[-1]
            file_ext = file_name.split('.')[-1].lower()
            
            if file_ext in ['jpg', 'jpeg', 'png', 'gif']:
                preview_html.append(
                    f'<div style="margin: 5px 0;"><strong>BP:</strong> '
                    f'<img src="{obj.business_proof_file.url}" style="max-width: 50px; max-height: 40px; border: 1px solid #ddd;" />'
                    f'<br><small>{file_name[:20]}...</small></div>'
                )
            else:
                preview_html.append(
                    f'<div style="margin: 5px 0;"><strong>BP:</strong> '
                    f'<a href="{obj.business_proof_file.url}" target="_blank">📄 {file_name[:20]}...</a></div>'
                )
        
        if not preview_html:
            return "No files"
        
        return format_html(''.join(preview_html))
    
    def get_detailed_file_preview(self, obj):
        """Display detailed file preview in detail view."""
        preview_html = []
        
        if obj.pan_or_aadhaar_file:
            file_url = obj.pan_or_aadhaar_file.url
            file_name = obj.pan_or_aadhaar_file.name.split('/')[-1]
            file_ext = file_name.split('.')[-1].lower()
            
            if file_ext in ['jpg', 'jpeg', 'png', 'gif']:
                preview_html.append(
                    f'<div style="margin: 15px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; background: #f9f9f9;">'
                    f'<strong>PAN/Aadhaar Document:</strong><br>'
                    f'<img src="{file_url}" style="max-width: 300px; max-height: 200px; border: 2px solid #007bff; border-radius: 5px; margin: 10px 0;" />'
                    f'<br><small style="color: #666;">📁 {file_name}</small>'
                    f'<br><a href="{file_url}" target="_blank" style="color: #007bff;">🔗 Open Full Size</a>'
                    f'</div>'
                )
            else:
                preview_html.append(
                    f'<div style="margin: 15px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; background: #f9f9f9;">'
                    f'<strong>PAN/Aadhaar Document:</strong><br>'
                    f'<a href="{file_url}" target="_blank" style="color: #007bff; text-decoration: none; font-size: 16px;">📄 {file_name}</a>'
                    f'<br><small style="color: #666;">Click to download/view</small>'
                    f'</div>'
                )
        
        if obj.business_proof_file:
            file_url = obj.business_proof_file.url
            file_name = obj.business_proof_file.name.split('/')[-1]
            file_ext = file_name.split('.')[-1].lower()
            
            if file_ext in ['jpg', 'jpeg', 'png', 'gif']:
                preview_html.append(
                    f'<div style="margin: 15px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; background: #f9f9f9;">'
                    f'<strong>Business Proof Document:</strong><br>'
                    f'<img src="{file_url}" style="max-width: 300px; max-height: 200px; border: 2px solid #28a745; border-radius: 5px; margin: 10px 0;" />'
                    f'<br><small style="color: #666;">📁 {file_name}</small>'
                    f'<br><a href="{file_url}" target="_blank" style="color: #28a745;">🔗 Open Full Size</a>'
                    f'</div>'
                )
            else:
                preview_html.append(
                    f'<div style="margin: 15px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; background: #f9f9f9;">'
                    f'<strong>Business Proof Document:</strong><br>'
                    f'<a href="{file_url}" target="_blank" style="color: #28a745; text-decoration: none; font-size: 16px;">📄 {file_name}</a>'
                    f'<br><small style="color: #666;">Click to download/view</small>'
                    f'</div>'
                )
        
        if not preview_html:
            return format_html('<div style="color: #999; font-style: italic;">No files uploaded</div>')
        
        return format_html(''.join(preview_html))
    
    get_file_preview.short_description = 'File Preview'
    get_file_preview.allow_tags = True
    get_detailed_file_preview.short_description = 'File Preview'
    get_detailed_file_preview.allow_tags = True


@admin.register(Tour)
class TourAdmin(ImportExportModelAdmin):
    list_display = [
        'id', 'partner', 'title', 'get_destinations', 'duration_days', 'duration_nights',
        'tour_type', 'provider_name', 'starting_price', 'price_type', 'tour_status',
        'visibility_score', 'created_at'
    ]
    list_filter = [
        'tour_type', 'tour_status', 'price_type', 'includes_flights', 'includes_hotels',
        'includes_meals', 'includes_transfers', 'visa_support', 'created_at'
    ]
    search_fields = [
        'title', 'provider_name', 'partner__user__email', 'destinations',
        'tour_start_location', 'tour_drop_location'
    ]
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'visibility_score']
    raw_id_fields = ['partner']
    list_editable = ['tour_status', 'price_type']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('partner', 'tour_link', 'title', 'destinations', 'duration_days', 'duration_nights')
        }),
        ('Tour Details', {
            'fields': ('tour_type', 'provider_name', 'contact_link', 'categories', 'tags', 'summary', 'highlights')
        }),
        ('Pricing & Schedule', {
            'fields': ('starting_price', 'price_type', 'departure_cities', 'tour_start_location', 'tour_drop_location', 'departure_months')
        }),
        ('Status & Inclusions', {
            'fields': ('tour_status', 'includes_flights', 'includes_hotels', 'includes_meals', 'includes_transfers', 'visa_support')
        }),
        ('Offers & Promotions', {
            'fields': ('offers_type', 'discount_details', 'promotional_tagline'),
            'classes': ('collapse',)
        }),
        ('Media & SEO', {
            'fields': ('cover_image', 'visibility_score'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_destinations(self, obj):
        if obj.destinations:
            return ', '.join(obj.destinations)
        return '-'
    get_destinations.short_description = 'Destinations'
    
    def get_short_title(self, obj):
        if len(obj.title) > 50:
            return obj.title[:50] + '...'
        return obj.title
    get_short_title.short_description = 'Title'
