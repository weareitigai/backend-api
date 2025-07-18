# Django API Project

This project implements a comprehensive API system for a travel partner platform with authentication, partner onboarding, and common data services.

## Project Structure

```
apiproject/
├── manage.py
├── requirements.txt
├── build.md
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── __init__.py
│   ├── authentication/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── utils.py
│   ├── partner/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   └── common/
│       ├── __init__.py
│       ├── models.py
│       ├── views.py
│       ├── serializers.py
│       └── urls.py
```

## APIs Overview

### Authentication APIs
- **POST** `/api/auth/send-email-otp` - Send OTP to user's email
- **POST** `/api/auth/verify-email-otp` - Verify OTP sent to email
- **POST** `/api/auth/send-mobile-otp` - Send OTP to user's mobile
- **POST** `/api/auth/verify-mobile-otp` - Verify OTP sent to mobile
- **POST** `/api/auth/signup` - Register new user
- **POST** `/api/auth/login` - Login with email/mobile & password
- **POST** `/api/auth/logout` - Logout user
- **POST** `/api/auth/forgot-password` - Initiate password reset
- **POST** `/api/auth/reset-password` - Complete password reset

### Partner APIs
- **PATCH/GET** `/api/partner/business-details` - Business information management
- **PATCH/GET** `/api/partner/location-coverage` - Location and coverage info
- **PATCH/GET** `/api/partner/tours-services` - Tours and services overview
- **PATCH/GET** `/api/partner/legal-banking` - Legal and banking information
- **GET** `/api/partner/status` - Get step completion status
- **POST** `/api/partner/complete-onboarding` - Mark profile as complete

### Common APIs
- **GET** `/api/common/destinations` - Autocomplete for destinations
- **GET** `/api/common/languages` - Available language options
- **GET** `/api/common/tour-types` - All tour types
- **GET** `/api/common/timezones` - Timezone list

## Setup Instructions

### 1. PostgreSQL Setup
Follow the detailed setup guide: [POSTGRESQL_SETUP_GUIDE.md](POSTGRESQL_SETUP_GUIDE.md)

Quick setup:
```bash
# Install PostgreSQL and create database
sudo apt install postgresql postgresql-contrib
sudo -u postgres psql -c "CREATE DATABASE travel_partner_db;"
sudo -u postgres psql -c "CREATE USER travel_partner_user WITH PASSWORD 'your_password_here';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE travel_partner_db TO travel_partner_user;"
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.template .env
# Edit .env with your database credentials and other settings
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Load Sample Data (Optional)
```bash
python manage.py populate_sample_data
```

### 7. Run Development Server
```bash
python manage.py runserver
```

### 8. Frontend Setup (Optional)
```bash
cd frontend
npm install
npm start
```

## Environment Variables

Create a `.env` file in the project root using the template:

```bash
cp .env.template .env
```

Key variables to configure:

```env
# Django Configuration
SECRET_KEY=your-secret-key
DEBUG=True

# PostgreSQL Database
DB_NAME=travel_partner_db
DB_USER=travel_partner_user
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432

# Email Configuration (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Twilio Configuration (optional)
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=your-twilio-phone

# Redis Configuration (optional)
REDIS_URL=redis://localhost:6379/0
```

See [EMAIL_SETUP_GUIDE.md](EMAIL_SETUP_GUIDE.md) and [SMS_SETUP_GUIDE.md](SMS_SETUP_GUIDE.md) for detailed email and SMS configuration.

## Features

- Token-based Authentication
- OTP verification for email and mobile (with console fallback for development)
- Multi-step partner onboarding workflow
- File upload support
- API documentation with Swagger
- CORS support for frontend integration
- Celery for background tasks
- Redis for caching and task queue
- PostgreSQL database
- React frontend for testing all APIs
- Quick Test API for automated testing flows
# djangosapis
