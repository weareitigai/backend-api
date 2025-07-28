import time
import logging
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import Partner, BusinessDetails, LocationCoverage, ToursServices, LegalBanking, Tour
from .serializers import (
    BusinessDetailsSerializer, BusinessDetailsResponseSerializer,
    LocationCoverageSerializer, LocationCoverageResponseSerializer,
    ToursServicesSerializer, ToursServicesResponseSerializer,
    LegalBankingSerializer, LegalBankingResponseSerializer,
    PartnerStatusSerializer, TourScrapingRequestSerializer, TourScrapingResponseSerializer, TourSerializer
)
from .utils import optimize_file_upload, log_performance_metric
from .scraping_service import TourScrapingService

# Set up logging
logger = logging.getLogger(__name__)


def get_or_create_partner(user):
    """Get or create partner for user."""
    partner, created = Partner.objects.get_or_create(user=user)
    return partner


def get_partner_by_user_id(user_id):
    """Get partner by user ID."""
    try:
        return Partner.objects.get(user_id=user_id)
    except Partner.DoesNotExist:
        return None


def get_verified_partner_by_user_id(user_id):
    """Get verified partner by user ID."""
    try:
        return Partner.objects.get(user_id=user_id, is_verified=True)
    except Partner.DoesNotExist:
        return None


