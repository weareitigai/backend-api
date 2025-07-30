# Tour API Documentation

## Tour Creation Workflow

### Two-Step Process (Recommended)

#### Step 1: Scrape Tour Details
**Endpoint:** `POST /partner/scrape-tour-details/`
**Description:** Scrape tour details from a URL and return the extracted data for frontend editing
**Authentication:** Not required (public endpoint)

**Request:**
```json
{
  "url": "https://example.com/tour-page"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Tour details extracted successfully",
  "data": {
    "tourLink": "https://example.com/tour-page",
    "title": "Amazing Tour Title",
    "destinations": ["Mumbai", "Goa"],
    "durationDays": 5,
    "durationNights": 4,
    "tourType": "FIT",
    "providerName": "Travel Agency",
    "startingPrice": 15000.00,
    "priceType": "Starting From",
    "departureCities": ["Delhi", "Mumbai"],
    "tourStartLocation": "Delhi",
    "tourDropLocation": "Mumbai",
    "departureMonths": ["January", "February", "March"],
    "tourStatus": "Live",
    "categories": ["Adventure", "Beach"],
    "tags": ["adventure", "beach", "vacation"],
    "summary": "Amazing 5-day adventure tour",
    "highlights": ["Beach activities", "Water sports", "Local cuisine"],
    "includesFlights": true,
    "includesHotels": true,
    "includesMeals": true,
    "includesTransfers": true,
    "visaSupport": false,
    "offersType": ["Early Bird", "Group Discount"],
    "discountDetails": "10% off for early booking",
    "promotionalTagline": "Book now and save!"
  },
  "request_data": {
    "url": "https://example.com/tour-page"
  }
}
```

#### Step 2: Create Tour with Edited Data
**Endpoint:** `POST /partner/user/<user_id>/tours/create/`
**Description:** Create a new tour with the edited scraped data

**Request:**
```json
{
  "url": "https://example.com/tour-page"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Tour created successfully from scraped data",
  "data": {
    "id": 1,
    "tourLink": "https://example.com/tour-page",
    "title": "Amazing Tour Title",
    "destinations": ["Mumbai", "Goa"],
    "durationDays": 5,
    "durationNights": 4,
    "tourType": "FIT",
    "providerName": "Travel Agency",
    "startingPrice": 15000.00,
    "priceType": "Starting From",
    "departureCities": ["Delhi", "Mumbai"],
    "tourStartLocation": "Delhi",
    "tourDropLocation": "Mumbai",
    "departureMonths": ["January", "February", "March"],
    "tourStatus": "Live",
    "categories": ["Adventure", "Beach"],
    "tags": ["adventure", "beach", "vacation"],
    "summary": "Amazing 5-day adventure tour",
    "highlights": ["Beach activities", "Water sports", "Local cuisine"],
    "includesFlights": true,
    "includesHotels": true,
    "includesMeals": true,
    "includesTransfers": true,
    "visaSupport": false,
    "offersType": ["Early Bird", "Group Discount"],
    "discountDetails": "10% off for early booking",
    "promotionalTagline": "Book now and save!",
    "visibilityScore": 85,
    "createdAt": "2025-07-30T14:30:00Z",
    "updatedAt": "2025-07-30T14:30:00Z"
  },
  "request_data": {
    "url": "https://example.com/tour-page",
    "scraped_data": {
      "tourLink": "https://example.com/tour-page",
      "title": "Amazing Tour Title",
      "destinations": ["Mumbai", "Goa"],
      "durationDays": 5,
      "durationNights": 4,
      "tourType": "FIT",
      "providerName": "Travel Agency",
      "startingPrice": 15000.00,
      "priceType": "Starting From",
      "departureCities": ["Delhi", "Mumbai"],
      "tourStartLocation": "Delhi",
      "tourDropLocation": "Mumbai",
      "departureMonths": ["January", "February", "March"],
      "tourStatus": "Live",
      "categories": ["Adventure", "Beach"],
      "tags": ["adventure", "beach", "vacation"],
      "summary": "Amazing 5-day adventure tour",
      "highlights": ["Beach activities", "Water sports", "Local cuisine"],
      "includesFlights": true,
      "includesHotels": true,
      "includesMeals": true,
      "includesTransfers": true,
      "visaSupport": false,
      "offersType": ["Early Bird", "Group Discount"],
      "discountDetails": "10% off for early booking",
      "promotionalTagline": "Book now and save!"
    }
  }
}
```

