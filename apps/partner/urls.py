from django.urls import path
from . import views

urlpatterns = [
    # Business Details
    path('business-details/', views.business_details_view, name='business-details'),
    
    # Location Coverage
    path('location-coverage/', views.location_coverage_view, name='location-coverage'),
    
    # Tours Services
    path('tours-services/', views.tours_services_view, name='tours-services'),
    
    # Legal Banking
    path('legal-banking/', views.legal_banking_view, name='legal-banking'),
    
    # Status and Completion
    path('status/', views.get_partner_status, name='get-partner-status'),
    path('complete-onboarding/', views.complete_onboarding, name='complete-onboarding'),
]
