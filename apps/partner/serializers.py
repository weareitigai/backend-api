from rest_framework import serializers
from .models import Partner, BusinessDetails, LocationCoverage, ToursServices, LegalBanking


class BusinessDetailsSerializer(serializers.ModelSerializer):
    """Serializer for business details."""
    
    class Meta:
        model = BusinessDetails
        fields = '__all__'
        extra_kwargs = {
            'partner': {'read_only': True}
        }


class LocationCoverageSerializer(serializers.ModelSerializer):
    """Serializer for location and coverage information."""
    
    class Meta:
        model = LocationCoverage
        fields = '__all__'
        extra_kwargs = {
            'partner': {'read_only': True}
        }


class ToursServicesSerializer(serializers.ModelSerializer):
    """Serializer for tours and services information."""
    
    class Meta:
        model = ToursServices
        fields = '__all__'
        extra_kwargs = {
            'partner': {'read_only': True}
        }


class LegalBankingSerializer(serializers.ModelSerializer):
    """Serializer for legal and banking information."""
    
    class Meta:
        model = LegalBanking
        fields = '__all__'
        extra_kwargs = {
            'partner': {'read_only': True}
        }


class PartnerStatusSerializer(serializers.ModelSerializer):
    """Serializer for partner status information."""
    completed_steps = serializers.ReadOnlyField()
    
    class Meta:
        model = Partner
        fields = ['completed_steps', 'is_verified']