### Option 2: Manual Tour Creation
**Endpoint:** `POST /partner/user/<user_id>/tours/create/`
**Description:** Create a new tour manually with provided data

**Request:**
```json
{
  "url": "https://example.com/tour-page"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Tour details extracted successfully",
  "data": {
    "tourLink": "https://example.com/tour-page",
    "title": "Amazing Tour Title",
    "destinations": ["Mumbai", "Goa"],
    "durationDays": 5,
    "durationNights": 4,
    "tourType": "FIT",
    "providerName": "Travel Agency",
    "startingPrice": 15000.00,
    "priceType": "Starting From",
    "departureCities": ["Delhi", "Mumbai"],
    "tourStartLocation": "Delhi",
    "tourDropLocation": "Mumbai",
    "departureMonths": ["January", "February", "March"],
    "tourStatus": "Live",
    "categories": ["Adventure", "Beach"],
    "tags": ["adventure", "beach", "vacation"],
    "summary": "Amazing 5-day adventure tour",
    "highlights": ["Beach activities", "Water sports", "Local cuisine"],
    "includesFlights": true,
    "includesHotels": true,
    "includesMeals": true,
    "includesTransfers": true,
    "visaSupport": false,
    "offersType": ["Early Bird", "Group Discount"],
    "discountDetails": "10% off for early booking",
    "promotionalTagline": "Book now and save!"
  }
}
```

### Step 2: Create Tour
**Endpoint:** `POST /partner/user/<user_id>/tours/create/`
**Description:** Create a new tour using the scraped data (or manual data)

**Request:**
```json
{
  "tourLink": "https://example.com/tour-page",
  "title": "Amazing Tour Title",
  "destinations": ["Mumbai", "Goa"],
  "durationDays": 5,
  "durationNights": 4,
  "tourType": "FIT",
  "providerName": "Travel Agency",
  "startingPrice": 15000.00,
  "priceType": "Starting From",
  "departureCities": ["Delhi", "Mumbai"],
  "tourStartLocation": "Delhi",
  "tourDropLocation": "Mumbai",
  "departureMonths": ["January", "February", "March"],
  "tourStatus": "Live",
  "categories": ["Adventure", "Beach"],
  "tags": ["adventure", "beach", "vacation"],
  "summary": "Amazing 5-day adventure tour",
  "highlights": ["Beach activities", "Water sports", "Local cuisine"],
  "includesFlights": true,
  "includesHotels": true,
  "includesMeals": true,
  "includesTransfers": true,
  "visaSupport": false,
  "offersType": ["Early Bird", "Group Discount"],
  "discountDetails": "10% off for early booking",
  "promotionalTagline": "Book now and save!"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Tour created successfully",
  "data": {
    "id": 1,
    "tourLink": "https://example.com/tour-page",
    "title": "Amazing Tour Title",
    "destinations": ["Mumbai", "Goa"],
    "durationDays": 5,
    "durationNights": 4,
    "tourType": "FIT",
    "providerName": "Travel Agency",
    "startingPrice": 15000.00,
    "priceType": "Starting From",
    "departureCities": ["Delhi", "Mumbai"],
    "tourStartLocation": "Delhi",
    "tourDropLocation": "Mumbai",
    "departureMonths": ["January", "February", "March"],
    "tourStatus": "Live",
    "categories": ["Adventure", "Beach"],
    "tags": ["adventure", "beach", "vacation"],
    "summary": "Amazing 5-day adventure tour",
    "highlights": ["Beach activities", "Water sports", "Local cuisine"],
    "includesFlights": true,
    "includesHotels": true,
    "includesMeals": true,
    "includesTransfers": true,
    "visaSupport": false,
    "offersType": ["Early Bird", "Group Discount"],
    "discountDetails": "10% off for early booking",
    "promotionalTagline": "Book now and save!",
    "visibilityScore": 85,
    "createdAt": "2025-07-30T14:30:00Z",
    "updatedAt": "2025-07-30T14:30:00Z"
  },
  "request_data": {
    "tourLink": "https://example.com/tour-page",
    "title": "Amazing Tour Title",
    "destinations": ["Mumbai", "Goa"],
    "durationDays": 5,
    "durationNights": 4,
    "tourType": "FIT",
    "providerName": "Travel Agency",
    "startingPrice": 15000.00,
    "priceType": "Starting From",
    "departureCities": ["Delhi", "Mumbai"],
    "tourStartLocation": "Delhi",
    "tourDropLocation": "Mumbai",
    "departureMonths": ["January", "February", "March"],
    "tourStatus": "Live",
    "categories": ["Adventure", "Beach"],
    "tags": ["adventure", "beach", "vacation"],
    "summary": "Amazing 5-day adventure tour",
    "highlights": ["Beach activities", "Water sports", "Local cuisine"],
    "includesFlights": true,
    "includesHotels": true,
    "includesMeals": true,
    "includesTransfers": true,
    "visaSupport": false,
    "offersType": ["Early Bird", "Group Discount"],
    "discountDetails": "10% off for early booking",
    "promotionalTagline": "Book now and save!"
  }
}
```

