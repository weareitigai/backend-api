# API Documentation

This document provides comprehensive documentation for all APIs implemented in the Django Travel Partner Platform.

## Base URL
```
http://127.0.0.1:8000
```

## Authentication
Most APIs require authentication using Token-based authentication. Include the token in the header:
```
Authorization: Token <your_token_here>
```

---

## Authentication APIs

### 1. Send Email OTP
**Endpoint:** `POST /api/auth/send-email-otp/`
**Authentication:** Not required
**Purpose:** Send OTP to user's email for verification

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OTP sent to your email successfully"
}
```

---

### 2. Verify Email OTP
**Endpoint:** `POST /api/auth/verify-email-otp/`
**Authentication:** Not required
**Purpose:** Verify OTP sent to email

**Request Body:**
```json
{
  "email": "user@example.com",
  "otp": "123456"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OTP verified successfully"
}
```

---

### 3. Send Mobile OTP
**Endpoint:** `POST /api/auth/send-mobile-otp/`
**Authentication:** Not required
**Purpose:** Send OTP to user's mobile number

**Request Body:**
```json
{
  "mobile": "+1234567890"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OTP sent to your mobile successfully"
}
```

---

### 4. Verify Mobile OTP
**Endpoint:** `POST /api/auth/verify-mobile-otp/`
**Authentication:** Not required
**Purpose:** Verify OTP sent to mobile

**Request Body:**
```json
{
  "mobile": "+1234567890",
  "otp": "123456"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OTP verified successfully"
}
```

---

### 5. User Signup
**Endpoint:** `POST /api/auth/signup/`
**Authentication:** Not required
**Purpose:** Register new user

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "mobile": "+1234567890",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "mobile": "+1234567890",
    "is_email_verified": true,
    "is_mobile_verified": true,
    "date_joined": "2025-07-16T10:30:00Z"
  },
  "token": "abc123token456"
}
```

---

### 6. User Login
**Endpoint:** `POST /api/auth/login/`
**Authentication:** Not required
**Purpose:** Login with email/mobile & password

**Request Body:**
```json
{
  "emailOrMobile": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "mobile": "+1234567890",
    "is_email_verified": true,
    "is_mobile_verified": true,
    "date_joined": "2025-07-16T10:30:00Z"
  },
  "token": "abc123token456"
}
```

---

### 7. User Logout
**Endpoint:** `POST /api/auth/logout/`
**Authentication:** Required
**Purpose:** Logout user

**Request Headers:**
```
Authorization: Token abc123token456
```

**Response:**
```json
{
  "success": true
}
```

---

### 8. Forgot Password
**Endpoint:** `POST /api/auth/forgot-password/`
**Authentication:** Not required
**Purpose:** Initiate password reset

**Request Body:**
```json
{
  "email": "john@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Password reset OTP sent to your email"
}
```

---

### 9. Reset Password
**Endpoint:** `POST /api/auth/reset-password/`
**Authentication:** Not required
**Purpose:** Complete password reset

**Request Body:**
```json
{
  "email": "john@example.com",
  "otp": "123456",
  "newPassword": "newsecurepassword123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Password reset successfully"
}
```

---

## Partner APIs

### 1. Business Details
**Endpoint:** `GET/PATCH /api/partner/business-details/`
**Authentication:** Required
**Purpose:** Get or update business details (Step 1)

**GET Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "ABC Travel Company",
    "type_of_provider": ["Tour Operator", "Travel Agent"],
    "gstin": "22AAAAA0000A1Z5",
    "years": 5,
    "website": "https://www.abctravel.com",
    "reg_number": "REG123456",
    "address": "123 Business Street, Mumbai, Maharashtra",
    "employees": 25,
    "seasonal": false,
    "annual_bookings": 1000
  }
}
```

**PATCH Request Body:**
```json
{
  "name": "ABC Travel Company",
  "type_of_provider": ["Tour Operator", "Travel Agent"],
  "gstin": "22AAAAA0000A1Z5",
  "years": 5,
  "website": "https://www.abctravel.com",
  "reg_number": "REG123456",
  "address": "123 Business Street, Mumbai, Maharashtra",
  "employees": 25,
  "seasonal": false,
  "annual_bookings": 1000
}
```

---

### 2. Location & Coverage
**Endpoint:** `GET/PATCH /api/partner/location-coverage/`
**Authentication:** Required
**Purpose:** Get or update location and coverage info (Step 2)

**GET Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "primary_location": "Mumbai",
    "destinations": [1, 2, 3, 4],
    "languages": ["English", "Hindi", "Marathi"],
    "regions": ["Western India", "Central India"],
    "pan_india": false,
    "seasons": ["Winter", "Summer", "Monsoon"],
    "timezone": "Asia/Kolkata"
  }
}
```

**PATCH Request Body:**
```json
{
  "primary_location": "Mumbai",
  "destinations": [1, 2, 3, 4],
  "languages": ["English", "Hindi", "Marathi"],
  "regions": ["Western India", "Central India"],
  "pan_india": false,
  "seasons": ["Winter", "Summer", "Monsoon"],
  "timezone": "Asia/Kolkata"
}
```

