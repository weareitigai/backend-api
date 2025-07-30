# Backend API Documentation

This document provides instructions for setting up and running the backend server for the Travel Partner project. It also includes details about the available API endpoints.

## Base URLs

- **Local:** `http://localhost:8000/api/`
- **Deployed (Render):** `https://backend-api-vpx2.onrender.com/api/`

## Admin Panel

- First paste `django-insecure-g9m2w@k8z$x7@e4v!t#h$2f&a5*p6n9c8q1r$x%w@j4m8s!l6k`
  in https://backend-api-vpx2.onrender.com/api/docs/  `Token` (apiKey)

- **Admin Panel** `https://backend-api-vpx2.onrender.com/admin/`

- admin email: admin@example.com and password: admin123

## PostgreSQL Database Setup

To set up the PostgreSQL database, follow these steps:

1.  **Install PostgreSQL:**
    If you don't have PostgreSQL installed, download and install it from the [official website](https://www.postgresql.org/download/).

2.  **Create the database and user:**
    Open the PostgreSQL command-line interface (`psql`) and run the following commands:

    ```sql
    CREATE DATABASE travel_partner_db;
    CREATE USER travel_partner_user WITH PASSWORD 'your_password_here';
    ALTER ROLE travel_partner_user SET client_encoding TO 'utf8';
    ALTER ROLE travel_partner_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE travel_partner_user SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE travel_partner_db TO travel_partner_user;
    ```

    Replace `'your_password_here'` with a secure password.

## Alternatively you can also migrate database 

```python
python manage.py migrate --noinput 
```

## Environment Configuration

1.  **Create a `.env` file:**
    Copy the `.env.template` file to a new file named `.env`:

    ```bash
    cp .env.template .env
    ```

2.  **Update the `.env` file:**
    Open the `.env` file and update the following variables:

    ```
    # Django Configuration
    SECRET_KEY=django-insecure-g9m2w@k8z$x7@e4v!t#h$2f&a5*p6n9c8q1r$x%w@j4m8s!l6k
    DEBUG=True

    # Database Configuration
    DB_NAME=travel_partner_db
    DB_USER=travel_partner_user
    DB_PASSWORD=your_password_here
    DB_HOST=localhost
    DB_PORT=5432
    ```

    Make sure to use the same password you set during the database setup.

## Running the Backend Server

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt && pip install git+https://github.com/dmpayton/django-admin-honeypot
    ```

2.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

3. **Create superuser for django admin panel**

    ```python
    python manage.py create_superuser_from_env
    ```

4.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```

The server will be running at `http://localhost:8000`.

## Temporary OTP Generation

For testing purposes, you can create a temporary OTP in the terminal using a management command. The application is configured to print the OTP to the console when `DEBUG` is `True`. When you request an OTP via the API, check the terminal output where you are running the `runserver` command.

Alternatively, you can use the following management command to populate the database with dummy data, including users with pre-verified states:

```bash
python manage.py populate_dummy_data
```

This command will create test users and partners, which can be useful for testing authenticated endpoints.

## Mobile OTP Configuration

Mobile OTP functionality can be temporarily disabled using the `MOBILE_OTP_ENABLED` environment variable:

- Set `MOBILE_OTP_ENABLED=False` to disable mobile OTP (default)
- Set `MOBILE_OTP_ENABLED=True` to enable mobile OTP

When disabled, the mobile OTP endpoints will return a 503 Service Unavailable error with an appropriate message.

### Bypassing Mobile Verification (When OTP is Disabled)

When mobile OTP is disabled, you can use the bypass endpoint:
- **`POST /auth/bypass-mobile-verification/`**: Manually mark a mobile number as verified
  - **Parameters**: `{ "mobile": "+1234567890" }`
  - Only works when `MOBILE_OTP_ENABLED=False`

### Management Commands

Check mobile OTP status:
```bash
python manage.py toggle_mobile_otp --status
```

