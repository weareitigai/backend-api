# Building Django API Project - Step by Step Guide

This guide explains how the Django API project was created step by step to implement all the APIs defined in the CSV specification.

## Step 1: Project Initialization

### 1.1 Create Django Project Structure
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate  # On Windows

# Install Django and create project
pip install django
django-admin startproject config .
```

### 1.2 Install Required Dependencies
```bash
pip install -r requirements.txt
```

Key packages installed:
- **Django**: Web framework
- **Django REST Framework**: API development
- **django-cors-headers**: CORS support
- **python-decouple**: Environment variable management
- **celery & redis**: Background task processing
- **Pillow**: Image processing
- **pyotp**: OTP generation
- **twilio**: SMS services
- **sendgrid**: Email services
- **drf-spectacular**: API documentation

## Step 2: Project Configuration

### 2.1 Settings Configuration (`config/settings.py`)
Key configurations added:
- REST Framework with Token authentication
- CORS settings for frontend integration
- Custom User model configuration
- Media and static files setup
- Email and SMS service configurations
- Celery for background tasks
- API documentation with Spectacular

### 2.2 URL Configuration (`config/urls.py`)
- Main API routing
- API documentation endpoints
- Media file serving for development

## Step 3: App Creation and Structure

### 3.1 Authentication App (`apps/authentication/`)
**Purpose**: Handle all authentication-related functionality

**Models Created:**
- `User`: Extended Django User model with email/mobile verification
- `OTPVerification`: Store and manage OTP codes

**APIs Implemented:**
1. **POST** `/api/auth/send-email-otp` - Send OTP to email
2. **POST** `/api/auth/verify-email-otp` - Verify email OTP
3. **POST** `/api/auth/send-mobile-otp` - Send OTP to mobile
4. **POST** `/api/auth/verify-mobile-otp` - Verify mobile OTP
5. **POST** `/api/auth/signup` - User registration
6. **POST** `/api/auth/login` - User login
7. **POST** `/api/auth/logout` - User logout
8. **POST** `/api/auth/forgot-password` - Initiate password reset
9. **POST** `/api/auth/reset-password` - Complete password reset

**Key Features:**
- JWT token-based authentication
- Email and SMS OTP verification
- Password reset functionality
- Input validation and error handling

### 3.2 Partner App (`apps/partner/`)
**Purpose**: Manage partner onboarding and profile management

**Models Created:**
- `Partner`: Main partner profile
- `BusinessDetails`: Business information (Step 1)
- `LocationCoverage`: Location and coverage data (Step 2)
- `ToursServices`: Tours and services information (Step 3)
- `LegalBanking`: Legal and banking details (Step 4)

**APIs Implemented:**
1. **GET/PATCH** `/api/partner/business-details` - Business information
2. **GET/PATCH** `/api/partner/location-coverage` - Location & coverage
3. **GET/PATCH** `/api/partner/tours-services` - Tours & services
4. **GET/PATCH** `/api/partner/legal-banking` - Legal & banking info
5. **GET** `/api/partner/status` - Onboarding status
6. **POST** `/api/partner/complete-onboarding` - Complete profile

**Key Features:**
- Multi-step onboarding workflow
- Data persistence across steps
- File upload support for documents
- Progress tracking

### 3.3 Common App (`apps/common/`)
**Purpose**: Provide common data and utilities

**Models Created:**
- `Destination`: Travel destinations with search capability
- `Language`: Available languages
- `TourType`: Types of tours
- `Timezone`: Timezone information

**APIs Implemented:**
1. **GET** `/api/common/destinations` - Destinations with search
2. **GET** `/api/common/languages` - Language options
3. **GET** `/api/common/tour-types` - Tour type list
4. **GET** `/api/common/timezones` - Timezone list

**Key Features:**
- Autocomplete search for destinations
- Static data management
- Admin interface for data management

## Step 4: Database Design

### 4.1 User Authentication System
```python
class User(AbstractUser):
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    is_mobile_verified = models.BooleanField(default=False)
```

### 4.2 OTP Verification System
```python
class OTPVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    otp_type = models.CharField(max_length=10, choices=OTP_TYPES)
    otp_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