@extend_schema(
    request=BusinessDetailsSerializer,
    responses={200: BusinessDetailsResponseSerializer}
)
@api_view(['GET', 'POST', 'PATCH'])
@permission_classes([IsAuthenticated])
def business_details_view(request):
    """Get or update business details."""
    user_id = request.query_params.get('user_id')
    if user_id:
        partner = get_partner_by_user_id(user_id)
        if not partner:
            return Response({'success': False, 'message': 'Partner for user_id not found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
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
        # Create or update business details (upsert behavior)
        try:
            # Try to get existing business details
            business_details = partner.business_details
            # If exists, update it
            serializer = BusinessDetailsSerializer(business_details, data=request.data, partial=True)
            if serializer.is_valid():
                business_details = serializer.save(partner=partner)
                return Response({
                    'success': True,
                    'message': 'Business details updated successfully'
                }, status=status.HTTP_200_OK)
        except BusinessDetails.DoesNotExist:
            # If doesn't exist, create new record
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
    user_id = request.query_params.get('user_id')
    if user_id:
        partner = get_partner_by_user_id(user_id)
        if not partner:
            return Response({'success': False, 'message': 'Partner for user_id not found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
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
        # Create or update location coverage (upsert behavior)
        try:
            # Try to get existing location coverage
            location_coverage = partner.location_coverage
            # If exists, update it
            serializer = LocationCoverageSerializer(location_coverage, data=request.data, partial=True)
            if serializer.is_valid():
                location_coverage = serializer.save(partner=partner)
                return Response({
                    'success': True,
                    'message': 'Location coverage updated successfully'
                }, status=status.HTTP_200_OK)
        except LocationCoverage.DoesNotExist:
            # If doesn't exist, create new record
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
                'message': 'Location coverage updated successfully'
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
    user_id = request.query_params.get('user_id')
    if user_id:
        partner = get_partner_by_user_id(user_id)
        if not partner:
            return Response({'success': False, 'message': 'Partner for user_id not found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
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
        # Create or update tours services (upsert behavior)
        try:
            # Try to get existing tours services
            tours_services = partner.tours_services
            # If exists, update it
            serializer = ToursServicesSerializer(tours_services, data=request.data, partial=True)
            if serializer.is_valid():
                tours_services = serializer.save(partner=partner)
                return Response({
                    'success': True,
                    'message': 'Tours and services updated successfully'
                }, status=status.HTTP_200_OK)
        except ToursServices.DoesNotExist:
            # If doesn't exist, create new record
            serializer = ToursServicesSerializer(data=request.data)
            if serializer.is_valid():
                tours_services = serializer.save(partner=partner)
                return Response({
                    'success': True,
                    'message': 'Tours and services created successfully'
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
                'message': 'Tours and services not found. Use POST to create first.'
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
    start_time = time.time()
    
    user_id = request.query_params.get('user_id')
    if user_id:
        partner = get_partner_by_user_id(user_id)
        if not partner:
            return Response({'success': False, 'message': 'Partner for user_id not found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        partner = get_or_create_partner(request.user)
    
    if request.method == 'GET':
        try:
            legal_banking = partner.legal_banking
            serializer = LegalBankingSerializer(legal_banking)
            
            # Log performance
            duration = time.time() - start_time
            log_performance_metric("Legal banking GET", duration)
            
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
        # Create or update legal banking (upsert behavior)
        try:
            # Handle file uploads efficiently
            data = request.data.copy()
            
            # Process file uploads if present
            if 'panOrAadhaarFile' in request.FILES:
                file_obj = request.FILES['panOrAadhaarFile']
                try:
                    optimized_path = optimize_file_upload(file_obj, partner.user.id, 'pan_aadhaar_docs')
                    data['pan_or_aadhaar_file'] = optimized_path
                except Exception as e:
                    logger.error(f"PAN/Aadhaar file upload error: {str(e)}")
                    return Response({
                        'success': False,
                        'message': f'File upload failed: {str(e)}'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            if 'businessProofFile' in request.FILES:
                file_obj = request.FILES['businessProofFile']
                try:
                    optimized_path = optimize_file_upload(file_obj, partner.user.id, 'business_proofs')
                    data['business_proof_file'] = optimized_path
                except Exception as e:
                    logger.error(f"Business proof file upload error: {str(e)}")
                    return Response({
                        'success': False,
                        'message': f'File upload failed: {str(e)}'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Try to get existing legal banking
            try:
                legal_banking = partner.legal_banking
                # If exists, update it
                serializer = LegalBankingSerializer(legal_banking, data=data, partial=True)
                if serializer.is_valid():
                    legal_banking = serializer.save(partner=partner)
                    
                    # Log performance
                    duration = time.time() - start_time
                    log_performance_metric("Legal banking POST (update)", duration)
                    
                    return Response({
                        'success': True,
                        'message': 'Legal banking details updated successfully'
                    }, status=status.HTTP_200_OK)
            except LegalBanking.DoesNotExist:
                # If doesn't exist, create new record
                serializer = LegalBankingSerializer(data=data)
                if serializer.is_valid():
                    legal_banking = serializer.save(partner=partner)
                    
                    # Log performance
                    duration = time.time() - start_time
                    log_performance_metric("Legal banking POST (create)", duration)
                    
                    return Response({
                        'success': True,
                        'message': 'Legal banking details created successfully'
                    }, status=status.HTTP_201_CREATED)
            
            return Response({
                'success': False,
                'message': 'Invalid data provided',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Legal banking POST error: {str(e)}")
            return Response({
                'success': False,
                'message': f'An error occurred: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'PATCH':
        # Update existing legal banking
        try:
            legal_banking = partner.legal_banking
            
            # Handle file uploads efficiently
            data = request.data.copy()
            
            # Process file uploads if present
            if 'panOrAadhaarFile' in request.FILES:
                file_obj = request.FILES['panOrAadhaarFile']
                try:
                    optimized_path = optimize_file_upload(file_obj, partner.user.id, 'pan_aadhaar_docs')
                    data['pan_or_aadhaar_file'] = optimized_path
                except Exception as e:
                    logger.error(f"PAN/Aadhaar file upload error: {str(e)}")
                    return Response({
                        'success': False,
                        'message': f'File upload failed: {str(e)}'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            if 'businessProofFile' in request.FILES:
                file_obj = request.FILES['businessProofFile']
                try:
                    optimized_path = optimize_file_upload(file_obj, partner.user.id, 'business_proofs')
                    data['business_proof_file'] = optimized_path
                except Exception as e:
                    logger.error(f"Business proof file upload error: {str(e)}")
                    return Response({
                        'success': False,
                        'message': f'File upload failed: {str(e)}'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = LegalBankingSerializer(legal_banking, data=data, partial=True)
        except LegalBanking.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Legal banking details not found. Use POST to create first.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if serializer.is_valid():
            legal_banking = serializer.save(partner=partner)
            
            # Log performance
            duration = time.time() - start_time
            log_performance_metric("Legal banking PATCH", duration)
            
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
    user_id = request.query_params.get('user_id')
    if user_id:
        partner = get_partner_by_user_id(user_id)
        if not partner:
            return Response({'success': False, 'message': 'Partner for user_id not found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
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
        partner.status = 'in-process'
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


@api_view(['POST', 'PATCH'])
@permission_classes([IsAuthenticated])
def create_or_update_tour(request, user_id):
    """Create a new tour (POST) or update an existing tour (PATCH) for a verified partner."""
    partner = get_verified_partner_by_user_id(user_id)
    if not partner:
        return Response({'success': False, 'message': 'Partner not found or not verified.'}, status=403)
    if request.method == 'POST':
        serializer = TourSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(partner=partner)
            return Response({'success': True, 'data': serializer.data}, status=201)
        return Response({'success': False, 'errors': serializer.errors}, status=400)
    elif request.method == 'PATCH':
        tour_id = request.data.get('id')
        if not tour_id:
            return Response({'success': False, 'message': 'Tour id is required for update.'}, status=400)
        try:
            tour = Tour.objects.get(id=tour_id, partner=partner)
        except Tour.DoesNotExist:
            return Response({'success': False, 'message': 'Tour not found.'}, status=404)
        serializer = TourSerializer(tour, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=200)
        return Response({'success': False, 'errors': serializer.errors}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_tours(request, user_id):
    """Get all tours for a verified partner."""
    partner = get_verified_partner_by_user_id(user_id)
    if not partner:
        return Response({'success': False, 'message': 'Partner not found or not verified.'}, status=403)
    tours = Tour.objects.filter(partner=partner)
    serializer = TourSerializer(tours, many=True)
    return Response({'success': True, 'data': serializer.data}, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tour_details(request, user_id, tour_id):
    """Get details of a specific tour for a verified partner."""
    partner = get_verified_partner_by_user_id(user_id)
    if not partner:
        return Response({'success': False, 'message': 'Partner not found or not verified.'}, status=403)
    try:
        tour = Tour.objects.get(id=tour_id, partner=partner)
    except Tour.DoesNotExist:
        return Response({'success': False, 'message': 'Tour not found.'}, status=404)
    serializer = TourSerializer(tour)
    return Response({'success': True, 'data': serializer.data}, status=200)


@extend_schema(
    request=TourScrapingRequestSerializer,
    responses={200: TourScrapingResponseSerializer}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def scrape_tour_details(request):
    """Scrape tour details from a URL."""
    url = request.data.get('url')
    
    if not url:
        return Response({
            'success': False,
            'message': 'URL is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate URL format
    if not url.startswith(('http://', 'https://')):
        return Response({
            'success': False,
            'message': 'Invalid URL format. Please provide a complete URL starting with http:// or https://'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Initialize scraping service
        scraping_service = TourScrapingService()
        
        # Extract tour details
        result = scraping_service.extract_tour_details(url)
        
        if result.get('success'):
            return Response({
                'success': True,
                'data': result['data'],
                'message': 'Tour details extracted successfully'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': result.get('error', 'Failed to extract tour details'),
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'success': False,
            'message': f'An error occurred while scraping: {str(e)}',
            'data': {}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