## API Endpoints

All endpoints are prefixed with `/api/`.

### Authentication

-   **`POST /auth/send-email-otp/`**: Sends an OTP to the user's email.
    -   **Parameters**: `{ "email": "user@example.com" }`
-   **`POST /auth/verify-email-otp/`**: Verifies the OTP sent to the email.
    -   **Parameters**: `{ "email": "user@example.com", "otp": "123456" }`
-   **`POST /auth/send-mobile-otp/`**: Sends an OTP to the user's mobile number.
    -   **Parameters**: `{ "mobileNumber": "+1234567890" }`
-   **`POST /auth/verify-mobile-otp/`**: Verifies the OTP sent to the mobile number.
    -   **Parameters**: `{ "mobileNumber": "+1234567890", "otp": "123456" }`
-   **`POST /auth/signup/`**: Registers a new user.
    -   **Parameters**: `{ "email": "user@example.com", "password": "password123", "fullName": "Test User" }`
-   **`POST /auth/login/`**: Logs in a user.
    -   **Parameters**: `{ "email": "user@example.com", "password": "password123" }`
-   **`POST /auth/logout/`**: Logs out the currently authenticated user.
-   **`GET /auth/profile/`**: Retrieves the profile of the authenticated user.
-   **`POST /auth/forgot-password/`**: Initiates the password reset process.
    -   **Parameters**: `{ "email": "user@example.com" }`
-   **`POST /auth/reset-password/`**: Resets the password using a token.
    -   **Parameters**: `{ "token": "reset_token", "newPassword": "new_password123" }`
-   **`POST /auth/change-password/`**: Changes the password for an authenticated user.
    -   **Parameters**: `{ "oldPassword": "current_password", "newPassword": "new_password123" }`

### Partner Onboarding

-   **`POST /partner/business-details/`**: Creates or updates business details for a partner (upsert behavior).
-   **`GET /partner/business-details/`**: Retrieves business details for a partner.
-   **`PATCH /partner/business-details/`**: Updates existing business details for a partner.
-   **`POST /partner/location-coverage/`**: Creates or updates location coverage for a partner (upsert behavior).
-   **`GET /partner/location-coverage/`**: Retrieves location coverage for a partner.
-   **`PATCH /partner/location-coverage/`**: Updates existing location coverage for a partner.
-   **`POST /partner/tours-services/`**: Creates or updates tours and services information for a partner (upsert behavior).
-   **`GET /partner/tours-services/`**: Retrieves tours and services information for a partner.
-   **`PATCH /partner/tours-services/`**: Updates existing tours and services information for a partner.
-   **`POST /partner/legal-banking/`**: Creates or updates legal and banking details for a partner (upsert behavior).
-   **`GET /partner/legal-banking/`**: Retrieves legal and banking details for a partner.
-   **`PATCH /partner/legal-banking/`**: Updates existing legal and banking details for a partner.
-   **`GET /partner/status/`**: Retrieves the onboarding status of a partner.
-   **`POST /partner/complete-onboarding/`**: Marks the partner's onboarding as complete.

**Note**: All POST endpoints for partner onboarding now support "upsert" behavior - they will create the record if it doesn't exist, or update it if it already exists. This provides a better user experience by eliminating the confusion between when to use POST vs PATCH.

### Common Data

-   **`GET /common/destinations/`**: Retrieves a list of available destinations.
-   **`GET /common/languages/`**: Retrieves a list of available languages.
-   **`GET /common/tour-types/`**: Retrieves a list of available tour types.
-   **`GET /common/timezones/`**: Retrieves a list of available timezones.

## API Testing with Postman

You can test the deployed APIs using Postman.

1.  **Set the Base URL:**
    Use the deployed base URL: `https://backend-api-vpx2.onrender.com/api/`

