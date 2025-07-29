#!/usr/bin/env python3
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/home/yash/office/apiproject')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.partner.scraping_service import TourScrapingService

def test_scraping():
    service = TourScrapingService()
    
    # Test with a sample URL (you can replace this with a real tour URL)
    test_url = "https://example.com"
    
    print("Testing improved scraping service...")
    result = service.extract_tour_details(test_url)
    
    print("Result:")
    print(f"Success: {result.get('success')}")
    if result.get('success'):
        data = result.get('data', {})
        print(f"Title: {data.get('title')}")
        print(f"Contact Info: '{data.get('contact_info')}'")
        print(f"Provider: {data.get('provider_name')}")
        print(f"Tour Type: {data.get('tour_type')}")
        print(f"Destinations: {data.get('destinations')}")
        print(f"Duration Days: {data.get('duration_days')}")
        print(f"Duration Nights: {data.get('duration_nights')}")
    else:
        print(f"Error: {result.get('error')}")

if __name__ == "__main__":
    test_scraping() 