import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urlparse
import logging
from typing import Dict, Any, Optional
from django.conf import settings
from firecrawl import FirecrawlApp
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class TourExtractionSchema(BaseModel):
    """Schema for extracting tour details from web pages."""
    tourLink: str
    title: str
    destinations: list[str]
    durationDays: int
    durationNights: int
    tourType: str  # "FIT", "Group", or "Customizable"
    providerName: str
    contactLink: str = ""
    tourStatus: str = "Live"
    categories: list[str] = []
    tags: list[str] = []
    summary: str = ""
    highlights: list[str] = []
    startingPrice: float = 0.0
    priceType: str = "Starting From"
    departureCities: list[str] = []
    tourStartLocation: str = ""
    tourDropLocation: str = ""
    departureMonths: list[str] = []
    includesFlights: bool = False
    includesHotels: bool = False
    includesMeals: bool = False
    includesTransfers: bool = False
    visaSupport: bool = False
    offersType: list[str] = []
    discountDetails: str = ""
    promotionalTagline: str = ""

class TourScrapingService:
    """Service for scraping tour details from URLs."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_tour_details(self, url: str) -> Dict[str, Any]:
        """
        Extract tour details from a given URL using Firecrawl.
        
        Args:
            url (str): The URL to scrape
            
        Returns:
            Dict[str, Any]: Extracted tour details
        """
        try:
            logger.info(f"Starting tour extraction for URL: {url}")
            
            # Get Firecrawl API key
            firecrawl_api_key = getattr(settings, 'FIRECRAWL_API_KEY', None)
            if not firecrawl_api_key:
                logger.warning("No Firecrawl API key found, falling back to manual scraping")
                return self._manual_scraping_fallback(url)
            
            # Initialize Firecrawl
            logger.info("Initializing Firecrawl...")
            app = FirecrawlApp(api_key=firecrawl_api_key)
            
            # Scrape with Firecrawl
            logger.info("Scraping with Firecrawl...")
            scrape_result = app.scrape_url(
                url,
                formats=["markdown"],
                only_main_content=False,
                timeout=120000
            )
            
            if not scrape_result.success:
                logger.error(f"Firecrawl scraping failed: {scrape_result.error}")
                return self._manual_scraping_fallback(url)
            
            # Extract the markdown data
            if hasattr(scrape_result, 'markdown') and scrape_result.markdown:
                logger.info("Successfully extracted markdown data with Firecrawl")
                markdown_content = scrape_result.markdown
                
                # Use AI to extract structured data from markdown
                extracted_data = self._extract_from_markdown_with_ai(markdown_content, url)
                
                if extracted_data:
                    # Clean and validate the data
                    cleaned_data = self._clean_extracted_data(extracted_data)
                    
                    return {
                        'success': True,
                        'data': cleaned_data,
                        'message': 'Tour details extracted successfully using Firecrawl + AI'
                    }
                else:
                    logger.warning("AI extraction failed, falling back to manual scraping")
                    return self._manual_scraping_fallback(url)
            else:
                logger.warning("No markdown data found in Firecrawl response, falling back to manual scraping")
                return self._manual_scraping_fallback(url)
                
        except Exception as e:
            logger.error(f"Error in Firecrawl extraction: {str(e)}")
            return self._manual_scraping_fallback(url)
    
    def _extract_from_markdown_with_ai(self, markdown_content: str, url: str) -> Dict[str, Any]:
        """Extract structured tour data from markdown content using AI."""
        try:
            logger.info("Extracting structured data from markdown using AI...")
            
            # Get AI API key
            openai_api_key = getattr(settings, 'OPENAI_API_KEY', None)
            gemini_api_key = getattr(settings, 'GEMINI_API_KEY', None)
            
            if openai_api_key:
                return self._extract_with_openai(markdown_content, url, openai_api_key)
            elif gemini_api_key:
                return self._extract_with_gemini(markdown_content, url, gemini_api_key)
            else:
                logger.warning("No AI API keys available for markdown extraction")
                return None
                
        except Exception as e:
            logger.error(f"Error extracting from markdown with AI: {str(e)}")
            return None
    
    def _extract_with_openai(self, markdown_content: str, url: str, api_key: str) -> Dict[str, Any]:
        """Extract tour data from markdown using OpenAI."""
        try:
            import openai
            # Create a fresh OpenAI client without any session interference
            client = openai.OpenAI(
                api_key=api_key,
                # Explicitly avoid any session configuration
            )
            
            prompt = f"""
            Extract tour details from the following markdown content and return them as a JSON object.
            
            Markdown content:
            {markdown_content[:4000]}
            
            URL: {url}
            
            Please extract and return the following information in JSON format:
            {{
                "tourLink": "{url}",
                "title": "Tour title",
                "destinations": ["destination1", "destination2"],
                "durationDays": number,
                "durationNights": number,
                "tourType": "FIT|Group|Customizable",
                "providerName": "Provider name",
                "contactLink": "Contact URL or empty string",
                "tourStatus": "Live|Draft|Coming Soon",
                "categories": ["category1", "category2"],
                "tags": ["tag1", "tag2"],
                "summary": "Brief tour description",
                "highlights": ["highlight1", "highlight2"],
                "startingPrice": price_in_decimal,
                "priceType": "Starting From|Fixed",
                "departureCities": ["city1", "city2"],
                "tourStartLocation": "Starting location",
                "tourDropLocation": "Ending location",
                "departureMonths": ["January", "February"],
                "includesFlights": true/false,
                "includesHotels": true/false,
                "includesMeals": true/false,
                "includesTransfers": true/false,
                "visaSupport": true/false,
                "offersType": ["Early Bird Offer", "Group Discount"],
                "discountDetails": "Discount description",
                "promotionalTagline": "Promotional message"
            }}
            
            CRITICAL INSTRUCTIONS FOR DURATION EXTRACTION:
            - Look for patterns like "X days Y nights", "X days", "Y nights", "X day tour", "Y night tour"
            - Extract ONLY numeric values for durationDays and durationNights
            - If you find "X days Y nights", set durationDays = X and durationNights = Y
            - If you find only "X days" without nights, set durationDays = X and durationNights = X-1
            - If you find only "Y nights" without days, set durationDays = Y+1 and durationNights = Y
            - If no duration found, set both to 0
            - NEVER return non-numeric values for duration fields
            
            TOUR TYPE MAPPING:
            - "FIT" or "FIT Tour" → "FIT"
            - "Group" or "Group Tour" → "Group"
            - "Custom" or "Customizable" → "Customizable"
            - Default: "FIT"
            
            IMPORTANT RULES:
            - For destinations, only include actual city/destination names
            - For duration, extract numeric values for days and nights
            - For contactLink, include URLs or contact information
            - If any information is not available, use empty strings, empty arrays, or 0 for numbers
            - Ensure all duration values are integers
            - For price, extract numeric values only (e.g., 25000.00)
            """
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
                temperature=0.1
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Try to parse JSON response
            try:
                import json
                extracted_data = json.loads(ai_response)
                logger.info("Successfully extracted data with OpenAI")
                return extracted_data
            except json.JSONDecodeError:
                logger.error("Failed to parse OpenAI JSON response")
                return None
                
        except Exception as e:
            logger.error(f"OpenAI extraction failed: {str(e)}")
            return None
    
    def _extract_with_gemini(self, markdown_content: str, url: str, api_key: str) -> Dict[str, Any]:
        """Extract tour data from markdown using Gemini."""
        try:
            import google.generativeai as genai
            
            # Configure Gemini
            genai.configure(api_key=api_key)
            
            prompt = f"""
            Extract tour details from the following markdown content and return them as a JSON object.
            
            Markdown content:
            {markdown_content[:4000]}
            
            URL: {url}
            
            Please extract and return the following information in JSON format:
            {{
                "tourLink": "{url}",
                "title": "Tour title",
                "destinations": ["destination1", "destination2"],
                "durationDays": number,
                "durationNights": number,
                "tourType": "FIT|Group|Customizable",
                "providerName": "Provider name",
                "contactLink": "Contact URL or empty string",
                "tourStatus": "Live|Draft|Coming Soon",
                "categories": ["category1", "category2"],
                "tags": ["tag1", "tag2"],
                "summary": "Brief tour description",
                "highlights": ["highlight1", "highlight2"],
                "startingPrice": price_in_decimal,
                "priceType": "Starting From|Fixed",
                "departureCities": ["city1", "city2"],
                "tourStartLocation": "Starting location",
                "tourDropLocation": "Ending location",
                "departureMonths": ["January", "February"],
                "includesFlights": true/false,
                "includesHotels": true/false,
                "includesMeals": true/false,
                "includesTransfers": true/false,
                "visaSupport": true/false,
                "offersType": ["Early Bird Offer", "Group Discount"],
                "discountDetails": "Discount description",
                "promotionalTagline": "Promotional message"
            }}
            
            CRITICAL INSTRUCTIONS FOR DURATION EXTRACTION:
            - Look for patterns like "X days Y nights", "X days", "Y nights", "X day tour", "Y night tour"
            - Extract ONLY numeric values for durationDays and durationNights
            - If you find "X days Y nights", set durationDays = X and durationNights = Y
            - If you find only "X days" without nights, set durationDays = X and durationNights = X-1
            - If you find only "Y nights" without days, set durationDays = Y+1 and durationNights = Y
            - If no duration found, set both to 0
            - NEVER return non-numeric values for duration fields
            
            TOUR TYPE MAPPING:
            - "FIT" or "FIT Tour" → "FIT"
            - "Group" or "Group Tour" → "Group"
            - "Custom" or "Customizable" → "Customizable"
            - Default: "FIT"
            
            IMPORTANT RULES:
            - For destinations, only include actual city/destination names
            - For duration, extract numeric values for days and nights
            - For contactLink, include URLs or contact information
            - If any information is not available, use empty strings, empty arrays, or 0 for numbers
            - Ensure all duration values are integers
            - For price, extract numeric values only (e.g., 25000.00)
            """
            
            # Generate content using Gemini
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            response = model.generate_content(prompt)
            
            ai_response = response.text.strip()
            
            # Try to parse JSON response
            try:
                import json
                extracted_data = json.loads(ai_response)
                logger.info("Successfully extracted data with Gemini")
                return extracted_data
            except json.JSONDecodeError:
                logger.error("Failed to parse Gemini JSON response")
                return None
                
        except Exception as e:
            logger.error(f"Gemini extraction failed: {str(e)}")
            return None
    
    def _manual_scraping_fallback(self, url: str) -> Dict[str, Any]:
        """Fallback to manual scraping when Firecrawl is not available."""
        try:
            logger.info("Using manual scraping fallback...")
            
            # Fetch the webpage
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic information
            extracted_data = self._extract_basic_info(soup, url)
            
            # Use AI to enhance and structure the data
            enhanced_data = self._enhance_with_ai(extracted_data, soup.get_text()[:3000])
            
            # Clean and validate the data to ensure all comprehensive fields are present
            if enhanced_data and 'data' in enhanced_data:
                enhanced_data['data'] = self._clean_extracted_data(enhanced_data['data'])
            
            return enhanced_data
            
        except Exception as e:
            logger.error(f"Error in manual scraping fallback: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to scrape URL: {str(e)}',
                'data': {}
            }
    
    def _clean_extracted_data(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and validate extracted data from AI extraction."""
        try:
            # Convert to dict if it's a Pydantic model
            if hasattr(extracted_data, 'dict'):
                data = extracted_data.dict()
            else:
                data = extracted_data
            
            # Clean destinations
            if 'destinations' in data and isinstance(data['destinations'], list):
                cleaned_destinations = []
                for dest in data['destinations']:
                    if isinstance(dest, str) and dest.strip():
                        clean_dest = re.sub(r'\s+', ' ', dest.strip())
                        if clean_dest and len(clean_dest) > 2:
                            cleaned_destinations.append(clean_dest)
                data['destinations'] = cleaned_destinations
            
            # Clean contact link
            if 'contactLink' in data and data['contactLink']:
                contact_link = re.sub(r'\s+', ' ', data['contactLink'].strip())
                data['contactLink'] = contact_link
            
            # Enhanced duration validation and cleaning
            data = self._validate_and_clean_duration(data)
            
            # Set defaults for missing fields according to new schema
            data.setdefault('tourLink', '')
            data.setdefault('title', '')
            data.setdefault('destinations', [])
            data.setdefault('durationDays', 0)
            data.setdefault('durationNights', 0)
            data.setdefault('tourType', 'FIT')
            data.setdefault('providerName', '')
            data.setdefault('contactLink', '')
            data.setdefault('tourStatus', 'Live')
            data.setdefault('categories', [])
            data.setdefault('tags', [])
            data.setdefault('summary', '')
            data.setdefault('highlights', [])
            data.setdefault('startingPrice', 0.0)
            data.setdefault('priceType', 'Starting From')
            data.setdefault('departureCities', [])
            data.setdefault('tourStartLocation', '')
            data.setdefault('tourDropLocation', '')
            data.setdefault('departureMonths', [])
            data.setdefault('includesFlights', False)
            data.setdefault('includesHotels', False)
            data.setdefault('includesMeals', False)
            data.setdefault('includesTransfers', False)
            data.setdefault('visaSupport', False)
            data.setdefault('offersType', [])
            data.setdefault('discountDetails', '')
            data.setdefault('promotionalTagline', '')
            
            return data
            
        except Exception as e:
            logger.error(f"Error cleaning extracted data: {str(e)}")
            return {
                'tourLink': '',
                'title': '',
                'destinations': [],
                'durationDays': 0,
                'durationNights': 0,
                'tourType': 'FIT',
                'providerName': '',
                'contactLink': '',
                'tourStatus': 'Live',
                'categories': [],
                'tags': [],
                'summary': '',
                'highlights': [],
                'startingPrice': 0.0,
                'priceType': 'Starting From',
                'departureCities': [],
                'tourStartLocation': '',
                'tourDropLocation': '',
                'departureMonths': [],
                'includesFlights': False,
                'includesHotels': False,
                'includesMeals': False,
                'includesTransfers': False,
                'visaSupport': False,
                'offersType': [],
                'discountDetails': '',
                'promotionalTagline': ''
            }
    
    def _validate_and_clean_duration(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced duration validation and cleaning."""
        try:
            # Handle durationDays
            if 'durationDays' in data:
                duration_days = data['durationDays']
                if isinstance(duration_days, str):
                    # Extract numeric value from string
                    days_match = re.search(r'(\d+)', str(duration_days))
                    if days_match:
                        data['durationDays'] = int(days_match.group(1))
                    else:
                        data['durationDays'] = 0
                elif isinstance(duration_days, (int, float)):
                    data['durationDays'] = int(duration_days)
                else:
                    data['durationDays'] = 0
            else:
                data['durationDays'] = 0
            
            # Handle durationNights
            if 'durationNights' in data:
                duration_nights = data['durationNights']
                if isinstance(duration_nights, str):
                    # Extract numeric value from string
                    nights_match = re.search(r'(\d+)', str(duration_nights))
                    if nights_match:
                        data['durationNights'] = int(nights_match.group(1))
                    else:
                        data['durationNights'] = 0
                elif isinstance(duration_nights, (int, float)):
                    data['durationNights'] = int(duration_nights)
                else:
                    data['durationNights'] = 0
            else:
                data['durationNights'] = 0
            
            # Additional validation logic
            if data['durationDays'] < 0:
                data['durationDays'] = 0
            if data['durationNights'] < 0:
                data['durationNights'] = 0
            
            # If we have days but no nights, calculate nights
            if data['durationDays'] > 0 and data['durationNights'] == 0:
                data['durationNights'] = max(0, data['durationDays'] - 1)
            
            # If we have nights but no days, calculate days
            if data['durationNights'] > 0 and data['durationDays'] == 0:
                data['durationDays'] = data['durationNights'] + 1
            
            return data
            
        except Exception as e:
            logger.error(f"Error validating duration: {str(e)}")
            data['durationDays'] = 0
            data['durationNights'] = 0
            return data
    
    def _extract_basic_info(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Extract basic information from the HTML."""
        data = {
            'tourLink': url,
            'title': '',
            'destinations': [],
            'durationDays': 0,
            'durationNights': 0,
            'tourType': 'FIT',
            'providerName': '',
            'contactLink': '',
            'startingPrice': 0.0,
            'priceType': 'Starting From',
            'summary': ''
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
                    data['summary'] = element.get('content', '')
                else:
                    data['summary'] = element.get_text(strip=True)
                if data['summary']:
                    break
        
        # Extract provider name from domain or page content
        domain = urlparse(url).netloc
        data['providerName'] = domain.replace('www.', '').split('.')[0].title()
        
        # Enhanced duration extraction from page content
        text_content = soup.get_text()
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
        
        for pattern in duration_patterns:
            match = re.search(pattern, text_content, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    # We have both days and nights
                    if 'day' in pattern.lower() and 'night' in pattern.lower():
                        data['durationDays'] = int(match.group(1))
                        data['durationNights'] = int(match.group(2))
                    else:
                        # Handle N/D or D/N format
                        data['durationNights'] = int(match.group(1))
                        data['durationDays'] = int(match.group(2))
                else:
                    # We have only one value
                    value = int(match.group(1))
                    if 'day' in pattern.lower():
                        data['durationDays'] = value
                        data['durationNights'] = max(0, value - 1)
                    else:
                        data['durationNights'] = value
                        data['durationDays'] = value + 1
                break
        
        # Look for contact information
        contact_patterns = [
            r'\+?[\d\s\-\(\)]{10,}',  # Phone numbers
            r'[\w\.-]+@[\w\.-]+\.\w+',  # Email addresses
        ]
        
        # Get text content and clean it
        text_content = soup.get_text()
        contact_info_parts = []
        
        # Extract phone numbers
        phone_matches = re.findall(r'\+?[\d\s\-\(\)]{10,}', text_content)
        if phone_matches:
            # Clean and format phone numbers
            for phone in phone_matches[:2]:  # Limit to first 2 phone numbers
                cleaned_phone = re.sub(r'\s+', ' ', phone.strip())
                if cleaned_phone and len(cleaned_phone) >= 10:
                    contact_info_parts.append(cleaned_phone)
        
        # Extract email addresses
        email_matches = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text_content)
        if email_matches:
            for email in email_matches[:2]:  # Limit to first 2 emails
                cleaned_email = email.strip()
                if cleaned_email:
                    contact_info_parts.append(cleaned_email)
        
        # Also look for contact information in specific elements
        contact_selectors = [
            '.contact', '.contact-info', '.phone', '.email', '.address',
            '[class*="contact"]', '[class*="phone"]', '[class*="email"]',
            '[class*="address"]', '.footer', '.header', '.contact-details',
            '[id*="contact"]', '[id*="phone"]', '[id*="email"]'
        ]
        
        for selector in contact_selectors:
            elements = soup.select(selector)
            for element in elements:
                element_text = element.get_text(strip=True)
                if element_text and len(element_text) > 5:
                    # Check if it contains contact info
                    if any(char.isdigit() for char in element_text) or '@' in element_text:
                        # Clean the text
                        cleaned_text = re.sub(r'\s+', ' ', element_text.strip())
                        if cleaned_text and len(cleaned_text) > 5:
                            contact_info_parts.append(cleaned_text)
        
        # Also check for contact info in links (tel: and mailto:)
        contact_links = soup.find_all('a', href=True)
        for link in contact_links:
            href = link.get('href', '')
            if href.startswith('tel:') or href.startswith('mailto:'):
                link_text = link.get_text(strip=True)
                if link_text:
                    contact_info_parts.append(link_text)
        
        # Combine all contact information
        if contact_info_parts:
            data['contactLink'] = ' | '.join(contact_info_parts[:3])  # Limit to 3 items
        else:
            data['contactLink'] = ''
        
        return data
    
    def _enhance_with_ai(self, extracted_data: Dict[str, Any], page_text: str) -> Dict[str, Any]:
        """Use AI to enhance and structure the extracted data."""
        try:
            # Try OpenAI first, then Gemini as fallback
            openai_api_key = getattr(settings, 'OPENAI_API_KEY', None)
            gemini_api_key = getattr(settings, 'GEMINI_API_KEY', None)
            
            if openai_api_key:
                return self._enhance_with_openai(extracted_data, page_text, openai_api_key)
            elif gemini_api_key:
                return self._enhance_with_gemini(extracted_data, page_text, gemini_api_key)
            else:
                return self._fallback_enhancement(extracted_data)
                
        except Exception as e:
            logger.error(f"AI enhancement failed: {str(e)}")
            return self._fallback_enhancement(extracted_data)
    
    def _enhance_with_openai(self, extracted_data: Dict[str, Any], page_text: str, api_key: str) -> Dict[str, Any]:
        """Use OpenAI to enhance and structure the extracted data."""
        try:
            import openai
            # Create a fresh OpenAI client without any session interference
            client = openai.OpenAI(
                api_key=api_key,
                # Explicitly avoid any session configuration
            )
            
            prompt = f"""
            Extract tour details from the following webpage content and structure them for a tour booking form.
            
            Current extracted data: {json.dumps(extracted_data, indent=2)}
            
            Page content (first 3000 chars): {page_text[:3000]}
            
            Please extract and structure the following information:
            1. Tour Title (clean, descriptive title)
            2. Destinations (list of destinations/cities/countries)
            3. Duration (extract days and nights, format as separate numbers)
            4. Tour Type (FIT, Group, or Customizable)
            5. Provider/Brand Name
            6. Contact Information (clean phone numbers, emails, addresses - remove extra whitespace and newlines)
            
            CRITICAL DURATION EXTRACTION RULES:
            - Look for patterns like "X days Y nights", "X days", "Y nights", "X day tour", "Y night tour"
            - Extract ONLY numeric values for durationDays and durationNights
            - If you find "X days Y nights", set durationDays = X and durationNights = Y
            - If you find only "X days" without nights, set durationDays = X and durationNights = X-1
            - If you find only "Y nights" without days, set durationDays = Y+1 and durationNights = Y
            - If no duration found, set both to 0
            - NEVER return non-numeric values for duration fields
            
            TOUR TYPE MAPPING:
            - "FIT" or "FIT Tour" → "FIT"
            - "Group" or "Group Tour" → "Group"
            - "Custom" or "Customizable" → "Customizable"
            - Default: "FIT"
            
            Return the data in this JSON format:
            {{
                "title": "Clean tour title",
                "destinations": ["destination1", "destination2"],
                "durationDays": number,
                "durationNights": number,
                "tourType": "FIT|Group|Customizable",
                "providerName": "Provider name",
                "contactLink": "clean contact details without extra whitespace"
            }}
            
            Important: For contactLink, clean up any extra whitespace, newlines, or formatting issues. 
            If contactLink contains only whitespace or newlines, set it to empty string.
            If any information is not available, use null or empty values.
            """
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.1
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Try to parse JSON response
            try:
                ai_data = json.loads(ai_response)
                
                # Clean contactLink if it exists
                if 'contactLink' in ai_data and ai_data['contactLink']:
                    contact_link = ai_data['contactLink']
                    # Remove extra whitespace and newlines
                    contact_link = re.sub(r'\s+', ' ', contact_link.strip())
                    if contact_link == '' or contact_link.isspace():
                        contact_link = ''
                    ai_data['contactLink'] = contact_link
                
                # Validate and clean duration data
                ai_data = self._validate_and_clean_duration(ai_data)
                
                return {
                    'success': True,
                    'data': ai_data
                }
            except json.JSONDecodeError:
                return self._fallback_enhancement(extracted_data)
                
        except Exception as e:
            logger.error(f"OpenAI enhancement failed: {str(e)}")
            return self._fallback_enhancement(extracted_data)
    
    def _enhance_with_gemini(self, extracted_data: Dict[str, Any], page_text: str, api_key: str) -> Dict[str, Any]:
        """Use Google Gemini to enhance and structure the extracted data."""
        try:
            import google.generativeai as genai
            
            # Configure Gemini
            genai.configure(api_key=api_key)
            
            prompt = f"""
            Extract tour details from the following webpage content and structure them for a tour booking form.
            
            Current extracted data: {json.dumps(extracted_data, indent=2)}
            
            Page content (first 3000 chars): {page_text[:3000]}
            
            Please extract and structure the following information:
            1. Tour Title (clean, descriptive title)
            2. Destinations (list of destinations/cities/countries)
            3. Duration (extract days and nights, format as separate numbers)
            4. Tour Type (Fast Traffic Immigration, Group Tour, or Customizable Tour)
            5. Provider/Brand Name
            6. Contact Information (clean phone numbers, emails, addresses - remove extra whitespace and newlines)
            
            CRITICAL DURATION EXTRACTION RULES:
            - Look for patterns like "X days Y nights", "X days", "Y nights", "X day tour", "Y night tour"
            - Extract ONLY numeric values for durationDays and durationNights
            - If you find "X days Y nights", set durationDays = X and durationNights = Y
            - If you find only "X days" without nights, set durationDays = X and durationNights = X-1
            - If you find only "Y nights" without days, set durationDays = Y+1 and durationNights = Y
            - If no duration found, set both to 0
            - NEVER return non-numeric values for duration fields
            
            TOUR TYPE MAPPING:
            - "FIT" or "FIT Tour" → "FIT"
            - "Group" or "Group Tour" → "Group"
            - "Custom" or "Customizable" → "Customizable"
            - Default: "FIT"
            
            Return the data in this JSON format:
            {{
                "title": "Clean tour title",
                "destinations": ["destination1", "destination2"],
                "durationDays": number,
                "durationNights": number,
                "tourType": "FIT|Group|Customizable",
                "providerName": "Provider name",
                "contactLink": "clean contact details without extra whitespace"
            }}
            
            Important: For contactLink, clean up any extra whitespace, newlines, or formatting issues. 
            If contactLink contains only whitespace or newlines, set it to empty string.
            If any information is not available, use null or empty values.
            """
            
            # Generate content using Gemini
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            response = model.generate_content(prompt)
            
            ai_response = response.text.strip()
            
            # Try to parse JSON response
            try:
                ai_data = json.loads(ai_response)
                
                # Clean contactLink if it exists
                if 'contactLink' in ai_data and ai_data['contactLink']:
                    contact_link = ai_data['contactLink']
                    # Remove extra whitespace and newlines
                    contact_link = re.sub(r'\s+', ' ', contact_link.strip())
                    if contact_link == '' or contact_link.isspace():
                        contact_link = ''
                    ai_data['contactLink'] = contact_link
                
                # Validate and clean duration data
                ai_data = self._validate_and_clean_duration(ai_data)
                
                return {
                    'success': True,
                    'data': ai_data
                }
            except json.JSONDecodeError:
                return self._fallback_enhancement(extracted_data)
                
        except Exception as e:
            logger.error(f"Gemini enhancement failed: {str(e)}")
            return self._fallback_enhancement(extracted_data)
    
    def _fallback_enhancement(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback enhancement without AI."""
        # Basic parsing and enhancement
        title = extracted_data.get('title', '')
        summary = extracted_data.get('summary', '')
        
        # Extract destinations from title or summary
        destinations = []
        if title:
            # Simple destination extraction
            common_destinations = ['Bali', 'Thailand', 'Singapore', 'Maldives', 'Dubai', 'Europe', 'India', 'Japan', 'Korea', 'Australia', 'New Zealand', 'USA', 'Canada', 'Mexico', 'Brazil', 'Argentina', 'South Africa', 'Egypt', 'Morocco', 'Turkey', 'Greece', 'Italy', 'Spain', 'France', 'Germany', 'Netherlands', 'Belgium', 'Switzerland', 'Austria', 'Czech Republic', 'Poland', 'Hungary', 'Romania', 'Bulgaria', 'Croatia', 'Slovenia', 'Slovakia', 'Lithuania', 'Latvia', 'Estonia', 'Finland', 'Sweden', 'Norway', 'Denmark', 'Iceland', 'Ireland', 'UK', 'Portugal', 'Malta', 'Cyprus', 'Iceland']
            for dest in common_destinations:
                if dest.lower() in title.lower() or dest.lower() in summary.lower():
                    destinations.append(dest)
        
        # Enhanced duration extraction
        durationDays = 0
        durationNights = 0
        
        # Look for duration patterns in title and summary
        duration_text = title + ' ' + summary
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
        
        for pattern in duration_patterns:
            match = re.search(pattern, duration_text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    # We have both days and nights
                    if 'day' in pattern.lower() and 'night' in pattern.lower():
                        durationDays = int(match.group(1))
                        durationNights = int(match.group(2))
                    else:
                        # Handle N/D or D/N format
                        durationNights = int(match.group(1))
                        durationDays = int(match.group(2))
                else:
                    # We have only one value
                    value = int(match.group(1))
                    if 'day' in pattern.lower():
                        durationDays = value
                        durationNights = max(0, value - 1)
                    else:
                        durationNights = value
                        durationDays = value + 1
                break
        
        # Determine tour type
        tourType = 'FIT' # Changed default
        if 'group' in title.lower() or 'group' in summary.lower():
            tourType = 'Group'
        elif 'custom' in title.lower() or 'custom' in summary.lower():
            tourType = 'Customizable'
        
        # Clean contact info
        contactLink = extracted_data.get('contactLink', '')
        if contactLink:
            # Remove extra whitespace and newlines
            contactLink = re.sub(r'\s+', ' ', contactLink.strip())
            if contactLink == '' or contactLink.isspace():
                contactLink = ''
        
        # Create the basic data structure
        basic_data = {
            'title': title or 'Tour Package',
            'destinations': destinations,
            'durationDays': durationDays,
            'durationNights': durationNights,
            'tourType': tourType,
            'providerName': extracted_data.get('providerName', ''),
            'contactLink': contactLink
        }
        
        # Clean and add all comprehensive fields
        cleaned_data = self._clean_extracted_data(basic_data)
        
        return {
            'success': True,
            'data': cleaned_data
        } 