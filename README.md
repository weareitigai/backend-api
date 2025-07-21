# Backend API Documentation

This document provides instructions for setting up and running the backend server for the Travel Partner project. It also includes details about the available API endpoints.

## Base URLs

- **Local:** `http://localhost:8000/api/`
- **Deployed (Render):** `https://backend-api-vpx2.onrender.com/api/`

## Admin Panel

- First paste `django-insecure-g9m2w@k8z$x7@e4v!t#h$2f&a5*p6n9c8q1r$x%w@j4m8s!l6k`
  in https://backend-api-vpx2.onrender.com/api/docs/  `tokenAuth` (apiKey)

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

-   **`POST /partner/business-details/`**: Saves the business details for a partner.
-   **`POST /partner/location-coverage/`**: Saves the location coverage for a partner.
-   **`POST /partner/tours-services/`**: Saves the tours and services information for a partner.
-   **`POST /partner/legal-banking/`**: Saves the legal and banking details for a partner.
-   **`GET /partner/status/`**: Retrieves the onboarding status of a partner.
-   **`POST /partner/complete-onboarding/`**: Marks the partner's onboarding as complete.

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
