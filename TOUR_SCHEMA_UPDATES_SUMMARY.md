# Tour Schema Updates Summary

## Overview

This document summarizes all the changes made to update the tour scraping and API functionality according to the new schema provided in the chat conversation.

## Changes Made

### 1. Updated Tour Extraction Schema (`apps/partner/scraping_service.py`)

**File:** `apps/partner/scraping_service.py`

**Changes:**
- Updated `TourExtractionSchema` class to match the new schema format
- Changed field names from snake_case to camelCase:
  - `duration_days` → `durationDays`
  - `duration_nights` → `durationNights`
  - `tour_type` → `tourType`
  - `provider_name` → `providerName`
  - `contact_info` → `contactLink`
- Added new fields:
  - `tourLink`: URL of the tour
  - `tourStatus`: Status of the tour (Live, Draft, Coming Soon)
  - `categories`: Array of categories
  - `tags`: Array of tags/keywords
  - `summary`: Tour summary
  - `highlights`: Array of tour highlights
  - `startingPrice`: Starting price
  - `priceType`: Price type (Starting From, Fixed)
  - `departureCities`: Array of departure cities
  - `tourStartLocation`: Tour start location
  - `tourDropLocation`: Tour drop location
  - `departureMonths`: Array of departure months
  - `includesFlights`: Boolean for flight inclusion
  - `includesHotels`: Boolean for hotel inclusion
  - `includesMeals`: Boolean for meal inclusion
  - `includesTransfers`: Boolean for transfer inclusion
  - `visaSupport`: Boolean for visa support
  - `offersType`: Array of offer types
  - `discountDetails`: Discount details
  - `promotionalTagline`: Promotional tagline

### 2. Updated AI Extraction Prompts

**File:** `apps/partner/scraping_service.py`

**Changes:**
- Updated OpenAI extraction prompt to return data in the new schema format
- Updated Gemini extraction prompt to return data in the new schema format
- Changed tour type mapping:
  - "FIT" or "FIT Tour" → "FIT"
  - "Group" or "Group Tour" → "Group"
  - "Custom" or "Customizable" → "Customizable"
- Updated field names in prompts to match new schema

### 3. Updated Data Cleaning Methods

**File:** `apps/partner/scraping_service.py`

**Changes:**
- Updated `_clean_extracted_data()` method to handle new schema fields
- Updated `_validate_and_clean_duration()` method to use new field names
- Added default values for all new fields
- Updated error handling to return data in new schema format

### 4. Updated Serializers

**File:** `apps/partner/serializers.py`

**Changes:**
- Updated `TourScrapingDataSerializer` to include `tourStatus` field
- All existing serializers already supported the new schema format
- No changes needed to `TourCreateSerializer`, `TourUpdateSerializer`, etc.

### 5. Updated API Documentation

**File:** `TOUR_API_DOCUMENTATION.md`

**Changes:**
- Completely rewrote the documentation to reflect the new schema
- Added comprehensive examples using the new schema format
- Updated all request/response examples
- Added detailed field descriptions
- Added usage examples and cURL commands
- Added error handling documentation

## New Schema Format

The updated schema now includes all fields from the example provided in the chat:

```json
{
  "tourLink": "https://www.kesari.in/tourIti/Group-Tours/Himachal/H3/SPECTACULAR-SHIMLA-MANALI",
  "title": "Spectacular Shimla Manali Tour",
  "destinations": ["Shimla", "Manali"],
  "durationDays": 10,
  "durationNights": 9,
  "tourType": "Group",
  "providerName": "Kesari Tours",
  "contactLink": "https://littleniqqa.com",
  "tourStatus": "Live",
  "categories": ["Adventure Tours", "Mountain Tours", "Group Tours"],
  "tags": ["shimla", "manali", "himachal", "mountains", "adventure"],
  "summary": "Experience the beauty of Shimla and Manali with this comprehensive 10-day tour package",
  "highlights": [
    "Visit Shimla's famous Mall Road",
    "Explore Manali's scenic beauty",
    "Adventure activities in Solang Valley",
    "Visit Hadimba Temple",
    "Shopping at local markets"
  ],
  "startingPrice": 25000.00,
  "priceType": "Starting From",
  "departureCities": ["Mumbai", "Delhi", "Bangalore"],
  "tourStartLocation": "Shimla",
  "tourDropLocation": "Manali",
  "departureMonths": ["March", "April", "May", "June", "September", "October"],
  "includesFlights": true,
  "includesHotels": true,
  "includesMeals": true,
  "includesTransfers": true,
  "visaSupport": false,
  "offersType": ["Early Bird Offer", "Group Discount"],
  "discountDetails": "Get 10% off on bookings made 30 days in advance",
  "promotionalTagline": "Discover the magic of Himachal Pradesh"
}
```

