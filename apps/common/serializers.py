from rest_framework import serializers
from .models import Destination, Language, TourType, Timezone


class DestinationSerializer(serializers.ModelSerializer):
    """Serializer for destinations."""
    
    class Meta:
        model = Destination
        fields = ['id', 'name', 'country', 'state', 'city']


class LanguageSerializer(serializers.ModelSerializer):
    """Serializer for languages."""
    
    class Meta:
        model = Language
        fields = ['id', 'name', 'code']


class TourTypeSerializer(serializers.ModelSerializer):
    """Serializer for tour types."""
    
    class Meta:
        model = TourType
        fields = ['id', 'name', 'description']


class TimezoneSerializer(serializers.ModelSerializer):
    """Serializer for timezones."""
    
    class Meta:
        model = Timezone
        fields = ['id', 'name', 'offset']


class DestinationResponseSerializer(serializers.Serializer):
    """Serializer for destination autocomplete response."""
    results = DestinationSerializer(many=True)
