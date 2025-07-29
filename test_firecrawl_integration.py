#!/usr/bin/env python3
import os
import sys
import django
import logging

# Add the project directory to Python path
sys.path.append('/home/yash/office/apiproject')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

from apps.partner.scraping_service import TourScrapingService

def test_firecrawl_integration():
    service = TourScrapingService()
    
    # Test URLs - you can replace these with actual tour URLs
    test_urls = [
        "https://www.sotc.in/holiday-packages/india-holidays",
        "https://www.makemytrip.com/holidays-india/",
        "https://www.goibibo.com/holidays/",
        "https://example.com",  # Fallback for testing
    ]
    
    for i, test_url in enumerate(test_urls, 1):
        print(f"\n{'=' * 80}")
        print(f"TESTING FIRECRAWL INTEGRATION - URL #{i}: {test_url}")
        print(f"{'=' * 80}")
        
        try:
            result = service.extract_tour_details(test_url)
            
            print(f"\n{'=' * 80}")
            print(f"RESULT FOR URL #{i}")
            print(f"{'=' * 80}")
            print(f"Success: {result.get('success')}")
            if result.get('success'):
                data = result.get('data', {})
                print(f"Title: '{data.get('title')}'")
                print(f"Destinations: {data.get('destinations')}")
                print(f"Duration Days: {data.get('duration_days')}")
                print(f"Duration Nights: {data.get('duration_nights')}")
                print(f"Tour Type: {data.get('tour_type')}")
                print(f"Provider: {data.get('provider_name')}")
                print(f"Contact Info: '{data.get('contact_info')}'")
                print(f"Price Info: '{data.get('price_info')}'")
                print(f"Description: '{data.get('description')[:100]}...'")
                
                # If we get a successful result with good data, we can stop testing
                if data.get('title') and data.get('destinations'):
                    print(f"\n✅ SUCCESS! Found good data from URL #{i}")
                    break
            else:
                print(f"Error: {result.get('error')}")
                
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
    
    print(f"\n{'=' * 80}")
    print("FIRECRAWL INTEGRATION TESTING COMPLETE")
    print(f"{'=' * 80}")

if __name__ == "__main__":
    test_firecrawl_integration() 