2.  **Example: User Signup**
    -   **Method:** `POST`
    -   **URL:** `https://backend-api-vpx2.onrender.com/api/auth/signup/`
    -   **Body (raw, JSON):**
        ```json
        {
            "email": "testuser@example.com",
            "password": "password123",
            "fullName": "Test User"
        }
        ```

3.  **Example: User Login**
    -   **Method:** `POST`
    -   **URL:** `https://backend-api-vpx2.onrender.com/api/auth/login/`
    -   **Body (raw, JSON):**
        ```json
        {
            "email": "testuser@example.com",
            "password": "password123"
        }
        ```
    -   After logging in, you will receive an access token. Use this token in the `Authorization` header for authenticated requests (e.g., `Authorization: Bearer <your_token>`).


## Temporary Frontend

A temporary frontend is available in the `frontend` directory. To run it:

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Start the development server:**
    ```bash
    npm run dev
    ```

The frontend will be available at `http://localhost:5173`.

## Email Configuration (SendGrid Integration)

This project supports multiple email backends for sending OTP emails:

### SendGrid Setup (Recommended)

1. **Create a SendGrid account** at https://sendgrid.com
2. **Verify your sender email** in SendGrid dashboard
3. **Create an API key** with Mail Send permissions
4. **Update your .env file:**
   ```bash
   EMAIL_BACKEND=sendgrid
   SENDGRID_API_KEY=your-sendgrid-api-key-here
   DEFAULT_FROM_EMAIL=your-verified-email@domain.com
   FROM_NAME=Travel Partner Platform
   ```

### Email Features

✅ **Professional HTML Templates**: Beautiful, responsive email design  
✅ **Plain Text Fallback**: Automatic plain text versions  
✅ **Multiple Backends**: SendGrid, SMTP, or console support  
✅ **Graceful Fallback**: Automatic fallback if primary method fails  
✅ **Testing Tools**: Built-in commands for validation  

### Testing Email Integration

Use the management command to test your email setup:

```bash
# Check configuration only
python manage.py test_email_otp --check-config

# Send test email
python manage.py test_email_otp --email your-test@email.com

# Send with custom OTP
python manage.py test_email_otp --email test@example.com --otp 999888
```

### Alternative Email Backends