---

### 3. Tours & Services
**Endpoint:** `GET/PATCH /api/partner/tours-services/`
**Authentication:** Required
**Purpose:** Get or update tours and services overview (Step 3)

**GET Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "number_of_tours": 50,
    "types_of_tours": ["Adventure", "Cultural", "Wildlife"],
    "custom_tour_type": "Photography Tours",
    "min_price": 5000.00,
    "group_size_min": 2,
    "group_size_max": 25,
    "preference": "Small Groups",
    "offers_custom_tours": true
  }
}
```

**PATCH Request Body:**
```json
{
  "number_of_tours": 50,
  "types_of_tours": ["Adventure", "Cultural", "Wildlife"],
  "custom_tour_type": "Photography Tours",
  "min_price": 5000.00,
  "group_size_min": 2,
  "group_size_max": 25,
  "preference": "Small Groups",
  "offers_custom_tours": true
}
```

---

### 4. Legal & Banking
**Endpoint:** `GET/PATCH /api/partner/legal-banking/`
**Authentication:** Required
**Purpose:** Get or update legal and banking info (Step 4)

**GET Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "pan_or_aadhaar": "ABCDE1234F",
    "business_proof_file": "/media/business_proofs/document.pdf",
    "license_number": "LIC123456",
    "company_type": "Private Limited",
    "emergency_contact": "+91-9876543210",
    "terms_accepted": true
  }
}
```

**PATCH Request Body:**
```json
{
  "pan_or_aadhaar": "ABCDE1234F",
  "license_number": "LIC123456",
  "company_type": "Private Limited",
  "emergency_contact": "+91-9876543210",
  "terms_accepted": true
}
```

---

### 5. Partner Status
**Endpoint:** `GET /api/partner/status/`
**Authentication:** Required
**Purpose:** Get step completion status

**Response:**
```json
{
  "completed_steps": [1, 2, 3, 4],
  "is_verified": true
}
```

---

### 6. Complete Onboarding
**Endpoint:** `POST /api/partner/complete-onboarding/`
**Authentication:** Required
**Purpose:** Mark profile as complete

**Response:**
```json
{
  "success": true,
  "message": "Onboarding completed successfully"
}
```

---

## Common APIs

### 1. Destinations
**Endpoint:** `GET /api/common/destinations/`
**Authentication:** Not required
**Purpose:** Autocomplete for destinations

**Query Parameters:**
- `search` (optional): Search term for filtering destinations

**Examples:**
```
GET /api/common/destinations/
GET /api/common/destinations/?search=Mumbai
```

**Response:**
```json
{
  "results": [
    {
      "id": 1,
      "name": "Mumbai",
      "country": "India",
      "state": "Maharashtra",
      "city": "Mumbai"
    },
    {
      "id": 2,
      "name": "Delhi",
      "country": "India",
      "state": "Delhi",
      "city": "Delhi"
    }
  ]
}
```

---

### 2. Languages
**Endpoint:** `GET /api/common/languages/`
**Authentication:** Not required
**Purpose:** Fetch available language options

**Response:**
```json
{
  "results": [
    "English",
    "Hindi",
    "Tamil",
    "Telugu",
    "Bengali",
    "Marathi",
    "Gujarati",
    "Kannada",
    "Malayalam",
    "Punjabi"
  ]
}
```

---

### 3. Tour Types
**Endpoint:** `GET /api/common/tour-types/`
**Authentication:** Not required
**Purpose:** Fetch all tour types

**Response:**
```json
{
  "results": [
    "Adventure",
    "Cultural",
    "Wildlife",
    "Beach",
    "Mountain",
    "Religious",
    "Historical",
    "Luxury",
    "Budget",
    "Family",
    "Honeymoon",
    "Group",
    "Solo",
    "Photography",
    "Food & Culinary"
  ]
}
```

---

### 4. Timezones
**Endpoint:** `GET /api/common/timezones/`
**Authentication:** Not required
**Purpose:** Fetch timezone list

**Response:**
```json
{
  "results": [
    "Asia/Kolkata",
    "UTC",
    "Asia/Dubai",
    "Asia/Singapore",
    "Europe/London",
    "America/New_York",
    "America/Los_Angeles",
    "Australia/Sydney",
    "Asia/Tokyo",
    "Europe/Paris"
  ]
}
```

---

## Error Responses

All APIs follow a consistent error response format:

**Client Errors (4xx):**
```json
{
  "success": false,
  "message": "Error description",
  "errors": {
    "field_name": ["Field-specific error message"]
  }
}
```

**Server Errors (5xx):**
```json
{
  "success": false,
  "message": "Internal server error occurred"
}
```

## Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Interactive Documentation

For interactive API testing and detailed schema information, visit:
```
http://127.0.0.1:8000/api/docs/
```

This provides a Swagger UI interface where you can test all endpoints directly from the browser.