## API Endpoints

The following endpoints have been updated to work with the new schema:

1. **POST** `/api/partner/scrape-tour-details/` - Scrapes tour details from URL
2. **POST** `/api/partner/user/{user_id}/tours/create/` - Creates a new tour
3. **POST** `/api/partner/user/{user_id}/tours/create-from-scraped/` - Creates tour from scraped data
4. **GET** `/api/partner/user/{user_id}/tours/` - Gets all tours
5. **GET** `/api/partner/user/{user_id}/tours/{tour_id}/` - Gets tour details
6. **PATCH** `/api/partner/user/{user_id}/tours/{tour_id}/update/` - Updates tour

## Frontend Integration

The frontend API service (`frontend/src/services/api.js`) already supports the new schema:

```javascript
// Scrape tour details
const scrapeTour = async (url) => {
  const response = await partnerAPI.scrapeTourDetails(url);
  return response.data;
};

// Create tour
const createTour = async (userId, tourData) => {
  const response = await partnerAPI.createTour(userId, tourData);
  return response.data;
};
```

## Key Improvements

1. **Comprehensive Data Structure**: The new schema includes all necessary fields for a complete tour description
2. **Better AI Extraction**: Updated prompts ensure more accurate data extraction from web pages
3. **Consistent Field Naming**: All fields use camelCase for consistency
4. **Enhanced Validation**: Better data cleaning and validation for all fields
5. **Complete Documentation**: Comprehensive API documentation with examples

## Testing

To test the updated functionality:

1. **Test Scraping:**
   ```bash
   curl -X POST http://localhost:8000/api/partner/scrape-tour-details/ \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.kesari.in/tourIti/Group-Tours/Himachal/H3/SPECTACULAR-SHIMLA-MANALI"}'
   ```

2. **Test Tour Creation:**
   ```bash
   curl -X POST http://localhost:8000/api/partner/user/1/tours/create/ \
     -H "Authorization: Token your_token_here" \
     -H "Content-Type: application/json" \
     -d '{
       "tourLink": "https://www.kesari.in/tourIti/Group-Tours/Himachal/H3/SPECTACULAR-SHIMLA-MANALI",
       "title": "Spectacular Shimla Manali Tour",
       "destinations": ["Shimla", "Manali"],
       "durationDays": 10,
       "durationNights": 9,
       "tourType": "Group",
       "providerName": "Kesari Tours",
       "startingPrice": 25000.00,
       "priceType": "Starting From"
     }'
   ```

## Notes

- The scraping accuracy depends on the website structure and AI model performance
- Manual verification of scraped data is recommended
- All endpoints maintain backward compatibility where possible
- The new schema provides a more comprehensive tour data structure
- Error handling has been improved for better debugging

## Files Modified

1. `apps/partner/scraping_service.py` - Updated schema and extraction logic
2. `apps/partner/serializers.py` - Updated TourScrapingDataSerializer
3. `TOUR_API_DOCUMENTATION.md` - Complete documentation rewrite
4. `TOUR_SCHEMA_UPDATES_SUMMARY.md` - This summary document

## Next Steps

1. Test the scraping functionality with various tour websites
2. Verify the tour creation API with the new schema
3. Update frontend forms to handle all new fields
4. Add validation for new fields in the frontend
5. Consider adding more AI models for better extraction accuracy 