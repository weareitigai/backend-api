#!/usr/bin/env python3
"""
Test script for the tour scraping API.
"""

import requests
import json
import os

def test_scraping_api():
    """Test the tour scraping API endpoint."""
    
    # API endpoint
    api_url = "http://localhost:8000/api/partner/scrape-tour-details/"
    
    # Test URLs
    test_urls = [
        "https://www.tripadvisor.com/Attraction_Review-g297701-d1234567-Reviews-Bali_Tour-Bali.html",
        "https://www.viator.com/Bali-attractions/Bali-Tour/d461-a12345",
        "https://www.getyourguide.com/bali-l196/bali-tour-t12345"
    ]
    
    # You'll need to get a valid token from your authentication system
    # For testing, you can create a token manually or use the admin interface
    token = "YOUR_AUTH_TOKEN_HERE"  # Replace with actual token
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {token}'
    }
    
    for url in test_urls:
        print(f"\nTesting URL: {url}")
        
        payload = {
            'url': url
        }
        
        try:
            response = requests.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Success!")
                print(f"Extracted data: {json.dumps(result['data'], indent=2)}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    test_scraping_api() 