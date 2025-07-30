from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from .models import Destination, Language, TourType, Timezone
from .serializers import (
    DestinationSerializer, LanguageSerializer,
    TourTypeSerializer, TimezoneSerializer, DestinationResponseSerializer
)

# Create response serializers for drf-spectacular
class GenericListResponseSerializer(serializers.Serializer):
    results = serializers.ListField(child=serializers.CharField())


@extend_schema(
    parameters=[
        {
            'name': 'search',
            'in': 'query',
            'description': 'Search term for destination names',
            'required': False,
            'schema': {'type': 'string', 'format': 'string'}
        }
    ],
    responses={200: DestinationResponseSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def destinations_view(request):
    """Autocomplete for destinations."""
    search = request.GET.get('search', '')
    
    queryset = Destination.objects.filter(is_active=True)
    
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(city__icontains=search) |
            Q(state__icontains=search) |
            Q(country__icontains=search)
        )
    
    # Limit results for autocomplete
    queryset = queryset[:20]
    
    serializer = DestinationSerializer(queryset, many=True)
    return Response({
        'results': serializer.data
    }, status=status.HTTP_200_OK)


@extend_schema(
    responses={200: GenericListResponseSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def languages_view(request):
    """Fetch available language options."""
    languages = Language.objects.filter(is_active=True).values_list('name', flat=True)
    
    return Response({
        'results': list(languages)
    }, status=status.HTTP_200_OK)


@extend_schema(
    responses={200: GenericListResponseSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def tour_types_view(request):
    """Fetch all tour types."""
    tour_types = TourType.objects.filter(is_active=True).values_list('name', flat=True)
    
    return Response({
        'results': list(tour_types)
    }, status=status.HTTP_200_OK)


@extend_schema(
    responses={200: GenericListResponseSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def timezones_view(request):
    """Fetch timezone list."""
    timezones = Timezone.objects.filter(is_active=True).values_list('name', flat=True)
    
    return Response({
        'results': list(timezones)
    }, status=status.HTTP_200_OK)
