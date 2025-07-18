from django.core.management.base import BaseCommand
from apps.common.models import Destination, Language, TourType, Timezone


class Command(BaseCommand):
    help = 'Populate database with sample data for common models'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create Destinations
        destinations_data = [
            {'name': 'Mumbai', 'city': 'Mumbai', 'state': 'Maharashtra', 'country': 'India'},
            {'name': 'Delhi', 'city': 'Delhi', 'state': 'Delhi', 'country': 'India'},
            {'name': 'Bangalore', 'city': 'Bangalore', 'state': 'Karnataka', 'country': 'India'},
            {'name': 'Chennai', 'city': 'Chennai', 'state': 'Tamil Nadu', 'country': 'India'},
            {'name': 'Kolkata', 'city': 'Kolkata', 'state': 'West Bengal', 'country': 'India'},
            {'name': 'Hyderabad', 'city': 'Hyderabad', 'state': 'Telangana', 'country': 'India'},
            {'name': 'Pune', 'city': 'Pune', 'state': 'Maharashtra', 'country': 'India'},
            {'name': 'Ahmedabad', 'city': 'Ahmedabad', 'state': 'Gujarat', 'country': 'India'},
            {'name': 'Jaipur', 'city': 'Jaipur', 'state': 'Rajasthan', 'country': 'India'},
            {'name': 'Surat', 'city': 'Surat', 'state': 'Gujarat', 'country': 'India'},
            {'name': 'Goa', 'city': 'Panaji', 'state': 'Goa', 'country': 'India'},
            {'name': 'Kerala', 'city': 'Kochi', 'state': 'Kerala', 'country': 'India'},
            {'name': 'Agra', 'city': 'Agra', 'state': 'Uttar Pradesh', 'country': 'India'},
            {'name': 'Varanasi', 'city': 'Varanasi', 'state': 'Uttar Pradesh', 'country': 'India'},
            {'name': 'Rishikesh', 'city': 'Rishikesh', 'state': 'Uttarakhand', 'country': 'India'},
        ]
        
        for dest_data in destinations_data:
            Destination.objects.get_or_create(**dest_data)
        
        # Create Languages
        languages_data = [
            {'name': 'English', 'code': 'en'},
            {'name': 'Hindi', 'code': 'hi'},
            {'name': 'Tamil', 'code': 'ta'},
            {'name': 'Telugu', 'code': 'te'},
            {'name': 'Bengali', 'code': 'bn'},
            {'name': 'Marathi', 'code': 'mr'},
            {'name': 'Gujarati', 'code': 'gu'},
            {'name': 'Kannada', 'code': 'kn'},
            {'name': 'Malayalam', 'code': 'ml'},
            {'name': 'Punjabi', 'code': 'pa'},
            {'name': 'Urdu', 'code': 'ur'},
            {'name': 'Spanish', 'code': 'es'},
            {'name': 'French', 'code': 'fr'},
            {'name': 'German', 'code': 'de'},
            {'name': 'Chinese', 'code': 'zh'},
        ]
        
        for lang_data in languages_data:
            Language.objects.get_or_create(**lang_data)
        
        # Create Tour Types
        tour_types_data = [
            {'name': 'Adventure', 'description': 'Thrilling outdoor activities and experiences'},
            {'name': 'Cultural', 'description': 'Explore local culture, traditions, and heritage'},
            {'name': 'Wildlife', 'description': 'Safari and wildlife viewing experiences'},
            {'name': 'Beach', 'description': 'Coastal and beach destinations'},
            {'name': 'Mountain', 'description': 'Hill stations and mountain destinations'},
            {'name': 'Religious', 'description': 'Spiritual and religious site visits'},
            {'name': 'Historical', 'description': 'Ancient monuments and historical sites'},
            {'name': 'Luxury', 'description': 'Premium and luxury travel experiences'},
            {'name': 'Budget', 'description': 'Affordable travel options'},
            {'name': 'Family', 'description': 'Family-friendly tours and activities'},
            {'name': 'Honeymoon', 'description': 'Romantic destinations for couples'},
            {'name': 'Group', 'description': 'Large group travel experiences'},
            {'name': 'Solo', 'description': 'Individual traveler experiences'},
            {'name': 'Photography', 'description': 'Photography-focused tours'},
            {'name': 'Food & Culinary', 'description': 'Food tours and culinary experiences'},
        ]
        
        for tour_data in tour_types_data:
            TourType.objects.get_or_create(name=tour_data['name'], defaults=tour_data)
        
        # Create Timezones
        timezones_data = [
            {'name': 'Asia/Kolkata', 'offset': '+05:30'},
            {'name': 'UTC', 'offset': '+00:00'},
            {'name': 'Asia/Dubai', 'offset': '+04:00'},
            {'name': 'Asia/Singapore', 'offset': '+08:00'},
            {'name': 'Europe/London', 'offset': '+00:00'},
            {'name': 'America/New_York', 'offset': '-05:00'},
            {'name': 'America/Los_Angeles', 'offset': '-08:00'},
            {'name': 'Australia/Sydney', 'offset': '+10:00'},
            {'name': 'Asia/Tokyo', 'offset': '+09:00'},
            {'name': 'Europe/Paris', 'offset': '+01:00'},
        ]
        
        for tz_data in timezones_data:
            Timezone.objects.get_or_create(**tz_data)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data for all common models')
        )