## Complete Workflow Example

### Two-Step Process (Recommended)

#### Step 1: Scrape Tour Details
```bash
curl -X POST "https://api.example.com/partner/scrape-tour-details/" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/tour-page"}'
```

#### Step 2: Create Tour with Edited Data
```bash
curl -X POST "https://api.example.com/partner/user/123/tours/create/" \
  -H "Authorization: Token your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "tourLink": "https://example.com/tour-page",
    "title": "Amazing Tour Title (Edited)",
    "destinations": ["Mumbai", "Goa"],
    "durationDays": 5,
    "durationNights": 4,
    "tourType": "FIT",
    "providerName": "Travel Agency",
    "startingPrice": 15000.00,
    "priceType": "Starting From",
    "departureCities": ["Delhi", "Mumbai"],
    "tourStartLocation": "Delhi",
    "tourDropLocation": "Mumbai",
    "departureMonths": ["January", "February", "March"],
    "tourStatus": "Live",
    "categories": ["Adventure", "Beach"],
    "tags": ["adventure", "beach", "vacation"],
    "summary": "Amazing 5-day adventure tour",
    "highlights": ["Beach activities", "Water sports", "Local cuisine"],
    "includesFlights": true,
    "includesHotels": true,
    "includesMeals": true,
    "includesTransfers": true,
    "visaSupport": false,
    "offersType": ["Early Bird", "Group Discount"],
    "discountDetails": "10% off for early booking",
    "promotionalTagline": "Book now and save!"
  }'
```

### Manual Tour Creation (Alternative)
```bash
curl -X POST "https://api.example.com/partner/user/123/tours/create/" \
  -H "Authorization: Token your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "tourLink": "https://example.com/tour-page",
    "title": "Amazing Tour Title",
    "destinations": ["Mumbai", "Goa"],
    "durationDays": 5,
    "durationNights": 4,
    "tourType": "FIT",
    "providerName": "Travel Agency",
    "startingPrice": 15000.00,
    "priceType": "Starting From",
    "departureCities": ["Delhi", "Mumbai"],
    "tourStartLocation": "Delhi",
    "tourDropLocation": "Mumbai",
    "departureMonths": ["January", "February", "March"],
    "tourStatus": "Live",
    "categories": ["Adventure", "Beach"],
    "tags": ["adventure", "beach", "vacation"],
    "summary": "Amazing 5-day adventure tour",
    "highlights": ["Beach activities", "Water sports", "Local cuisine"],
    "includesFlights": true,
    "includesHotels": true,
    "includesMeals": true,
    "includesTransfers": true,
    "visaSupport": false,
    "offersType": ["Early Bird", "Group Discount"],
    "discountDetails": "10% off for early booking",
    "promotionalTagline": "Book now and save!"
  }'
```

## Benefits of This Approach

### Two-Step Process (Recommended)
1. **User Control:** Users can review and edit scraped data before creating tour
2. **Data Quality:** Ensures accurate tour information through manual verification
3. **Flexibility:** Users can modify any field before submission
4. **Error Prevention:** Reduces errors by allowing data review
5. **Better UX:** Clear separation between scraping and tour creation

### Manual Tour Creation (Alternative)
1. **Separation of Concerns:** Scraping and tour creation are separate operations
2. **Flexibility:** You can modify scraped data before creating the tour
3. **Reusability:** The scraping API can be used independently
4. **Cleaner Code:** No duplicate logic for tour creation
5. **Better Testing:** Each API can be tested independently

## Available Tour Management APIs

### Two-Step Tour Creation
- `POST /partner/scrape-tour-details/` - Scrape URL and return extracted data for editing
- `POST /partner/user/<user_id>/tours/create/` - Create tour with edited data

### Tour Management
- `GET /partner/user/<user_id>/tours/` - Get all tours
- `PATCH /partner/user/<user_id>/tours/<tour_id>/update/` - Update tour
- `GET /partner/user/<user_id>/tours/<tour_id>/` - Get tour details 