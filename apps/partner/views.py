from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Partner, BusinessDetails, LocationCoverage, ToursServices, LegalBanking
from .serializers import (
    BusinessDetailsSerializer, LocationCoverageSerializer,
    ToursServicesSerializer, LegalBankingSerializer, PartnerStatusSerializer
)


def get_or_create_partner(user):
    """Get or create partner for user."""
    partner, created = Partner.objects.get_or_create(user=user)
    return partner


@extend_schema(
    request=BusinessDetailsSerializer,
    responses={200: {'type': 'object', 'properties': {'success': {'type': 'boolean'}, 'message': {'type': 'string'}, 'data': BusinessDetailsSerializer}}}
)
@api_view(['GET', 'PATCH'])
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
    
    elif request.method == 'PATCH':
        try:
            business_details = partner.business_details
            serializer = BusinessDetailsSerializer(business_details, data=request.data, partial=True)
        except BusinessDetails.DoesNotExist:
            serializer = BusinessDetailsSerializer(data=request.data)
        
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
    responses={200: {'type': 'object', 'properties': {'success': {'type': 'boolean'}, 'message': {'type': 'string'}, 'data': LocationCoverageSerializer}}}
)
@api_view(['GET', 'PATCH'])
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
    
    elif request.method == 'PATCH':
        try:
            location_coverage = partner.location_coverage
            serializer = LocationCoverageSerializer(location_coverage, data=request.data, partial=True)
        except LocationCoverage.DoesNotExist:
            serializer = LocationCoverageSerializer(data=request.data)
        
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
    responses={200: {'type': 'object', 'properties': {'success': {'type': 'boolean'}, 'message': {'type': 'string'}, 'data': ToursServicesSerializer}}}
)
@api_view(['GET', 'PATCH'])
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
    
    elif request.method == 'PATCH':
        try:
            tours_services = partner.tours_services
            serializer = ToursServicesSerializer(tours_services, data=request.data, partial=True)
        except ToursServices.DoesNotExist:
            serializer = ToursServicesSerializer(data=request.data)
        
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
    responses={200: {'type': 'object', 'properties': {'success': {'type': 'boolean'}, 'message': {'type': 'string'}, 'data': LegalBankingSerializer}}}
)
@api_view(['GET', 'PATCH'])
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
    
    elif request.method == 'PATCH':
        try:
            legal_banking = partner.legal_banking
            serializer = LegalBankingSerializer(legal_banking, data=request.data, partial=True)
        except LegalBanking.DoesNotExist:
            serializer = LegalBankingSerializer(data=request.data)
        
        if serializer.is_valid():
            legal_banking = serializer.save(partner=partner)
            return Response({
                'success': True,
                'message': 'Legal and banking information updated successfully'
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
