from rest_framework import serializers
from .models import Partner, BusinessDetails, LocationCoverage, ToursServices, LegalBanking


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
                 'regNumber', 'address', 'employeeCount', 'isSeasonalBusiness', 'annualBookings',
                 'createdAt', 'updatedAt']


class LocationCoverageSerializer(serializers.ModelSerializer):
    """Serializer for location and coverage information."""
    primaryLocation = serializers.CharField(source='primary_location')
    panIndia = serializers.BooleanField(source='pan_india')
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    
    class Meta:
        model = LocationCoverage
        fields = ['primaryLocation', 'destinations', 'languages', 'regions', 
                 'panIndia', 'seasons', 'timezone', 'createdAt', 'updatedAt']


class ToursServicesSerializer(serializers.ModelSerializer):
    """Serializer for tours and services information."""
    numberOfTours = serializers.IntegerField(source='number_of_tours')
    typesOfTours = serializers.JSONField(source='types_of_tours')
    customTourType = serializers.CharField(source='custom_tour_type', required=False, allow_blank=True, allow_null=True)
    minPrice = serializers.DecimalField(source='min_price', max_digits=10, decimal_places=2)
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
