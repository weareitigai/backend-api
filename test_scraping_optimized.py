#!/usr/bin/env python3

import requests
import json
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test URLs with different duration formats
test_urls = [
    "https://www.thomascook.in/india-tour-packages/5-days-4-nights-delhi-agra-jaipur-tour-package",
    "https://www.makemytrip.com/holidays-india/3-days-2-nights-mumbai-package.html",
    "https://www.goibibo.com/holidays/7-days-6-nights-kerala-tour-package",
    "https://www.yatra.com/india-tour-packages/4-days-3-nights-goa-package",
    "https://www.cleartrip.com/holidays/6-days-5-nights-rajasthan-tour"
]

def test_scraping_api():
    """Test the optimized scraping API with various URLs."""
    
    api_url = "http://localhost:8000/api/partner/scrape-tour-details/"
    
    print("🧪 Testing Optimized Tour Scraping API")
    print("=" * 50)
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n📋 Test {i}: {url}")
        print("-" * 40)
        
        try:
            # Make API request
            response = requests.post(
                api_url,
                json={"url": url},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    tour_data = data.get('data', {})
                    
                    print(f"✅ Success!")
                    print(f"📝 Title: {tour_data.get('title', 'N/A')}")
                    print(f"🌍 Destinations: {tour_data.get('destinations', [])}")
                    print(f"📅 Duration Days: {tour_data.get('duration_days', 0)}")
                    print(f"🌙 Duration Nights: {tour_data.get('duration_nights', 0)}")
                    print(f"🏷️ Tour Type: {tour_data.get('tour_type', 'N/A')}")
                    print(f"🏢 Provider: {tour_data.get('provider_name', 'N/A')}")
                    print(f"📞 Contact: {tour_data.get('contact_info', 'N/A')}")
                    
                    # Validate duration data
                    days = tour_data.get('duration_days', 0)
                    nights = tour_data.get('duration_nights', 0)
                    
                    if isinstance(days, int) and isinstance(nights, int):
                        if days >= 0 and nights >= 0:
                            print(f"✅ Duration validation: PASSED")
                        else:
                            print(f"❌ Duration validation: FAILED (negative values)")
                    else:
                        print(f"❌ Duration validation: FAILED (non-integer values)")
                        
                else:
                    print(f"❌ Failed: {data.get('message', 'Unknown error')}")
                    
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request Error: {str(e)}")
        except Exception as e:
            print(f"❌ Unexpected Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🏁 Testing Complete!")

def test_duration_extraction():
    """Test specific duration extraction patterns."""
    
    print("\n🔍 Testing Duration Extraction Patterns")
    print("=" * 50)
    
    # Test patterns
    test_patterns = [
        "5 days 4 nights",
        "3 days 2 nights",
        "7 days 6 nights",
        "4 days 3 nights",
        "6 days 5 nights",
        "3 days tour",
        "5 nights tour",
        "3N/4D",
        "4D/3N",
        "7 days",
        "5 nights"
    ]
    
    import re
    
    duration_patterns = [
        r'(\d+)\s*days?\s*(\d+)\s*nights?',
        r'(\d+)\s*nights?\s*(\d+)\s*days?',
        r'(\d+)\s*day\s*tour',
        r'(\d+)\s*night\s*tour',
        r'(\d+)\s*days?',
        r'(\d+)\s*nights?',
        r'(\d+)[Nn]/(\d+)[Dd]',
        r'(\d+)[Dd]/(\d+)[Nn]'
    ]
    
    for pattern_text in test_patterns:
        print(f"\n📝 Testing: '{pattern_text}'")
        
        duration_days = 0
        duration_nights = 0
        
        for pattern in duration_patterns:
            match = re.search(pattern, pattern_text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    # We have both days and nights
                    if 'day' in pattern.lower() and 'night' in pattern.lower():
                        duration_days = int(match.group(1))
                        duration_nights = int(match.group(2))
                    else:
                        # Handle N/D or D/N format
                        duration_nights = int(match.group(1))
                        duration_days = int(match.group(2))
                else:
                    # We have only one value
                    value = int(match.group(1))
                    if 'day' in pattern.lower():
                        duration_days = value
                        duration_nights = max(0, value - 1)
                    else:
                        duration_nights = value
                        duration_days = value + 1
                break
        
        print(f"   Days: {duration_days}, Nights: {duration_nights}")

if __name__ == "__main__":
    print("🚀 Starting Optimized Scraping Tests")
    
    # Test duration extraction patterns
    test_duration_extraction()
    
    # Test actual API
    test_scraping_api() 