**SMTP Configuration (Gmail/Outlook):**
```bash
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

**Console Backend (Development):**
```bash
EMAIL_BACKEND=console
```

For detailed setup instructions, see `SENDGRID_SETUP.md`.





### Partner Onboarding GET APIs with user_id

In apps/partner/views.py, the following endpoints allow you to pass a user_id as a query parameter to fetch another user's partner-related details (if you have permission):
- GET /api/partner/business-details/?user_id=<id>
Returns business details for the partner associated with the given user ID.
- GET /api/partner/location-coverage/?user_id=<id>
Returns location coverage for the partner associated with the given user ID.
- GET /api/partner/tours-services/?user_id=<id>
Returns tours and services info for the partner associated with the given user ID.
- GET /api/partner/legal-banking/?user_id=<id>
Returns legal and banking details for the partner associated with the given user ID.
- GET /api/partner/status/?user_id=<id>
Returns onboarding status for the partner associated with the given user ID.
If you do not provide user_id, these endpoints return data for the currently authenticated user.




---

Absolutely! Here’s a comprehensive overview of your backend architecture, including all the main features, flows, and the relevant API endpoints. This will help you design the frontend and understand how each part connects.

---

# **Backend Architecture & API Overview**

---

## 1. **Authentication & User Management**

### **User Registration & Login Flow**
- **Signup:**  
  `POST /auth/signup/`  
  **Body:** `{ "email": "...", "password": "...", "fullName": "..." }`  
  _Registers a new user._

- **Login:**  
  `POST /auth/login/`  
  **Body:** `{ "email": "...", "password": "..." }`  
  _Returns an access token for authenticated requests._

- **Logout:**  
  `POST /auth/logout/`  
  _Logs out the current user (token invalidation)._

- **Get Profile:**  
  `GET /auth/profile/`  
  _Fetches the authenticated user's profile._

---

### **OTP Verification**
- **Send Email OTP:**  
  `POST /auth/send-email-otp/`  
  **Body:** `{ "email": "..." }`  
  _Sends OTP to email._

- **Verify Email OTP:**  
  `POST /auth/verify-email-otp/`  
  **Body:** `{ "email": "...", "otp": "..." }`  
  _Verifies the email OTP._

- **Send Mobile OTP:**  
  `POST /auth/send-mobile-otp/`  
  **Body:** `{ "mobileNumber": "..." }`  
  _Sends OTP to mobile (if enabled)._

- **Verify Mobile OTP:**  
  `POST /auth/verify-mobile-otp/`  
  **Body:** `{ "mobileNumber": "...", "otp": "..." }`  
  _Verifies the mobile OTP._

- **Bypass Mobile Verification:**  
  `POST /auth/bypass-mobile-verification/`  
  **Body:** `{ "mobile": "..." }`  
  _For dev/testing, marks mobile as verified if OTP is disabled._

---

### **Password Management**
- **Forgot Password:**  
  `POST /auth/forgot-password/`  
  **Body:** `{ "email": "..." }`  
  _Initiates password reset._

- **Reset Password:**  
  `POST /auth/reset-password/`  
  **Body:** `{ "token": "...", "newPassword": "..." }`  
  _Resets password using token._

- **Change Password:**  
  `POST /auth/change-password/`  
  **Body:** `{ "oldPassword": "...", "newPassword": "..." }`  
  _Changes password for logged-in user._

---

## 2. **Partner Onboarding (Multi-Step Form Flow)**

Each step is a separate API. All POST endpoints support "upsert" (create or update).

### **Business Details**
- **Create/Update:**  
  `POST /partner/business-details/`
- **Get:**  
  `GET /partner/business-details/`
- **Patch:**  
  `PATCH /partner/business-details/`

### **Location Coverage**
- **Create/Update:**  
  `POST /partner/location-coverage/`
- **Get:**  
  `GET /partner/location-coverage/`
- **Patch:**  
  `PATCH /partner/location-coverage/`

### **Tours & Services**
- **Create/Update:**  
  `POST /partner/tours-services/`
- **Get:**  
  `GET /partner/tours-services/`
- **Patch:**  
  `PATCH /partner/tours-services/`

### **Legal & Banking**
- **Create/Update:**  
  `POST /partner/legal-banking/`
- **Get:**  
  `GET /partner/legal-banking/`
- **Patch:**  
  `PATCH /partner/legal-banking/`

### **Onboarding Status**
- **Get Status:**  
  `GET /partner/status/`

### **Complete Onboarding**
- **Mark Complete:**  
  `POST /partner/complete-onboarding/`

#### **Admin/Privileged User Access**
- All the above GET endpoints accept an optional `user_id` query parameter:  
  e.g. `GET /partner/business-details/?user_id=<id>`  
  _Returns data for the specified user if you have permission. If not provided, returns data for the current user._

---

## 3. **Common Data Endpoints**

- **Get Destinations:**  
  `GET /common/destinations/`

- **Get Languages:**  
  `GET /common/languages/`

- **Get Tour Types:**  
  `GET /common/tour-types/`

- **Get Timezones:**  
  `GET /common/timezones/`

_These are used to populate dropdowns, filters, etc. in the frontend._

---

## 4. **Admin Panel**

- **Django Admin:**  
  `/admin/`  
  _For superusers to manage all data._

---

## 5. **Email Integration**

- **SendGrid (Recommended):**  
  Configured via `.env` for production.
- **SMTP/Console:**  
  For development/testing.

---

## 6. **Testing & Utilities**

- **Populate Dummy Data:**  
  `python manage.py populate_dummy_data`  
  _Creates test users and partners for development._

- **Toggle Mobile OTP:**  
  `python manage.py toggle_mobile_otp --status`  
  _Check or change OTP status._

- **Test Email Integration:**  
  `python manage.py test_email_otp --email ...`  
  _Send test emails._

---

## 7. **Frontend Integration Flow**

### **User Flow**
1. **Signup → Email/Mobile OTP → Login → Profile Completion**
2. **Onboarding:**  
   - Multi-step forms for business, location, tours, legal, etc.
   - Each step saves via its respective API.
   - On completion, call `/partner/complete-onboarding/`.
3. **Profile & Data:**  
   - Fetch and display user profile and onboarding status.
   - Use common data endpoints for form options.
4. **Admin/Privileged User:**  
   - Can view/edit onboarding data for any user by passing `user_id`.

### **Authentication**
- All protected endpoints require the `Authorization: Bearer <token>` header.

### **Error Handling**
- Handle 503 for OTP endpoints if disabled.
- Handle permission errors for cross-user data access.

---

## 8. **Security & Permissions**
- Most endpoints require authentication.
- Some endpoints (with `user_id`) require admin/privileged access.
- Tokens must be sent in the `Authorization` header.

---

## 9. **Dev/Testing**
- Dummy data and bypasses are available for local development.
- Console/email backends for OTPs in dev mode.

---

# **Summary Table of Key APIs**

| Area                | Endpoint                                      | Method | Notes/Usage                                 |
|---------------------|-----------------------------------------------|--------|----------------------------------------------|
| Auth                | /auth/signup/                                 | POST   | Register user                                |
|                     | /auth/login/                                  | POST   | Login, get token                             |
|                     | /auth/logout/                                 | POST   | Logout                                       |
|                     | /auth/profile/                                | GET    | Get user profile                             |
|                     | /auth/send-email-otp/                         | POST   | Send email OTP                               |
|                     | /auth/verify-email-otp/                       | POST   | Verify email OTP                             |
|                     | /auth/send-mobile-otp/                        | POST   | Send mobile OTP                              |
|                     | /auth/verify-mobile-otp/                      | POST   | Verify mobile OTP                            |
|                     | /auth/bypass-mobile-verification/             | POST   | Bypass mobile OTP (dev only)                 |
|                     | /auth/forgot-password/                        | POST   | Forgot password                              |
|                     | /auth/reset-password/                         | POST   | Reset password                               |
|                     | /auth/change-password/                        | POST   | Change password                              |
| Partner Onboarding  | /partner/business-details/                    | GET/POST/PATCH | Business details (upsert)           |
|                     | /partner/location-coverage/                   | GET/POST/PATCH | Location coverage (upsert)           |
|                     | /partner/tours-services/                      | GET/POST/PATCH | Tours/services (upsert)              |
|                     | /partner/legal-banking/                       | GET/POST/PATCH | Legal/banking (upsert)               |
|                     | /partner/status/                              | GET    | Onboarding status                            |
|                     | /partner/complete-onboarding/                 | POST   | Mark onboarding complete                     |
| Common Data         | /common/destinations/                         | GET    | List of destinations                         |
|                     | /common/languages/                            | GET    | List of languages                            |
|                     | /common/tour-types/                           | GET    | List of tour types                           |
|                     | /common/timezones/                            | GET    | List of timezones                            |
| Tour Management     | /partner/user/{user_id}/tours/create/         | POST   | Create new tour                              |
|                     | /partner/user/{user_id}/tours/{tour_id}/update/ | PATCH | Update tour                              |
|                     | /partner/user/{user_id}/tours/                 | GET    | Get all tours                                |
|                     | /partner/user/{user_id}/tours/{tour_id}/       | GET    | Get tour details                             |
|                     | /partner/scrape-tour-details/                   | POST   | Scrape URL and return data for editing      |
| Admin Panel         | /admin/                                       | -      | Django admin                                 |

---
