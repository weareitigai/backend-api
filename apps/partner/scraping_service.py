import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urlparse
import logging
from typing import Dict, Any, Optional
from django.conf import settings

logger = logging.getLogger(__name__)

class TourScrapingService:
    """Service for scraping tour details from URLs."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_tour_details(self, url: str) -> Dict[str, Any]:
        """
        Extract tour details from a given URL.
        
        Args:
            url (str): The URL to scrape
            
        Returns:
            Dict[str, Any]: Extracted tour details
        """
        try:
            # Fetch the webpage
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic information
            extracted_data = self._extract_basic_info(soup, url)
            
            # Use AI to enhance and structure the data
            enhanced_data = self._enhance_with_ai(extracted_data, soup.get_text()[:2000])
            
            return enhanced_data
            
        except Exception as e:
            logger.error(f"Error scraping URL {url}: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to scrape URL: {str(e)}',
                'data': {}
            }
    
    def _extract_basic_info(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Extract basic information from the HTML."""
        data = {
            'url': url,
            'title': '',
            'destinations': [],
            'duration': '',
            'tour_type': '',
            'provider_name': '',
            'contact_info': '',
            'price_info': '',
            'description': ''
        }
        
        # Extract title
        title_selectors = [
            'h1', 'h2', '.title', '.tour-title', '[class*="title"]',
            'meta[property="og:title"]', 'meta[name="title"]'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'meta':
                    data['title'] = element.get('content', '')
                else:
                    data['title'] = element.get_text(strip=True)
                if data['title']:
                    break
        
        # Extract description
        desc_selectors = [
            'meta[name="description"]', 'meta[property="og:description"]',
            '.description', '.tour-description', '[class*="description"]'
        ]
        
        for selector in desc_selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'meta':
                    data['description'] = element.get('content', '')
                else:
                    data['description'] = element.get_text(strip=True)
                if data['description']:
                    break
        
        # Extract provider name from domain or page content
        domain = urlparse(url).netloc
        data['provider_name'] = domain.replace('www.', '').split('.')[0].title()
        
        # Look for contact information
        contact_patterns = [
            r'\+?[\d\s\-\(\)]{10,}',  # Phone numbers
            r'[\w\.-]+@[\w\.-]+\.\w+',  # Email addresses
        ]
        
        text_content = soup.get_text()
        for pattern in contact_patterns:
            matches = re.findall(pattern, text_content)
            if matches:
                data['contact_info'] = matches[0]
                break
        
        return data
    
    def _enhance_with_ai(self, extracted_data: Dict[str, Any], page_text: str) -> Dict[str, Any]:
        """Use AI to enhance and structure the extracted data."""
        try:
            # Initialize OpenAI client (you'll need to add OPENAI_API_KEY to settings)
            api_key = getattr(settings, 'OPENAI_API_KEY', None)
            if not api_key:
                return self._fallback_enhancement(extracted_data)
            
            import openai
            client = openai.OpenAI(api_key=api_key)
            
            prompt = f"""
            Extract tour details from the following webpage content and structure them for a tour booking form.
            
            Current extracted data: {json.dumps(extracted_data, indent=2)}
            
            Page content (first 2000 chars): {page_text[:2000]}
            
            Please extract and structure the following information:
            1. Tour Title (clean, descriptive title)
            2. Destinations (list of destinations/cities/countries)
            3. Duration (extract days and nights, format as separate numbers)
            4. Tour Type (FIT, Group, or Customizable)
            5. Provider/Brand Name
            6. Contact Information
            
            Return the data in this JSON format:
            {{
                "title": "Clean tour title",
                "destinations": ["destination1", "destination2"],
                "duration_days": number,
                "duration_nights": number,
                "tour_type": "FIT|Group|Customizable",
                "provider_name": "Provider name",
                "contact_info": "contact details"
            }}
            
            If any information is not available, use null or empty values.
            """
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.3
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Try to parse JSON response
            try:
                ai_data = json.loads(ai_response)
                return {
                    'success': True,
                    'data': ai_data
                }
            except json.JSONDecodeError:
                return self._fallback_enhancement(extracted_data)
                
        except Exception as e:
            logger.error(f"AI enhancement failed: {str(e)}")
            return self._fallback_enhancement(extracted_data)
    
    def _fallback_enhancement(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback enhancement without AI."""
        # Basic parsing and enhancement
        title = extracted_data.get('title', '')
        description = extracted_data.get('description', '')
        
        # Extract destinations from title or description
        destinations = []
        if title:
            # Simple destination extraction
            common_destinations = ['Bali', 'Thailand', 'Singapore', 'Maldives', 'Dubai', 'Europe', 'India', 'Japan', 'Korea', 'Australia', 'New Zealand', 'USA', 'Canada', 'Mexico', 'Brazil', 'Argentina', 'South Africa', 'Egypt', 'Morocco', 'Turkey', 'Greece', 'Italy', 'Spain', 'France', 'Germany', 'Netherlands', 'Belgium', 'Switzerland', 'Austria', 'Czech Republic', 'Poland', 'Hungary', 'Romania', 'Bulgaria', 'Croatia', 'Slovenia', 'Slovakia', 'Lithuania', 'Latvia', 'Estonia', 'Finland', 'Sweden', 'Norway', 'Denmark', 'Iceland', 'Ireland', 'UK', 'Portugal', 'Malta', 'Cyprus', 'Iceland']
            for dest in common_destinations:
                if dest.lower() in title.lower() or dest.lower() in description.lower():
                    destinations.append(dest)
        
        # Extract duration
        duration_days = 0
        duration_nights = 0
        duration_match = re.search(r'(\d+)[Nn]/(\d+)[Dd]', title + ' ' + description)
        if duration_match:
            duration_nights = int(duration_match.group(1))
            duration_days = int(duration_match.group(2))
        
        # Determine tour type
        tour_type = 'FIT'
        if 'group' in title.lower() or 'group' in description.lower():
            tour_type = 'Group'
        elif 'custom' in title.lower() or 'custom' in description.lower():
            tour_type = 'Customizable'
        
        return {
            'success': True,
            'data': {
                'title': title or 'Tour Package',
                'destinations': destinations,
                'duration_days': duration_days,
                'duration_nights': duration_nights,
                'tour_type': tour_type,
                'provider_name': extracted_data.get('provider_name', ''),
                'contact_info': extracted_data.get('contact_info', '')
            }
        } 