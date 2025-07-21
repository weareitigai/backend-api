from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Partner, BusinessDetails, LocationCoverage, ToursServices, LegalBanking
from .serializers import (
    BusinessDetailsSerializer, LocationCoverageSerializer,
    ToursServicesSerializer, LegalBankingSerializer, PartnerStatusSerializer,
    BusinessDetailsResponseSerializer, LocationCoverageResponseSerializer,
    ToursServicesResponseSerializer, LegalBankingResponseSerializer
)


def get_or_create_partner(user):
    """Get or create partner for user."""
    partner, created = Partner.objects.get_or_create(user=user)
    return partner


@extend_schema(
    request=BusinessDetailsSerializer,
    responses={200: BusinessDetailsResponseSerializer}
)
@api_view(['GET', 'POST', 'PATCH'])
@permission_classes([IsAuthenticated])
def business_details_view(request):
    """Get or update business details."""
    partner = get_or_create_partner(request.user)
    
    if request.method == 'GET':
        try:
            business_details = partner.business_details
            serializer = BusinessDetailsSerializer(business_details)
            return Response({
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except BusinessDetails.DoesNotExist:
            return Response({
                'success': True,
                'data': {}
            }, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # Create new business details (first time)
        try:
            # Check if already exists
            partner.business_details
            return Response({
                'success': False,
                'message': 'Business details already exist. Use PATCH to update.'
            }, status=status.HTTP_400_BAD_REQUEST)
        except BusinessDetails.DoesNotExist:
            # Create new record
            serializer = BusinessDetailsSerializer(data=request.data)
            if serializer.is_valid():
                business_details = serializer.save(partner=partner)
                return Response({
                    'success': True,
                    'message': 'Business details created successfully'
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                'success': False,
                'message': 'Invalid data provided',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        # Update existing business details
        try:
            business_details = partner.business_details
            serializer = BusinessDetailsSerializer(business_details, data=request.data, partial=True)
        except BusinessDetails.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Business details not found. Use POST to create first.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if serializer.is_valid():
            business_details = serializer.save(partner=partner)
            return Response({
                'success': True,
                'message': 'Business details updated successfully'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'message': 'Invalid data provided',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=LocationCoverageSerializer,
    responses={200: LocationCoverageResponseSerializer}
)
@api_view(['GET', 'POST', 'PATCH'])
@permission_classes([IsAuthenticated])
def location_coverage_view(request):
    """Get or update location and coverage information."""
    partner = get_or_create_partner(request.user)
    
    if request.method == 'GET':
        try:
            location_coverage = partner.location_coverage
            serializer = LocationCoverageSerializer(location_coverage)
            return Response({
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except LocationCoverage.DoesNotExist:
            return Response({
                'success': True,
                'data': {}
            }, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # Create new location coverage (first time)
        try:
            # Check if already exists
            partner.location_coverage
            return Response({
                'success': False,
                'message': 'Location coverage already exists. Use PATCH to update.'
            }, status=status.HTTP_400_BAD_REQUEST)
        except LocationCoverage.DoesNotExist:
            # Create new record
            serializer = LocationCoverageSerializer(data=request.data)
            if serializer.is_valid():
                location_coverage = serializer.save(partner=partner)
                return Response({
                    'success': True,
                    'message': 'Location coverage created successfully'
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                'success': False,
                'message': 'Invalid data provided',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        # Update existing location coverage
        try:
            location_coverage = partner.location_coverage
            serializer = LocationCoverageSerializer(location_coverage, data=request.data, partial=True)
        except LocationCoverage.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Location coverage not found. Use POST to create first.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if serializer.is_valid():
            location_coverage = serializer.save(partner=partner)
            return Response({
                'success': True,
                'message': 'Location and coverage updated successfully'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'message': 'Invalid data provided',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=ToursServicesSerializer,
    responses={200: ToursServicesResponseSerializer}
)
@api_view(['GET', 'POST', 'PATCH'])
@permission_classes([IsAuthenticated])
def tours_services_view(request):
    """Get or update tours and services information."""
    partner = get_or_create_partner(request.user)
    
    if request.method == 'GET':
        try:
            tours_services = partner.tours_services
            serializer = ToursServicesSerializer(tours_services)
            return Response({
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except ToursServices.DoesNotExist:
            return Response({
                'success': True,
                'data': {}
            }, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # Create new tours services (first time)
        try:
            # Check if already exists
            partner.tours_services
            return Response({
                'success': False,
                'message': 'Tours services already exist. Use PATCH to update.'
            }, status=status.HTTP_400_BAD_REQUEST)
        except ToursServices.DoesNotExist:
            # Create new record
            serializer = ToursServicesSerializer(data=request.data)
            if serializer.is_valid():
                tours_services = serializer.save(partner=partner)
                return Response({
                    'success': True,
                    'message': 'Tours services created successfully'
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                'success': False,
                'message': 'Invalid data provided',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        # Update existing tours services
        try:
            tours_services = partner.tours_services
            serializer = ToursServicesSerializer(tours_services, data=request.data, partial=True)
        except ToursServices.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Tours services not found. Use POST to create first.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if serializer.is_valid():
            tours_services = serializer.save(partner=partner)
            return Response({
                'success': True,
                'message': 'Tours and services updated successfully'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'message': 'Invalid data provided',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=LegalBankingSerializer,
    responses={200: LegalBankingResponseSerializer}
)
@api_view(['GET', 'POST', 'PATCH'])
@permission_classes([IsAuthenticated])
def legal_banking_view(request):
    """Get or update legal and banking information."""
    partner = get_or_create_partner(request.user)
    
    if request.method == 'GET':
        try:
            legal_banking = partner.legal_banking
            serializer = LegalBankingSerializer(legal_banking)
            return Response({
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except LegalBanking.DoesNotExist:
            return Response({
                'success': True,
                'data': {}
            }, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # Create new legal banking (first time)
        try:
            # Check if already exists
            partner.legal_banking
            return Response({
                'success': False,
                'message': 'Legal banking details already exist. Use PATCH to update.'
            }, status=status.HTTP_400_BAD_REQUEST)
        except LegalBanking.DoesNotExist:
            # Create new record
            serializer = LegalBankingSerializer(data=request.data)
            if serializer.is_valid():
                legal_banking = serializer.save(partner=partner)
                return Response({
                    'success': True,
                    'message': 'Legal banking details created successfully'
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                'success': False,
                'message': 'Invalid data provided',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        # Update existing legal banking
        try:
            legal_banking = partner.legal_banking
            serializer = LegalBankingSerializer(legal_banking, data=request.data, partial=True)
        except LegalBanking.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Legal banking details not found. Use POST to create first.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if serializer.is_valid():
            legal_banking = serializer.save(partner=partner)
            return Response({
                'success': True,
                'message': 'Legal and banking details updated successfully'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'message': 'Invalid data provided',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={200: PartnerStatusSerializer}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_partner_status(request):
    """Get step completion status."""
    partner = get_or_create_partner(request.user)
    serializer = PartnerStatusSerializer(partner)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    responses={200: {'type': 'object', 'properties': {'success': {'type': 'boolean'}, 'message': {'type': 'string'}}}}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_onboarding(request):
    """Mark profile as complete."""
    partner = get_or_create_partner(request.user)
    
    # Check if all steps are completed
    completed_steps = partner.completed_steps
    if len(completed_steps) >= 4:  # All 4 steps completed
        partner.is_verified = True
        partner.save()
        return Response({
            'success': True,
            'message': 'Onboarding completed successfully'
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'success': False,
            'message': 'Please complete all onboarding steps first'
        }, status=status.HTTP_400_BAD_REQUEST)
