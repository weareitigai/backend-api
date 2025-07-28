from django.core.management.base import BaseCommand
from apps.partner.scraping_service import TourScrapingService
import json

class Command(BaseCommand):
    help = 'Test the tour scraping functionality'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='URL to scrape')

    def handle(self, *args, **options):
        url = options['url']
        
        self.stdout.write(f"Testing scraping for URL: {url}")
        
        # Initialize scraping service
        scraping_service = TourScrapingService()
        
        # Extract tour details
        result = scraping_service.extract_tour_details(url)
        
        if result.get('success'):
            self.stdout.write(
                self.style.SUCCESS('✅ Scraping successful!')
            )
            self.stdout.write(
                f"Extracted data:\n{json.dumps(result['data'], indent=2)}"
            )
        else:
            self.stdout.write(
                self.style.ERROR(f"❌ Scraping failed: {result.get('error')}")
            ) 