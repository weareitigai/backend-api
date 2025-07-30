from django.db import models
from django.contrib.auth import get_user_model
from .validators import validate_document_file
from .utils import get_secure_upload_path

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
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    destinations = models.JSONField(default=list, help_text="Array of destination IDs")
    languages = models.JSONField(default=list, help_text="Array of languages")
    regions = models.JSONField(default=list, help_text="Array of regions")
    pan_india = models.BooleanField(default=False)
    seasons = models.JSONField(default=list, help_text="Array of seasons")
    timezone = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Coverage: {self.city}, {self.state}"


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
        upload_to=get_secure_upload_path, 
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
    
    business_proof_file = models.FileField(upload_to=get_secure_upload_path, blank=True, null=True)
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
    
    # Step 1: Tour Info & Basics
    tour_link = models.URLField(verbose_name='Tour Link (External URL)', blank=True, null=True)
    title = models.CharField(max_length=255, verbose_name='Tour Title', blank=True, null=True)
    destinations = models.JSONField(default=list, verbose_name='Destination(s)', help_text='List of destinations')
    duration_days = models.PositiveIntegerField(verbose_name='Tour Duration (Days)', default=1)
    duration_nights = models.PositiveIntegerField(verbose_name='Tour Duration (Nights)', default=0)
    TOUR_TYPE_CHOICES = [
        ('FIT', 'FIT'),
        ('Group', 'Group'),
        ('Customizable', 'Customizable'),
    ]
    tour_type = models.CharField(max_length=20, choices=TOUR_TYPE_CHOICES, default='FIT', verbose_name='Tour Type')
    provider_name = models.CharField(max_length=255, verbose_name='Tour Provider Name', blank=True, null=True)
    contact_link = models.URLField(blank=True, null=True, verbose_name='Contact Link (Optional)')
    
    # Step 2: Positioning, Highlights & Visuals
    categories = models.JSONField(default=list, verbose_name='Categories', help_text='List of categories like Honeymoon, Adventure, Family, Beach, etc.')
    tags = models.JSONField(default=list, verbose_name='Tags/Keywords', help_text='SEO tags and keywords')
    summary = models.TextField(verbose_name='Tour Summary', help_text='1-3 lines describing the experience', blank=True, null=True)
    highlights = models.JSONField(default=list, verbose_name='Tour Highlights', help_text='List of tour highlights')
    cover_image = models.ImageField(upload_to='tour_covers/', blank=True, null=True, verbose_name='Cover Image')
    
    # Step 3: Pricing, Schedule & Inclusions
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Starting Price (Per Person)')
    PRICE_TYPE_CHOICES = [
        ('Fixed', 'Fixed'),
        ('Starting From', 'Starting From'),
    ]
    price_type = models.CharField(max_length=20, choices=PRICE_TYPE_CHOICES, default='Starting From', verbose_name='Price Type')
    departure_cities = models.JSONField(default=list, verbose_name='Departure Cities', help_text='List of departure cities')
    tour_start_location = models.CharField(max_length=255, verbose_name='Tour Start Location', blank=True, null=True)
    tour_drop_location = models.CharField(max_length=255, verbose_name='Tour Drop Location', blank=True, null=True)
    departure_months = models.JSONField(default=list, verbose_name='Departure Months', help_text='List of months (Jan-Dec)')
    
    TOUR_STATUS_CHOICES = [
        ('Live', 'Live'),
        ('Draft', 'Draft'),
        ('Coming Soon', 'Coming Soon'),
    ]
    tour_status = models.CharField(max_length=20, choices=TOUR_STATUS_CHOICES, default='Draft', verbose_name='Tour Status')
    
    # Inclusions
    includes_flights = models.BooleanField(default=False, verbose_name='Includes Flights?')
    includes_hotels = models.BooleanField(default=False, verbose_name='Includes Hotels?')
    includes_meals = models.BooleanField(default=False, verbose_name='Includes Meals?')
    includes_transfers = models.BooleanField(default=False, verbose_name='Includes Transfers?')
    visa_support = models.BooleanField(default=False, verbose_name='Visa Support Provided?')
    
    # Step 4: Offers & Promotions
    offers_type = models.JSONField(default=list, verbose_name='Offers Type', help_text='Early Bird Offer, Group Discount, Seasonal Discount')
    discount_details = models.TextField(blank=True, null=True, verbose_name='Discount Details')
    promotional_tagline = models.CharField(max_length=255, blank=True, null=True, verbose_name='Promotional Tagline')
    
    # SEO & Visibility
    visibility_score = models.PositiveIntegerField(default=0, verbose_name='Tripsetter Visibility Score')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.partner.user.email})"
    
    def calculate_visibility_score(self):
        """Calculate visibility score based on form completeness and SEO."""
        score = 0
        
        # Basic info (40 points)
        if self.tour_link: score += 10
        if self.title: score += 10
        if self.destinations: score += 10
        if self.duration_days and self.duration_nights: score += 10
        
        # Positioning (30 points)
        if self.categories: score += 10
        if self.summary: score += 10
        if self.highlights: score += 10
        
        # Pricing & Schedule (30 points)
        if self.starting_price: score += 10
        if self.departure_cities: score += 10
        if self.departure_months: score += 10
        
        return min(score, 100)
    
    def save(self, *args, **kwargs):
        self.visibility_score = self.calculate_visibility_score()
        super().save(*args, **kwargs)