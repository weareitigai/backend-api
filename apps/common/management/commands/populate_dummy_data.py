from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
import random

from apps.authentication.models import User, OTPVerification
from apps.partner.models import Partner, BusinessDetails, LocationCoverage, ToursServices, LegalBanking
from apps.common.models import Destination, Language, TourType, Timezone

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with comprehensive dummy data for all models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create (default: 10)'
        )
        parser.add_argument(
            '--partners',
            type=int,
            default=5,
            help='Number of partners to create (default: 5)'
        )

    def handle(self, *args, **options):
        self.stdout.write('Creating comprehensive dummy data...')
        
        # Create common data first
        self.create_common_data()
        
        # Create users
        users_count = options['users']
        users = self.create_users(users_count)
        
        # Create partners
        partners_count = options['partners']
        self.create_partners(users[:partners_count])
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created dummy data: {users_count} users, {partners_count} partners'
            )
        )

    def create_common_data(self):
        """Create or update common reference data."""
        self.stdout.write('Creating common reference data...')
        
        # Enhanced Destinations
        destinations_data = [
            {'name': 'Mumbai', 'city': 'Mumbai', 'state': 'Maharashtra', 'country': 'India'},
            {'name': 'Delhi', 'city': 'New Delhi', 'state': 'Delhi', 'country': 'India'},
            {'name': 'Bangalore', 'city': 'Bangalore', 'state': 'Karnataka', 'country': 'India'},
            {'name': 'Chennai', 'city': 'Chennai', 'state': 'Tamil Nadu', 'country': 'India'},
            {'name': 'Kolkata', 'city': 'Kolkata', 'state': 'West Bengal', 'country': 'India'},
            {'name': 'Hyderabad', 'city': 'Hyderabad', 'state': 'Telangana', 'country': 'India'},
            {'name': 'Pune', 'city': 'Pune', 'state': 'Maharashtra', 'country': 'India'},
            {'name': 'Ahmedabad', 'city': 'Ahmedabad', 'state': 'Gujarat', 'country': 'India'},
            {'name': 'Jaipur', 'city': 'Jaipur', 'state': 'Rajasthan', 'country': 'India'},
            {'name': 'Goa', 'city': 'Panaji', 'state': 'Goa', 'country': 'India'},
            {'name': 'Kerala Backwaters', 'city': 'Kochi', 'state': 'Kerala', 'country': 'India'},
            {'name': 'Agra', 'city': 'Agra', 'state': 'Uttar Pradesh', 'country': 'India'},
            {'name': 'Varanasi', 'city': 'Varanasi', 'state': 'Uttar Pradesh', 'country': 'India'},
            {'name': 'Rishikesh', 'city': 'Rishikesh', 'state': 'Uttarakhand', 'country': 'India'},
            {'name': 'Shimla', 'city': 'Shimla', 'state': 'Himachal Pradesh', 'country': 'India'},
            {'name': 'Manali', 'city': 'Manali', 'state': 'Himachal Pradesh', 'country': 'India'},
            {'name': 'Udaipur', 'city': 'Udaipur', 'state': 'Rajasthan', 'country': 'India'},
            {'name': 'Jodhpur', 'city': 'Jodhpur', 'state': 'Rajasthan', 'country': 'India'},
            {'name': 'Pushkar', 'city': 'Pushkar', 'state': 'Rajasthan', 'country': 'India'},
            {'name': 'Darjeeling', 'city': 'Darjeeling', 'state': 'West Bengal', 'country': 'India'},
            {'name': 'Gangtok', 'city': 'Gangtok', 'state': 'Sikkim', 'country': 'India'},
            {'name': 'Leh Ladakh', 'city': 'Leh', 'state': 'Jammu and Kashmir', 'country': 'India'},
            {'name': 'Jim Corbett', 'city': 'Ramnagar', 'state': 'Uttarakhand', 'country': 'India'},
            {'name': 'Ranthambore', 'city': 'Sawai Madhopur', 'state': 'Rajasthan', 'country': 'India'},
        ]
        
        for dest_data in destinations_data:
            Destination.objects.get_or_create(**dest_data)
        
        # Languages
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
        
        # Tour Types
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
            {'name': 'Trekking', 'description': 'Hiking and trekking adventures'},
            {'name': 'Wellness', 'description': 'Spa and wellness retreats'},
            {'name': 'Festival', 'description': 'Cultural festival experiences'},
        ]
        
        for tour_data in tour_types_data:
            TourType.objects.get_or_create(name=tour_data['name'], defaults=tour_data)
        
        # Timezones
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

    def create_users(self, count):
        """Create dummy users."""
        self.stdout.write(f'Creating {count} users...')
        
        users = []
        user_data = [
            {'first_name': 'Rajesh', 'last_name': 'Kumar', 'email': 'rajesh.kumar@example.com', 'mobile': '9876543210'},
            {'first_name': 'Priya', 'last_name': 'Sharma', 'email': 'priya.sharma@example.com', 'mobile': '9876543211'},
            {'first_name': 'Amit', 'last_name': 'Patel', 'email': 'amit.patel@example.com', 'mobile': '9876543212'},
            {'first_name': 'Sneha', 'last_name': 'Singh', 'email': 'sneha.singh@example.com', 'mobile': '9876543213'},
            {'first_name': 'Vikram', 'last_name': 'Reddy', 'email': 'vikram.reddy@example.com', 'mobile': '9876543214'},
            {'first_name': 'Kavya', 'last_name': 'Iyer', 'email': 'kavya.iyer@example.com', 'mobile': '9876543215'},
            {'first_name': 'Rohit', 'last_name': 'Gupta', 'email': 'rohit.gupta@example.com', 'mobile': '9876543216'},
            {'first_name': 'Anita', 'last_name': 'Das', 'email': 'anita.das@example.com', 'mobile': '9876543217'},
            {'first_name': 'Suresh', 'last_name': 'Nair', 'email': 'suresh.nair@example.com', 'mobile': '9876543218'},
            {'first_name': 'Meera', 'last_name': 'Joshi', 'email': 'meera.joshi@example.com', 'mobile': '9876543219'},
        ]
        
        for i in range(count):
            if i < len(user_data):
                data = user_data[i]
            else:
                data = {
                    'first_name': f'User{i+1}',
                    'last_name': 'Demo',
                    'email': f'user{i+1}@example.com',
                    'mobile': f'{987654320 + i}'
                }
            
            username = data['email'].split('@')[0]
            user, created = User.objects.get_or_create(
                email=data['email'],
                defaults={
                    'username': username,
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'mobile': data['mobile'],
                    'is_email_verified': True,
                    'is_mobile_verified': True,
                    'is_active': True
                }
            )
            
            if created:
                user.set_password('demo123')
                user.save()
                
            users.append(user)
        
        return users

    def create_partners(self, users):
        """Create partner profiles with complete onboarding data."""
        self.stdout.write(f'Creating {len(users)} partners...')
        
        # Get all reference data
        destinations = list(Destination.objects.all())
        languages = list(Language.objects.all())
        tour_types = list(TourType.objects.all())
        timezones = list(Timezone.objects.all())
        
        business_names = [
            "Incredible India Tours",
            "Heritage Travel Co.",
            "Adventure Seekers",
            "Royal Rajasthan Travels",
            "South India Explorations",
            "Mountain Escape Tours",
            "Cultural Journey India",
            "Luxury Travel Experts",
            "Budget Backpackers",
            "Family Fun Tours"
        ]
        
        provider_types = [
            ["Tour Operator", "Travel Agent"],
            ["Hotel Partner", "Transport Provider"],
            ["Adventure Sports", "Trekking Guide"],
            ["Cultural Guide", "Heritage Expert"],
            ["Wildlife Expert", "Nature Guide"],
        ]
        
        company_types = ["Private Limited", "Partnership", "Proprietorship", "LLP"]
        
        for i, user in enumerate(users):
            # Create Partner
            partner, created = Partner.objects.get_or_create(
                user=user,
                defaults={'is_verified': random.choice([True, False])}
            )
            
            if not created:
                continue
            
            # Create Business Details
            business_name = business_names[i] if i < len(business_names) else f"Travel Business {i+1}"
            BusinessDetails.objects.create(
                partner=partner,
                name=business_name,
                type_of_provider=random.choice(provider_types),
                gstin=f"22AAAAA000A{i:01d}Z{i:01d}" if random.choice([True, False]) else None,
                years=random.randint(1, 15),
                website=f"https://{business_name.lower().replace(' ', '')}.com" if random.choice([True, False]) else None,
                reg_number=f"REG{random.randint(100000, 999999)}",
                city=random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad']),
                state=random.choice(['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'West Bengal', 'Telangana', 'Gujarat']),
                country='India',
                employees=random.randint(1, 50),
                seasonal=random.choice([True, False]),
                annual_bookings=random.randint(50, 1000)
            )
            
            # Create Location Coverage
            primary_location = random.choice(destinations).name
            selected_destinations = random.sample(destinations, random.randint(3, 8))
            selected_languages = random.sample(languages, random.randint(2, 5))
            
            LocationCoverage.objects.create(
                partner=partner,
                primary_location=primary_location,
                destinations=[dest.id for dest in selected_destinations],
                languages=[lang.code for lang in selected_languages],
                regions=random.sample(["North India", "South India", "West India", "East India", "Central India", "Northeast India"], random.randint(2, 4)),
                pan_india=random.choice([True, False]),
                seasons=random.sample(["Spring", "Summer", "Monsoon", "Winter"], random.randint(2, 4)),
                timezone=random.choice(timezones).name
            )
            
            # Create Tours Services
            selected_tour_types = random.sample(tour_types, random.randint(3, 6))
            ToursServices.objects.create(
                partner=partner,
                number_of_tours=random.randint(5, 50),
                types_of_tours=[tour.name for tour in selected_tour_types],
                custom_tour_type="Spiritual Journey" if random.choice([True, False]) else None,
                min_price=Decimal(str(random.randint(1000, 10000))),
                group_size_min=random.randint(1, 5),
                group_size_max=random.randint(10, 50),
                preference="Eco-friendly travel" if random.choice([True, False]) else None,
                offers_custom_tours=random.choice([True, False])
            )
            
            # Create Legal Banking
            LegalBanking.objects.create(
                partner=partner,
                pan_or_aadhaar=f"{'ABCDE1234F' if random.choice([True, False]) else '123456789012'}",
                license_number=f"LIC{random.randint(100000, 999999)}" if random.choice([True, False]) else None,
                company_type=random.choice(company_types),
                emergency_contact=f"987654{random.randint(1000, 9999)}",
                terms_accepted=True
            )
            
            # Create some OTP records for verification history
            if random.choice([True, False]):
                OTPVerification.objects.create(
                    user=user,
                    email=user.email,
                    otp_type='email',
                    otp_code=str(random.randint(100000, 999999)),
                    is_verified=True,
                    expires_at=timezone.now() + timezone.timedelta(minutes=10)
                ) 