```

### 4.3 Partner Profile System
Each onboarding step has a separate model:
- **BusinessDetails**: Company info, GSTIN, employees, etc.
- **LocationCoverage**: Service areas, languages, regions
- **ToursServices**: Tour types, pricing, group sizes
- **LegalBanking**: Legal documents, banking details

## Step 5: API Implementation Details

### 5.1 Authentication Flow
1. **Email/Mobile OTP**: Generate 6-digit OTP → Store with expiration → Send via email/SMS
2. **Registration**: Validate input → Check OTP verification → Create user → Generate token
3. **Login**: Support email/mobile → Validate credentials → Return JWT token
4. **Password Reset**: Send OTP → Verify OTP → Update password

### 5.2 Partner Onboarding Flow
- **Step 1**: Business details with company information
- **Step 2**: Location coverage and service areas
- **Step 3**: Tours and services overview
- **Step 4**: Legal and banking information
- **Step 5**: Status tracking and completion

### 5.3 Common Data Management
- **Destinations**: Searchable with autocomplete
- **Languages**: Predefined language options
- **Tour Types**: Categorized tour offerings
- **Timezones**: Standard timezone support

## Step 6: Security Implementation

### 6.1 Authentication & Authorization
- Token-based authentication using Django REST Framework
- Permission-based access control
- OTP expiration and rate limiting
- Secure password handling

### 6.2 Data Validation
- Serializer-based input validation
- Custom business rule validators
- File upload security
- SQL injection prevention

### 6.3 Error Handling
- Standardized API responses
- Custom exception handling
- Comprehensive logging
- User-friendly error messages

## Step 7: File Structure and Organization

```
apiproject/
├── manage.py                     # Django management
├── requirements.txt              # Dependencies
├── setup.sh                     # Setup script
├── test_apis.py                 # API testing script
├── config/                      # Project configuration
│   ├── settings.py              # Django settings
│   ├── urls.py                  # URL routing
│   └── wsgi.py                  # WSGI config
├── apps/                        # Application modules
│   ├── authentication/          # Auth functionality
│   │   ├── models.py            # User and OTP models
│   │   ├── views.py             # Auth API views
│   │   ├── serializers.py       # Data serialization
│   │   ├── utils.py             # OTP utilities
│   │   └── urls.py              # Auth URL patterns
│   ├── partner/                 # Partner management
│   │   ├── models.py            # Partner models
│   │   ├── views.py             # Partner API views
│   │   ├── serializers.py       # Partner serializers
│   │   └── urls.py              # Partner URL patterns
│   └── common/                  # Shared utilities
│       ├── models.py            # Common data models
│       ├── views.py             # Common API views
│       ├── serializers.py       # Common serializers
│       ├── urls.py              # Common URL patterns
│       └── management/commands/ # Management commands
└── media/                       # File uploads
```

## Step 8: Setup and Deployment

### 8.1 Quick Setup
```bash
# Clone and setup
cd apiproject
chmod +x setup.sh
./setup.sh

# Start development server
source venv/bin/activate
python manage.py runserver
```

### 8.2 Database Operations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Populate sample data
python manage.py populate_sample_data

# Create admin user
python manage.py createsuperuser
```

### 8.3 Testing
```bash
# Test all APIs
python test_apis.py

# Run Django tests
python manage.py test
```

## Step 9: Advanced Features

### 9.1 API Documentation
- Swagger/OpenAPI integration with drf-spectacular
- Interactive API explorer at `/api/docs/`
- Comprehensive endpoint documentation
- Schema generation for frontend integration

### 9.2 Background Tasks
- Celery integration for asynchronous processing
- Redis as message broker
- Background email and SMS sending
- Scalable task processing

### 9.3 File Handling
- Secure file upload and storage
- Media file configuration
- File type validation
- Proper file serving in development

### 9.4 Admin Interface
- Django admin for data management
- Custom admin configurations
- User and partner management
- Data import/export capabilities

## Step 10: API Endpoints Summary

### Authentication APIs (9 endpoints)
- Email/Mobile OTP sending and verification
- User registration and login
- Password reset functionality
- Logout capability

### Partner APIs (6 endpoints)
- Business details management
- Location and coverage information
- Tours and services configuration
- Legal and banking data
- Onboarding status tracking
- Profile completion

### Common APIs (4 endpoints)
- Destination search and listing
- Language options
- Tour type categories
- Timezone information

**Total: 19 API endpoints** matching the CSV specification exactly.

## Database Migration to PostgreSQL

### Original Implementation
The project was initially built with SQLite for rapid development and prototyping.

### Migration to PostgreSQL
For production readiness, the project has been migrated to PostgreSQL:

#### Changes Made:
1. **Database Engine Update**: Changed from SQLite to PostgreSQL in `settings.py`
2. **Environment Configuration**: Added PostgreSQL connection parameters
3. **Dependencies**: Included `psycopg2-binary` for PostgreSQL connectivity
4. **Migration Tools**: Created automated migration script and detailed setup guide

#### Migration Process:
```bash
# Automated migration
./migrate_to_postgresql.sh

# Or manual setup
# See POSTGRESQL_SETUP_GUIDE.md for detailed instructions
```

#### Benefits of PostgreSQL:
- Better performance for concurrent users
- Advanced features (JSON fields, full-text search)
- Production-grade reliability
- Better data integrity and ACID compliance
- Scalability for larger datasets

## Conclusion

This implementation provides a complete, production-ready API system that:
- ✅ Matches all CSV requirements exactly
- ✅ Follows Django and REST API best practices
- ✅ Includes comprehensive documentation
- ✅ Provides security and validation
- ✅ Supports scalable architecture
- ✅ Includes testing and setup automation

The project is ready for development, testing, and deployment with proper documentation and tooling in place.
