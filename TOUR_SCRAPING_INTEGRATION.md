# Tour Scraping API Integration

This document describes the complete integration of web scraping functionality into your Django Tripsetter application.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install beautifulsoup4==4.12.2 lxml==4.9.3 openai==1.3.7
```

### 2. Environment Variables

Add to your `.env` file:
```bash
OPENAI_API_KEY=your-openai-api-key-here
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Test the API

```bash
python manage.py test_scraping https://example-tour-website.com/tour-package
```

## 📁 Files Added/Modified

### Backend Files

1. **`requirements.txt`** - Added web scraping dependencies
2. **`apps/partner/scraping_service.py`** - Core scraping service
3. **`apps/partner/views.py`** - Added `scrape_tour_details` endpoint
4. **`apps/partner/urls.py`** - Added scraping URL pattern
5. **`apps/partner/serializers.py`** - Added scraping serializers
6. **`config/settings.py`** - Added OpenAI configuration
7. **`apps/partner/management/commands/test_scraping.py`** - Test command

### Frontend Files

1. **`frontend/src/services/api.js`** - Added scraping API calls
2. **`frontend/src/components/TourForm.jsx`** - Tour form with scraping

## 🔗 API Endpoints

### POST `/api/partner/scrape-tour-details/`

**Request:**
```json
{
    "url": "https://example-tour-website.com/tour-package"
}
```

**Response:**
```json
{
    "success": true,
    "data": {
        "title": "Bali Honeymoon Escape - 6N/5D",
        "destinations": ["Bali", "Indonesia"],
        "duration_days": 5,
        "duration_nights": 6,
        "tour_type": "FIT",
        "provider_name": "Tripsetter Tours",
        "contact_info": "+1234567890"
    },
    "message": "Tour details extracted successfully"
}
```

## 🎯 Features

### Smart Data Extraction
- **Tour Title**: Extracts clean, descriptive titles
- **Destinations**: Identifies cities, countries, and regions
- **Duration**: Parses days and nights separately
- **Tour Type**: Classifies as FIT, Group, or Customizable
- **Provider Info**: Extracts brand/company names
- **Contact Details**: Finds phone numbers and emails

### AI Enhancement
- Uses OpenAI GPT for intelligent parsing
- Falls back to rule-based parsing if AI unavailable
- Handles various website formats and structures

### Multi-Platform Support
- TripAdvisor
- Viator
- GetYourGuide
- Booking.com tours
- Custom tour operator websites

## 🔄 Usage Flow

1. **User pastes tour URL** in the form
2. **Clicks "Auto-Fill Tour Details"** button
3. **API scrapes the webpage** and extracts tour information
4. **Form fields are automatically populated** with extracted data
5. **User reviews and edits** the data if needed
6. **Submits the form** to create the tour

## 🛠️ Testing

### Command Line Testing

```bash
# Test scraping with a specific URL
python manage.py test_scraping https://example-tour-website.com/tour-package

# Test the API endpoint
python test_scraping_api.py
```

### Frontend Testing

1. Start the Django server: `python manage.py runserver`
2. Start the frontend: `cd frontend && npm run dev`
3. Navigate to the tour form
4. Paste a tour URL and test the auto-fill functionality

## 🔒 Security & Performance

### Rate Limiting
- Implement rate limiting to prevent abuse
- Add delays between requests for large-scale scraping

### Error Handling
- Graceful fallback when scraping fails
- Detailed error messages for debugging
- Timeout protection for long-running requests

### Authentication
- Requires valid authentication token
- Validates URLs before processing
- Logs scraping attempts for monitoring

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**
   ```bash
   OPENAI_API_KEY=your-production-openai-key
   ```

2. **Rate Limiting**
   ```python
   # Add to settings.py
   RATE_LIMIT_SCRAPING = '100/hour'
   ```

3. **Monitoring**
   ```python
   # Add logging for scraping attempts
   LOGGING = {
       'handlers': {
           'scraping_file': {
               'level': 'INFO',
               'class': 'logging.FileHandler',
               'filename': 'scraping.log',
           },
       },
   }
   ```

## 🎨 Customization

### Adding New Website Support

1. **Update selectors** in `scraping_service.py`
2. **Add domain-specific parsing** logic
3. **Test with sample URLs** from the website

### Enhancing AI Prompts

1. **Modify the prompt** in `_enhance_with_ai()`
2. **Add specific instructions** for your use case
3. **Test with various URL types**

### Custom Data Extraction

1. **Add new fields** to the extraction logic
2. **Update the AI prompt** to include new fields
3. **Modify the frontend form** to display new fields

## 🐛 Troubleshooting

### Common Issues

1. **Scraping fails for certain websites**
   - Some websites block automated requests
   - Solution: Add more user agents or use Selenium

2. **AI enhancement not working**
   - Check if OPENAI_API_KEY is set
   - Falls back to basic parsing automatically

3. **Rate limiting issues**
   - Implement delays between requests
   - Use proxy rotation if needed

### Debug Mode

Enable debug logging:
```python
import logging
logging.getLogger('apps.partner.scraping_service').setLevel(logging.DEBUG)
```

## 📈 Future Enhancements

- **Selenium support** for JavaScript-heavy websites
- **Proxy rotation** for better scraping success
- **More AI models** support for different providers
- **Caching** scraped results to avoid re-scraping
- **Batch processing** for multiple URLs
- **Advanced parsing** for complex tour structures

## 🤝 Contributing

1. **Test thoroughly** with various URLs
2. **Add error handling** for edge cases
3. **Update documentation** for new features
4. **Follow the existing code style**

---

The integration is now complete and ready for production use! The web scraping API will automatically extract tour details from URLs and populate your tour creation form, making it much easier for partners to add their tours to the platform. 