from django.db import models
from django.contrib.auth import get_user_model
from .validators import validate_document_file

User = get_user_model()


class Partner(models.Model):
    """Main partner profile model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='partner')
    is_verified = models.BooleanField(default=False)
    STATUS_CHOICES = [
        ('in-process', 'In Process'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in-process')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Partner: {self.user.email}"
    
    @property
    def completed_steps(self):
        """Return list of completed onboarding steps."""
        steps = []
        if hasattr(self, 'business_details') and self.business_details:
            steps.append(1)
        if hasattr(self, 'location_coverage') and self.location_coverage:
            steps.append(2)
        if hasattr(self, 'tours_services') and self.tours_services:
            steps.append(3)
        if hasattr(self, 'legal_banking') and self.legal_banking:
            steps.append(4)
        return steps


class BusinessDetails(models.Model):
    """Business information for partner."""
    partner = models.OneToOneField(Partner, on_delete=models.CASCADE, related_name='business_details')
    name = models.CharField(max_length=255)
    type_of_provider = models.JSONField(default=list, help_text="Array of provider types")
    gstin = models.CharField(max_length=15, blank=True, null=True)
    years = models.PositiveIntegerField(help_text="Years in business")
    website = models.URLField(blank=True, null=True)
    reg_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Registration Number")
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    employees = models.PositiveIntegerField()
    seasonal = models.BooleanField(default=False)
    annual_bookings = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Business: {self.name}"


class LocationCoverage(models.Model):
    """Location and coverage information."""
    partner = models.OneToOneField(Partner, on_delete=models.CASCADE, related_name='location_coverage')
    primary_location = models.CharField(max_length=255)
    destinations = models.JSONField(default=list, help_text="Array of destination IDs")
    languages = models.JSONField(default=list, help_text="Array of languages")
    regions = models.JSONField(default=list, help_text="Array of regions")
    pan_india = models.BooleanField(default=False)
    seasons = models.JSONField(default=list, help_text="Array of seasons")
    timezone = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Coverage: {self.primary_location}"


class ToursServices(models.Model):
    """Tours and services information."""
    partner = models.OneToOneField(Partner, on_delete=models.CASCADE, related_name='tours_services')
    number_of_tours = models.PositiveIntegerField()
    types_of_tours = models.JSONField(default=list, help_text="Array of tour types")
    custom_tour_type = models.CharField(max_length=255, blank=True, null=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    group_size_min = models.PositiveIntegerField()
    group_size_max = models.PositiveIntegerField()
    preference = models.CharField(max_length=255, blank=True, null=True)
    offers_custom_tours = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Tours: {self.number_of_tours} tours"


class LegalBanking(models.Model):
    """Legal and banking information."""
    partner = models.OneToOneField(Partner, on_delete=models.CASCADE, related_name='legal_banking')
    
    # File upload for PAN/Aadhaar document
    pan_or_aadhaar_file = models.FileField(
        upload_to='pan_aadhaar_docs/', 
        blank=True, 
        null=True,
        validators=[validate_document_file],
        help_text="Upload PAN/Aadhaar document (PDF/Image, max 10MB)"
    )
    
    # Text field as backup/alternative
    pan_or_aadhaar_text = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        help_text="PAN/Aadhaar number as text"
    )
    
    business_proof_file = models.FileField(upload_to='business_proofs/', blank=True, null=True)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    company_type = models.CharField(max_length=100)
    emergency_contact = models.CharField(max_length=15)
    terms_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Legal: {self.company_type}"

class Tour(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='tours')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.partner.user.email})"