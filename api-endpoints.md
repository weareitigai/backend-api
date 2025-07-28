
## **Complete API Endpoints Summary**

### **Base URL**
- **Local:** `http://localhost:8000/api/`
- **Deployed:** `https://backend-api-vpx2.onrender.com/api/`

---

## **1. Authentication Endpoints**

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/send-email-otp/` | Send OTP to email | No |
| POST | `/auth/verify-email-otp/` | Verify email OTP | No |
| POST | `/auth/send-mobile-otp/` | Send OTP to mobile | No |
| POST | `/auth/verify-mobile-otp/` | Verify mobile OTP | No |
| POST | `/auth/bypass-mobile-verification/` | Bypass mobile verification (dev only) | No |
| POST | `/auth/signup/` | Register new user | No |
| POST | `/auth/login/` | Login user | No |
| POST | `/auth/logout/` | Logout user | Yes |
| GET | `/auth/profile/` | Get user profile | Yes |
| POST | `/auth/forgot-password/` | Initiate password reset | No |
| POST | `/auth/reset-password/` | Reset password with token | No |
| POST | `/auth/change-password/` | Change password | Yes |

---

## **2. Partner Onboarding Endpoints**

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/partner/business-details/` | Get business details | Yes |
| POST | `/partner/business-details/` | Create/update business details | Yes |
| PATCH | `/partner/business-details/` | Update business details | Yes |
| GET | `/partner/location-coverage/` | Get location coverage | Yes |
| POST | `/partner/location-coverage/` | Create/update location coverage | Yes |
| PATCH | `/partner/location-coverage/` | Update location coverage | Yes |
| GET | `/partner/tours-services/` | Get tours & services info | Yes |
| POST | `/partner/tours-services/` | Create/update tours & services | Yes |
| PATCH | `/partner/tours-services/` | Update tours & services | Yes |
| GET | `/partner/legal-banking/` | Get legal & banking info | Yes |
| POST | `/partner/legal-banking/` | Create/update legal & banking | Yes |
| PATCH | `/partner/legal-banking/` | Update legal & banking | Yes |
| GET | `/partner/status/` | Get onboarding status | Yes |
| POST | `/partner/complete-onboarding/` | Mark onboarding complete | Yes |

**Note:** All GET endpoints support optional `user_id` query parameter for admin/privileged access.

---

## **3. Tour Management Endpoints**

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/partner/user/{user_id}/tours/` | Get all tours for partner | Yes |
| POST | `/partner/user/{user_id}/tours/create/` | Create new tour | Yes |
| PATCH | `/partner/user/{user_id}/tours/create/` | Update existing tour | Yes |
| GET | `/partner/user/{user_id}/tours/{tour_id}/` | Get specific tour details | Yes |

---

## **4. Web Scraping Endpoints**

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/partner/scrape-tour-details/` | Scrape tour details from URL | No |

---

## **5. Common Data Endpoints**

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/common/destinations/` | Get destinations (with optional search) | No |
| GET | `/common/languages/` | Get available languages | No |
| GET | `/common/tour-types/` | Get tour types | No |
| GET | `/common/timezones/` | Get timezones | No |

---

## **6. Health Check Endpoints**

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/health/` | Health check | No |

---

## **7. Admin & Documentation Endpoints**

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| - | `/admin/` | Django admin panel | Yes (superuser) |
| GET | `/api/schema/` | API schema | No |
| GET | `/api/docs/` | Swagger documentation | No |

---

## **Key Features:**

1. **Authentication:** Token-based authentication with Bearer tokens
2. **Upsert Behavior:** All POST endpoints for onboarding support create-or-update functionality
3. **Admin Access:** GET endpoints support `user_id` parameter for cross-user data access
4. **Search Support:** Destinations endpoint supports search functionality
5. **Tour Management:** Full CRUD operations for tours (for verified partners only)
6. **Web Scraping:** AI-powered tour details extraction from URLs
7. **Health Monitoring:** Simple health check endpoint

The updated Postman collection (`Backend_collection.json`) now includes all these endpoints organized by category, making it easy to test and integrate with your frontend application.