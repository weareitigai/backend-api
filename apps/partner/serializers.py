from rest_framework import serializers
from .models import Partner, BusinessDetails, LocationCoverage, ToursServices, LegalBanking, Tour

class TourSerializer(serializers.ModelSerializer):
    # Step 1: Tour Info & Basics
    tourLink = serializers.URLField(source='tour_link')
    title = serializers.CharField()
    destinations = serializers.ListField(child=serializers.CharField(), required=True)
    durationDays = serializers.IntegerField(
        source='duration_days',
        min_value=1,
        default=1,
        help_text="Duration in days (minimum 1)"
    )
    durationNights = serializers.IntegerField(
        source='duration_nights',
        min_value=0,
        default=0,
        help_text="Duration in nights (minimum 0)"
    )
    tourType = serializers.CharField(source='tour_type')
    providerName = serializers.CharField(source='provider_name')
    contactLink = serializers.URLField(source='contact_link', required=False, allow_null=True)
    
    # Step 2: Positioning, Highlights & Visuals
    categories = serializers.ListField(child=serializers.CharField(), required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    summary = serializers.CharField(required=False)
    highlights = serializers.ListField(child=serializers.CharField(), required=False)
    coverImage = serializers.ImageField(source='cover_image', required=False, allow_null=True)
    
    # Step 3: Pricing, Schedule & Inclusions
    startingPrice = serializers.DecimalField(
        source='starting_price', 
        max_digits=10, 
        decimal_places=2, 
        coerce_to_string=False,
        min_value=0.01,
        default=0.00,
        help_text="Starting price in INR (minimum 0.01)"
    )
    priceType = serializers.CharField(source='price_type')
    departureCities = serializers.ListField(child=serializers.CharField(), source='departure_cities', required=False)
    tourStartLocation = serializers.CharField(source='tour_start_location')
    tourDropLocation = serializers.CharField(source='tour_drop_location')
    departureMonths = serializers.ListField(child=serializers.CharField(), source='departure_months', required=False)
    tourStatus = serializers.CharField(source='tour_status')
    
    # Inclusions
    includesFlights = serializers.BooleanField(source='includes_flights')
    includesHotels = serializers.BooleanField(source='includes_hotels')
    includesMeals = serializers.BooleanField(source='includes_meals')
    includesTransfers = serializers.BooleanField(source='includes_transfers')
    visaSupport = serializers.BooleanField(source='visa_support')
    
    # Step 4: Offers & Promotions
    offersType = serializers.ListField(child=serializers.CharField(), source='offers_type', required=False)
    discountDetails = serializers.CharField(source='discount_details', required=False, allow_blank=True, allow_null=True)
    promotionalTagline = serializers.CharField(source='promotional_tagline', required=False, allow_blank=True, allow_null=True)
    
    # SEO & Visibility
    visibilityScore = serializers.IntegerField(source='visibility_score', read_only=True)
    
    # Timestamps
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = Tour
        fields = [
            'id',
            'tourLink',
            'title',
            'destinations',
            'durationDays',
            'durationNights',
            'tourType',
            'providerName',
            'contactLink',
            'categories',
            'tags',
            'summary',
            'highlights',
            'coverImage',
            'startingPrice',
            'priceType',
            'departureCities',
            'tourStartLocation',
            'tourDropLocation',
            'departureMonths',
            'tourStatus',
            'includesFlights',
            'includesHotels',
            'includesMeals',
            'includesTransfers',
            'visaSupport',
            'offersType',
            'discountDetails',
            'promotionalTagline',
            'visibilityScore',
            'createdAt',
            'updatedAt',
        ]

class TourCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tours with user_id parameter."""
    user_id = serializers.IntegerField(write_only=True)
    
    # Step 1: Tour Info & Basics
    tourLink = serializers.URLField(source='tour_link', required=False, allow_blank=True, allow_null=True)
    title = serializers.CharField(required=False, allow_blank=True)
    destinations = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    durationDays = serializers.IntegerField(
        source='duration_days',
        required=False,
        default=1,
        help_text="Duration in days (minimum 1)"
    )
    durationNights = serializers.IntegerField(
        source='duration_nights',
        required=False,
        default=0,
        help_text="Duration in nights (minimum 0)"
    )
    tourType = serializers.CharField(source='tour_type', required=False, default='FIT')
    providerName = serializers.CharField(source='provider_name', required=False, allow_blank=True)
    contactLink = serializers.URLField(source='contact_link', required=False, allow_null=True, allow_blank=True)
    
    # Step 2: Positioning, Highlights & Visuals
    categories = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    tags = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    summary = serializers.CharField(required=False, allow_blank=True)
    highlights = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    coverImage = serializers.ImageField(source='cover_image', required=False, allow_null=True)
    
    # Step 3: Pricing, Schedule & Inclusions
    startingPrice = serializers.DecimalField(
        source='starting_price', 
        max_digits=10, 
        decimal_places=2, 
        coerce_to_string=False,
        required=False,
        default=0.00,
        help_text="Starting price in INR"
    )
    priceType = serializers.CharField(source='price_type', required=False, default='Starting From')
    departureCities = serializers.ListField(child=serializers.CharField(), source='departure_cities', required=False, default=list)
    tourStartLocation = serializers.CharField(source='tour_start_location', required=False, allow_blank=True)
    tourDropLocation = serializers.CharField(source='tour_drop_location', required=False, allow_blank=True)
    departureMonths = serializers.ListField(child=serializers.CharField(), source='departure_months', required=False, default=list)
    tourStatus = serializers.CharField(source='tour_status', required=False, default='Draft')
    
    # Inclusions
    includesFlights = serializers.BooleanField(source='includes_flights', required=False, default=False)
    includesHotels = serializers.BooleanField(source='includes_hotels', required=False, default=False)
    includesMeals = serializers.BooleanField(source='includes_meals', required=False, default=False)
    includesTransfers = serializers.BooleanField(source='includes_transfers', required=False, default=False)
    visaSupport = serializers.BooleanField(source='visa_support', required=False, default=False)
    
    # Step 4: Offers & Promotions
    offersType = serializers.ListField(child=serializers.CharField(), source='offers_type', required=False, default=list)
    discountDetails = serializers.CharField(source='discount_details', required=False, allow_blank=True, allow_null=True)
    promotionalTagline = serializers.CharField(source='promotional_tagline', required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Tour
        fields = [
            'user_id',
            'tourLink',
            'title',
            'destinations',
            'durationDays',
            'durationNights',
            'tourType',
            'providerName',
            'contactLink',
            'categories',
            'tags',
            'summary',
            'highlights',
            'coverImage',
            'startingPrice',
            'priceType',
            'departureCities',
            'tourStartLocation',
            'tourDropLocation',
            'departureMonths',
            'tourStatus',
            'includesFlights',
            'includesHotels',
            'includesMeals',
            'includesTransfers',
            'visaSupport',
            'offersType',
            'discountDetails',
            'promotionalTagline',
        ]

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        try:
            partner = Partner.objects.get(user_id=user_id)
        except Partner.DoesNotExist:
            raise serializers.ValidationError("Partner not found for the given user_id")
        
        validated_data['partner'] = partner
        return super().create(validated_data)

class TourUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating tours."""
    
    # Step 1: Tour Info & Basics
    tourLink = serializers.URLField(source='tour_link', required=False)
    title = serializers.CharField(required=False)
    destinations = serializers.ListField(child=serializers.CharField(), required=False)
    durationDays = serializers.IntegerField(source='duration_days', required=False)
    durationNights = serializers.IntegerField(source='duration_nights', required=False)
    tourType = serializers.CharField(source='tour_type', required=False)
    providerName = serializers.CharField(source='provider_name', required=False)
    contactLink = serializers.URLField(source='contact_link', required=False, allow_null=True)
    
    # Step 2: Positioning, Highlights & Visuals
    categories = serializers.ListField(child=serializers.CharField(), required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    summary = serializers.CharField(required=False)
    highlights = serializers.ListField(child=serializers.CharField(), required=False)
    coverImage = serializers.ImageField(source='cover_image', required=False, allow_null=True)
    
    # Step 3: Pricing, Schedule & Inclusions
    startingPrice = serializers.DecimalField(
        source='starting_price', 
        max_digits=10, 
        decimal_places=2, 
        coerce_to_string=False, 
        required=False,
        min_value=0.01,
        help_text="Starting price in INR (minimum 0.01)"
    )
    priceType = serializers.CharField(source='price_type', required=False)
    departureCities = serializers.ListField(child=serializers.CharField(), source='departure_cities', required=False)
    tourStartLocation = serializers.CharField(source='tour_start_location', required=False)
    tourDropLocation = serializers.CharField(source='tour_drop_location', required=False)
    departureMonths = serializers.ListField(child=serializers.CharField(), source='departure_months', required=False)
    tourStatus = serializers.CharField(source='tour_status', required=False)
    
    # Inclusions
    includesFlights = serializers.BooleanField(source='includes_flights', required=False)
    includesHotels = serializers.BooleanField(source='includes_hotels', required=False)
    includesMeals = serializers.BooleanField(source='includes_meals', required=False)
    includesTransfers = serializers.BooleanField(source='includes_transfers', required=False)
    visaSupport = serializers.BooleanField(source='visa_support', required=False)
    
    # Step 4: Offers & Promotions
    offersType = serializers.ListField(child=serializers.CharField(), source='offers_type', required=False)
    discountDetails = serializers.CharField(source='discount_details', required=False, allow_blank=True, allow_null=True)
    promotionalTagline = serializers.CharField(source='promotional_tagline', required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Tour
        fields = [
            'tourLink',
            'title',
            'destinations',
            'durationDays',
            'durationNights',
            'tourType',
            'providerName',
            'contactLink',
            'categories',
            'tags',
            'summary',
            'highlights',
            'coverImage',
            'startingPrice',
            'priceType',
            'departureCities',
            'tourStartLocation',
            'tourDropLocation',
            'departureMonths',
            'tourStatus',
            'includesFlights',
            'includesHotels',
            'includesMeals',
            'includesTransfers',
            'visaSupport',
            'offersType',
            'discountDetails',
            'promotionalTagline',
        ]

class TourListSerializer(serializers.ModelSerializer):
    """Serializer for listing tours with essential fields."""
    tourLink = serializers.URLField(source='tour_link')
    durationDays = serializers.IntegerField(source='duration_days')
    durationNights = serializers.IntegerField(source='duration_nights')
    tourType = serializers.CharField(source='tour_type')
    providerName = serializers.CharField(source='provider_name')
    startingPrice = serializers.DecimalField(
        source='starting_price', 
        max_digits=10, 
        decimal_places=2, 
        coerce_to_string=False,
        min_value=0.01,
        help_text="Starting price in INR (minimum 0.01)"
    )
    priceType = serializers.CharField(source='price_type')
    tourStatus = serializers.CharField(source='tour_status')
    visibilityScore = serializers.IntegerField(source='visibility_score')
    createdAt = serializers.DateTimeField(source='created_at')
    updatedAt = serializers.DateTimeField(source='updated_at')

    class Meta:
        model = Tour
        fields = [
            'id',
            'tourLink',
            'title',
            'destinations',
            'durationDays',
            'durationNights',
            'tourType',
            'providerName',
            'startingPrice',
            'priceType',
            'tourStatus',
            'visibilityScore',
            'createdAt',
            'updatedAt',
        ]

class TourDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed tour view with all fields."""
    tourLink = serializers.URLField(source='tour_link')
    durationDays = serializers.IntegerField(source='duration_days')
    durationNights = serializers.IntegerField(source='duration_nights')
    tourType = serializers.CharField(source='tour_type')
    providerName = serializers.CharField(source='provider_name')
    contactLink = serializers.URLField(source='contact_link')
    coverImage = serializers.ImageField(source='cover_image')
    startingPrice = serializers.DecimalField(
        source='starting_price', 
        max_digits=10, 
        decimal_places=2, 
        coerce_to_string=False,
        min_value=0.01,
        help_text="Starting price in INR (minimum 0.01)"
    )
    priceType = serializers.CharField(source='price_type')
    departureCities = serializers.ListField(child=serializers.CharField(), source='departure_cities')
    tourStartLocation = serializers.CharField(source='tour_start_location')
    tourDropLocation = serializers.CharField(source='tour_drop_location')
    departureMonths = serializers.ListField(child=serializers.CharField(), source='departure_months')
    tourStatus = serializers.CharField(source='tour_status')
    includesFlights = serializers.BooleanField(source='includes_flights')
    includesHotels = serializers.BooleanField(source='includes_hotels')
    includesMeals = serializers.BooleanField(source='includes_meals')
    includesTransfers = serializers.BooleanField(source='includes_transfers')
    visaSupport = serializers.BooleanField(source='visa_support')
    offersType = serializers.ListField(child=serializers.CharField(), source='offers_type')
    discountDetails = serializers.CharField(source='discount_details')
    promotionalTagline = serializers.CharField(source='promotional_tagline')
    visibilityScore = serializers.IntegerField(source='visibility_score')
    createdAt = serializers.DateTimeField(source='created_at')
    updatedAt = serializers.DateTimeField(source='updated_at')

    class Meta:
        model = Tour
        fields = [
            'id',
            'tourLink',
            'title',
            'destinations',
            'durationDays',
            'durationNights',
            'tourType',
            'providerName',
            'contactLink',
            'categories',
            'tags',
            'summary',
            'highlights',
            'coverImage',
            'startingPrice',
            'priceType',
            'departureCities',
            'tourStartLocation',
            'tourDropLocation',
            'departureMonths',
            'tourStatus',
            'includesFlights',
            'includesHotels',
            'includesMeals',
            'includesTransfers',
            'visaSupport',
            'offersType',
            'discountDetails',
            'promotionalTagline',
            'visibilityScore',
            'createdAt',
            'updatedAt',
        ]

class TourScrapingDataSerializer(serializers.Serializer):
    """Serializer for tour data extracted from scraping."""
    tourLink = serializers.URLField(help_text="External URL of the tour page")
    title = serializers.CharField(help_text="Tour title")
    destinations = serializers.ListField(child=serializers.CharField(), help_text="List of destinations")
    durationDays = serializers.IntegerField(help_text="Duration in days (minimum 1)")
    durationNights = serializers.IntegerField(help_text="Duration in nights (minimum 0)")
    tourType = serializers.CharField(help_text="Tour type: FIT, Group, or Customizable")
    providerName = serializers.CharField(help_text="Tour provider/agency name")
    contactLink = serializers.URLField(required=False, allow_null=True, help_text="Contact URL or WhatsApp link")
    tourStatus = serializers.CharField(required=False, default="Live", help_text="Tour status: Live, Draft, or Coming Soon")
    categories = serializers.ListField(child=serializers.CharField(), required=False, help_text="List of categories (e.g., Adventure, Honeymoon, Family)")
    tags = serializers.ListField(child=serializers.CharField(), required=False, help_text="SEO tags and keywords")
    summary = serializers.CharField(required=False, help_text="Brief tour description (1-3 lines)")
    highlights = serializers.ListField(child=serializers.CharField(), required=False, help_text="List of tour highlights")
    startingPrice = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        coerce_to_string=False,
        min_value=0.01,
        help_text="Starting price in INR (minimum 0.01)"
    )
    priceType = serializers.CharField(help_text="Price type: Starting From or Fixed")
    departureCities = serializers.ListField(child=serializers.CharField(), required=False, help_text="List of departure cities")
    tourStartLocation = serializers.CharField(required=False, help_text="Tour start location")
    tourDropLocation = serializers.CharField(required=False, help_text="Tour drop location")
    departureMonths = serializers.ListField(child=serializers.CharField(), required=False, help_text="List of departure months")
    includesFlights = serializers.BooleanField(required=False, help_text="Whether tour includes flights")
    includesHotels = serializers.BooleanField(required=False, help_text="Whether tour includes hotels")
    includesMeals = serializers.BooleanField(required=False, help_text="Whether tour includes meals")
    includesTransfers = serializers.BooleanField(required=False, help_text="Whether tour includes transfers")
    visaSupport = serializers.BooleanField(required=False, help_text="Whether visa support is provided")
    offersType = serializers.ListField(child=serializers.CharField(), required=False, help_text="List of offer types (e.g., Early Bird, Group Discount)")
    discountDetails = serializers.CharField(required=False, allow_blank=True, allow_null=True, help_text="Detailed discount information")
    promotionalTagline = serializers.CharField(required=False, allow_blank=True, allow_null=True, help_text="Promotional tagline or message")

class BusinessDetailsSerializer(serializers.ModelSerializer):
    """Serializer for business details."""
    companyName = serializers.CharField(source='name')
    typeOfProvider = serializers.JSONField(source='type_of_provider')
    yearsInBusiness = serializers.IntegerField(source='years')
    regNumber = serializers.CharField(source='reg_number', required=False, allow_blank=True, allow_null=True)
    employeeCount = serializers.IntegerField(source='employees')
    isSeasonalBusiness = serializers.BooleanField(source='seasonal')
    annualBookings = serializers.IntegerField(source='annual_bookings', required=False, allow_null=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    
    class Meta:
        model = BusinessDetails
        fields = ['companyName', 'typeOfProvider', 'gstin', 'yearsInBusiness', 'website', 
                 'regNumber', 'city', 'state', 'country', 'employeeCount', 'isSeasonalBusiness', 'annualBookings',
                 'createdAt', 'updatedAt']


class LocationCoverageSerializer(serializers.ModelSerializer):
    """Serializer for location and coverage information."""
    panIndia = serializers.BooleanField(source='pan_india')
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    
    class Meta:
        model = LocationCoverage
        fields = ['city', 'state', 'destinations', 'languages', 'regions', 
                 'panIndia', 'seasons', 'timezone', 'createdAt', 'updatedAt']


class ToursServicesSerializer(serializers.ModelSerializer):
    """Serializer for tours and services information."""
    numberOfTours = serializers.IntegerField(source='number_of_tours')
    typesOfTours = serializers.JSONField(source='types_of_tours')
    customTourType = serializers.CharField(source='custom_tour_type', required=False, allow_blank=True, allow_null=True)
    minPrice = serializers.DecimalField(source='min_price', max_digits=10, decimal_places=2, coerce_to_string=False)
    groupSizeMin = serializers.IntegerField(source='group_size_min')
    groupSizeMax = serializers.IntegerField(source='group_size_max')
    offersCustomTours = serializers.BooleanField(source='offers_custom_tours')
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    
    class Meta:
        model = ToursServices
        fields = ['numberOfTours', 'typesOfTours', 'customTourType', 'minPrice',
                 'groupSizeMin', 'groupSizeMax', 'preference', 'offersCustomTours',
                 'createdAt', 'updatedAt']


class LegalBankingSerializer(serializers.ModelSerializer):
    """Serializer for legal and banking information."""
    panOrAadhaarFile = serializers.FileField(
        source='pan_or_aadhaar_file', 
        required=False, 
        allow_null=True,
        help_text="Upload PAN/Aadhaar document (PDF/Image, max 10MB)"
    )
    panOrAadhaarText = serializers.CharField(
        source='pan_or_aadhaar_text', 
        required=False, 
        allow_blank=True, 
        allow_null=True,
        help_text="PAN/Aadhaar number as text"
    )
    businessProofFile = serializers.FileField(source='business_proof_file', required=False, allow_null=True)
    licenseNumber = serializers.CharField(source='license_number', required=False, allow_blank=True, allow_null=True)
    companyType = serializers.CharField(source='company_type')
    emergencyContact = serializers.CharField(source='emergency_contact')
    termsAccepted = serializers.BooleanField(source='terms_accepted')
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    
    class Meta:
        model = LegalBanking
        fields = ['panOrAadhaarFile', 'panOrAadhaarText', 'businessProofFile', 'licenseNumber', 
                 'companyType', 'emergencyContact', 'termsAccepted', 'createdAt', 'updatedAt']


class PartnerStatusSerializer(serializers.ModelSerializer):
    """Serializer for partner status information."""
    completedSteps = serializers.ReadOnlyField(source='completed_steps')
    isVerified = serializers.BooleanField(source='is_verified', read_only=True)
    status = serializers.CharField(read_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Partner
        fields = ['completedSteps', 'isVerified', 'status', 'user']

    def get_user(self, obj):
        from apps.authentication.serializers import UserSerializer
        return UserSerializer(obj.user).data
    
    def get_completedSteps(self, obj) -> list:
        """Get completed steps with proper type hint."""
        return obj.completed_steps
    
    def get_user(self, obj) -> dict:
        """Get user data with proper type hint."""
        from apps.authentication.serializers import UserSerializer
        return UserSerializer(obj.user).data


class BusinessDetailsResponseSerializer(serializers.Serializer):
    """Serializer for business details response."""
    success = serializers.BooleanField()
    message = serializers.CharField(required=False)
    data = BusinessDetailsSerializer()


class LocationCoverageResponseSerializer(serializers.Serializer):
    """Serializer for location and coverage response."""
    success = serializers.BooleanField()
    message = serializers.CharField(required=False)
    data = LocationCoverageSerializer()


class ToursServicesResponseSerializer(serializers.Serializer):
    """Serializer for tours and services response."""
    success = serializers.BooleanField()
    message = serializers.CharField(required=False)
    data = ToursServicesSerializer()


class LegalBankingResponseSerializer(serializers.Serializer):
    """Serializer for legal and banking response."""
    success = serializers.BooleanField()
    message = serializers.CharField(required=False)
    data = LegalBankingSerializer()


class TourScrapingRequestSerializer(serializers.Serializer):
    """Serializer for tour scraping request."""
    url = serializers.URLField(
        help_text="URL of the tour page to scrape. Must be a complete URL starting with http:// or https://"
    )


class TourScrapingResponseSerializer(serializers.Serializer):
    """Serializer for tour scraping response."""
    success = serializers.BooleanField(help_text="Whether the scraping was successful")
    data = serializers.DictField(help_text="Extracted tour data in the new schema format")
    message = serializers.CharField(help_text="Success or error message")
